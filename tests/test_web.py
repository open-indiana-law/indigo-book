from indigo_book import web
from indigo_book.mcp_server import build_server


def test_landing_has_locked_mark():
    landing = web.landing_html()
    assert "Indigo Book MCP" in landing
    assert "--paper: #F6F0E2" in landing and "--paper: #14181F" in landing
    assert 'href="/favicon.svg"' in landing
    assert 'src="/icon.svg"' in landing
    assert "green dome" in landing
    assert "not legal advice" in landing.lower()
    assert 'href="/privacy"' in landing
    privacy = web.privacy_html()
    assert "do not send" in privacy.lower()
    assert "train a model" in privacy


def test_icon_svg_is_locked_mark():
    svg = web.icon_svg()
    assert "#2E8068" in svg and "#B3820B" in svg and "#8F7E5E" in svg
    assert "#F6F0E2" in svg
    assert web.brand_path("favicon.ico").is_file()


def test_icon_routes_registered():
    mcp = build_server(conn=object())
    paths = {route.path for route in mcp._custom_starlette_routes}
    assert {"/", "/terms", "/privacy", "/icon.svg", "/favicon.svg", "/favicon.ico", "/apple-touch-icon.png", "/site.webmanifest", "/og.png", "/icon-512.png", "/health"} <= paths


def test_manifest_theme_color_and_share_card():
    import json

    landing = web.landing_html()
    assert 'rel="manifest" href="/site.webmanifest"' in landing
    assert 'content="#14181F" media="(prefers-color-scheme: dark)"' in landing
    assert 'property="og:image" content="https://indigo.openindianalaw.org/og.png"' in landing
    assert 'name="twitter:card" content="summary_large_image"' in landing
    assert json.loads(web.manifest_json())["start_url"] == "/"
    assert web.brand_path("og.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
