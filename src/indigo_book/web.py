"""Minimal landing pages. CC0 book text; MIT code; not legal advice. Colours follow the Open Indiana Law mark (Statehouse green)."""

_MARK = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Open Indiana Law logo"><defs><mask id="pg"><rect width="100" height="100" fill="#fff"/><g stroke="#000" stroke-width="1.8" fill="none"><path d="M19 72A31 31 0 0 1 46 41.5"/><path d="M81 72A31 31 0 0 0 54 41.5"/><path d="M28 72A22 22 0 0 1 46 51.5"/><path d="M72 72A22 22 0 0 0 54 51.5"/></g></mask></defs><g mask="url(#pg)" fill="#2E8068"><path d="M9 72A41 41 0 0 1 47 31.1V72Z"/><path d="M91 72A41 41 0 0 0 53 31.1V72Z"/></g><circle cx="50" cy="22" r="6.4" fill="#B3820B"/><path d="M50 31V72" stroke="#B3820B" stroke-width="2.56"/><rect x="11.465" y="76" width="77.07" height="4" fill="#8F7E5E"/><rect x="11.465" y="84" width="77.07" height="4" fill="#8F7E5E"/></svg>"""

_CSS = """
:root {
  color-scheme: light dark;
  --paper: #f6f0e2; --ink: #1c1917; --muted: #5c5348; --rule: #d6cbb6;
  --card: #f9f5ea; --link: #1e5a46; --warn: #7a5a07;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #14181f; --ink: #efe9d8; --muted: #b8b1a0; --rule: #2c343f;
    --card: #1d232c; --link: #6fc4a6; --warn: #d9a93c;
  }
}
html, body { background: var(--paper); color: var(--ink); }
body {
  font: 17px/1.55 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  max-width: 40rem; margin: 0 auto; padding: 2.25rem 1.25rem 3rem;
}
.brand { display: flex; align-items: center; gap: 0.75rem; margin: 0 0 1rem; }
.brand svg { width: 2.75rem; height: 2.75rem; flex: none; }
.brand .flag { margin: 0; }
.flag { font: 0.78rem/1.3 ui-sans-serif, system-ui, sans-serif;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 0 0 1rem; }
h1 { font-size: 1.85rem; font-weight: 600; margin: 0 0 0.75rem; }
h2 { font-size: 1.15rem; margin: 1.75rem 0 0.5rem; }
p, li { margin: 0 0 0.85rem; }
a { color: var(--link); }
.warn { border-left: 4px solid var(--warn); padding: 0.35rem 0 0.35rem 0.85rem; }
.note { background: var(--card); border: 1px solid var(--rule); padding: 0.7rem 0.9rem; }
pre, code { font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 0.86rem; }
pre { background: var(--card); border: 1px solid var(--rule); padding: 0.75rem 1rem; overflow: auto; }
ul { padding-left: 1.2rem; }
"""

LANDING = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Indigo Book MCP</title>
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <style>{_CSS}</style>
</head>
<body>
  <div class="brand">{_MARK}<p class="flag">Open Indiana Law</p></div>
<h1>Indigo Book MCP</h1>
<p>A local, read-only MCP of <cite>The Indigo Book: A Manual of Legal Citation</cite>
(CC0, Public.Resource.Org). Not The Bluebook. Not legal advice.</p>
<p>Hosted at <a href="https://indigo.openindianalaw.org/mcp">indigo.openindianalaw.org/mcp</a>.
Source: <a href="https://github.com/open-indiana-law/indigo-book">open-indiana-law/indigo-book</a>
and <a href="https://indigobook.github.io/">indigobook.github.io</a>.
Terms: <a href="/terms">/terms</a>.</p>
<p>This service counts only how many times each tool is used and each page is opened, per day. It does not record what you ask.</p>
</body>
</html>
"""

TERMS = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Indigo Book MCP terms</title>
  <link rel="icon" href="/icon.svg" type="image/svg+xml">
  <style>{_CSS}</style>
</head>
<body>
  <p class="flag"><a href="/">← Indigo Book MCP</a></p>
<h1>Terms</h1>
<p>The Indigo Book is published by Public.Resource.Org under a CC0 1.0 public
domain dedication. This MCP copies that text so agents can search and retrieve
full rules. It is not affiliated with or authorized by The Bluebook.</p>
<p>This service is not legal advice and is not an official court or bar
publication. Verify citations against the edition you must follow.</p>
<p>Cite as: The Indigo Book: A Manual of Legal Citation (Christopher Sprigman
&amp; Jennifer Romig et al. eds., Public.Resource.Org 2d ed. 2021).</p>
</body>
</html>
"""


def icon_svg() -> str:
    """The locked Open Indiana Law mark on its cream ground."""
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" role="img" aria-label="Open Indiana Law logo: a green dome, split like an open book, with a gold bookmark rising through it to a small gold light, above stone steps."><title>Open Indiana Law logo: a green dome, split like an open book, with a gold bookmark rising through it to a small gold light, above stone steps.</title><rect x="-50" y="-50" width="200" height="200" fill="#F6F0E2"/><defs><mask id="pg"><rect width="100" height="100" fill="#fff"/><g stroke="#000" stroke-width="1.8" fill="none"><path d="M19 72A31 31 0 0 1 46 41.5"/><path d="M81 72A31 31 0 0 0 54 41.5"/><path d="M28 72A22 22 0 0 1 46 51.5"/><path d="M72 72A22 22 0 0 0 54 51.5"/></g></mask></defs><g mask="url(#pg)" fill="#2E8068"><path d="M9 72A41 41 0 0 1 47 31.1V72Z"/><path d="M91 72A41 41 0 0 0 53 31.1V72Z"/></g><circle cx="50" cy="22" r="6.4" fill="#B3820B"/><path d="M50 31V72" stroke="#B3820B" stroke-width="2.56"/><rect x="11.465" y="76" width="77.07" height="4" fill="#8F7E5E"/><rect x="11.465" y="84" width="77.07" height="4" fill="#8F7E5E"/></svg>
"""


def landing_html() -> str:
    return LANDING


def terms_html() -> str:
    return TERMS
