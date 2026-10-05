"""Build the blog: blog/_src/posts/*.md → blog/<slug>/index.html, blog/index.html and blog/sitemap.xml.

    python blog/_system/build.py              build everything that is due
    python blog/_system/build.py --today 2026-12-01   pretend it is another day (to preview scheduled posts)

A post is published when draft is false and its date has arrived (Pakistan time), so future-dated posts
go live on their own day. Writes only inside /blog; exits with an error (and writes nothing) if a post breaks
the SEO rules.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import shutil
import sys
from pathlib import Path

from common import (BLOG_DIR, GENERATED_MARK, TEMPLATES_DIR, Post, check_post, inside_blog, load_config,
                    load_posts, render_post, today)


def fill(template: str, values: dict) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", str(value))
    if "{{" in template:
        raise RuntimeError("template placeholder left unfilled: " + template.split("{{", 1)[1].split("}}", 1)[0])
    return template


def jsonld(data: dict) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")
    return "\n".join("  " + line for line in text.split("\n"))


def human_date(d: dt.date) -> str:
    return f"{d.day} {d.strftime('%b %Y')}"


def write_if_changed(path: Path, text: str) -> bool:
    path = inside_blog(path)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def build(cfg: dict, day: dt.date) -> int:
    site = cfg["site"]
    base, blog_url = site["base_url"], site["base_url"] + "blog/"
    image = base + site["image"]
    esc = lambda s: html.escape(str(s), quote=True)
    tpl = lambda name: (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    partial = lambda name, root, blog: fill(tpl(name), {"root": root, "blog": blog, "email": site["email"]})

    posts = load_posts()
    slugs = [p.slug for p in posts]
    problems = 0
    for p in posts:
        render_post(p, base)
        errors, warnings = check_post(p, cfg, strict=False, known_slugs=set(slugs))
        if slugs.count(p.slug) > 1:
            errors.append(f"slug '{p.slug}' is used by more than one post")
        for w in warnings:
            print(f"  warning  {p.path.name}: {w}")
        for e in errors:
            print(f"  ERROR    {p.path.name}: {e}")
        problems += len(errors)
    if problems:
        print(f"Build stopped: {problems} error(s). Nothing was changed.")
        return 1

    live = sorted([p for p in posts if not p.draft and p.date <= day], key=lambda p: (p.date, p.slug), reverse=True)
    waiting = [p for p in posts if not p.draft and p.date > day]
    changed = []

    # ----- post pages
    for p in live:
        m, url = p.meta, f"{blog_url}{p.slug}/"
        tz = site["timezone_offset"]
        published, modified = f"{p.date}T09:00:00{tz}", f"{p.updated}T09:00:00{tz}"
        values = {
            "slug": p.slug, "page_title": esc(f"{m.get('seo_title') or m['title']} | {site['name']}"),
            "title": esc(m["title"]), "short_title": esc(m.get("short_title") or m.get("seo_title") or m["title"]),
            "description": esc(m["description"]), "dek": esc(m["dek"]), "keywords": esc(", ".join(m["keywords"])),
            "author": esc(m.get("author") or site["author"]), "author_bio": esc(site["author_bio"]), "email": site["email"],
            "site_name": esc(site["name"]), "url": url, "image": image, "category": esc(m["category"]),
            "published_iso": published, "modified_iso": modified,
            "date": p.date.isoformat(), "date_human": human_date(p.date), "reading_time": max(1, round(p.words / 200)),
            "og_tags": "\n".join(f'  <meta property="article:tag" content="{esc(t)}">' for t in m["tags"]),
            "tags_html": "".join(f"<li>{esc(t)}</li>" for t in m["tags"]),
            "toc_html": "\n".join(f'              <li><a href="#{i}">{esc(label)}</a></li>' for i, label in p.toc),
            "body_html": p.html,
            "nav": partial("nav.html", "../../", "../"), "footer": partial("footer.html", "../../", "../"),
            "jsonld_post": jsonld({
                "@context": "https://schema.org", "@type": "BlogPosting", "headline": m["title"],
                "description": m["description"], "keywords": m["keywords"], "articleSection": m["category"],
                "wordCount": p.words, "datePublished": published, "dateModified": modified, "inLanguage": "en",
                "mainEntityOfPage": url, "image": image,
                "author": {"@type": "Person", "name": m.get("author") or site["author"], "url": base},
                "publisher": {"@type": "Person", "name": site["name"], "url": base},
            }),
            "jsonld_crumbs": jsonld({
                "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": base},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": blog_url},
                    {"@type": "ListItem", "position": 3, "name": m.get("short_title") or m.get("seo_title") or m["title"]},
                ]}),
        }
        if write_if_changed(BLOG_DIR / p.slug / "index.html", fill(tpl("post.html"), values)):
            changed.append(f"{p.slug}/index.html")

    # ----- remove pages of posts that were deleted, unpublished or renamed (only folders this script made)
    keep = {p.slug for p in live}
    for folder in BLOG_DIR.iterdir():
        page = folder / "index.html"
        if folder.is_dir() and folder.name not in keep and not folder.name.startswith(("_", ".")) and page.exists() \
                and GENERATED_MARK in page.read_text(encoding="utf-8"):
            shutil.rmtree(inside_blog(folder))
            changed.append(f"{folder.name}/ (removed)")

    # ----- listing
    cards = []
    for n, p in enumerate(live, 1):
        cards.append(f"""        <li class="post-card">
          <a href="{p.slug}/">
            <span class="post-card__num" aria-hidden="true">{n:02d}</span>
            <span class="post-card__meta"><time datetime="{p.date}">{human_date(p.date)}</time> · {esc(p.meta['category'])}</span>
            <h2>{esc(p.meta['title'])}</h2>
            <p>{esc(p.meta['description'])}</p>
            <span class="post-card__more">Read article <span aria-hidden="true">→</span></span>
          </a>
        </li>""")
    listing = fill(tpl("listing.html"), {
        "blog_url": blog_url, "site_name": esc(site["name"]), "image": image,
        "cards_html": "\n".join(cards) if cards else '        <li class="post-card"><p>New articles are on the way.</p></li>',
        "nav": partial("nav.html", "../", "./"), "footer": partial("footer.html", "../", "./"),
        "jsonld_blog": jsonld({
            "@context": "https://schema.org", "@type": "Blog", "name": f"{site['name']}: Blog", "url": blog_url,
            "inLanguage": "en", "author": {"@type": "Person", "name": site["author"], "url": base},
            "blogPost": [{"@type": "BlogPosting", "headline": p.meta["title"], "url": f"{blog_url}{p.slug}/",
                          "datePublished": p.date.isoformat()} for p in live],
        }),
        "jsonld_crumbs": jsonld({
            "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": base},
                {"@type": "ListItem", "position": 2, "name": "Blog"},
            ]}),
    })
    if write_if_changed(BLOG_DIR / "index.html", listing):
        changed.append("index.html")

    # ----- blog sitemap (submit https://…/blog/sitemap.xml in Google Search Console once)
    newest = max((p.updated for p in live), default=day)
    urls = [(blog_url, newest)] + [(f"{blog_url}{p.slug}/", p.updated) for p in live]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               "<!-- Generated by blog/_system/build.py. Blog pages only; the portfolio keeps its own /sitemap.xml. -->\n"
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n" for u, d in urls)
               + "</urlset>\n")
    if write_if_changed(BLOG_DIR / "sitemap.xml", sitemap):
        changed.append("sitemap.xml")

    print(f"Built {len(live)} live post(s) for {day}; {len(waiting)} scheduled for later"
          + (": " + ", ".join(f"{p.slug} ({p.date})" for p in waiting) if waiting else "") + ".")
    print("Changed: " + (", ".join(changed) if changed else "nothing"))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--today", type=dt.date.fromisoformat, help="build as if it were this date (YYYY-MM-DD)")
    args = ap.parse_args()
    config = load_config()
    sys.exit(build(config, args.today or today(config)))
