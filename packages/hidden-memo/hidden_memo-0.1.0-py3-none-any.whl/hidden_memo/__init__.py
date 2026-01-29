"""
Hidden Memo: A local NoSQL MCP server for unstructured data.
"""

from .main import list_tables, mcp, read_from_table, save_to_table, update_memo_content

__all__ = [
    "mcp",
    "save_to_table",
    "read_from_table",
    "update_memo_content",
    "list_tables",
]

__version__ = "0.1.0"
