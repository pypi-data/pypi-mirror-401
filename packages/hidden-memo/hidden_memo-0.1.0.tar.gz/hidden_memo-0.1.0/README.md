# Hidden Memo

Hidden Memo is a lightweight MCP server and CLI for storing unstructured JSON locally.
It uses TinyDB to persist per-table JSON files and exposes MCP tools for CRUD-like operations.

## Highlights

-   Store data in tables (one JSON file per table)
-   CLI for save/read/update/latest/list/delete
-   MCP tools for programmatic access
-   Local-first storage under your home directory

## Requirements

-   Python 3.11+

## Data Location

Memos are stored under `~/.hidden_memo/` in your home directory, keyed by table name.
Example: `~/.hidden_memo/ideas.json`

## MCP Tools

These tools are exposed via MCP:

-   `save_to_table(table, title, content)`
-   `read_table_all(table)`
-   `read_from_table(table, title)`
-   `update_memo_content(table, title, new_content)`
-   `get_latest_data(table)`
-   `list_tables()`
-   `get_all_tables_data()`
-   `delete_memo(table, title)`
-   `drop_table(table)`

## MCP Client Setup (uvx)

### Claude Desktop

```json
{
    "mcpServers": {
        "hidden-memo": {
            "command": "uvx",
            "args": ["--from", "hidden-memo", "hidden-memo", "serve"]
        }
    }
}
```

### Codex (OpenAI)

```toml
[mcp_servers.hidden-memo]
command = "uvx"
args = ["--from", "hidden-memo", "hidden-memo", "serve"]
```

### Cursor

```json
{
    "mcpServers": {
        "hidden-memo": {
            "command": "uvx",
            "args": ["--from", "hidden-memo", "hidden-memo", "serve"]
        }
    }
}
```

## CLI

Start the MCP server:

```bash
hidden-memo serve
```

Save a memo:

```bash
hidden-memo save projects hidden_memo "{\"name\": \"hidden-memo\", \"status\": \"ship\"}"
```

Shell-specific quoting (save)

-   Bash/Zsh (macOS/Linux):

```bash
hidden-memo save projects hidden_memo '{"name":"hidden-memo","status":"ship"}'
```

-   Windows CMD:

```bat
hidden-memo save projects hidden_memo "{\"name\":\"hidden-memo\",\"status\":\"ship\"}"
```

-   PowerShell:

```powershell
hidden-memo save projects hidden_memo '{"name":"hidden-memo","status":"ship"}'
```

Read a memo (or all memos in a table when title is omitted):

```bash
hidden-memo read projects hidden_memo
hidden-memo read projects
```

Update a memo:

```bash
hidden-memo update projects hidden_memo "{\"status\": \"published\"}"
```

Shell-specific quoting (update)

-   Bash/Zsh (macOS/Linux):

```bash
hidden-memo update projects hidden_memo '{"status":"published"}'
```

-   Windows CMD:

```bat
hidden-memo update projects hidden_memo "{\"status\":\"published\"}"
```

-   PowerShell:

```powershell
hidden-memo update projects hidden_memo '{"status":"published"}'
```

Get latest in a table:

```bash
hidden-memo latest projects
```

List tables:

```bash
hidden-memo ls
```

Delete a memo or drop a table:

```bash
hidden-memo delete projects hidden_memo
hidden-memo drop projects
```
