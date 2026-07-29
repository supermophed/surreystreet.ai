#!/usr/bin/env python3
"""
Surrey Street Partners — static blog builder.

Turns markdown posts (content/blog/*.md, each with YAML-ish frontmatter) into:
  - /blog/<slug>/index.html   one page per post, from templates/post.html
  - /blog/index.html          the listing page, from templates/blog-index.html
  - /blog/rss.xml             RSS 2.0 feed (full content + summary)
  - /sitemap.xml              regenerated with core pages + every post

Zero third-party dependencies — runs on any stock Python 3.8+.

Usage:
    python3 build_blog.py            # build everything
    python3 build_blog.py --check    # build, then validate every post's OG/SEO tags

Frontmatter fields (in content/blog/<slug>.md, between leading --- fences):
    title:        required.  The post headline.
    description:  required.  ~1-2 sentences. Used for meta description, OG, RSS, listing.
    slug:         optional.  URL segment. Defaults to the filename without .md.
    date:         optional.  YYYY-MM-DD. Defaults to today.
    author:       optional.  Defaults to "Surrey Street Partners".
    og_image:     optional.  Absolute or root-relative image URL for the unfurl card.
                             Defaults to DEFAULT_OG_IMAGE below.
    og_image_alt: optional.  Alt text for the OG image.
    eyebrow:      optional.  Small kicker above the title (e.g. "Payments").
    draft:        optional.  true => skipped by the build (won't publish).
"""

import os
import re
import sys
import html
import json
import datetime

# ── Config ──────────────────────────────────────────────────────────────────
SITE_URL          = "https://surreystreet.ai"          # no trailing slash
ROOT              = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR       = os.path.join(ROOT, "content", "blog")
OUT_BLOG_DIR      = os.path.join(ROOT, "blog")
TEMPLATE_POST     = os.path.join(ROOT, "templates", "post.html")
TEMPLATE_INDEX    = os.path.join(ROOT, "templates", "blog-index.html")
SITEMAP_PATH      = os.path.join(ROOT, "sitemap.xml")
OUT_TEASER_DIR    = os.path.join(ROOT, "teasers")   # copy-paste promo blurbs (not linked from the site)

DEFAULT_AUTHOR    = "Surrey Street Partners"
DEFAULT_OG_IMAGE  = "/logo/leopard_face.png"
DEFAULT_EYEBROW   = "Insights"
ORG_NAME          = "Surrey Street Partners"

# beehiiv subscribe form (v3 embed). This is the `data-beehiiv-form` value from
# Subscribers → Subscribe forms → Get embed code. Until it's set, the band
# renders a styled, non-functional placeholder so you can see the layout.
BEEHIIV_FORM_ID   = "358a45c0-b037-4d97-9539-76a43f858308"

# Core (non-blog) URLs to keep in the sitemap, with change frequency + priority.
# NOTE: /index.md and /llms.txt intentionally NOT in sitemap — they're LLM/agent
# discovery files, not search-indexable pages. Keeping them in sitemap creates
# false "not indexed" signals in Google Search Console.
CORE_URLS = [
    ("/",              "monthly", "1.0"),
    ("/consulting/",   "monthly", "0.8"),
    ("/team/",         "monthly", "0.8"),
    ("/blog/",         "weekly",  "0.9"),
    ("/privacy.html",  "yearly",  "0.4"),
    ("/terms.html",    "yearly",  "0.4"),
    ("/consent.html",  "yearly",  "0.3"),
]


# ── Frontmatter ─────────────────────────────────────────────────────────────
def _parse_kv(block):
    """Parse a block of `key: value` lines (a small YAML subset: optional
    quotes, inline `[a, b]` lists). Used for both frontmatter and sidecars."""
    meta = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",")]
            meta[key] = [v for v in items if v]
        else:
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            meta[key] = val
    return meta


