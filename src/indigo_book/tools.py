"""Read-only Indigo Book lookups. CC0 text; not legal advice; not the Bluebook."""
from __future__ import annotations

import re
import sqlite3

DISCLAIMER = (
    "The Indigo Book is a CC0 public-domain citation manual published by "
    "Public.Resource.Org. It is not The Bluebook and is not affiliated with "
    "or authorized by The Bluebook. This tool is not legal advice."
)
SOURCE_PAGE = "https://indigobook.github.io/"
CITE_AS = (
    "The Indigo Book: A Manual of Legal Citation "
    "(Christopher Sprigman & Jennifer Romig et al. eds., "
    "Public.Resource.Org 2d ed. 2021)."
)
RULE_TOKEN = re.compile(
    r"\b(R\d+(?:\.\d+){0,3}|T\d+(?:\.\d+){0,2}|[A-J])\b",
    re.I,
)
_STOP = {
    "a", "an", "the", "of", "to", "in", "on", "for", "and", "or", "is", "are",
    "be", "by", "what", "when", "how", "do", "does", "with", "as", "at",
}


def _current(conn: sqlite3.Connection, edition_id: str | None = None):
    if edition_id:
        row = conn.execute(
            "SELECT * FROM edition WHERE edition_id=?", (edition_id,)
        ).fetchone()
        if row:
            return row
    row = conn.execute(
        "SELECT * FROM edition WHERE is_current=1 LIMIT 1"
    ).fetchone()
    return row or conn.execute("SELECT * FROM edition LIMIT 1").fetchone()


def _assurance(conn: sqlite3.Connection, edition=None) -> dict:
    ed = edition or _current(conn)
    editions = [
        dict(r)
        for r in conn.execute(
            "SELECT edition_id, version, label, published, source_url, is_current "
            "FROM edition ORDER BY edition_id"
        )
    ]
    return {
        "cc0": True,
        "license": "CC0-1.0",
        "not_legal_advice": True,
        "not_the_bluebook": True,
        "disclaimer": DISCLAIMER,
        "cite_as": CITE_AS,
        "source_page": SOURCE_PAGE,
        "edition_id": ed["edition_id"] if ed else None,
        "edition_label": ed["label"] if ed else None,
        "edition_url": ed["source_url"] if ed else None,
        "editions": editions,
    }


def _row_out(row: sqlite3.Row, *, include_text: bool, include_html: bool = False) -> dict:
    out = {
        "slug": row["slug"],
        "rule_id": row["rule_id"],
        "heading": row["heading"],
        "kind": row["kind"],
        "part": row["part"],
        "parent_slug": row["parent_slug"],
        "level": row["level"],
    }
    if include_text:
        out["text"] = row["text"]
        out["full_text"] = f"{row['heading']}\n\n{row['text']}".strip()
    if include_html:
        out["html"] = row["html"]
    return out


def _fts_query(q: str) -> str:
    words = [w for w in re.findall(r"[\w.]+", q) if w.lower() not in _STOP] or re.findall(
        r"[\w.]+", q
    )
    return " ".join('"%s"' % w.replace('"', "") for w in words)


