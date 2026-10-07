"""Autopilot writer: picks a new topic, writes the article with an AI model, checks it, saves blog/_src/posts/<slug>.md.

    python blog/_system/write.py                 write only if a post is due (see config.yml → autopilot)
    python blog/_system/write.py --force         write now, even if not due
    options: --result FILE (JSON summary for the workflow)  --pr-body FILE (Markdown preview for the pull request)

Providers are tried in the order listed in config.yml; each needs its key in an environment variable
(GEMINI_API_KEY, GROQ_API_KEY). With no keys set, it does nothing and exits cleanly.
Test hook: BLOG_MOCK_RESPONSES=<file.json> replays canned model replies instead of calling any API.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from common import (POSTS_DIR, SYSTEM_DIR, Post, check_post, front_matter_text, inside_blog, keyword_in,
                    load_config, load_posts, render_post, slugify, today)

KEY_ENV = {"gemini": "GEMINI_API_KEY", "groq": "GROQ_API_KEY"}
REPAIRS = 2   # how many times a model may rewrite its work after failing the checks


class LLMError(Exception):
    pass


# ---------------------------------------------------------------------------------------------- AI providers

def http_json(url: str, payload: dict, headers: dict, timeout: int = 180) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST", headers={
        "Content-Type": "application/json", "User-Agent": "portfolio-blog-autopilot/1.0", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:300]
        raise LLMError(f"HTTP {e.code}: {detail}") from None
    except (urllib.error.URLError, TimeoutError) as e:
        raise LLMError(f"network error: {e}") from None


def ask_gemini(model: str, system: str, user: str, want_json: bool) -> str:
    data = http_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        {"systemInstruction": {"parts": [{"text": system}]},
         "contents": [{"role": "user", "parts": [{"text": user}]}],
         "generationConfig": {"temperature": 0.8, "maxOutputTokens": 8192,
                              **({"responseMimeType": "application/json"} if want_json else {})}},
        {"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    try:
        cand = data["candidates"][0]
        if cand.get("finishReason") not in (None, "STOP"):
            raise LLMError(f"stopped early: {cand.get('finishReason')}")
        return "".join(p.get("text", "") for p in cand["content"]["parts"] if not p.get("thought"))
    except (KeyError, IndexError):
        raise LLMError(f"unexpected reply: {json.dumps(data)[:300]}") from None


def ask_groq(model: str, system: str, user: str, want_json: bool) -> str:
    data = http_json(
        "https://api.groq.com/openai/v1/chat/completions",
        {"model": model, "temperature": 0.8, "max_completion_tokens": 6000,
         "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
         **({"response_format": {"type": "json_object"}} if want_json else {})},
        {"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"})
    try:
        choice = data["choices"][0]
        if choice.get("finish_reason") not in (None, "stop"):
            raise LLMError(f"stopped early: {choice.get('finish_reason')}")
        return choice["message"]["content"]
    except (KeyError, IndexError):
        raise LLMError(f"unexpected reply: {json.dumps(data)[:300]}") from None


_mock: list | None = None


def ask(provider: str, model: str, system: str, user: str, want_json: bool = False) -> str:
    global _mock
    if os.environ.get("BLOG_MOCK_RESPONSES"):
        if _mock is None:
            _mock = json.loads(Path(os.environ["BLOG_MOCK_RESPONSES"]).read_text(encoding="utf-8"))
        if not _mock:
            raise LLMError("mock: no replies left")
        reply = _mock.pop(0)
        if isinstance(reply, dict) and "error" in reply:
            raise LLMError("mock: " + reply["error"])
        return reply if isinstance(reply, str) else json.dumps(reply)
    fn = {"gemini": ask_gemini, "groq": ask_groq}[provider]
    waits = [30, 60]   # free tiers return 429/503 when busy; wait and retry, then let the caller move on
    for attempt in range(len(waits) + 1):
        try:
            return fn(model, system, user, want_json)
        except LLMError as e:
            if attempt < len(waits) and re.search(r"HTTP (429|500|502|503|504)", str(e)):
                print(f"    busy ({str(e)[:8]}), retrying in {waits[attempt]}s …")
                time.sleep(waits[attempt])
                continue
            raise
    raise LLMError("unreachable")


def parse_json(text: str) -> dict:
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            return json.loads(m.group(0))
        raise LLMError("reply was not valid JSON") from None


# Common AI clichés swapped for plain words, so one stray word doesn't sink a good article.
# Phrases that need a real rewrite (e.g. "look no further") are still left to the checks.
PLAIN_WORDS = [
    (r"\bin conclusion,\s*(\w)", lambda m: m.group(1).upper() if m.group(0)[0].isupper() else m.group(1)),
    (r"\bin conclusion\b", "to sum up"),
    (r"\bdelve(?=\s+(?:into|deeper))", "dig"),
    (r"\bdelve\b", "dig in"),
    (r"\bgame[- ]changers\b", "turning points"),
    (r"\bgame[- ]changer\b", "turning point"),
    (r"\bunlock the (?:full )?(?:power|potential) of\b", "get the most out of"),
]


def plain_words(text: str) -> str:
    for pattern, plain in PLAIN_WORDS:
        if isinstance(plain, str):
            plain = (lambda w: lambda m: w[:1].upper() + w[1:] if m.group(0)[:1].isupper() else w)(plain)
        text = re.sub(pattern, plain, text, flags=re.I)
    return text


def clean_body(text: str) -> str:
    text = plain_words(text.strip())
    text = re.sub(r"^```(?:markdown|md)?\s*\n(.*)\n```$", r"\1", text, flags=re.S)   # model wrapped it in a code fence
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)                            # model added front matter anyway
    text = re.sub(r"^# [^\n]*\n+", "", text)                                            # model added an h1 anyway
    return text.strip() + "\n"


# ---------------------------------------------------------------------------------------------- prompts

def system_prompt(cfg: dict) -> str:
    return (SYSTEM_DIR / "style-guide.md").read_text(encoding="utf-8")


def topic_prompt(cfg: dict, posts: list[Post]) -> str:
    w = cfg["writing"]
    existing = "\n".join(f"- {p.meta.get('title')} (category: {p.meta.get('category')}; main keyword: "
                         f"{(p.meta.get('keywords') or ['?'])[0]})" for p in posts) or "- (none yet)"
    counts = {c: sum(p.meta.get("category") == c for p in posts) for c in w["categories"]}
    return f"""Choose the topic for the next blog article and write its details.