def parse_frontmatter(text):
    """Split a markdown file into (frontmatter dict, body). Frontmatter is the
    block between leading `---` fences; absent that, returns ({}, text)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n", 1)
    rest = parts[1] if len(parts) > 1 else ""
    end = rest.find("\n---")
    if end == -1:
        return {}, text
    fm_block = rest[:end]
    body = rest[end + 4:]              # skip the "\n---"
    if body.startswith("\n"):
        body = body[1:]
    return _parse_kv(fm_block), body


def strip_leading_comment(body):
    """Remove a single leading HTML comment block (e.g. 'Editor notes: delete
    before publish') so drafts straight from Cowork never leak notes on-page."""
    return re.sub(r"^\s*<!--.*?-->\s*", "", body, count=1, flags=re.S)


def extract_h1(body):
    """If the first non-blank line is a `# Heading`, lift it out as the document
    title and strip it from the body (so it isn't rendered twice). Returns
    (title_or_None, body)."""
    lines = body.split("\n")
    for idx, line in enumerate(lines):
        if line.strip() == "":
            continue
        m = re.match(r"^#\s+(.*?)\s*#*\s*$", line)
        if m:
            del lines[idx]
            return m.group(1).strip(), "\n".join(lines)
        break  # first real line isn't an H1 — nothing to lift
    return None, body


# ── Inline markdown ─────────────────────────────────────────────────────────
def _render_inline(text):
    """Escape HTML, then apply inline markdown. Code spans, links, and images
    are tokenized first so emphasis never mangles their contents or URLs."""
    text = html.escape(text, quote=False)        # & < >  (leaves quotes alone)
    stash = []

    def keep(htmlfrag):
        stash.append(htmlfrag)
        return "\x00%d\x00" % (len(stash) - 1)

    # inline code: `code`
    text = re.sub(r"`([^`]+)`",
                  lambda m: keep("<code>%s</code>" % m.group(1)), text)

    # images: ![alt](src "title")
    def img(m):
        alt, src = m.group(1), m.group(2)
        title = ' title="%s"' % m.group(3) if m.group(3) else ""
        return keep('<img src="%s" alt="%s"%s>' % (src, alt, title))
    text = re.sub(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', img, text)

    # links: [text](href "title")
    def link(m):
        label, href = m.group(1), m.group(2)
        title = ' title="%s"' % m.group(3) if m.group(3) else ""
        ext = ' target="_blank" rel="noopener noreferrer"' if href.startswith("http") else ""
        return keep('<a href="%s"%s%s>%s</a>' % (href, title, ext, label))
    text = re.sub(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)', link, text)

    # bold then italic
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"(?<![_\w])_([^_\n]+)_(?!_)", r"<em>\1</em>", text)

    # restore stashed tokens
    text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


# ── Block markdown ──────────────────────────────────────────────────────────
def markdown_to_html(md):
    """A pragmatic markdown -> HTML converter covering what prose posts use:
    headings, paragraphs, lists, blockquotes, fenced code, tables, rules,
    images, and raw-HTML block passthrough."""
    lines = md.replace("\r\n", "\n").split("\n")
    out = []
    i, n = 0, len(lines)

    def is_blank(s):
        return s.strip() == ""

    while i < n:
        line = lines[i]

        # blank
        if is_blank(line):
            i += 1
            continue

        # fenced code ```lang
        m = re.match(r"^```(.*)$", line)
        if m:
            i += 1
            buf = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # closing fence
            code = html.escape("\n".join(buf), quote=False)
            out.append("<pre><code>%s</code></pre>" % code)
            continue

        # horizontal rule
        if re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # ATX heading
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if m:
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, _render_inline(m.group(2)), level))
            i += 1
            continue

        # blockquote
        if line.lstrip().startswith(">"):
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = markdown_to_html("\n".join(buf))
            out.append("<blockquote>%s</blockquote>" % inner)
            continue

        # table (pipe) — header row, separator row of ---, then body
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lines[i + 1]) \
                and "|" in lines[i + 1]:
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < n and "|" in lines[i] and not is_blank(lines[i]):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join("<th>%s</th>" % _render_inline(c) for c in header)
            body = ""
            for r in rows:
                body += "<tr>%s</tr>" % "".join("<td>%s</td>" % _render_inline(c) for c in r)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (thead, body))
            continue

        # unordered list
        if re.match(r"^\s*[-*+]\s+", line):
            i, htmlfrag = _consume_list(lines, i, ordered=False)
            out.append(htmlfrag)
            continue

        # ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            i, htmlfrag = _consume_list(lines, i, ordered=True)
            out.append(htmlfrag)
            continue

        # raw HTML block passthrough (line starts with a tag)
        if re.match(r"^\s*<(?:div|section|figure|iframe|img|table|ul|ol|p|h[1-6]|blockquote|pre|video|svg|a)\b", line, re.I):
            buf = []
            while i < n and not is_blank(lines[i]):
                buf.append(lines[i])
                i += 1
            out.append("\n".join(buf))
            continue

        # paragraph — gather until blank line
        buf = []
        while i < n and not is_blank(lines[i]) and not _starts_block(lines[i]):
            buf.append(lines[i])
            i += 1
        para = " ".join(s.strip() for s in buf)
        out.append("<p>%s</p>" % _render_inline(para))

    return "\n".join(out)


