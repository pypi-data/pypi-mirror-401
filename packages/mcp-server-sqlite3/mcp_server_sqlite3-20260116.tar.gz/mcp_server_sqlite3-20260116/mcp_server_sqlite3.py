from pathlib import Path
import sqlite3
import os
import threading
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP


# Initialize FastMCP server
mcp = FastMCP("SQLite Explorer", log_level="CRITICAL")

# SQLite database 文件路径
if "SQLITE_DB_PATH" not in os.environ:
    os.environ["SQLITE_DB_PATH"] = ":memory:"
DB_PATH = Path(os.environ["SQLITE_DB_PATH"])
READ_ONLY = os.environ.get("SQLITE_READ_ONLY", "TRUE").upper() == "TRUE"


class SQLiteConnection:
    __lock__ = threading.Lock()

    def __init__(
        self, db_path: Path, wal_mode: bool = True, enable_foreign_keys: bool = True
    ):
        self.db_path = db_path
        self.conn = None
        self.wal_mode = wal_mode
        self.enable_foreign_keys = enable_foreign_keys

    def __enter__(self) -> sqlite3.Connection:
        self.__lock__.acquire()
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        # 开启 WAL模式
        if self.wal_mode:
            self.conn.execute("PRAGMA journal_mode=WAL;")
        # 启用外键支持
        if self.enable_foreign_keys:
            self.conn.execute("PRAGMA foreign_keys=ON;")
        self.conn.commit()

        return self.conn

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self.conn:
            self.conn.close()
        self.__lock__.release()


@mcp.tool()
def read_query(
    query: str,
    params: Optional[List[Any]] = None,
    fetch_all: bool = True,
    row_limit: int = 1000,
) -> List[Dict[str, Any]]:
    """在 SQLite 数据库上执行查询。

    Args:
        query: 要执行的 SELECT SQL 查询语句
        params: 可选的查询参数列表
        fetch_all: 如果为 True，获取所有结果。如果为 False，获取一行。
        row_limit: 返回的最大行数（默认 1000）

    Returns:
        包含查询结果的字典列表
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Messages database not found at: {DB_PATH}")

    # Clean and validate the query
    query = query.strip()

    # Remove trailing semicolon if present
    if query.endswith(";"):
        query = query[:-1].strip()

    # Check for multiple statements by looking for semicolons not inside quotes
    def contains_multiple_statements(sql: str) -> bool:
        in_single_quote = False
        in_double_quote = False
        for char in sql:
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
            elif char == ";" and not in_single_quote and not in_double_quote:
                return True
        return False

    if contains_multiple_statements(query):
        raise ValueError("Multiple SQL statements are not allowed")

    # Validate query type (allowing common CTEs)
    query_lower = query.lower()
    if READ_ONLY and not any(
        query_lower.startswith(prefix) for prefix in ("select", "with")
    ):
        raise ValueError(
            "Only SELECT queries (including WITH clauses) are allowed for safety"
        )

    params = params or []

    with SQLiteConnection(DB_PATH, wal_mode=True, enable_foreign_keys=True) as conn:
        cursor = conn.cursor()

        try:
            # Only add LIMIT if query doesn't already have one
            if "limit" not in query_lower:
                query = f"{query} LIMIT {row_limit}"

            cursor.execute(query, params)

            if fetch_all:
                results = cursor.fetchall()
            else:
                results = [cursor.fetchone()]

            return [dict(row) for row in results if row is not None]

        except sqlite3.Error as e:
            raise ValueError(f"SQLite error: {str(e)}")


@mcp.tool()
def list_tables() -> List[str]:
    """列出 Messages 数据库中的所有表。

    Returns:
        数据库中的表名列表
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Messages database not found at: {DB_PATH}")

    with SQLiteConnection(DB_PATH, wal_mode=True, enable_foreign_keys=True) as conn:
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """)

            return [row["name"] for row in cursor.fetchall()]

        except sqlite3.Error as e:
            raise ValueError(f"SQLite error: {str(e)}")


@mcp.tool()
def describe_table(table_name: str) -> List[Dict[str, str]]:
    """获取表模式的详细信息。

    Args:
        table_name: 要描述的表名

    Returns:
        包含列信息的字典列表：
        - name: 列名
        - type: 列数据类型
        - notnull: 列是否可以包含 NULL 值
        - dflt_value: 列的默认值
        - pk: 列是否为主键的一部分
    """
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Messages database not found at: {DB_PATH}")

    with SQLiteConnection(DB_PATH, wal_mode=True, enable_foreign_keys=True) as conn:
        cursor = conn.cursor()

        try:
            # Verify table exists
            cursor.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """,
                [table_name],
            )

            if not cursor.fetchone():
                raise ValueError(f"Table '{table_name}' does not exist")

            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            return [dict(row) for row in columns]

        except sqlite3.Error as e:
            raise ValueError(f"SQLite error: {str(e)}")


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
