#!/usr/bin/env python3
"""
Post a completed draft to soberlivinglocal.com via the WordPress REST API.

Usage:
    python3 post_draft.py

Reads credentials from environment variables (loaded by the SessionStart hook
from .env) or falls back to .env directly if running locally.

Content workflow before calling this script:
    1. /url  — pick or mint a slug
    2. /wordpress           — write the 4,000–8,000 word article
    3. /schema — generate the JSON-LD <script> block
    4. Verify all links
    5. Set TITLE, SLUG, CONTENT, and SCHEMA below, then run this script.
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


# ── Load .env if env vars not already set ─────────────────────────────────────

def _load_env(path=".env"):
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

_load_env()


# ── Credentials ────────────────────────────────────────────────────────────────

USERNAME     = os.environ.get("WP_USERNAME", "")
APP_PASSWORD = os.environ.get("WP_APP_PASSWORD", "")
API_ENDPOINT = os.environ.get("WP_API_ENDPOINT",
                              "https://soberlivinglocal.com/wp-json/wp/v2/posts")


# ── Draft content — fill these in before running ──────────────────────────────
# Step 1: slug from /url
# Step 2: article body from /wordpress (Gutenberg block HTML)
# Step 3: schema block from /schema (raw <script> tag)

TITLE = ""   # SEO title from the /wordpress deliverables block

SLUG  = ""   # e.g. "subchapter-v-mca-debt"

# Full Gutenberg HTML from /wordpress, with the schema appended as a wp:html block
CONTENT = """
<!-- paste article content from /wordpress here -->

<!-- wp:html -->
<!-- paste <script type="application/ld+json"> block from /schema here -->
<!-- /wp:html -->
""".strip()


# ── Post ───────────────────────────────────────────────────────────────────────

def main():
    if not USERNAME or not APP_PASSWORD:
        print("ERROR: WP_USERNAME and WP_APP_PASSWORD are not set.")
        print("  Run the session-start hook or fill in .env, then retry.")
        sys.exit(1)

    if not TITLE or not SLUG or not CONTENT:
        print("ERROR: TITLE, SLUG, and CONTENT must all be filled in before posting.")
        print("  Complete the /url → /wordpress → /schema workflow first.")
        sys.exit(1)

    credentials = base64.b64encode(f"{USERNAME}:{APP_PASSWORD}".encode()).decode()

    payload = json.dumps({
        "title":   TITLE,
        "slug":    SLUG,
        "content": CONTENT,
        "status":  "draft",
    }).encode("utf-8")

    req = urllib.request.Request(
        API_ENDPOINT,
        data=payload,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type":  "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            body     = json.loads(resp.read().decode())
            post_id  = body.get("id")
            preview  = body.get("link", "")
            edit_url = f"{API_ENDPOINT}/{post_id}"

            print(f"Draft posted successfully.")
            print(f"  Post ID : {post_id}")
            print(f"  Slug    : {SLUG}")
            print(f"  Preview : {preview}")
            print(f"  Edit    : {edit_url}")

    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} — {e.reason}")
        print(e.read().decode())
        sys.exit(1)


if __name__ == "__main__":
    main()