def normalize_rule(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    m = RULE_TOKEN.search(value)
    if not m:
        return value
    token = m.group(1)
    if len(token) == 1:
        return token.upper()
    return token[0].upper() + token[1:]


def search(
    conn: sqlite3.Connection,
    query: str,
    *,
    edition_id: str | None = None,
    kind: str | None = None,
    limit: int = 10,
) -> dict:
    ed = _current(conn, edition_id)
    limit = max(1, min(int(limit), 25))
    out = {"query": query, "results": [], "flags": [], **_assurance(conn, ed)}
    if not ed:
        out["flags"].append("store is empty; run ingest")
        return out
    if not query.strip():
        out["flags"].append("empty query")
        return out
    token = normalize_rule(query)
    sql = (
        "SELECT s.*, snippet(section_fts, 1, '[', ']', '...', 24) AS snip "
        "FROM section_fts JOIN section s ON s.id=section_fts.rowid "
        "WHERE section_fts MATCH ? AND s.edition_id=? "
    )
    args: list = [_fts_query(query), ed["edition_id"]]
    if kind:
        sql += "AND s.kind=? "
        args.append(kind)
    sql += "ORDER BY rank LIMIT ?"
    args.append(limit)
    try:
        rows = list(conn.execute(sql, args))
    except sqlite3.OperationalError:
        rows = []
        out["flags"].append("fts query failed; try fewer words")
    if not rows and token:
        row = conn.execute(
            "SELECT * FROM section WHERE edition_id=? AND (rule_id=? OR slug=?) "
            "ORDER BY sort_order LIMIT 1",
            (ed["edition_id"], token, query.strip().lower()),
        ).fetchone()
        if row:
            rows = [row]
            out["flags"].append("exact rule_id match")
    for row in rows:
        item = _row_out(row, include_text=False)
        item["snippet"] = row["snip"] if "snip" in row.keys() else row["text"][:240]
        out["results"].append(item)
    if not out["results"]:
        out["flags"].append("no hits")
    return out


def get_rule(
    conn: sqlite3.Connection,
    rule: str,
    *,
    edition_id: str | None = None,
    include_children: bool = True,
) -> dict:
    ed = _current(conn, edition_id)
    out = {"rule": rule, **_assurance(conn, ed)}
    if not ed:
        out["found"] = False
        out["flags"] = ["store is empty; run ingest"]
        return out
    token = normalize_rule(rule) or rule.strip()
    slug = rule.strip().lower().replace(".", "-")
    row = conn.execute(
        "SELECT * FROM section WHERE edition_id=? AND (rule_id=? OR slug=?) "
        "ORDER BY length(IFNULL(rule_id,'')) ASC, sort_order LIMIT 1",
        (ed["edition_id"], token, slug),
    ).fetchone()
    if not row:
        out["found"] = False
        out["flags"] = ["rule not found"]
        nearby = [
            _row_out(r, include_text=False)
            for r in conn.execute(
                "SELECT * FROM section WHERE edition_id=? AND "
                "(rule_id LIKE ? OR heading LIKE ?) ORDER BY sort_order LIMIT 8",
                (ed["edition_id"], f"{token}%", f"%{rule.strip()}%"),
            )
        ]
        out["nearby"] = nearby
        return out
    body = _row_out(row, include_text=True, include_html=True)
    children = []
    if include_children:
        children = [
            _row_out(r, include_text=True)
            for r in conn.execute(
                "SELECT * FROM section WHERE edition_id=? AND parent_slug=? "
                "ORDER BY sort_order",
                (ed["edition_id"], row["slug"]),
            )
        ]
        if children:
            parts = [body["full_text"]] + [c["full_text"] for c in children]
            body["full_text"] = "\n\n".join(parts)
    out.update(found=True, flags=[], **body, children=children)
    return out


def browse(
    conn: sqlite3.Connection,
    *,
    edition_id: str | None = None,
    part: str | None = None,
    kind: str | None = None,
) -> dict:
    ed = _current(conn, edition_id)
    out = {"entries": [], **_assurance(conn, ed)}
    if not ed:
        out["flags"] = ["store is empty; run ingest"]
        return out
    sql = "SELECT * FROM section WHERE edition_id=?"
    args: list = [ed["edition_id"]]
    if part:
        token = normalize_rule(part) or part
        sql += " AND (part=? OR rule_id=?)"
        args.extend([token, token])
    if kind:
        sql += " AND kind=?"
        args.append(kind)
    elif not part:
        sql += " AND kind IN ('part','frontmatter','backmatter')"
    sql += " ORDER BY sort_order"
    out["entries"] = [_row_out(r, include_text=False) for r in conn.execute(sql, args)]
    out["flags"] = []
    return out


def get_text(
    conn: sqlite3.Connection,
    rule: str | None = None,
    *,
    edition_id: str | None = None,
    whole_book: bool = False,
) -> dict:
    """Return full text of one rule (with descendants) or the current edition."""
    ed = _current(conn, edition_id)
    out = {**_assurance(conn, ed)}
    if not ed:
        out["found"] = False
        out["flags"] = ["store is empty; run ingest"]
        return out
    if whole_book or not rule:
        rows = list(
            conn.execute(
                "SELECT heading, text FROM section WHERE edition_id=? ORDER BY sort_order",
                (ed["edition_id"],),
            )
        )
        text = "\n\n".join(f"{r['heading']}\n\n{r['text']}".strip() for r in rows)
        out.update(
            found=True,
            flags=["full edition text"],
            heading=ed["label"],
            full_text=text,
            section_count=len(rows),
            characters=len(text),
        )
        return out
    got = get_rule(conn, rule, edition_id=ed["edition_id"], include_children=False)
    if not got.get("found"):
        return got
    start = conn.execute(
        "SELECT sort_order FROM section WHERE edition_id=? AND slug=?",
        (ed["edition_id"], got["slug"]),
    ).fetchone()
    rows = list(
        conn.execute(
            "SELECT * FROM section WHERE edition_id=? AND sort_order>=? ORDER BY sort_order",
            (ed["edition_id"], start["sort_order"]),
        )
    )
    collected = []
    start_level = rows[0]["level"]
    for i, r in enumerate(rows):
        if i and r["level"] <= start_level:
            break
        collected.append(_row_out(r, include_text=True))
    full = "\n\n".join(c["full_text"] for c in collected)
    out.update(
        found=True,
        flags=[],
        slug=got["slug"],
        rule_id=got["rule_id"],
        heading=got["heading"],
        kind=got["kind"],
        full_text=full,
        section_count=len(collected),
        characters=len(full),
    )
    return out
