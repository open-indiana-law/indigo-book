"""Minimal landing pages. CC0 book text; MIT code; not legal advice."""

LANDING = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Indigo Book MCP</title></head>
<body>
<h1>Indigo Book MCP</h1>
<p>A local, read-only MCP of <cite>The Indigo Book: A Manual of Legal Citation</cite>
(CC0, Public.Resource.Org). Not The Bluebook. Not legal advice.</p>
<p>Hosted at <a href="https://indigo.openindianalaw.org/mcp">indigo.openindianalaw.org/mcp</a>.
Source: <a href="https://github.com/open-indiana-law/indigo-book">open-indiana-law/indigo-book</a>
and <a href="https://indigobook.github.io/">indigobook.github.io</a>.
Terms: <a href="/terms">/terms</a>.</p>
<p>This service counts only how many times each tool is used and each page is opened, per day. It does not record what you ask.</p>
</body></html>
"""

TERMS = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Indigo Book MCP terms</title></head>
<body>
<h1>Terms</h1>
<p>The Indigo Book is published by Public.Resource.Org under a CC0 1.0 public
domain dedication. This MCP copies that text so agents can search and retrieve
full rules. It is not affiliated with or authorized by The Bluebook.</p>
<p>This service is not legal advice and is not an official court or bar
publication. Verify citations against the edition you must follow.</p>
<p>Cite as: The Indigo Book: A Manual of Legal Citation (Christopher Sprigman
&amp; Jennifer Romig et al. eds., Public.Resource.Org 2d ed. 2021).</p>
</body></html>
"""


def landing_html() -> str:
    return LANDING


def terms_html() -> str:
    return TERMS
