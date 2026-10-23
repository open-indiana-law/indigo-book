"""Load vendored Indigo Book HTML into the store. CC0; not legal advice."""
from __future__ import annotations

import argparse
from pathlib import Path

from . import parse, store

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "source"
DEFAULT_DB = ROOT / "data" / "store" / "indigo-book.db"

EDITIONS = [
    {
        "edition_id": "2.0-2023-2",
        "version": "2.0",
        "label": "Second Edition (2023 updates, 2nd printing)",
        "published": "2023-08-25",
        "source_url": "https://indigobook.github.io/versions/indigobook-2.0-rev2023-2.html",
        "filename": "indigobook-2.0-rev2023-2.html",
        "is_current": True,
        "license": "CC0-1.0",
    },
    {
        "edition_id": "2.0-2022",
        "version": "2.0",
        "label": "Second Edition (2022)",
        "published": "2022-08-31",
        "source_url": "https://indigobook.github.io/versions/indigobook-2.0.html",
        "filename": "indigobook-2.0.html",
        "is_current": False,
        "license": "CC0-1.0",
    },
    {
        "edition_id": "1.0-2016",
        "version": "1.0",
        "label": "First Edition (2016)",
        "published": "2016-05-02",
        "source_url": "https://law.resource.org/pub/us/code/blue/IndigoBook.html",
        "filename": "indigobook-1.0.html",
        "is_current": False,
        "license": "CC0-1.0",
    },
]


def ingest_edition(conn, spec: dict, source_dir: Path) -> dict:
    path = source_dir / spec["filename"]
    html = path.read_text(encoding="utf-8")
    sections = parse.parse_html(html)
    meta = {
        **spec,
        "source_path": str(path),
        "source_sha256": store.sha256_file(path),
    }
    n = store.replace_edition(conn, meta, sections)
    return {
        "edition_id": spec["edition_id"],
        "sections": n,
        "rules": sum(1 for s in sections if s["kind"] == "rule"),
        "tables": sum(1 for s in sections if s["kind"] == "table"),
        "sha256": meta["source_sha256"],
        "source_url": spec["source_url"],
        "license": spec["license"],
        "cc0": True,
        "not_legal_advice": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest Indigo Book HTML (CC0).")
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--source", default=str(SOURCE))
    args = parser.parse_args(argv)
    conn = store.connect(args.db)
    source_dir = Path(args.source)
    reports = [ingest_edition(conn, spec, source_dir) for spec in EDITIONS]
    conn.close()
    for row in reports:
        print(
            f"{row['edition_id']}: {row['sections']} sections "
            f"({row['rules']} rules, {row['tables']} tables) "
            f"sha256={row['sha256'][:12]}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
