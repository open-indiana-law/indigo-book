"""Minimal landing pages. CC0 book text; MIT code; not legal advice."""

from pathlib import Path

MARK_ALT = (
    "Open Indiana Law logo: a green dome, split like an open book, with a gold "
    "bookmark rising through it to a small gold light, above stone steps."
)
BRAND_DIR = Path(__file__).resolve().parent / "brand"

_CSS = """
:root {
  color-scheme: light dark;
  --paper: #F6F0E2; --ink: #1C1917; --muted: #5C5348; --rule: #D6CBB6;
  --card: #F9F5EA; --link: #1E5A46; --flag: #8F7E5E;
}
@media (prefers-color-scheme: dark) {
  :root {
    --paper: #14181F; --ink: #EFE9D8; --muted: #B8B1A0; --rule: #2C343F;
    --card: #1D232C; --link: #6FC4A6; --flag: #B8B1A0;
  }
}
html, body { background: var(--paper); color: var(--ink); }
body {
  font: 17px/1.55 "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
  max-width: 40rem; margin: 0 auto; padding: 2.25rem 1.25rem 3rem;
}
.brand { margin: 0 0 1rem; }
.brand img { display: block; width: 5.5rem; height: 5.5rem; border-radius: 0.75rem; }
.flag { font: 0.78rem/1.3 ui-sans-serif, system-ui, sans-serif;
  letter-spacing: 0.08em; text-transform: uppercase; color: var(--flag); margin: 0 0 1rem; }
h1 { font-size: 1.85rem; font-weight: 600; margin: 0 0 0.75rem; }
h2 { font-size: 1.15rem; margin: 1.75rem 0 0.5rem; }
p, li { margin: 0 0 0.85rem; }
a { color: var(--link); }
"""


def brand_path(name: str) -> Path:
    path = BRAND_DIR / name
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


PUBLIC_HOST = "indigo.openindianalaw.org"
OG_DESCRIPTION = "The Indigo Book, a CC0 citation manual, for AI assistants. Not legal advice."


def _head_icons(title: str = "Indigo Book MCP", path: str = "/") -> str:
    return f"""  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#F6F0E2" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#14181F" media="(prefers-color-scheme: dark)">
  <meta name="description" content="{OG_DESCRIPTION}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Open Indiana Law">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{OG_DESCRIPTION}">
  <meta property="og:url" content="https://{PUBLIC_HOST}{path}">
  <meta property="og:image" content="https://{PUBLIC_HOST}/og.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Open Indiana Law: the open book dome mark above the name.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://{PUBLIC_HOST}/og.png">"""


def manifest_json() -> str:
    import json

    return json.dumps({
        "name": "Indigo Book MCP · Open Indiana Law",
        "short_name": "Indigo Book MCP",
        "description": "CC0 citation manual for AI assistants",
        "start_url": "/",
        "display": "browser",
        "background_color": "#F6F0E2",
        "theme_color": "#F6F0E2",
        "icons": [
            {"src": "/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any"},
            {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png", "purpose": "any"},
        ],
    }, indent=2)


def _logo() -> str:
    return f'<p class="brand"><img src="/icon.svg" width="88" height="88" alt="{MARK_ALT}"></p>'


def landing_html() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Indigo Book MCP</title>
{_head_icons("Indigo Book MCP", "/")}
  <style>{_CSS}</style>
</head>
<body>
  {_logo()}
  <p class="flag">Open Indiana Law</p>
  <h1>Indigo Book MCP</h1>
  <p>A local, read-only MCP of <cite>The Indigo Book: A Manual of Legal Citation</cite>
  (CC0, Public.Resource.Org). Not The Bluebook. Not legal advice.</p>
  <p>Hosted at <a href="https://indigo.openindianalaw.org/mcp">indigo.openindianalaw.org/mcp</a>.
  Source: <a href="https://github.com/open-indiana-law/indigo-book">open-indiana-law/indigo-book</a>
  and <a href="https://indigobook.github.io/">indigobook.github.io</a>.
  Terms: <a href="/terms">/terms</a>.
  Privacy: <a href="/privacy">/privacy</a>.</p>
  <p>This service counts only how many times each tool is used and each page is opened, per day. It does not record what you ask.</p>
</body>
</html>
"""


def terms_html() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Indigo Book MCP terms</title>
{_head_icons("Indigo Book MCP terms", "/terms")}
  <style>{_CSS}</style>
</head>
<body>
  {_logo()}
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


def privacy_html() -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Indigo Book MCP — privacy</title>
{_head_icons("Indigo Book MCP — privacy", "/privacy")}
  <style>{_CSS}</style>
</head>
<body>
  {_logo()}
  <p class="flag"><a href="/">← Indigo Book MCP</a></p>
  <h1>Privacy</h1>
  <p>Last updated 26 October 2026. Open Indiana Law is a public-good
  project operated by Danielle Teagarden. This page covers the unofficial
  Indigo Book MCP at
  <a href="https://indigo.openindianalaw.org">indigo.openindianalaw.org</a>
  and its aliases.</p>
  <p><strong>Not The Bluebook. Not legal advice.</strong>
  Do not send confidential client facts or sealed material to a public
  endpoint.</p>
  <h2>What this service is</h2>
  <p>A read-only search layer over The Indigo Book (CC0, Public.Resource.Org).
  No account is required. The tools do not write to the store.</p>
  <h2>What we collect on purpose</h2>
  <p>We do not keep a published log of search text, rule ids, or other tool
  arguments. We count how often each tool is used and each page is opened.
  For each UTC day we keep only how many times a tool or page was called,
  and how many of those calls failed. We do not record who called, from
  where, or what was asked. The counts are not sold and are not used to
  train a model.</p>
  <h2>What hosts see anyway</h2>
  <p>Traffic reaches the origin through a Cloudflare Tunnel. Cloudflare
  and the origin host can see ordinary web metadata: IP address, time,
  User-Agent, requested path, and status code. We do not run extra
  advertising or social pixels.</p>
  <p>If you connect through Claude, Cursor, or another AI client, that
  client also sees your prompts and our replies under <em>its</em>
  privacy policy.</p>
  <h2>Contact</h2>
  <p>Questions:
  <a href="https://github.com/open-indiana-law/indigo-book/issues">GitHub issues</a>.
  Related Code MCP privacy:
  <a href="https://mcp.openindianalaw.org/privacy">mcp.openindianalaw.org/privacy</a>.</p>
</body>
</html>
"""


def icon_svg() -> str:
    return brand_path("icon.svg").read_text(encoding="utf-8")