def _starts_block(line):
    """True if this line begins a non-paragraph block (so a paragraph stops)."""
    return bool(
        re.match(r"^```", line) or
        re.match(r"^#{1,6}\s", line) or
        re.match(r"^\s*([-*_])(\s*\1){2,}\s*$", line) or
        re.match(r"^\s*[-*+]\s+", line) or
        re.match(r"^\s*\d+\.\s+", line) or
        line.lstrip().startswith(">")
    )


def _consume_list(lines, i, ordered):
    n = len(lines)
    pat = r"^\s*\d+\.\s+(.*)$" if ordered else r"^\s*[-*+]\s+(.*)$"
    items = []
    while i < n:
        m = re.match(pat, lines[i])
        if not m:
            break
        items.append(_render_inline(m.group(1)))
        i += 1
    tag = "ol" if ordered else "ul"
    body = "".join("<li>%s</li>" % it for it in items)
    return i, "<%s>%s</%s>" % (tag, body, tag)


# ── Post model ──────────────────────────────────────────────────────────────
def reading_time(md):
    """Estimate reading time from prose only. URLs, code blocks and link targets are
    stripped first — otherwise a link-heavy post (a sources list, say) counts every
    path segment as a word and badly overstates the time."""
    t = re.sub(r"```.*?```", " ", md, flags=re.S)          # fenced code
    t = re.sub(r"`[^`]*`", " ", t)                          # inline code
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)        # links/images -> visible text only
    t = re.sub(r"<[^>]+>", " ", t)                          # raw html tags
    t = re.sub(r"https?://\S+", " ", t)                     # bare urls
    words = len(re.findall(r"\w+", t))
    mins = max(1, round(words / 200))
    return "%d min read" % mins


def human_date(iso):
    try:
        d = datetime.datetime.strptime(iso, "%Y-%m-%d")
        return d.strftime("%B %-d, %Y")
    except ValueError:
        return iso


def rfc822_date(iso):
    try:
        d = datetime.datetime.strptime(iso, "%Y-%m-%d")
    except ValueError:
        d = datetime.datetime.utcnow()
    return d.strftime("%a, %d %b %Y 00:00:00 +0000")


def abs_url(path_or_url):
    if path_or_url.startswith("http"):
        return path_or_url
    return SITE_URL + (path_or_url if path_or_url.startswith("/") else "/" + path_or_url)