Audience: {w['audience']}
Topic areas:
{chr(10).join('- ' + t for t in w['topic_areas'])}

Already published (do NOT repeat these topics or their main keywords):
{existing}

Posts per category so far: {json.dumps(counts)}. Prefer a category with fewer posts.

Pick ONE specific, practical topic that a small business owner would actually search for on Google, phrased the
way people search (for example "how to …", "X vs Y", "… checklist", "why is my … slow"). It must fit the author's
real experience from the style guide.

Reply with JSON only, exactly these keys:
{{
  "title": "Article title with the main keyword near the start, 45-70 characters",
  "seo_title": "Shorter title for the browser tab, max 38 characters, contains the main keyword",
  "short_title": "2-5 word label for breadcrumbs",
  "description": "Meta description, 120-155 characters, contains the main keyword, says what the reader gets",
  "dek": "One-sentence subtitle shown under the title, 100-170 characters, first person allowed",
  "slug": "lowercase-hyphenated-url-slug-containing-the-main-keyword, max 6 words",
  "category": "one of {w['categories']}",
  "tags": ["3 to 4 short tags"],
  "keywords": ["main keyword first (2-5 words, exactly as people search it)", "4 to 6 related keywords"],
  "outline": ["5 to 7 section headings in order; the last one is Frequently asked questions"]
}}"""


def article_prompt(cfg: dict, meta: dict, outline: list, posts: list[Post]) -> str:
    w = cfg["writing"]
    links = "\n".join(f"- ../{p.slug}/  ({p.meta.get('title')})" for p in posts) or "- (none yet)"
    return f"""Write the full article in Markdown.

