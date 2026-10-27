from indigo_book import web


def test_pages_use_the_mark_palette_and_follow_the_device():
    landing = web.landing_html()
    terms = web.terms_html()
    for page in (landing, terms):
        assert "--paper: #f6f0e2" in page and "prefers-color-scheme: dark" in page
        assert 'rel="icon"' in page and "{_" not in page
    assert "Open Indiana Law logo" in landing
    assert "Indigo Book MCP" in landing and "CC0" in landing and "Terms" in landing
    assert "not affiliated with or authorized by The Bluebook" in terms


def test_icon_is_the_locked_mark():
    svg = web.icon_svg()
    assert svg.startswith("<svg") and 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert "#2E8068" in svg and "#B3820B" in svg and "#F6F0E2" in svg


def test_favicon_is_the_hinted_16px_cut():
    svg = web.favicon_svg()
    assert 'viewBox="0 0 16 16"' in svg and "#2E8068" in svg
    assert 'href="/favicon.svg"' in web.landing_html()


def test_manifest_and_theme_color():
    import json
    m = json.loads(web.manifest_json())
    assert m["start_url"] == "/" and m["icons"][0]["src"] == "/icon.svg"
    page = web.landing_html()
    assert 'rel="manifest" href="/site.webmanifest"' in page
    assert 'content="#F6F0E2" media="(prefers-color-scheme: light)"' in page
    assert 'content="#14181F" media="(prefers-color-scheme: dark)"' in page
