# MCP Server SQLite3

一个基于 Model Context Protocol (MCP) 的 SQLite 数据库浏览和查询工具。

## 功能特性

本服务提供了一组工具，允许大语言模型（LLM）与 SQLite 数据库进行交互：

- **查询执行**: 安全地执行 SQL SELECT 查询（支持 CTE）。
- **表结构查看**: 列出数据库中的所有表。
- **模式描述**: 查看特定表的详细字段信息（列名、类型、主键等）。
- **安全机制**: 默认开启只读模式，防止意外修改数据。
- **高级特性**: 自动开启 WAL 模式和外键支持，提升性能和数据完整性。

## 安装

确保你的环境中已安装 Python 3.13 或更高版本。

使用 `uv` 运行（推荐）：

```bash
# 假设你在项目根目录
uv run mcp-server-sqlite3
```

或者安装依赖后直接运行：

```bash
pip install -e .
python mcp-server-sqlite3.py
```

## 配置

本服务通过环境变量进行配置：

| 环境变量 | 必填 | 默认值 | 描述 |
|----------|------|--------|------|
| `SQLITE_DB_PATH` | 是 | `:memory:` | SQLite 数据库文件的路径。 |
| `SQLITE_READ_ONLY` | 否 | `TRUE` | 是否开启只读模式。设置为 `FALSE` 可允许写入（如果工具代码允许，目前主要限制为 SELECT）。 |

### 示例用法

在 Claude Desktop 或其他 MCP 客户端中配置：

```json
{
  "mcpServers": {
    "sqlite-explorer": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-server-sqlite3",
        "run",
        "mcp-server-sqlite3"
      ],
      "env": {
        "SQLITE_DB_PATH": "/path/to/your/database.db",
        "SQLITE_READ_ONLY":true
      }
    }
  }
}
```

## 可用工具

### `read_query`
执行 SQL 查询。
- 参数:
  - `query`: SELECT SQL 查询语句。
  - `params`: (可选) 查询参数列表。
  - `fetch_all`: (可选) 是否获取所有结果，默认为 True。
  - `row_limit`: (可选) 最大返回行数，默认 1000。

### `list_tables`
列出数据库中的所有表名。

### `describe_table`
获取指定表的详细模式信息。
- 参数:
  - `table_name`: 表名。

## 开发

本项目使用 `uv` 进行包管理。

```bash
# 安装依赖
uv sync

# 运行服务
uv run mcp-server-sqlite3
```