Title (added automatically, do not repeat it as a heading): {meta['title']}
Main keyword: {meta['keywords'][0]}  (use it naturally in the opening paragraph and a few times in the article)
Related keywords: {', '.join(meta['keywords'][1:])}
Category: {meta['category']}
Planned sections: {' | '.join(outline)}
Length: {w['min_words']}-{w['max_words']} words.

Other articles on this blog you may link to when genuinely relevant:
{links}

Follow the style guide exactly, including the hard rules and the Frequently asked questions section at the end.
Reply with the article body in Markdown only: no front matter, no title line, no code fence around the whole reply."""


def fix_prompt(kind: str, previous: str, errors: list) -> str:
    return (f"Your {kind} broke these rules:\n" + "\n".join(f"- {e}" for e in errors)
            + f"\n\nRewrite the complete {kind} so that every rule is met, keeping everything else that was good. "
            + ("Reply with JSON only, same keys." if kind == "details" else
               "Reply with the full article body in Markdown only.")
            + f"\n\nYour previous {kind}:\n{previous}")


# ---------------------------------------------------------------------------------------------- pipeline

def meta_from_topic(topic: dict, cfg: dict, day: dt.date) -> dict:
    keys = ["title", "seo_title", "short_title", "description", "dek", "slug", "category", "tags", "keywords"]
    meta = {k: plain_words(v) if isinstance(v, str) and k != "slug" else v for k, v in ((k, topic.get(k)) for k in keys)}
    meta["slug"] = re.sub(r"[^a-z0-9-]+", "-", str(meta.get("slug") or "").lower()).strip("-")
    meta.update(date=day, updated=day, author=cfg["site"]["author"], draft=False)
    return meta


def check_meta(meta: dict, cfg: dict, taken: set) -> list:
    probe = Post(Path("probe.md"), meta, "Intro.\n\n## A\n\n## B\n\n## C\n\n## D {#faq}\n")
    errors, _ = check_post(probe, cfg, strict=False)
    errors = [e for e in errors if "section headings" not in e]
    main = (meta.get("keywords") or [""])[0]
    for name in ["title", "seo_title", "description"]:
        if main and not keyword_in(main, str(meta.get(name) or "")):
            errors.append(f"{name} must contain the main keyword '{main}'")
    if main and not all(w in meta["slug"].split("-") for w in slugify(main).split("-")):
        errors.append(f"slug must contain the words of the main keyword '{main}'")
    if meta["slug"] in taken:
        errors.append(f"slug '{meta['slug']}' is already used; choose a different topic")
    if len(meta.get("tags") or []) < 2:
        errors.append("give 3 to 4 tags")
    if len(meta.get("keywords") or []) < 3:
        errors.append("give at least 3 keywords, main keyword first")
    return errors


def generate(cfg: dict, provider: str, model: str, posts: list[Post], day: dt.date) -> tuple[Post, list]:
    system, taken = system_prompt(cfg), {p.slug for p in posts}

    # 1. topic + details (up to REPAIRS repair rounds)
    topic = parse_json(ask(provider, model, system, topic_prompt(cfg, posts), want_json=True))
    for round_no in range(REPAIRS + 1):
        meta = meta_from_topic(topic, cfg, day)
        errors = check_meta(meta, cfg, taken)
        if not errors:
            break
        print("    details need fixing: " + "; ".join(errors))
        if round_no == REPAIRS:
            raise LLMError("details still break the rules: " + "; ".join(errors))
        topic = parse_json(ask(provider, model, system, fix_prompt("details", json.dumps(topic), errors), want_json=True))
    print(f"    topic: {meta['title']}  [{meta['category']}]")

    # 2. article (up to REPAIRS repair rounds)
    outline = topic.get("outline") or []
    body = clean_body(ask(provider, model, system, article_prompt(cfg, meta, outline, posts)))
    for round_no in range(REPAIRS + 1):
        post = render_post(Post(POSTS_DIR / f"{meta['slug']}.md", meta, body), cfg["site"]["base_url"])
        errors, warnings = check_post(post, cfg, strict=True, known_slugs=taken)
        if not errors:
            return post, warnings
        print(f"    article needs fixing ({post.words} words): " + "; ".join(errors))
        if round_no < REPAIRS:
            body = clean_body(ask(provider, model, system, fix_prompt("article", body, errors)))
    raise LLMError("article still breaks the rules: " + "; ".join(errors))


def pr_body(post: Post, warnings: list, provider: str, model: str, owner: str) -> str:
    m = post.meta
    checks = "\n".join(f"- [ ] {w}" for w in warnings) or "- Nothing flagged by the automatic checks."
    return f"""{('@' + owner + ' ') if owner else ''}a new blog post is ready for review.

