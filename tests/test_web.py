from indigo_book import web
from indigo_book.mcp_server import build_server


def test_landing_has_locked_mark():
    landing = web.landing_html()
    assert "Indigo Book MCP" in landing
    assert "background: #F6F0E2" in landing
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
    assert {"/", "/terms", "/privacy", "/icon.svg", "/favicon.svg", "/favicon.ico", "/apple-touch-icon.png", "/health"} <= paths
