import ast
import asyncio
import datetime
import json
from pathlib import Path

import typer
from mcp.server.fastmcp import FastMCP
from tinydb import Query, TinyDB

HOME_DIR = Path.home()
MEMO_ROOT = HOME_DIR / ".hidden_memo"
MEMO_ROOT.mkdir(parents=True, exist_ok=True)

mcp = FastMCP("hidden_memo")
app = typer.Typer(help="Hidden Memo CLI & MCP Server")


def get_db(table_name: str) -> TinyDB:
    """Returns a TinyDB instance for the specified table name."""
    return TinyDB(MEMO_ROOT / f"{table_name}.json")


def parse_content(content: str) -> dict:
    """Parses JSON string or Python literal dict string for CLI flexibility."""
    try:
        return json.loads(content)
    except (json.JSONDecodeError, ValueError):
        # Fallback to ast for cases where shell strips double quotes
        return ast.literal_eval(content)


# ---------------------------------
# Core Logic
# ---------------------------------
async def core_save(table: str, title: str, content: dict) -> str:
    db = get_db(table)
    item = Query()
    now = datetime.datetime.now().isoformat()
    data = {"title": title, "content": content, "created_at": now, "updated_at": now}
    db.upsert(data, item.title == title)
    return f"Data successfully secured in the '{table}' table."


async def core_read_all(table: str) -> list[dict]:
    return get_db(table).all()


async def core_read_item(table: str, title: str) -> dict:
    db = get_db(table)
    item = Query()
    result = db.get(item.title == title)
    return result["content"] if result else {"error": "Document not found."}


async def core_update(table: str, title: str, new_content: dict) -> str:
    db = get_db(table)
    item = Query()
    existing = db.get(item.title == title)
    if not existing:
        return f"Error: Memo with title '{title}' not found in '{table}'."
    db.update(
        {"content": new_content, "updated_at": datetime.datetime.now().isoformat()},
        item.title == title,
    )
    return f"Successfully updated content for '{title}' in '{table}'."


async def core_get_latest(table: str) -> dict:
    all_data = await core_read_all(table)
    if not all_data:
        return {"error": "The table is empty."}
    return max(all_data, key=lambda x: x.get("updated_at", ""))


async def core_get_all_tables_data() -> dict[str, list]:
    all_data = {}
    json_files = list(MEMO_ROOT.glob("*.json"))
    if not json_files:
        return {"info": "No tables found."}
    for f in json_files:
        all_data[f.stem] = get_db(f.stem).all()
    return all_data


async def core_delete(table: str, title: str) -> str:
    db = get_db(table)
    item = Query()
    if not db.contains(item.title == title):
        return f"Error: Memo with title '{title}' not found in '{table}'."
    db.remove(item.title == title)
    return f"Successfully deleted '{title}' from '{table}'."


async def core_drop_table(table: str) -> str:
    db_path = MEMO_ROOT / f"{table}.json"
    if db_path.exists():
        db_path.unlink()
        return f"Table '{table}' has been completely removed."
    return f"Error: Table '{table}' does not exist."


# ---------------------------------
# MCP
# ---------------------------------
@mcp.tool()
async def save_to_table(table: str, title: str, content: dict) -> str:
    """
    Saves or updates unstructured data in a specific table.

    Args:
        table (str): The name of the table (JSON file) where data will be stored.
        title (str): A unique identifier for the record.
        content (dict): The actual JSON data to be stored.
    """
    return await core_save(table, title, content)


@mcp.tool()
async def read_table_all(table: str) -> list[dict]:
    """
    Retrieves all documents stored in a specific table.
    Use this when you need the full context of a certain category.

    Args:
        table (str): The name of the table (category) to read.
    """
    return await core_read_all(table)


@mcp.tool()
async def read_from_table(table: str, title: str) -> dict:
    """
    Retrieves a specific document from a table using its title.

    Args:
        table (str): The name of the table to search in.
        title (str): The unique title of the document to retrieve.
    """
    return await core_read_item(table, title)


