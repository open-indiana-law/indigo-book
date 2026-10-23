"""SQLite FTS store for Indigo Book sections. CC0 text; not legal advice."""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS edition (
    edition_id TEXT PRIMARY KEY,
    version TEXT NOT NULL,
    label TEXT NOT NULL,
    published TEXT,
    source_url TEXT NOT NULL,
    source_path TEXT NOT NULL,
    source_sha256 TEXT NOT NULL,
    license TEXT NOT NULL,
    is_current INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS section (
    id INTEGER PRIMARY KEY,
    edition_id TEXT NOT NULL,
    slug TEXT NOT NULL,
    rule_id TEXT,
    heading TEXT NOT NULL,
    kind TEXT NOT NULL,
    part TEXT,
    parent_slug TEXT,
    level INTEGER NOT NULL,
    sort_order INTEGER NOT NULL,
    html TEXT NOT NULL,
    text TEXT NOT NULL,
    UNIQUE(edition_id, slug)
);
CREATE INDEX IF NOT EXISTS section_rule ON section(edition_id, rule_id);
"""

FTS = """
DROP TABLE IF EXISTS section_fts;
CREATE VIRTUAL TABLE section_fts USING fts5(
    heading, text, rule_id, slug, edition_id,
    tokenize = 'porter unicode61'
);
INSERT INTO section_fts(rowid, heading, text, rule_id, slug, edition_id)
SELECT id, heading, text, IFNULL(rule_id,''), slug, edition_id FROM section;
"""


def connect(path: str | Path) -> sqlite3.Connection:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA)
    return conn


def rebuild_fts(conn: sqlite3.Connection) -> None:
    conn.executescript(FTS)
    conn.commit()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def replace_edition(conn: sqlite3.Connection, meta: dict, sections: list[dict]) -> int:
    eid = meta["edition_id"]
    conn.execute("DELETE FROM section WHERE edition_id=?", (eid,))
    conn.execute("DELETE FROM edition WHERE edition_id=?", (eid,))
    conn.execute(
        """INSERT INTO edition(edition_id, version, label, published, source_url,
           source_path, source_sha256, license, is_current)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            eid,
            meta["version"],
            meta["label"],
            meta.get("published"),
            meta["source_url"],
            meta["source_path"],
            meta["source_sha256"],
            meta.get("license", "CC0-1.0"),
            1 if meta.get("is_current") else 0,
        ),
    )
    if meta.get("is_current"):
        conn.execute("UPDATE edition SET is_current=0 WHERE edition_id!=?", (eid,))
    conn.executemany(
        """INSERT INTO section(edition_id, slug, rule_id, heading, kind, part,
           parent_slug, level, sort_order, html, text)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        [
            (
                eid,
                s["slug"],
                s.get("rule_id"),
                s["heading"],
                s["kind"],
                s.get("part"),
                s.get("parent_slug"),
                s["level"],
                s["sort_order"],
                s["html"],
                s["text"],
            )
            for s in sections
        ],
    )
    conn.commit()
    rebuild_fts(conn)
    return len(sections)
