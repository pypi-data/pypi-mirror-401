"""
Copyright (c) 2024 Danny, DA2 Studio (https://da2.35g.tw)
Database connection management for PostgreSQL MCP Server.


Handles dynamic database connections and management operations.
"""

import os
import logging
from typing import Any, Optional
from urllib.parse import urlparse
from dataclasses import dataclass

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

logger = logging.getLogger("mcp-postgresql")


@dataclass
class ServerConfig:
    """PostgreSQL server connection configuration (without specific database)."""
    
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = ""
    default_database: str = "postgres"  # Used for admin operations
    
    # Security settings
    max_rows: int = 1000
    query_timeout: int = 30  # seconds
    read_only: bool = False
    
    # Database management permissions
    allow_create_db: bool = False
    allow_drop_db: bool = False
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Create configuration from environment variables."""
        config = cls()
        
        # Check for DATABASE_URL first (extract host/port/user/password only)
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            parsed = urlparse(database_url)
            config.host = parsed.hostname or "localhost"
            config.port = parsed.port or 5432
            config.user = parsed.username or "postgres"
            config.password = parsed.password or ""
            config.default_database = parsed.path.lstrip("/") if parsed.path else "postgres"
        else:
            # Fall back to individual settings
            config.host = os.getenv("PG_HOST", "localhost")
            config.port = int(os.getenv("PG_PORT", "5432"))
            config.user = os.getenv("PG_USER", "postgres")
            config.password = os.getenv("PG_PASSWORD", "")
            config.default_database = os.getenv("PG_DATABASE", "postgres")
        
        # Security settings
        config.max_rows = int(os.getenv("MAX_ROWS", "1000"))
        config.query_timeout = int(os.getenv("QUERY_TIMEOUT", "30"))
        config.read_only = os.getenv("READ_ONLY", "false").lower() == "true"
        
        # Database management permissions
        config.allow_create_db = os.getenv("ALLOW_CREATE_DB", "false").lower() == "true"
        config.allow_drop_db = os.getenv("ALLOW_DROP_DB", "false").lower() == "true"
        
        return config


class DynamicDatabaseManager:
    """Manages dynamic PostgreSQL database connections and operations."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize the database manager.
        
        Args:
            config: Server configuration. If None, loads from environment.
        """
        self.config = config or ServerConfig.from_env()
        self._connections: dict[str, psycopg2.extensions.connection] = {}
    
    def _get_connection(self, database: Optional[str] = None) -> psycopg2.extensions.connection:
        """Get or create a connection to a specific database.
        
        Args:
            database: Database name. If None, uses default_database.
        """
        db_name = database or self.config.default_database
        
        # Check if we have an existing valid connection
        if db_name in self._connections:
            conn = self._connections[db_name]
            if not conn.closed:
                return conn
        
        # Create new connection
        logger.debug(f"Creating connection to database: {db_name}")
        conn = psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=db_name,
            options=f"-c statement_timeout={self.config.query_timeout * 1000}"
        )
        conn.autocommit = True
        self._connections[db_name] = conn
        return conn
    
    def close(self):
        """Close all database connections."""
        for db_name, conn in self._connections.items():
            if conn and not conn.closed:
                logger.debug(f"Closing connection to database: {db_name}")
                conn.close()
        self._connections.clear()
    
    def close_connection(self, database: str):
        """Close connection to a specific database."""
        if database in self._connections:
            conn = self._connections[database]
            if conn and not conn.closed:
                conn.close()
            del self._connections[database]
    
    def _is_read_query(self, query: str) -> bool:
        """Check if a query is read-only."""
        query_upper = query.strip().upper()
        read_keywords = ("SELECT", "EXPLAIN", "SHOW", "DESCRIBE", "WITH")
        return query_upper.startswith(read_keywords)
    
    # ==================== Database Management ====================
    
    def list_databases(self) -> dict[str, Any]:
        """List all databases on the server."""
        query = """
            SELECT 
                datname as database_name,
                pg_catalog.pg_get_userbyid(datdba) as owner,
                pg_catalog.pg_encoding_to_char(encoding) as encoding,
                datcollate as collation,
                pg_catalog.pg_database_size(datname) as size_bytes
            FROM pg_catalog.pg_database
            WHERE datistemplate = false
            ORDER BY datname;
        """
        return self.execute_query(query, database="postgres")
    
    def create_database(self, database_name: str, owner: Optional[str] = None) -> dict[str, Any]:
        """Create a new database.
        
        Args:
            database_name: Name of the database to create.
            owner: Optional owner for the database.
        """
        if not self.config.allow_create_db:
            return {
                "success": False,
                "error": "Database creation is not allowed. Set ALLOW_CREATE_DB=true to enable.",
                "error_type": "PermissionDenied"
            }
        
        # Use SQL identifier to prevent injection
        conn = self._get_connection("postgres")
        try:
            with conn.cursor() as cursor:
                if owner:
                    query = sql.SQL("CREATE DATABASE {} OWNER {}").format(
                        sql.Identifier(database_name),
                        sql.Identifier(owner)
                    )
                else:
                    query = sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(database_name)
                    )
                cursor.execute(query)
                logger.info(f"Created database: {database_name}")
                return {
                    "success": True,
                    "message": f"Database '{database_name}' created successfully.",
                    "database_name": database_name
                }
        except Exception as e:
            logger.error(f"Failed to create database {database_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def drop_database(self, database_name: str, confirm: bool = False) -> dict[str, Any]:
        """Drop a database.
        
        Args:
            database_name: Name of the database to drop.
            confirm: Must be True to actually drop the database.
        """
        if not self.config.allow_drop_db:
            return {
                "success": False,
                "error": "Database deletion is not allowed. Set ALLOW_DROP_DB=true to enable.",
                "error_type": "PermissionDenied"
            }
        
        if not confirm:
            return {
                "success": False,
                "error": f"To drop database '{database_name}', you must set confirm=True. This action is IRREVERSIBLE!",
                "error_type": "ConfirmationRequired"
            }
        
        # Prevent dropping important databases
        protected_dbs = ["postgres", "template0", "template1"]
        if database_name.lower() in protected_dbs:
            return {
                "success": False,
                "error": f"Cannot drop protected database: {database_name}",
                "error_type": "ProtectedDatabase"
            }
        
        # Close any existing connection to this database
        self.close_connection(database_name)
        
        conn = self._get_connection("postgres")
        try:
            with conn.cursor() as cursor:
                # Terminate existing connections to the database
                cursor.execute(sql.SQL("""
                    SELECT pg_terminate_backend(pid) 
                    FROM pg_stat_activity 
                    WHERE datname = %s AND pid <> pg_backend_pid()
                """), [database_name])
                
                # Drop the database
                query = sql.SQL("DROP DATABASE {}").format(
                    sql.Identifier(database_name)
                )
                cursor.execute(query)
                logger.info(f"Dropped database: {database_name}")
                return {
                    "success": True,
                    "message": f"Database '{database_name}' has been dropped.",
                    "database_name": database_name
                }
        except Exception as e:
            logger.error(f"Failed to drop database {database_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # ==================== Query Execution ====================
    
    def execute_query(self, query: str, database: Optional[str] = None) -> dict[str, Any]:
        """Execute a SQL query on a specific database.
        
        Args:
            query: The SQL query to execute.
            database: Database to execute on. If None, uses default.
        """
        # Check read-only mode
        if self.config.read_only and not self._is_read_query(query):
            return {
                "success": False,
                "error": "Read-only mode is enabled. Only SELECT, EXPLAIN, SHOW, and WITH queries are allowed.",
                "error_type": "ReadOnlyMode"
            }
        
        try:
            conn = self._get_connection(database)
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query)
                
                # Check if query returns results
                if cursor.description is None:
                    return {
                        "success": True,
                        "database": database or self.config.default_database,
                        "message": f"Query executed successfully. Rows affected: {cursor.rowcount}",
                        "rows_affected": cursor.rowcount
                    }
                
                # Fetch results with row limit
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchmany(self.config.max_rows)
                total_rows = len(rows)
                has_more = cursor.fetchone() is not None
                result_rows = [dict(row) for row in rows]
                
                return {
                    "success": True,
                    "database": database or self.config.default_database,
                    "columns": columns,
                    "rows": result_rows,
                    "row_count": total_rows,
                    "has_more": has_more,
                    "max_rows_limit": self.config.max_rows if has_more else None
                }
                
        except Exception as e:
            logger.error(f"Query failed on {database}: {e}")
            return {
                "success": False,
                "database": database or self.config.default_database,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    # ==================== Schema Operations ====================
    
    def list_schemas(self, database: Optional[str] = None) -> dict[str, Any]:
        """List all schemas in a database."""
        query = """
            SELECT 
                schema_name,
                schema_owner
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name;
        """
        result = self.execute_query(query, database)
        if result.get("success"):
            return {
                "success": True,
                "database": database or self.config.default_database,
                "schemas": result.get("rows", []),
                "count": result.get("row_count", 0)
            }
        return result
    
    def list_tables(self, database: Optional[str] = None, schema: str = "public") -> dict[str, Any]:
        """List all tables in a schema."""
        query = f"""
            SELECT 
                table_name,
                table_type,
                (
                    SELECT COUNT(*) 
                    FROM information_schema.columns c 
                    WHERE c.table_schema = t.table_schema 
                    AND c.table_name = t.table_name
                ) as column_count
            FROM information_schema.tables t
            WHERE table_schema = '{schema}'
            ORDER BY table_name;
        """
        result = self.execute_query(query, database)
        if result.get("success"):
            return {
                "success": True,
                "database": database or self.config.default_database,
                "schema": schema,
                "tables": result.get("rows", []),
                "count": result.get("row_count", 0)
            }
        return result
    
    def describe_table(self, table_name: str, database: Optional[str] = None, schema: str = "public") -> dict[str, Any]:
        """Get detailed information about a table."""
        db = database or self.config.default_database
        
        # Get columns
        columns_query = f"""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                numeric_precision,
                numeric_scale,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = '{schema}'
            AND table_name = '{table_name}'
            ORDER BY ordinal_position;
        """
        
        # Get primary keys
        pk_query = f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu 
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            WHERE tc.constraint_type = 'PRIMARY KEY'
            AND tc.table_schema = '{schema}'
            AND tc.table_name = '{table_name}';
        """
        
        # Get foreign keys
        fk_query = f"""
            SELECT 
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name
                AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON ccu.constraint_name = tc.constraint_name
                AND ccu.table_schema = tc.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_schema = '{schema}'
            AND tc.table_name = '{table_name}';
        """
        
        # Get indexes
        indexes_query = f"""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE schemaname = '{schema}'
            AND tablename = '{table_name}';
        """
        
        columns_result = self.execute_query(columns_query, db)
        pk_result = self.execute_query(pk_query, db)
        fk_result = self.execute_query(fk_query, db)
        indexes_result = self.execute_query(indexes_query, db)
        
        return {
            "success": True,
            "database": db,
            "schema": schema,
            "table_name": table_name,
            "columns": columns_result.get("rows", []) if columns_result.get("success") else [],
            "primary_keys": [row["column_name"] for row in pk_result.get("rows", [])] if pk_result.get("success") else [],
            "foreign_keys": fk_result.get("rows", []) if fk_result.get("success") else [],
            "indexes": indexes_result.get("rows", []) if indexes_result.get("success") else []
        }


# Keep backward compatibility
DatabaseConfig = ServerConfig
DatabaseManager = DynamicDatabaseManager