def load_posts():
    posts = []
    if not os.path.isdir(CONTENT_DIR):
        return posts
    for fn in sorted(os.listdir(CONTENT_DIR)):
        if not fn.endswith(".md") or fn.startswith("_"):
            continue
        path = os.path.join(CONTENT_DIR, fn)
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        meta, body = parse_frontmatter(raw)
        base = os.path.splitext(fn)[0]

        # Sidecar metadata: <slug>.meta holds publishing fields I own, so the
        # prose .md can be re-synced from Cowork without losing them. Inline
        # frontmatter (if any) overrides the sidecar.
        sidecar = os.path.join(CONTENT_DIR, base + ".meta")
        if os.path.exists(sidecar):
            with open(sidecar, encoding="utf-8") as sf:
                merged = _parse_kv(sf.read())
            merged.update(meta)
            meta = merged

        # Clean a raw Cowork draft: drop a leading editor-notes comment, lift the
        # leading "# H1" out as the title.
        body = strip_leading_comment(body)
        h1, body = extract_h1(body)

        if str(meta.get("draft", "")).lower() in ("true", "1", "yes"):
            continue
        title = meta.get("title") or h1
        desc = meta.get("description", "")
        if not title:
            print("  ! skipping %s — no title (add frontmatter, a %s.meta sidecar, "
                  "or a leading '# H1')" % (fn, base))
            continue
        slug = meta.get("slug") or base
        date = meta.get("date") or datetime.date.today().isoformat()
        posts.append({
            "file": fn,
            "title": title,
            "description": desc,
            "slug": slug,
            "date": date,
            "author": meta.get("author", DEFAULT_AUTHOR),
            "subtitle": meta.get("subtitle", ""),
            "hero": meta.get("hero", ""),
            "og_image": abs_url(meta.get("og_image") or meta.get("hero") or DEFAULT_OG_IMAGE),
            "og_image_alt": meta.get("og_image_alt", title),
            "eyebrow": meta.get("eyebrow", DEFAULT_EYEBROW),
            "canonical": "%s/blog/%s/" % (SITE_URL, slug),
            "body_md": body,
            "body_html": markdown_to_html(body),
            "reading_time": reading_time(body),
            "tags": _norm_tags(meta.get("tags")),
            "updated": meta.get("updated") or date,
        })
    # newest first
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def _norm_tags(v):
    if not v:
        return []
    if isinstance(v, list):
        return [t.strip() for t in v if str(t).strip()]
    return [t.strip() for t in str(v).split(",") if t.strip()]


def tag_meta(post):
    """keywords + article:tag meta — only emitted when the post declares tags."""
    tags = post.get("tags") or []
    if not tags:
        return ""
    lines = ['<meta name="keywords" content="%s">' % html.escape(", ".join(tags), quote=True)]
    lines += ['<meta property="article:tag" content="%s">' % html.escape(t, quote=True) for t in tags]
    return "\n".join(lines)


def jsonld(post):
    data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post["title"],
        "description": post["description"],
        "image": post["og_image"],
        "datePublished": post["date"],
        "dateModified": post["date"],
        "url": post["canonical"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": post["canonical"]},
        "author": {"@type": "Person", "name": post["author"], "url": SITE_URL},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "logo": {"@type": "ImageObject", "url": abs_url("/logo/leopard_face.png")},
        },
    }
    if post.get("tags"):
        data["keywords"] = ", ".join(post["tags"])
    return json.dumps(data, indent=2)


# ── Render ──────────────────────────────────────────────────────────────────
def fill(template, mapping):
    out = template
    for k, v in mapping.items():
        out = out.replace("{{%s}}" % k, v)
    return out


