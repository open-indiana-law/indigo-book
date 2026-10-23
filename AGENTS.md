# Indigo Book MCP — Agent Protocol

Fleet policy: https://github.com/noble-pirate/cruise-log/blob/main/AGENTS.md

## Project identity

- **Purpose:** Local MCP of The Indigo Book (CC0 citation manual) with full-text search and retrieval.
- **Human owner:** Danielle Teagarden
- **Class:** shared tool / open legal infrastructure
- **Portfolio record:** https://github.com/noble-pirate/cruise-log/blob/main/projects/indigo-book.md
- **Source of truth:** vendored HTML under `data/source/`; SQLite store at `data/store/indigo-book.db`

## Working boundaries

- Agents may ingest the vendored CC0 HTML, change parser/MCP code, and add tests.
- Do not ingest The Bluebook or other in-copyright citation manuals.
- Do not contact Public.Resource.Org, Indigo Book editors, or GitHub `indigobook` without Danielle's approval.
- Public GitHub, hosting, DNS, and Cloudflare need explicit approval.

## Setup and verification

- **Supported runtime:** Python 3.11+
- **Install:** `python3 -m pip install -e '.[dev]'`
- **Ingest:** `python3 -m indigo_book.ingest`
- **Run:** `INDIGO_BOOK_DB=data/store/indigo-book.db PYTHONPATH=src python3 -m indigo_book.mcp_server`
- **Test:** `python3 -m pytest`

## Git and review

- Work on a task branch; do not push directly to `main`.
- Merging, public release, and production deployment require Danielle's approval.

## Deployment and data

- **Staging / production:** none. Local stdio or loopback `:8766` only.
- **Data classification:** public CC0 text plus original MCP code (MIT).
- **Recovery:** rebuild the store from `data/source/` with `python3 -m indigo_book.ingest`.