**To publish:** press **Merge pull request** (it goes live about 2 minutes later).
**To discard:** press **Close pull request**. To edit first, change `{post.path.relative_to(POSTS_DIR.parents[2]).as_posix()}` in this pull request.

| | |
|---|---|
| Title | {m['title']} |
| Category | {m['category']} |
| URL after publishing | `blog/{post.slug}/` |
| Length | {post.words} words, {max(1, round(post.words / 200))} min read |
| Written by | {provider} / {model} |

**Please double-check:**
{checks}

---

# {m['title']}

*{m['dek']}*

{post.body_md}
"""[:60000]


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--force", action="store_true", help="write now even if not due")
    ap.add_argument("--today", type=dt.date.fromisoformat)
    ap.add_argument("--result", type=Path)
    ap.add_argument("--pr-body", type=Path)
    args = ap.parse_args()

    cfg = load_config()
    day = args.today or today(cfg)
    auto = cfg["autopilot"]

    def finish(status: str, **extra) -> int:
        print(f"Result: {status}" + (f" ({extra.get('reason')})" if extra.get("reason") else ""))
        if args.result:
            args.result.write_text(json.dumps({"status": status, **extra}, default=str), encoding="utf-8")
        return 1 if status == "failed" else 0

    if not args.force:
        if not auto.get("enabled", True):
            return finish("skipped", reason="autopilot is turned off in config.yml")
        if os.environ.get("BLOG_PENDING_DRAFT") == "1":
            return finish("skipped", reason="a draft is still waiting for review")
    posts = [p for p in load_posts() if not p.draft]
    newest = max((p.date for p in posts), default=None)
    if not args.force and newest and (day - newest).days < int(auto.get("every_days", 7)):
        return finish("skipped", reason=f"newest post is from {newest}; next one due after {auto.get('every_days', 7)} days")

    plan = [(p["name"], model) for p in cfg["providers"] for model in p["models"]
            if os.environ.get("BLOG_MOCK_RESPONSES") or os.environ.get(KEY_ENV.get(p["name"], ""))]
    if not plan:
        return finish("skipped", reason="no AI keys set yet (add GEMINI_API_KEY / GROQ_API_KEY as repository secrets)")

    failures = []
    for provider, model in plan:
        print(f"Trying {provider} / {model} …")
        try:
            post, warnings = generate(cfg, provider, model, posts, day)
        except (LLMError, ValueError, KeyError, TypeError) as e:
            print(f"    failed: {e}")
            failures.append(f"{provider}/{model}: {e}")
            continue
        post.meta["generated_by"] = f"{provider}/{model}"
        path = inside_blog(POSTS_DIR / f"{post.slug}.md")
        path.write_text(front_matter_text(post.meta) + post.body_md, encoding="utf-8", newline="\n")
        if args.pr_body:
            args.pr_body.write_text(pr_body(post, warnings, provider, model, os.environ.get("BLOG_OWNER", "")),
                                    encoding="utf-8")
        print(f"Saved {path.relative_to(POSTS_DIR.parents[2]).as_posix()} ({post.words} words)")
        for w in warnings:
            print(f"    check: {w}")
        return finish("written", slug=post.slug, title=post.meta["title"], provider=provider, model=model,
                      warnings=warnings)
    return finish("failed", reason="every provider failed", failures=failures)


if __name__ == "__main__":
    sys.exit(main())
