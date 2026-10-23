from pathlib import Path

from indigo_book import parse, store, tools

FIXTURE = """<!doctype html><html><body>
<h2 id="a-background-rules">A. BACKGROUND RULES</h2>
<p>Part intro.</p>
<h3 id="r1">R1 Scope</h3>
<p>The Indigo Book states the rules for standard legal documents.</p>
<h4 id="r1-1">R1.1 Standard Legal Documents</h4>
<p>Court filings and memoranda.</p>
<h3 id="r4">R4 Signals</h3>
<p>Use a signal to show support.</p>
<h4 id="r4-6">R4.6 Signals for Supporting Authority</h4>
<p>Parent of see.</p>
<h5 id="r4-6-4">R4.6.4 See</h5>
<p>See is used when the citation clearly supports the proposition.</p>
<h2 id="t-tables">H. TABLES</h2>
<h3 id="t3">T3. Jurisdictions</h3>
<p>Indiana abbreviations live in table T3.</p>
</body></html>
"""


def test_duplicate_rule_numbers_get_unique_slugs():
    html = """<h3 id="r12-3">R12.3 First</h3><p>a</p>
<h3 id="r12-3">R12.3 Second</h3><p>b</p>"""
    sections = parse.parse_html(html)
    slugs = [s["slug"] for s in sections]
    assert slugs == ["r12-3", "r12-3-2"]
    assert [s["rule_id"] for s in sections] == ["R12.3", "R12.3"]


def test_parse_rules_and_parents():
    sections = parse.parse_html(FIXTURE)
    by_id = {s["rule_id"]: s for s in sections if s["rule_id"]}
    assert by_id["R1.1"]["parent_slug"] == "r1"
    assert by_id["R4.6.4"]["text"].startswith("See is used")
    assert by_id["T3"]["kind"] == "table"
    assert by_id["A"]["kind"] == "part"


def test_search_get_and_full_text(tmp_path: Path):
    db = tmp_path / "indigo-book.db"
    conn = store.connect(db)
    sections = parse.parse_html(FIXTURE)
    store.replace_edition(
        conn,
        {
            "edition_id": "fixture",
            "version": "2.0",
            "label": "Fixture",
            "published": "2023-08-25",
            "source_url": "https://indigobook.github.io/",
            "source_path": "fixture.html",
            "source_sha256": "abc",
            "license": "CC0-1.0",
            "is_current": True,
        },
        sections,
    )
    hits = tools.search(conn, "see supports the proposition")
    assert hits["cc0"] is True
    assert hits["not_the_bluebook"] is True
    assert any(r["rule_id"] == "R4.6.4" for r in hits["results"])
    got = tools.get_rule(conn, "R4.6.4")
    assert got["found"] is True
    assert "clearly supports" in got["full_text"]
    chapter = tools.get_text(conn, "R4")
    assert "R4.6.4 See" in chapter["full_text"]
    book = tools.get_text(conn, whole_book=True)
    assert book["section_count"] == len(sections)
    toc = tools.browse(conn)
    assert any(e["rule_id"] == "A" for e in toc["entries"])
