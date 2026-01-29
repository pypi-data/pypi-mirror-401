"""UI output utilities for ForgeTerm."""

from __future__ import annotations

import json
import os


def should_use_ui_format(args_format: str | None = None) -> bool:
    """Check if UI format should be used."""
    if args_format == "ui":
        return True
    return os.environ.get("FORGETERM_UI") == "1"


def output_ui(blocks: list) -> None:
    """Output UiBlock JSON for ForgeTerm."""
    if not isinstance(blocks, list):
        blocks = [blocks]
    print(json.dumps({"uiVersion": 1, "blocks": blocks}, separators=(',', ':')))


def table_block(title: str, columns: list[str], rows: list[list]) -> dict:
    """Create a table block."""
    return {"type": "table", "title": title, "columns": columns, "rows": rows}


def card_block(
    title: str,
    subtitle: str | None = None,
    body: str | None = None,
    tone: str | None = None,
) -> dict:
    """Create a card block."""
    b: dict = {"type": "card", "title": title}
    if subtitle:
        b["subtitle"] = subtitle
    if body:
        b["body"] = body
    if tone:
        b["tone"] = tone
    return b


def error_block(msg: str) -> dict:
    """Create an error card block."""
    return card_block("Error", body=str(msg), tone="error")
