# Indigo Book MCP

Public repo: [open-legal-tools/indigo-book](https://github.com/open-legal-tools/indigo-book).

A local, read-only [MCP](https://modelcontextprotocol.io/) of
[The Indigo Book: A Manual of Legal Citation](https://indigobook.github.io/).
Full text of the CC0 second edition is searchable and retrievable by rule.

This is **not** The Bluebook and is **not legal advice**.

## Source

Current edition in the store: **Second Edition (2023 updates, 2nd printing)**,
HTML and PDF from [indigobook.github.io](https://indigobook.github.io/versions/indigobook-2.0-rev2023-2.html).
The 2022 second edition and 2016 first edition are ingested as additional
editions. Public.Resource.Org dedicated the work to the public domain under
[CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).

Cite as: *The Indigo Book: A Manual of Legal Citation* (Christopher Sprigman &
Jennifer Romig et al. eds., Public.Resource.Org 2d ed. 2021).

## Tools

- `indigo_search` — full-text search
- `indigo_get_rule` — one rule or table (`R10.2`, `T3`, `A`)
- `indigo_get_text` — rule plus nested subrules, or the whole book
- `indigo_browse` — table of contents

Every response names the edition, CC0, and that this is not legal advice.

## Setup

```bash
python3 -m pip install -e '.[dev]'
python3 -m indigo_book.ingest
INDIGO_BOOK_DB=data/store/indigo-book.db PYTHONPATH=src python3 -m indigo_book.mcp_server
python3 -m pytest
```

Default MCP transport is stdio. `--http` serves streamable HTTP on loopback
`:8766` (landing `/`, terms `/terms`, MCP `/mcp`). No public host or DNS is
configured.

## Limits

No Bluebook text is included. No message to Public.Resource.Org. Hosting and
DNS each need a separate approval.