@mcp.tool()
async def update_memo_content(table: str, title: str, new_content: dict) -> str:
    """
    Partially updates the content of an existing memo without changing the title.

    Args:
        table (str): The name of the table where the memo exists.
        title (str): The title of the memo to update.
        new_content (dict): The new JSON data to merge or replace in the 'content' field.
    """
    return await core_update(table, title, new_content)


@mcp.tool()
async def get_latest_data(table: str) -> dict:
    """
    Retrieves the most recently inserted or updated document from a specific table.

    Args:
        table (str): The name of the table to retrieve the latest data from.
    """
    return await core_get_latest(table)


@mcp.tool()
async def list_tables() -> list[str]:
    """
    Returns a list of all currently existing tables (JSON files).
    """
    return [f.stem for f in MEMO_ROOT.glob("*.json")]


@mcp.tool()
async def get_all_tables_data() -> dict[str, list]:
    """
    Retrieves all data from every existing table (JSON file).
    Returns a dictionary where keys are table names and values are lists of documents.
    """
    return await core_get_all_tables_data()


@mcp.tool()
async def delete_memo(table: str, title: str) -> str:
    """
    Deletes a specific memo from a table using its title.
    This operation is irreversible, so ensure the title is correct before proceeding.

    Args:
        table (str): The name of the table (JSON file) where the memo is stored.
        title (str): The unique title identifier of the memo to be deleted.
    """
    return await core_delete(table, title)


@mcp.tool()
async def drop_table(table: str) -> str:
    """
    Deletes an entire table (JSON file) and all its data.

    Args:
        table (str): The name of the table (JSON file) to be deleted.
    """
    return await core_drop_table(table)


# ---------------------------------
# CLI
# ---------------------------------
@app.command()
def serve():
    """Start the MCP server for Claude Desktop or other clients."""
    mcp.run()


@app.command()
def save(table: str, title: str, content: str):
    """CLI: Save/Update a memo. (content: JSON string)"""
    try:
        data = parse_content(content)
        res = asyncio.run(core_save(table, title, data))
        typer.echo(res)
    except Exception as e:
        typer.secho(f"Error parsing content: {e}", fg=typer.colors.RED)


@app.command()
def read(table: str, title: str = typer.Argument(None, help="Specific title to read")):
    """CLI: Read a specific memo or all memos in a table."""
    try:
        res = (
            asyncio.run(core_read_item(table, title))
            if title
            else asyncio.run(core_read_all(table))
        )
        typer.echo(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


@app.command()
def update(table: str, title: str, content: str):
    """CLI: Update an existing memo's content. (content: JSON string)"""
    try:
        data = parse_content(content)
        res = asyncio.run(core_update(table, title, data))
        typer.echo(res)
    except Exception as e:
        typer.secho(f"Error parsing content: {e}", fg=typer.colors.RED)


@app.command()
def latest(table: str):
    """CLI: Retrieves the most recently inserted or updated document from a table."""
    try:
        res = asyncio.run(core_get_latest(table))
        typer.echo(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


@app.command()
def dump():
    """CLI: Display all data from all existing tables."""
    res = asyncio.run(core_get_all_tables_data())
    typer.echo(json.dumps(res, indent=2, ensure_ascii=False))


@app.command()
def ls():
    """CLI: List all table names."""
    tables = [f.stem for f in MEMO_ROOT.glob("*.json")]
    typer.echo(f"Tables: {tables}")


@app.command()
def delete(table: str, title: str):
    """CLI: Delete a specific memo by title."""
    try:
        res = asyncio.run(core_delete(table, title))
        color = typer.colors.GREEN if "Successfully" in res else typer.colors.RED
        typer.secho(res, fg=color)
    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)


@app.command()
def drop(table: str):
    """CLI: Delete an entire table."""
    if typer.confirm(f"Are you sure you want to drop table '{table}'?"):
        try:
            res = asyncio.run(core_drop_table(table))
            typer.secho(res, fg=typer.colors.YELLOW)
        except Exception as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED)


def main():
    """Unified entry point for CLI and MCP."""
    app()


if __name__ == "__main__":
    main()
