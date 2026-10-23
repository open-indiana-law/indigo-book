"""Split Indigo Book HTML into ordered sections. CC0 source; not legal advice."""
from __future__ import annotations

import html as html_lib
import re
from html.parser import HTMLParser

HEADING_RE = re.compile(r"<h([1-6])\b([^>]*)>(.*?)</h\1>", re.I | re.S)
ID_RE = re.compile(r"""\bid\s*=\s*["']([^"']+)["']""", re.I)
TAG_RE = re.compile(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", re.I | re.S)
RULE_RE = re.compile(
    r"^(R\d+(?:\.\d+){0,3}|T\d+(?:\.\d+){0,2}|[A-J])(?:\.|\b)",
    re.I,
)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style"}:
            self._skip += 1
        elif tag in {"p", "div", "li", "br", "h1", "h2", "h3", "h4", "h5", "h6", "tr"}:
            self._chunks.append("\n")
        elif tag == "td":
            self._chunks.append("\t")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self._skip:
            self._skip -= 1
        elif tag in {"p", "div", "li", "table", "blockquote"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip:
            self._chunks.append(data)

    def text(self) -> str:
        raw = "".join(self._chunks)
        raw = html_lib.unescape(raw)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        return re.sub(r"[ \t]{2,}", " ", raw).strip()


def html_to_text(fragment: str) -> str:
    parser = _TextExtractor()
    parser.feed(fragment or "")
    parser.close()
    return parser.text()


def heading_text(inner_html: str) -> str:
    return re.sub(r"\s+", " ", html_to_text(inner_html)).strip()


def slug_from_heading(title: str, fallback: str) -> str:
    m = RULE_RE.match(title)
    if m:
        return m.group(1).lower().replace(".", "-")
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug or fallback


def rule_id_from_heading(title: str) -> str | None:
    m = RULE_RE.match(title)
    if not m:
        return None
    token = m.group(1)
    if len(token) == 1:
        return token.upper()
    return token[0].upper() + token[1:]


def kind_for(rule_id: str | None, title: str) -> str:
    if rule_id and rule_id.startswith("T"):
        return "table"
    if rule_id and rule_id.startswith("R"):
        return "rule"
    if rule_id and len(rule_id) == 1:
        return "part"
    lower = title.lower()
    if "introduction" in lower or "foreword" in lower or "manifest" in lower:
        return "frontmatter"
    if "codicil" in lower or "acknowledgment" in lower:
        return "backmatter"
    return "section"


def parse_html(html: str) -> list[dict]:
    """Return ordered section dicts with slug, rule_id, heading, html, text, level, parent_slug."""
    cleaned = TAG_RE.sub("", html)
    matches = list(HEADING_RE.finditer(cleaned))
    sections: list[dict] = []
    stack: list[tuple[int, str]] = []
    for i, match in enumerate(matches):
        level = int(match.group(1))
        attrs = match.group(2) or ""
        title = heading_text(match.group(3) or "")
        if not title:
            continue
        end = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned)
        body_html = cleaned[match.end() : end].strip()
        attr_id = ID_RE.search(attrs)
        rule_id = rule_id_from_heading(title)
        slug = (attr_id.group(1) if attr_id else slug_from_heading(title, f"s{i}"))
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_slug = stack[-1][1] if stack else None
        part = None
        if parent_slug:
            for prev in reversed(sections):
                if prev["slug"] == parent_slug:
                    part = prev["rule_id"] if prev["kind"] == "part" else prev.get("part")
                    break
        if rule_id and len(rule_id) == 1:
            part = rule_id
        used = {s["slug"] for s in sections}
        unique = slug
        n = 2
        while unique in used:
            unique = f"{slug}-{n}"
            n += 1
        sections.append(
            {
                "slug": unique,
                "rule_id": rule_id,
                "heading": title,
                "kind": kind_for(rule_id, title),
                "part": part,
                "parent_slug": parent_slug,
                "level": level,
                "sort_order": i,
                "html": body_html,
                "text": html_to_text(body_html),
            }
        )
        stack.append((level, unique))
    return sections
