"""
Copyright (c) 2024 Danny, DA2 Studio (https://da2.35g.tw)
Database connection management for MySQL MCP Server.


Handles dynamic database connections and management operations for MySQL/MariaDB.
"""

import os
import logging
from typing import Any, Optional
from urllib.parse import urlparse
from dataclasses import dataclass

# You need to install mysql-connector-python
import mysql.connector
from mysql.connector import errorcode

logger = logging.getLogger("mcp-mysql")


@dataclass
class ServerConfig:
    """MySQL server connection configuration."""
    
    host: str = "localhost"
    port: int = 3306
    user: str = "root"
    password: str = ""
    default_database: str = "mysql"  # Used for admin operations
    
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
        
        # Check for DATABASE_URL first (mysql://user:pass@host:port/db)
        database_url = os.getenv("MYSQL_DATABASE_URL")
        if database_url:
            parsed = urlparse(database_url)
            config.host = parsed.hostname or "localhost"
            config.port = parsed.port or 3306
            config.user = parsed.username or "root"
            config.password = parsed.password or ""
            config.default_database = parsed.path.lstrip("/") if parsed.path else "mysql"
        else:
            # Fall back to individual settings
            config.host = os.getenv("MYSQL_HOST", "localhost")
            config.port = int(os.getenv("MYSQL_PORT", "3306"))
            config.user = os.getenv("MYSQL_USER", "root")
            config.password = os.getenv("MYSQL_PASSWORD", "")
            config.default_database = os.getenv("MYSQL_DATABASE", "mysql")
        
        # Security settings
        config.max_rows = int(os.getenv("MAX_ROWS", "1000"))
        config.query_timeout = int(os.getenv("QUERY_TIMEOUT", "30"))
        config.read_only = os.getenv("READ_ONLY", "false").lower() == "true"
        
        # Database management permissions
        config.allow_create_db = os.getenv("ALLOW_CREATE_DB", "false").lower() == "true"
        config.allow_drop_db = os.getenv("ALLOW_DROP_DB", "false").lower() == "true"
        
        return config


