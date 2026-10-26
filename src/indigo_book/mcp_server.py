"""Local, read-only MCP server for The Indigo Book. CC0 text; not legal advice.

Run:  INDIGO_BOOK_DB=/path/to/indigo-book.db PYTHONPATH=src python -m indigo_book.mcp_server
"""
from __future__ import annotations

import os
import sqlite3
import sys
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import FileResponse, HTMLResponse, JSONResponse

from . import tools, usage, web

INSTRUCTIONS = (
    "The Indigo Book: A Manual of Legal Citation (CC0, Public.Resource.Org). "
    "A free implementation of the Uniform System of Citation for U.S. legal "
    "documents. Not The Bluebook and not affiliated with it. Use indigo_search "
    "to find rules, indigo_get_rule for one rule (R10.2, T3), indigo_get_text "
    "for full text of a rule and its descendants or the whole book, and "
    "indigo_browse for the table of contents. Always say the copy is CC0, name "
    "the edition, and that this is not legal advice."
)


def _connect():
    path = os.environ.get("INDIGO_BOOK_DB", "")
    if not path or not os.path.exists(path):
        sys.exit("Set INDIGO_BOOK_DB to the path of a built indigo-book.db store.")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def build_server(conn=None, host: str = "127.0.0.1", port: int = 8766):
    mcp = FastMCP(
        "indigo-book",
        instructions=INSTRUCTIONS,
        website_url="https://indigobook.github.io/",
        host=host,
        port=port,
        stateless_http=True,
        json_response=True,
    )
    db = conn or _connect()
    counter = usage.from_env()
    usage.count_tools(mcp, counter)
    usage.count_pages(mcp, counter)
    ro = dict(readOnlyHint=True, idempotentHint=True, openWorldHint=False, destructiveHint=False)

    @mcp.custom_route("/", methods=["GET"], name="landing")
    async def landing(_request: Request) -> HTMLResponse:
        return HTMLResponse(web.landing_html())

    @mcp.custom_route("/terms", methods=["GET"], name="terms")
    async def terms(_request: Request) -> HTMLResponse:
        return HTMLResponse(web.terms_html())

    @mcp.custom_route("/privacy", methods=["GET"], name="privacy")
    async def privacy(_request: Request) -> HTMLResponse:
        return HTMLResponse(web.privacy_html())

    @mcp.custom_route("/icon.svg", methods=["GET"], name="icon")
    async def icon(_request: Request) -> FileResponse:
        return FileResponse(web.brand_path("icon.svg"), media_type="image/svg+xml")

    @mcp.custom_route("/favicon.svg", methods=["GET"], name="favicon_svg")
    async def favicon_svg(_request: Request) -> FileResponse:
        return FileResponse(web.brand_path("favicon.svg"), media_type="image/svg+xml")

    @mcp.custom_route("/favicon.ico", methods=["GET"], name="favicon_ico")
    async def favicon_ico(_request: Request) -> FileResponse:
        return FileResponse(web.brand_path("favicon.ico"), media_type="image/x-icon")

    @mcp.custom_route("/apple-touch-icon.png", methods=["GET"], name="apple_touch")
    async def apple_touch(_request: Request) -> FileResponse:
        return FileResponse(web.brand_path("apple-touch-icon.png"), media_type="image/png")

    @mcp.custom_route("/health", methods=["GET"], name="health")
    async def health(_request: Request) -> JSONResponse:
        return JSONResponse({"ok": True, "service": "indigo-book", "cc0": True})

    @mcp.tool(title="Search The Indigo Book", annotations=ToolAnnotations(title="Search The Indigo Book", **ro))
    def indigo_search(query: str, edition_id: str | None = None, kind: str | None = None, limit: int = 10) -> dict[str, Any]:
        """Full-text search of Indigo Book rules, tables, and commentary. Returns headings and snippets; fetch full text with indigo_get_rule or indigo_get_text. `kind` may be rule, table, part, frontmatter, or backmatter."""
        return tools.search(db, query, edition_id=edition_id, kind=kind, limit=limit)

    @mcp.tool(title="Get an Indigo Book rule", annotations=ToolAnnotations(title="Get an Indigo Book rule", **ro))
    def indigo_get_rule(rule: str, edition_id: str | None = None, include_children: bool = True) -> dict[str, Any]:
        """Return the full text of one rule or table, such as 'R10.2', 'R4.6.2', 'T3', or 'A'. Direct children are included by default."""
        return tools.get_rule(db, rule, edition_id=edition_id, include_children=include_children)

    @mcp.tool(title="Get Indigo Book full text", annotations=ToolAnnotations(title="Get Indigo Book full text", **ro))
    def indigo_get_text(rule: str | None = None, edition_id: str | None = None, whole_book: bool = False) -> dict[str, Any]:
        """Return the full text of a rule and all nested subrules, or the entire current edition when whole_book is true."""
        return tools.get_text(db, rule, edition_id=edition_id, whole_book=whole_book)

    @mcp.tool(title="Browse Indigo Book contents", annotations=ToolAnnotations(title="Browse Indigo Book contents", **ro))
    def indigo_browse(part: str | None = None, kind: str | None = None, edition_id: str | None = None) -> dict[str, Any]:
        """Table of contents. With no args, lists parts and front matter. `part` is A–J; `kind` is rule, table, or part."""
        return tools.browse(db, edition_id=edition_id, part=part, kind=kind)

    return mcp


def main(argv: list[str] | None = None) -> None:
    args = list(argv if argv is not None else sys.argv[1:])
    transport = os.environ.get("INDIGO_BOOK_TRANSPORT", "stdio")
    if "--http" in args:
        transport = "streamable-http"
    host = os.environ.get("INDIGO_BOOK_HOST", "127.0.0.1")
    port = int(os.environ.get("INDIGO_BOOK_PORT", "8766"))
    if transport not in {"stdio", "streamable-http", "sse"}:
        sys.exit(f"Unknown INDIGO_BOOK_TRANSPORT={transport!r}")
    build_server(host=host, port=port).run(transport=transport)


if __name__ == "__main__":
    main()