def subscribe_band():
    """The branded newsletter band. When BEEHIIV_FORM_ID is set, the beehiiv
    form supplies its own title + subtitle, so we render just the navy frame
    around it (no duplicate heading). Until then, an on-brand placeholder with
    full chrome shows the intended layout."""
    if BEEHIIV_FORM_ID:
        return (
            '<section class="subscribe-band subscribe-band--embed" '
            'aria-label="Subscribe to the newsletter">\n'
            '    <div class="subscribe-embed">'
            '<script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" '
            'data-beehiiv-form="%s"></script></div>\n'
            '  </section>' % BEEHIIV_FORM_ID
        )
    return (
        '<section class="subscribe-band" aria-label="Subscribe to the newsletter">\n'
        '    <div class="eyebrow">The Newsletter</div>\n'
        '    <h3>Get these in your inbox</h3>\n'
        '    <p class="lead">Occasional field notes on payments, open banking, '
        'capital markets, and AI infrastructure. No noise.</p>\n'
        '    <form class="subscribe-form" onsubmit="return false">\n'
        '      <input type="email" placeholder="you@company.com" aria-label="Email address">\n'
        '      <button type="submit">Subscribe</button>\n'
        '    </form>\n'
        '    <p class="subscribe-note">Placeholder — set '
        '<code>BEEHIIV_FORM_ID</code> in build_blog.py to wire this to beehiiv.</p>\n'
        '  </section>'
    )


def subtitle_html(post):
    """Optional standfirst under the title — rendered only when the .meta sets `subtitle`."""
    if not post.get("subtitle"):
        return ""
    return '<p class="article-subtitle">%s</p>' % html.escape(post["subtitle"], quote=False)


def hero_html(post):
    """Optional on-page hero image at the top of a post — rendered only when the
    post's .meta sets `hero` (a root-relative image path). Also becomes the OG
    card unless the post sets an explicit og_image."""
    if not post.get("hero"):
        return ""
    alt = html.escape(post.get("og_image_alt") or post["title"], quote=True)
    return '<img class="article-hero" src="%s" alt="%s">' % (post["hero"], alt)


