#!/usr/bin/env python3
"""Thin Firecrawl CLI wrapper for the competitor-recon skill.

Original implementation for competitor-recon. Wraps the public Firecrawl
Python SDK to expose markdown / screenshot / extract / search / crawl / images
subcommands. Requires FIRECRAWL_API_KEY in the environment (or a .env file
in the current dir or the user's home dir).
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import urllib.request
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv is optional; env vars still work without it
    def load_dotenv(*_args, **_kwargs):
        return False

from firecrawl import Firecrawl


def _client() -> Firecrawl:
    # Firecrawl() reads FIRECRAWL_API_KEY from the environment.
    return Firecrawl()


def scrape_markdown(url: str, only_main: bool = False) -> str:
    result = _client().scrape(
        url,
        formats=["markdown"],
        only_main_content=only_main or None,
    )
    return result.markdown or ""


def take_screenshot(url: str, output_path: str | None = None) -> str:
    data = _client().scrape(url, formats=["screenshot"]).screenshot

    if data.startswith(("http://", "https://")):
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(data, output_path)
            return f"Screenshot saved to {output_path}"
        return f"[Screenshot URL: {data}]"

    if data.startswith("data:image"):
        data = data.split(",", 1)[1]

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as fh:
            fh.write(base64.b64decode(data))
        return f"Screenshot saved to {output_path}"

    return f"[Screenshot: {len(data)} bytes base64]"


def extract_data(url: str, schema: dict, prompt: str | None = None) -> dict:
    fmt = {"type": "json", "schema": schema}
    if prompt:
        fmt["prompt"] = prompt
    return _client().scrape(url, formats=[fmt]).json


def search_web(query: str, limit: int = 5) -> list:
    return _client().search(query, limit=limit).web or []


def crawl_site(url: str, limit: int = 50) -> list:
    return _client().crawl(
        url,
        limit=limit,
        scrape_options={"formats": ["markdown"], "onlyMainContent": True},
    ).data


# Skip UI chrome — logos, icons, sprites, tracking pixels — keep real creative.
_SKIP = ("logo", "icon", "sprite", "favicon", "pixel", "avatar", "spacer", "loader")


def scrape_images(url: str, limit: int = 12, min_dim: int = 200,
                  output: str | None = None) -> list[dict]:
    """Pull real content/campaign images from a page.

    Reads the page markdown, extracts image URLs (with alt text as caption),
    filters out UI chrome, optionally downloads them, and returns a list of
    {url, caption, saved} dicts so the report can embed them with sources.
    """
    md = _client().scrape(url, formats=["markdown"]).markdown or ""
    seen: set[str] = set()
    images: list[dict] = []
    # markdown images: ![alt](src)
    for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)\s]+)", md):
        src = src.strip()
        low = src.lower()
        if src in seen or not low.startswith("http"):
            continue
        if any(k in low for k in _SKIP):
            continue
        if not re.search(r"\.(jpg|jpeg|png|webp|gif|avif)", low):
            continue
        seen.add(src)
        images.append({"url": src, "caption": alt.strip() or "(no caption)", "saved": None})
        if len(images) >= limit:
            break

    if output:
        out = Path(output)
        out.mkdir(parents=True, exist_ok=True)
        for i, img in enumerate(images):
            ext = re.search(r"\.(jpg|jpeg|png|webp|gif|avif)", img["url"].lower())
            path = out / f"img_{i:02d}.{ext.group(1) if ext else 'jpg'}"
            try:
                req = urllib.request.Request(img["url"], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=20) as r, open(path, "wb") as f:
                    f.write(r.read())
                img["saved"] = str(path)
            except Exception as e:  # noqa: BLE001 - keep going on a single bad image
                img["saved"] = f"[download failed: {e}]"
    return images


def main() -> None:
    load_dotenv()
    load_dotenv(Path.home() / ".env")

    parser = argparse.ArgumentParser(description="Firecrawl web tools for competitor recon")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("markdown", help="Get page as markdown")
    p.add_argument("url")
    p.add_argument("--main-only", action="store_true", help="Exclude nav/footer")

    p = sub.add_parser("screenshot", help="Screenshot a webpage")
    p.add_argument("url")
    p.add_argument("--output", "-o", help="Save to file (PNG)")

    p = sub.add_parser("extract", help="Extract structured data")
    p.add_argument("url")
    p.add_argument("--schema", required=True, help="Path to JSON schema file")
    p.add_argument("--prompt", help="Extraction guidance")

    p = sub.add_parser("search", help="Search the web")
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=5)

    p = sub.add_parser("crawl", help="Crawl a site")
    p.add_argument("url")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--output", "-o", help="Save markdown pages to this directory")

    p = sub.add_parser("images", help="Extract (and optionally download) campaign/content images from a page")
    p.add_argument("url")
    p.add_argument("--limit", type=int, default=12, help="Max images")
    p.add_argument("--output", "-o", help="Download images into this directory")

    args = parser.parse_args()

    if args.command == "markdown":
        print(scrape_markdown(args.url, args.main_only))

    elif args.command == "screenshot":
        print(take_screenshot(args.url, args.output))

    elif args.command == "extract":
        with open(args.schema) as fh:
            schema = json.load(fh)
        print(json.dumps(extract_data(args.url, schema, args.prompt), indent=2))

    elif args.command == "search":
        for r in search_web(args.query, args.limit):
            print(f"## {r.title}\nURL: {r.url}\n{r.description or 'No description'}\n\n---\n")

    elif args.command == "crawl":
        pages = crawl_site(args.url, args.limit)
        if args.output:
            out = Path(args.output)
            out.mkdir(parents=True, exist_ok=True)
            for i, page in enumerate(pages):
                (out / f"page_{i:03d}.md").write_text(page.markdown or "")
            print(f"Saved {len(pages)} pages to {out}/")
        else:
            for page in pages:
                title = page.metadata.title if page.metadata else "Untitled"
                print(f"## {title}\n{(page.markdown or '')[:1000]}\n\n---\n")

    elif args.command == "images":
        imgs = scrape_images(args.url, args.limit, output=args.output)
        if not imgs:
            print("No content images found on this page.")
        for i, img in enumerate(imgs):
            print(f"[{i:02d}] {img['caption']}")
            print(f"     url:   {img['url']}")
            if img["saved"]:
                print(f"     saved: {img['saved']}")
        print(f"\n{len(imgs)} image(s). Source page: {args.url}")


if __name__ == "__main__":
    main()
