"""
Copyright (c) 2024 Danny, DA2 Studio (https://da2.35g.tw)
MySQL MCP Server - Main server implementation.


Provides tools for AI assistants to query and explore MySQL/MariaDB databases
with dynamic database selection and management capabilities.
"""

import json
import logging
import os
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Support both direct execution and module import
try:
    from .database import DynamicDatabaseManager, ServerConfig
except ImportError:
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    from database import DynamicDatabaseManager, ServerConfig


# Load environment variables from .env file
# Explicitly look for .env in the current working directory first
env_path = os.path.join(os.getcwd(), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stderr
)
logger = logging.getLogger("mcp-mysql")


# Global database manager instance
_db_manager: Optional[DynamicDatabaseManager] = None


def get_db_manager() -> DynamicDatabaseManager:
    """Get or create the global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DynamicDatabaseManager()
    return _db_manager


@dataclass
class AppContext:
    """Application context with database manager."""
    db: DynamicDatabaseManager


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with database connection."""
    logger.info("Starting MySQL MCP Server...")
    db = get_db_manager()
    config = db.config
    logger.info(f"MySQL Server: {config.host}:{config.port}")
    logger.info(f"Default Database: {config.default_database}")
    logger.info(f"Security: max_rows={config.max_rows}, timeout={config.query_timeout}s, read_only={config.read_only}")
    logger.info(f"Permissions: allow_create_db={config.allow_create_db}, allow_drop_db={config.allow_drop_db}")
    try:
        yield AppContext(db=db)
    finally:
        logger.info("Shutting down MySQL MCP Server...")
        db.close()


# Create MCP Server
mcp = FastMCP(
    "MySQL MCP Server",
    lifespan=app_lifespan,
    debug=True
)


def _format_result(data: Any) -> str:
    """Format data as JSON string for MCP response."""
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)


# ==================== Database Management Tools ====================

@mcp.tool()
def list_databases() -> str:
    """列出 MySQL 伺服器上的所有資料庫。
    
    Returns:
        JSON 格式的資料庫列表
    """
    logger.info("Listing all databases")
    db = get_db_manager()
    result = db.list_databases()
    # MySQL information_schema result might need parsing
    return _format_result(result)


@mcp.tool()
def create_database(database_name: str) -> str:
    """建立新的資料庫。
    
    需要設定 ALLOW_CREATE_DB=true 才能使用此功能。
    
    Args:
        database_name: 要建立的資料庫名稱
    """
    logger.info(f"Creating database: {database_name}")
    db = get_db_manager()
    result = db.create_database(database_name)
    return _format_result(result)


@mcp.tool()
def drop_database(database_name: str, confirm: bool = False) -> str:
    """刪除資料庫（危險操作！）。
    
    需要設定 ALLOW_DROP_DB=true 且 confirm=True 才能執行。
    
    Args:
        database_name: 要刪除的資料庫名稱
        confirm: 必須設為 True 才會真正執行刪除
    """
    logger.warning(f"Drop database requested: {database_name}, confirm={confirm}")
    db = get_db_manager()
    result = db.drop_database(database_name, confirm)
    return _format_result(result)


# ==================== Query Tools ====================

@mcp.tool()
def execute_query(query: str, database: Optional[str] = None) -> str:
    """執行 SQL 查詢並返回結果。
    
    可以執行任何 SQL 查詢（SELECT、INSERT、UPDATE、DELETE 等）。
    如果啟用了只讀模式，則只能執行 SELECT 查詢。
    
    Args:
        query: 要執行的 SQL 查詢語句
        database: 目標資料庫名稱（選填，預設使用預設資料庫）
        
    Returns:
        JSON 格式的查詢結果，包含 columns、rows 和 row_count
    """
    db_name = database or get_db_manager().config.default_database
    logger.debug(f"execute_query on {db_name}: {query[:100]}..." if len(query) > 100 else f"execute_query on {db_name}: {query}")
    
    db = get_db_manager()
    result = db.execute_query(query, database)
    
    return _format_result(result)


# ==================== Schema Tools ====================

@mcp.tool()
def list_tables(database: Optional[str] = None) -> str:
    """列出指定資料庫中的所有資料表。
    
    Args:
        database: 目標資料庫名稱（選填）
        
    Returns:
        JSON 格式的資料表列表
    """
    db_name = database or get_db_manager().config.default_database
    logger.debug(f"list_tables on {db_name}")
    
    db = get_db_manager()
    # MySQL doesn't use 'schema' argument in the same way, so we omit default schema
    result = db.list_tables(database)
    
    return _format_result(result)


@mcp.tool()
def describe_table(table_name: str, database: Optional[str] = None) -> str:
    """查看資料表的詳細結構。
    
    返回資料表的欄位定義和索引資訊。
    
    Args:
        table_name: 資料表名稱
        database: 目標資料庫名稱（選填）
        
    Returns:
        JSON 格式的資料表結構
    """
    db_name = database or get_db_manager().config.default_database
    logger.debug(f"describe_table {db_name}.{table_name}")
    
    db = get_db_manager()
    result = db.describe_table(table_name, database)
    
    return _format_result(result)


@mcp.tool()
def get_server_info() -> str:
    """取得 MCP Server 的配置資訊。"""
    config = ServerConfig.from_env()
    return _format_result({
        "server_name": "MySQL MCP Server",
        "version": "0.1.0",
        "connection": {
            "host": config.host,
            "port": config.port,
            "default_database": config.default_database,
            "user": config.user
        },
        "security": {
            "max_rows": config.max_rows,
            "query_timeout": config.query_timeout,
            "read_only": config.read_only
        }
    })


def main():
    """Entry point for the MCP server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MySQL MCP Server")
    parser.add_argument("--http", action="store_true", help="Run in HTTP mode")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP mode")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host for HTTP mode")
    args = parser.parse_args()
    
    if args.http:
        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.run(transport="streamable-http")
    else:
        mcp.run()


if __name__ == "__main__":
    main()