class DynamicDatabaseManager:
    """Manages dynamic MySQL database connections and operations."""
    
    def __init__(self, config: Optional[ServerConfig] = None):
        """Initialize the database manager.
        
        Args:
            config: Server configuration. If None, loads from environment.
        """
        self.config = config or ServerConfig.from_env()
        self._connections: dict[str, mysql.connector.MySQLConnection] = {}
    
    def _get_connection(self, database: Optional[str] = None) -> mysql.connector.MySQLConnection:
        """Get or create a connection to a specific database.
        
        Args:
            database: Database name. If None, uses default_database.
        """
        db_name = database or self.config.default_database
        
        # Check if we have an existing valid connection
        if db_name in self._connections:
            conn = self._connections[db_name]
            if conn.is_connected():
                return conn
        
        # Create new connection
        logger.debug(f"Creating connection to database: {db_name}")
        try:
            conn = mysql.connector.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=db_name,
                connection_timeout=self.config.query_timeout
            )
            self._connections[db_name] = conn
            return conn
        except mysql.connector.Error as err:
            logger.error(f"Error connecting to {db_name}: {err}")
            raise
    
    def close(self):
        """Close all database connections."""
        for db_name, conn in self._connections.items():
            if conn and conn.is_connected():
                logger.debug(f"Closing connection to database: {db_name}")
                conn.close()
        self._connections.clear()
    
    def close_connection(self, database: str):
        """Close connection to a specific database."""
        if database in self._connections:
            conn = self._connections[database]
            if conn and conn.is_connected():
                conn.close()
            del self._connections[database]
    
    def _is_read_query(self, query: str) -> bool:
        """Check if a query is read-only."""
        query_upper = query.strip().upper()
        read_keywords = ("SELECT", "EXPLAIN", "SHOW", "DESCRIBE")
        return query_upper.startswith(read_keywords)
    
    # ==================== Database Management ====================
    
    def list_databases(self) -> dict[str, Any]:
        """List all databases on the server."""
        query = """
            SELECT 
                schema_name as database_name,
                default_character_set_name as encoding,
                default_collation_name as collation
            FROM information_schema.schemata
            ORDER BY schema_name;
        """
        # Note: MySQL doesn't easily show DB size or owner in standard information_schema across all versions easily without privileges
        return self.execute_query(query, database="information_schema")
    
    def create_database(self, database_name: str, owner: Optional[str] = None) -> dict[str, Any]:
        """Create a new database.
        
        Args:
            database_name: Name of the database to create.
            owner: Ignored for MySQL (permissions handled separately).
        """
        if not self.config.allow_create_db:
            return {
                "success": False,
                "error": "Database creation is not allowed. Set ALLOW_CREATE_DB=true to enable.",
                "error_type": "PermissionDenied"
            }
        
        conn = self._get_connection(self.config.default_database)
        try:
            with conn.cursor() as cursor:
                # Basic protection against injection (MySQL identifiers should be backticked)
                # But better to use simple validation
                safe_name = database_name.replace("`", "")
                query = f"CREATE DATABASE `{safe_name}`"
                cursor.execute(query)
                logger.info(f"Created database: {safe_name}")
                return {
                    "success": True,
                    "message": f"Database '{safe_name}' created successfully.",
                    "database_name": safe_name
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
        protected_dbs = ["mysql", "information_schema", "performance_schema", "sys"]
        if database_name.lower() in protected_dbs:
            return {
                "success": False,
                "error": f"Cannot drop protected database: {database_name}",
                "error_type": "ProtectedDatabase"
            }
        
        self.close_connection(database_name)
        
        conn = self._get_connection(self.config.default_database)
        try:
            with conn.cursor() as cursor:
                safe_name = database_name.replace("`", "")
                query = f"DROP DATABASE `{safe_name}`"
                cursor.execute(query)
                logger.info(f"Dropped database: {safe_name}")
                return {
                    "success": True,
                    "message": f"Database '{safe_name}' has been dropped.",
                    "database_name": safe_name
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
        if self.config.read_only and not self._is_read_query(query):
            return {
                "success": False,
                "error": "Read-only mode is enabled. Only SELECT, EXPLAIN, SHOW, DESCRIBE queries are allowed.",
                "error_type": "ReadOnlyMode"
            }
        
        try:
            conn = self._get_connection(database)
            # dictionary=True returns rows as dicts
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query)
                
                if cursor.description is None:
                    # No result set (e.g. UPDATE, INSERT)
                    conn.commit()
                    return {
                        "success": True,
                        "database": database or self.config.default_database,
                        "message": f"Query executed successfully. Rows affected: {cursor.rowcount}",
                        "rows_affected": cursor.rowcount
                    }
                
                # Fetch results
                rows = cursor.fetchmany(self.config.max_rows)
                total_rows = len(rows)
                # MySQL connector fetchmany doesn't tell us if there are more immediately unless we fetch one more
                # Simplified check for now
                has_more = False 
                if len(rows) == self.config.max_rows:
                     # Try to fetch one more to see if there is more
                     extra = cursor.fetchone()
                     if extra:
                         has_more = True
                         # We don't include the extra row to stay within limit
                
                columns = [desc[0] for desc in cursor.description]
                
                return {
                    "success": True,
                    "database": database or self.config.default_database,
                    "columns": columns,
                    "rows": rows,
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
        """List all schemas (MySQL treats databases as schemas)."""
        # In MySQL, SCHEMA is synonymous with DATABASE. 
        # So we just list databases or return the current one.
        # To be compatible with the interface, we can return the databases list.
        return self.list_databases()
    
    def list_tables(self, database: Optional[str] = None, schema: str = "public") -> dict[str, Any]:
        """List all tables in a database (MySQL ignores schema arg usually)."""
        db_name = database or self.config.default_database
        
        query = """
            SELECT 
                TABLE_NAME as table_name,
                TABLE_TYPE as table_type,
                TABLE_ROWS as estimated_rows
            FROM information_schema.TABLES
            WHERE TABLE_SCHEMA = DATABASE()
            ORDER BY TABLE_NAME;
        """
        
        # We must execute this on the specific database
        result = self.execute_query(query, database=db_name)
        if result.get("success"):
            return {
                "success": True,
                "database": db_name,
                "schema": db_name, # MySQL schema is the db
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
                COLUMN_NAME as column_name,
                DATA_TYPE as data_type,
                CHARACTER_MAXIMUM_LENGTH as character_maximum_length,
                NUMERIC_PRECISION as numeric_precision,
                NUMERIC_SCALE as numeric_scale,
                IS_NULLABLE as is_nullable,
                COLUMN_DEFAULT as column_default,
                COLUMN_KEY as column_key,
                EXTRA as extra
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = '{db}'
            AND TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION;
        """
        
        columns_result = self.execute_query(columns_query, db)
        
        # Get indexes
        indexes_query = f"SHOW INDEX FROM `{table_name}`"
        indexes_result = self.execute_query(indexes_query, db)
        
        return {
            "success": True,
            "database": db,
            "table_name": table_name,
            "columns": columns_result.get("rows", []) if columns_result.get("success") else [],
            "indexes": indexes_result.get("rows", []) if indexes_result.get("success") else []
        }
