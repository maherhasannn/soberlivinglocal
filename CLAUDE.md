# Sober Living Local — Claude Code Instructions

## Project overview

This repo powers content operations for [soberlivinglocal.com](https://soberlivinglocal.com) — a recovery-housing referral and resource site that helps individuals and families find safe, vetted sober living homes and recovery housing. The site runs on WordPress.

All content targets people in recovery and their families searching for housing help. Every article must be written to genuinely help the reader make a confident, safe decision — supportive, not high-pressure. Sober Living Local is a housing resource, not a treatment provider.

---

## Environment

WordPress credentials are loaded automatically from `.env` at session start via the SessionStart hook. They are available as environment variables:

- `WP_USERNAME` — WordPress admin username
- `WP_APP_PASSWORD` — WordPress application password
- `WP_API_ENDPOINT` — `https://soberlivinglocal.com/wp-json/wp/v2/posts`

If credentials are missing, run the session-start hook manually:
```bash
CLAUDE_CODE_REMOTE=true CLAUDE_PROJECT_DIR=$(pwd) CLAUDE_ENV_FILE=/tmp/claude-env bash .claude/hooks/session-start.sh
```

---

## Available skills

Three custom skills are installed automatically at session start:

| Skill | Purpose |
|---|---|
| `/url` | Canonical URL map — city, specialty, guide, placement, and housing-type slugs across the site. Always pull slugs from here. |
| `/wordpress` | Full article engine — 2,500–6,000 words, supportive opt-in CTAs, 12–20 FAQs, tables, checklists |
| `/schema` | Generates the JSON-LD `<script>` block. Requires the article content as input. |

---

## Full content + posting routine

Follow these steps in order every time a new draft is created.

### Step 1 — Pick a slug with `/url`

Invoke `/url` to review the canonical page map. Either:
- Pick an existing slug that hasn't been built yet (unchecked box), or
- Identify the right section and mint a new slug following that section's naming convention

The slug drives the page URL and all internal linking. Never invent a slug without checking here first, and never reuse a slug that's already been built.

### Step 2 — Write the article with `/wordpress`

Invoke `/wordpress` with the chosen slug/topic. The skill will produce:

- 2,500–6,000 word article in WordPress Gutenberg block HTML (city and narrow FAQ pages run shorter; pillar pages longer)
- Supportive, opt-in CTA HTML blocks (no high-pressure or alarm styling) plus a crisis-resource note where appropriate
- 12–20 FAQ entries formatted for AI Overview extraction
- At least one comparison table and one checklist
- Internal links using only confirmed slugs from `/url`
- External links to authoritative, non-commercial sources only: SAMHSA, NARR, NIH/NIDA, 988, relevant state agencies
- Full deliverables block at the end (SEO title, meta description, slug, H1, internal link map, etc.)

**Before moving to Step 3:** Verify every link in the article — internal and external — returns a valid response. Do not skip this check.

### Step 3 — Generate schema with `/schema`

Invoke `/schema` and pass:
1. The full page URL (`https://soberlivinglocal.com/<slug>/`)
2. The complete article content from Step 2

The skill outputs a single `<script type="application/ld+json">` block — ready to paste into WordPress as a Custom HTML block at the bottom of the post content.

The schema includes: `Organization`, `ContactPoint`, `Place`, `Service` (site-wide), `LocalBusiness`, `WebSite`, `WebPage`, `Article`, `FAQPage`, `Service` (page-specific), `BreadcrumbList`, `DefinedTermSet`, and relevant `DefinedTerm` / `Thing` entities for the page's topic bucket.

**The schema skill will refuse to generate if:**
- No FAQ section exists in the article
- Any link hasn't been verified against the Verified Valid Links list in `schema.md`

### Step 4 — Final link check

Before posting, confirm:
- [ ] All internal links resolve to real, confirmed-live soberlivinglocal.com pages (use the Verified Valid Links list in `schema.md` — a planned slug in `url.md` is NOT a verified link)
- [ ] All external links return HTTP 200
- [ ] No bracketed placeholder text survives in the CTAs (`{city}`, `[CONTEXT-SPECIFIC HEADLINE]`, etc.)
- [ ] The crisis-resource note and "housing resource, not treatment" disclaimer are present where appropriate
- [ ] Schema JSON is valid (no trailing commas, all brackets matched)

### Step 5 — Post to WordPress

Post the draft using the WordPress REST API:

```bash
python3 post_draft.py
```

The script reads credentials from `.env`, posts to `https://soberlivinglocal.com/wp-json/wp/v2/posts` with `status: draft`, and prints the post ID and preview URL on success.

**The content field must include:**
1. The full Gutenberg block HTML from Step 2
2. The `<script type="application/ld+json">` block from Step 3 appended as a `<!-- wp:html -->` block at the bottom

**On success:** Log the post ID. The draft is live in WordPress and ready for review before publishing.

### Step 6 — Mark the slug complete in `url.md`

Immediately after a successful post in Step 5, edit `url.md` and change that slug's checkbox from `☐` to `✅` on its row. This is required, not optional — the "never reuse a slug" rule in `url.md` only works if completed slugs are actually checked off.

- Find the exact row for the slug just posted (e.g., `| ☐ | `/sober-living-irvine-ca/` |`) and flip only that row to `✅`.
- Change exactly one box. Do not touch any other rows.
- If the slug appears in more than one section (e.g., a city page also listed under "Priority Launch"), flip every occurrence of that same slug.
- If the slug's box is already `✅`, stop — it was likely built before, and posting again risks a duplicate. Flag it instead of proceeding.

---

## Content standards

- Voice: experienced, ethical recovery-housing professional speaking to a nervous newcomer or worried family member — specific, calm, compassionate, never sensational
- Every section opens with a 2–3 sentence direct answer (AI Overview ready)
- No sobriety or "success rate" guarantees, no "best" or "top rated", no outcome promises
- No medical or clinical advice, no relapse shaming, no triggering detail about substance use
- Cautious framing: "many homes," "often," "depending on the home and state," "may help" — never "will" or "guaranteed"
- Word count: 2,500–6,000 words per article
- CTAs: supportive and opt-in, contextually rewritten — no generic copy, no surviving placeholders, no high-pressure urgency
- Include a crisis-support resource note (SAMHSA Helpline, 988) where the topic warrants it

## NAP (never change)

- **Name:** Sober Living Local
- **Address:** 27420 Jefferson Ave, Temecula, CA 92590
- **Phone:** (714) 500-7432 / `+1-714-500-7432`
- **Email:** support@soberlivinglocal.com
- **Contact URL:** `https://soberlivinglocal.com/contact/`
- **API endpoint:** `https://soberlivinglocal.com/wp-json/wp/v2/posts`