def render_posts(posts, template):
    for p in posts:
        mapping = {
            "TITLE": html.escape(p["title"], quote=True),
            "DESCRIPTION": html.escape(p["description"], quote=True),
            "AUTHOR": html.escape(p["author"], quote=True),
            "CANONICAL_URL": p["canonical"],
            "OG_IMAGE": p["og_image"],
            "OG_IMAGE_ALT": html.escape(p["og_image_alt"], quote=True),
            "PUB_DATE_ISO": p["date"],
            "MOD_DATE_ISO": p.get("updated", p["date"]),
            "PUB_DATE_HUMAN": human_date(p["date"]),
            "TAG_META": tag_meta(p),
            "READING_TIME": p["reading_time"],
            "EYEBROW": html.escape(p["eyebrow"], quote=True),
            "SUBTITLE": subtitle_html(p),
            "HERO": hero_html(p),
            "BODY_HTML": p["body_html"],
            "JSONLD": jsonld(p),
            "SUBSCRIBE": subscribe_band(),
        }
        page = fill(template, mapping)
        out_dir = os.path.join(OUT_BLOG_DIR, p["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print("  + /blog/%s/" % p["slug"])


def render_index(posts, template):
    if posts:
        items = []
        for p in posts:
            items.append(
                '  <a class="post-item" href="/blog/%s/">\n'
                '    <div class="post-item-eyebrow">%s</div>\n'
                '    <h2>%s</h2>\n'
                '    <p>%s</p>\n'
                '    <div class="post-item-meta"><span>%s</span>'
                '<span class="dot">&#10022;</span><span>%s</span></div>\n'
                '    <span class="post-arrow">Read &rarr;</span>\n'
                '  </a>' % (
                    p["slug"],
                    html.escape(p["eyebrow"]),
                    html.escape(p["title"]),
                    html.escape(p["description"]),
                    human_date(p["date"]),
                    p["reading_time"],
                )
            )
        post_items = "\n".join(items)
    else:
        post_items = '  <div class="empty-state">No posts yet — first insight coming soon.</div>'
    page = template.replace("{{POST_ITEMS}}", post_items)
    page = page.replace("{{SUBSCRIBE}}", subscribe_band())
    os.makedirs(OUT_BLOG_DIR, exist_ok=True)
    with open(os.path.join(OUT_BLOG_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("  + /blog/  (index, %d post%s)" % (len(posts), "" if len(posts) == 1 else "s"))


def render_rss(posts):
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for p in posts:
        items.append(
            "    <item>\n"
            "      <title>%s</title>\n"
            "      <link>%s</link>\n"
            "      <guid isPermaLink=\"true\">%s</guid>\n"
            "      <pubDate>%s</pubDate>\n"
            "      <description>%s</description>\n"
            "      <content:encoded><![CDATA[%s]]></content:encoded>\n"
            "    </item>" % (
                html.escape(p["title"]),
                p["canonical"],
                p["canonical"],
                rfc822_date(p["date"]),
                html.escape(p["description"]),
                p["body_html"],
            )
        )
    feed = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/" '
        'xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        "    <title>Surrey Street Partners — Insights</title>\n"
        "    <link>%s/blog/</link>\n"
        '    <atom:link href="%s/blog/rss.xml" rel="self" type="application/rss+xml"/>\n'
        "    <description>Field notes on payments, open banking, capital markets, commerce, and AI infrastructure.</description>\n"
        "    <language>en-us</language>\n"
        "    <lastBuildDate>%s</lastBuildDate>\n"
        "%s\n"
        "  </channel>\n"
        "</rss>\n" % (SITE_URL, SITE_URL, now, "\n".join(items))
    )
    os.makedirs(OUT_BLOG_DIR, exist_ok=True)
    with open(os.path.join(OUT_BLOG_DIR, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(feed)
    print("  + /blog/rss.xml")


def render_sitemap(posts):
    today = datetime.date.today().isoformat()
    urls = []
    for loc, freq, pri in CORE_URLS:
        urls.append((SITE_URL + loc, today, freq, pri))
    for p in posts:
        urls.append((p["canonical"], p["date"], "monthly", "0.7"))
    body = ""
    for loc, lastmod, freq, pri in urls:
        body += (
            "  <url>\n"
            "    <loc>%s</loc>\n"
            "    <lastmod>%s</lastmod>\n"
            "    <changefreq>%s</changefreq>\n"
            "    <priority>%s</priority>\n"
            "  </url>\n" % (loc, lastmod, freq, pri)
        )
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          "%s</urlset>\n" % body)
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(sm)
    print("  + /sitemap.xml  (%d urls)" % len(urls))


# ── Teasers (for LinkedIn / lead-gen) ───────────────────────────────────────
def _plain_text(md):
    """Strip markdown formatting to plain prose for an excerpt."""
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", md)     # images -> alt
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)        # links  -> text
    t = re.sub(r"`([^`]+)`", r"\1", t)                    # code
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"__([^_]+)__", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"(?<!\w)_([^_]+)_(?!\w)", r"\1", t)
    return t.strip()


def _first_paragraph(body_md):
    """The lede — first real paragraph, skipping headings/lists/quotes/code."""
    for block in re.split(r"\n\s*\n", body_md.strip()):
        b = block.strip()
        if not b:
            continue
        if (b.startswith("#") or b.startswith(">") or b.startswith("```")
                or b.startswith("<") or re.match(r"^\s*[-*+]\s", b)
                or re.match(r"^\s*\d+\.\s", b)):
            continue
        return " ".join(line.strip() for line in b.splitlines())
    return ""


def with_utm(url, source, slug, medium="social"):
    sep = "&" if "?" in url else "?"
    return "%s%sutm_source=%s&utm_medium=%s&utm_campaign=%s" % (url, sep, source, medium, slug)


def render_teasers(posts):
    """Emit a copy-paste promo blurb per post for LinkedIn / lead-gen, with
    UTM-tagged links so source tracking survives referrer stripping. These are
    working files (not linked from the site); rebuilding overwrites them."""
    os.makedirs(OUT_TEASER_DIR, exist_ok=True)
    for p in posts:
        slug, url = p["slug"], p["canonical"]
        lede = _plain_text(_first_paragraph(p["body_md"]))
        cta = "Read the full piece → %s" % with_utm(url, "linkedin", slug)
        out = [
            "# Teaser — %s" % p["title"],
            "# Auto-generated by build_blog.py. Edit before posting; rebuilding overwrites this file.",
            "",
            "=== READY TO PASTE (LinkedIn / social) ===",
            p["title"],
            "",
            lede,
            "",
            cta,
            "",
            "=== UTM SHARE LINKS (pick by destination) ===",
            "LinkedIn:   %s" % with_utm(url, "linkedin", slug),
            "X/Twitter:  %s" % with_utm(url, "twitter", slug),
            "Newsletter: %s" % with_utm(url, "newsletter", slug, "email"),
            "Generic:    %s" % with_utm(url, "referral", slug),
            "",
            "=== COMPONENTS ===",
            "Headline:  %s" % p["title"],
            "One-liner: %s" % p["description"],
            "Hook:      %s" % lede,
            "",
        ]
        with open(os.path.join(OUT_TEASER_DIR, slug + ".md"), "w", encoding="utf-8") as f:
            f.write("\n".join(out))
        print("  + teasers/%s.md" % slug)


# ── OG / SEO validation ─────────────────────────────────────────────────────
REQUIRED_TAGS = [
    ('<link rel="canonical"', "canonical link"),
    ('property="og:title"', "og:title"),
    ('property="og:description"', "og:description"),
    ('property="og:image"', "og:image"),
    ('property="og:url"', "og:url"),
    ('property="og:type"', "og:type"),
    ('name="twitter:card"', "twitter:card"),
    ('name="twitter:image"', "twitter:image"),
    ('name="description"', "meta description"),
]


def check_post(slug):
    path = os.path.join(OUT_BLOG_DIR, slug, "index.html")
    if not os.path.exists(path):
        return ["FILE MISSING: %s" % path]
    with open(path, encoding="utf-8") as f:
        htmltext = f.read()
    problems = []
    for needle, label in REQUIRED_TAGS:
        if needle not in htmltext:
            problems.append("missing %s" % label)
    # og:image must resolve to a real local file (root-relative) or be remote
    m = re.search(r'property="og:image" content="([^"]+)"', htmltext)
    if m:
        img = m.group(1)
        local = img.replace(SITE_URL, "")
        if local.startswith("/"):
            fp = os.path.join(ROOT, local.lstrip("/"))
            if not os.path.exists(fp):
                problems.append("og:image file not found on disk: %s" % local)
    else:
        problems.append("could not read og:image url")
    return problems


def run_checks(posts):
    print("\nUnfurl / SEO check:")
    all_ok = True
    for p in posts:
        problems = check_post(p["slug"])
        if problems:
            all_ok = False
            print("  ✗ /blog/%s/" % p["slug"])
            for pr in problems:
                print("      - %s" % pr)
        else:
            print("  ✓ /blog/%s/  (title, description, canonical, OG, Twitter all present; og:image resolves)" % p["slug"])
    return all_ok


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    with open(TEMPLATE_POST, encoding="utf-8") as f:
        tpl_post = f.read()
    with open(TEMPLATE_INDEX, encoding="utf-8") as f:
        tpl_index = f.read()

    posts = load_posts()
    print("Building %d post%s from %s" %
          (len(posts), "" if len(posts) == 1 else "s",
           os.path.relpath(CONTENT_DIR, ROOT)))
    render_posts(posts, tpl_post)
    render_index(posts, tpl_index)
    render_rss(posts)
    render_sitemap(posts)
    render_teasers(posts)

    if not BEEHIIV_FORM_ID:
        print("\n  note: BEEHIIV_FORM_ID is unset — subscribe band shows a "
              "placeholder.\n        Set it in build_blog.py before publishing "
              "(see BLOG_PUBLISHING.md).")

    if "--check" in sys.argv:
        ok = run_checks(posts)
        if not ok:
            print("\nSome posts have issues — fix before sharing.")
            sys.exit(1)
        print("\nAll posts pass. Safe to share.")
    print("\nDone. Review locally, then deploy (see BLOG_PUBLISHING.md).")


if __name__ == "__main__":
    main()
