---
name: schema.md
description: Generate a complete enterprise-level JSON-LD schema @graph for Sober Living Local pages (sober living homes by city, demographic/specialty recovery housing, recovery housing guides, sober living FAQs, cost/insurance, placement/admissions, substance-specific recovery, housing-type definitions, and mental-health housing). The user provides a page slug plus the full page content; the skill outputs only the final JSON-LD script tag — Google-indexable, ready to paste into WordPress. Use whenever the user pastes Sober Living Local page content and asks for schema, JSON-LD, structured data, or anything along those lines.
---

# Sober Living Local Schema Generator

This skill produces one thing: a complete, valid, Google-indexable `<script type="application/ld+json">` block for a Sober Living Local page. Nothing else. No preamble, no "here you go", no closing notes. Just the script tag.

## Input contract

The user will always provide:
1. A slug or full URL (e.g., `sober-living-irvine-ca` or `https://soberlivinglocal.com/sober-living-irvine-ca/`)
2. The full page content (HTML or pasted text — title, meta description, H1, body copy, FAQ section, internal links)

If either is missing, ask once. Do not fetch the page. Do not invent content.

## Output contract

Return only:

```
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [ ... ]
}
</script>
```

No text before. No text after. No code-fence labels like ```json. Just the script tag and its valid JSON-LD contents.

---

## Build process

Work through these steps in order.

### Step 1: Extract page facts

From the pasted page content, pull:
- **Full page URL**: `https://soberlivinglocal.com/<slug>/` (always trailing slash)
- **SEO title**: from the `<title>` tag or page title
- **Meta description**: from the meta description tag
- **H1**: the main article headline
- **Word count**: count words in the article body (exclude nav/footer; include FAQ text if part of article flow)
- **Primary keyword**: main topic phrase from H1/title
- **Secondary keyword**: closely related phrase from subheads or repeated body language
- **City / region** (if a location page): the city name and county/region for areaServed
- **FAQs**: pull every Q&A pair verbatim. Do not paraphrase. Do not invent. If no FAQ section exists, stop and tell the user.
- **Internal/external links**: collect every URL for use in Step 3.

### Step 2: Classify the page topic

Assign the page to one bucket. The bucket drives breadcrumb parent, Service entity, and DefinedTerms/Things.

- **City / Location** — "Sober Living [City] CA" pages for specific cities
  - Breadcrumb parent: `Sober Living by Location` → `https://soberlivinglocal.com/sober-living-by-location/`
- **Demographic / Specialty Housing** — women's, men's, LGBTQ, pet-friendly, luxury, executive, couples, Christian, MAT-friendly, dual diagnosis, young adult, veteran, professionals, college students, mothers
  - Breadcrumb parent: `Specialty Sober Living` → `https://soberlivinglocal.com/specialty-sober-living/`
- **Guides / FAQs** — how-to, decision guides, "can you" questions, cost/insurance, curfew, drug testing, house managers, what to bring, how long to stay
  - Breadcrumb parent: `Sober Living Resources` → `https://soberlivinglocal.com/sober-living-resources/`
- **Placement / Admissions** — emergency placement, same-day admissions, 24-hour placement, treatment-adjacent (near detox/outpatient/rehab)
  - Breadcrumb parent: `Sober Living Resources` → `https://soberlivinglocal.com/sober-living-resources/`
- **Housing Type / Definitions** — transitional housing, structured recovery housing, recovery residences, halfway houses, sober living vs halfway houses, mental health housing, substance-specific recovery
  - Breadcrumb parent: `Recovery Housing Guides` → `https://soberlivinglocal.com/recovery-housing-guides/`

If the page is genuinely mixed, pick the bucket that best matches the H1's primary intent.

> NOTE: The parent hub URLs above are conventions for breadcrumb structure. Before using a parent URL as an actual link target anywhere other than the breadcrumb `item` field, confirm it exists in the Verified Valid Links section. If a hub page is not yet built, the breadcrumb can still reference it (breadcrumbs describe site hierarchy), but do not place it in `significantLink`.

### Step 3: Verify every link before using it

Only use links from the **Verified Valid Links** section at the bottom of this skill. If a link in the page content isn't on that list and you can't match it to a confirmed page, leave it out. Never link to a page that may not exist.

For DefinedTerm `url` fields: only attach a URL if the term maps cleanly to a confirmed page. When in doubt, omit the URL field.

For external `sameAs` on Thing entities: use only the authoritative external sources listed in Verified Valid Links.

### Step 4: Assemble the @graph

Build every required entity — all six site-wide entities plus the page-specific ones for the assigned bucket. Follow the schema specs in the **Schema Spec** section exactly.

Key rules:
- **NAP must be exact**: Sober Living Local / 27420 Jefferson Ave, Temecula, CA 92590 / +1-714-500-7432
- **Stable @id values**: use exactly the IDs documented below
- **Dates**: use today's date for both `datePublished` and `dateModified` in YYYY-MM-DD format
- **FAQ entities**: one `Question` per Q&A, verbatim from the page
- **Word count**: include as a string in the Article entity
- **Keywords array**: lead with primary keyword, then secondary, then the standard topical keywords
- **DefinedTerms and Things**: include only the ones for the page's bucket (see bucket map in Schema Spec)

### Step 5: Compliance check

Before outputting, verify:
- [ ] All URLs are absolute (start with `https://`)
- [ ] All `@id` values are stable and follow the documented pattern
- [ ] No fake reviews, no `aggregateRating`, no fake testimonials
- [ ] No "best", "top rated", "guaranteed sobriety", or outcome promises
- [ ] No medical claims that the site treats or cures addiction (Sober Living Local is a directory/resource, not a treatment provider)
- [ ] Every link points to a confirmed-real page
- [ ] FAQ answers are cautious and informational — describe how things generally work, not guarantees
- [ ] JSON is valid (no trailing commas, all strings quoted, all brackets matched)
- [ ] Output is ONLY the `<script>` block — no preamble or commentary

### Step 6: Return the script block

Output the `<script type="application/ld+json">` block. Nothing else.

---

## What this skill never does

- Never fetches pages from the web
- Never invents FAQs
- Never links to unverified pages
- Never adds preamble, explanations, or closing remarks
- Never includes `aggregateRating`, fake reviews, or fake testimonials
- Never uses superlatives like "best" or "top rated"
- Never claims the site provides medical treatment, detox, or clinical care — it connects people with vetted housing

---

## Schema Spec

### NAP and stable IDs

**Name / Address / Phone / Email — exact on every page:**
- Sober Living Local / 27420 Jefferson Ave, Temecula, CA 92590 / +1-714-500-7432 / support@soberlivinglocal.com

**Site-wide stable @id values:**
- `https://soberlivinglocal.com/#organization`
- `https://soberlivinglocal.com/#service`
- `https://soberlivinglocal.com/#localbusiness`
- `https://soberlivinglocal.com/#website`
- `https://soberlivinglocal.com/#place`
- `https://soberlivinglocal.com/#contact`

**Page-specific @id pattern** (`[URL]` = full page URL with trailing slash):
- `[URL]#webpage`, `[URL]#article`, `[URL]#faq`, `[URL]#service`, `[URL]#breadcrumb`, `[URL]#terms`, `[URL]#primary-topic`, `[URL]#<term-slug>`

---

### Site-wide entities (include all six on every page)

**Organization**
```json
{
  "@type": "Organization",
  "@id": "https://soberlivinglocal.com/#organization",
  "name": "Sober Living Local",
  "url": "https://soberlivinglocal.com/",
  "telephone": "+1-714-500-7432",
  "email": "support@soberlivinglocal.com",
  "logo": { "@type": "ImageObject", "url": "https://soberlivinglocal.com/wp-content/uploads/2025/11/cropped-Sober-Living-Local-Icon-270x270.png" },
  "address": { "@type": "PostalAddress", "streetAddress": "27420 Jefferson Ave", "addressLocality": "Temecula", "addressRegion": "CA", "postalCode": "92590", "addressCountry": "US" },
  "contactPoint": { "@id": "https://soberlivinglocal.com/#contact" },
  "sameAs": [
    "https://www.facebook.com/",
    "https://www.instagram.com/",
    "https://www.youtube.com/"
  ]
}
```
> The social URLs above are placeholders. Replace with the exact profile URLs once confirmed, or remove any that cannot be verified. Do not guess handles.

**ContactPoint**
```json
{
  "@type": "ContactPoint",
  "@id": "https://soberlivinglocal.com/#contact",
  "telephone": "+1-714-500-7432",
  "email": "support@soberlivinglocal.com",
  "contactType": "customer service",
  "areaServed": "US",
  "availableLanguage": "English"
}
```

**Place**
```json
{
  "@type": "Place",
  "@id": "https://soberlivinglocal.com/#place",
  "name": "Sober Living Local Office",
  "address": { "@type": "PostalAddress", "streetAddress": "27420 Jefferson Ave", "addressLocality": "Temecula", "addressRegion": "CA", "postalCode": "92590", "addressCountry": "US" }
}
```

**Service (site-wide)**
```json
{
  "@type": "Service",
  "@id": "https://soberlivinglocal.com/#service",
  "name": "Sober Living and Recovery Housing Referral and Resource Service",
  "url": "https://soberlivinglocal.com/",
  "telephone": "+1-714-500-7432",
  "provider": { "@id": "https://soberlivinglocal.com/#organization" },
  "address": { "@type": "PostalAddress", "streetAddress": "27420 Jefferson Ave", "addressLocality": "Temecula", "addressRegion": "CA", "postalCode": "92590", "addressCountry": "US" },
  "areaServed": [
    { "@type": "State", "name": "California" },
    { "@type": "Country", "name": "United States" }
  ],
  "serviceType": [
    "Sober living home referral","Recovery housing placement","Sober living home directory",
    "Transitional housing referral","Structured recovery housing referral","Dual diagnosis housing referral",
    "Specialty sober living referral","Recovery housing resources","Sober living cost and insurance guidance",
    "Emergency sober living placement","Recovery community resources"
  ],
  "knowsAbout": [
    "Sober living homes","Recovery residences","Transitional housing","Halfway houses",
    "Structured recovery housing","Dual diagnosis housing","Medication-assisted treatment friendly housing",
    "Sober living house rules","Drug testing in recovery housing","Sober living cost",
    "Insurance and recovery housing","Relapse and recovery housing","Recovery support after rehab"
  ]
}
```

**LocalBusiness**
```json
{
  "@type": "LocalBusiness",
  "@id": "https://soberlivinglocal.com/#localbusiness",
  "name": "Sober Living Local",
  "url": "https://soberlivinglocal.com/",
  "telephone": "+1-714-500-7432",
  "email": "support@soberlivinglocal.com",
  "image": "https://soberlivinglocal.com/wp-content/uploads/2025/11/cropped-Sober-Living-Local-Icon-270x270.png",
  "address": { "@type": "PostalAddress", "streetAddress": "27420 Jefferson Ave", "addressLocality": "Temecula", "addressRegion": "CA", "postalCode": "92590", "addressCountry": "US" },
  "parentOrganization": { "@id": "https://soberlivinglocal.com/#organization" },
  "areaServed": ["Temecula", "California", "United States"]
}
```

**WebSite**
```json
{
  "@type": "WebSite",
  "@id": "https://soberlivinglocal.com/#website",
  "name": "Sober Living Local",
  "url": "https://soberlivinglocal.com/",
  "publisher": { "@id": "https://soberlivinglocal.com/#organization" },
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://soberlivinglocal.com/?s={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

---

### Page-specific entities

**WebPage**
```json
{
  "@type": "WebPage",
  "@id": "[URL]#webpage",
  "url": "[URL]",
  "name": "[SEO TITLE]",
  "description": "[META DESCRIPTION]",
  "isPartOf": { "@id": "https://soberlivinglocal.com/#website" },
  "publisher": { "@id": "https://soberlivinglocal.com/#organization" },
  "provider": { "@id": "https://soberlivinglocal.com/#service" },
  "breadcrumb": { "@id": "[URL]#breadcrumb" },
  "mainEntity": [ { "@id": "[URL]#article" }, { "@id": "[URL]#faq" }, { "@id": "[URL]#service" } ],
  "about": [ { "@id": "[URL]#primary-topic" } ],
  "mentions": [ /* refs to relevant Thing @ids from bucket map */ ],
  "significantLink": [ /* verified internal links relevant to this page */ ],
  "inLanguage": "en-US"
}
```

**Article**
```json
{
  "@type": "Article",
  "@id": "[URL]#article",
  "headline": "[H1]",
  "description": "[META DESCRIPTION]",
  "author": { "@id": "https://soberlivinglocal.com/#organization" },
  "publisher": { "@id": "https://soberlivinglocal.com/#organization" },
  "mainEntityOfPage": { "@id": "[URL]#webpage" },
  "datePublished": "[TODAY YYYY-MM-DD]",
  "dateModified": "[TODAY YYYY-MM-DD]",
  "articleSection": ["Sober Living","Recovery Housing","Addiction Recovery","Transitional Housing","Recovery Resources"],
  "keywords": [
    "[PRIMARY KEYWORD]","[SECONDARY KEYWORD]",
    "sober living","recovery housing","sober living homes","transitional housing",
    "structured recovery housing","recovery residences","addiction recovery housing",
    "dual diagnosis housing","sober living after rehab"
  ],
  "about": [ { "@id": "[URL]#primary-topic" } ],
  "mentions": [ /* same Thing refs as WebPage */ ],
  "wordCount": "[INTEGER AS STRING]",
  "inLanguage": "en-US"
}
```

**FAQPage** — one `Question` per Q&A verbatim from the page; if no FAQ section exists, stop and tell the user
```json
{
  "@type": "FAQPage",
  "@id": "[URL]#faq",
  "mainEntity": [
    { "@type": "Question", "name": "[QUESTION VERBATIM]", "acceptedAnswer": { "@type": "Answer", "text": "[ANSWER VERBATIM]" } }
  ]
}
```

**DefinedTermSet**
```json
{
  "@type": "DefinedTermSet",
  "@id": "[URL]#terms",
  "name": "Sober Living and Recovery Housing Terms",
  "hasDefinedTerm": [ /* refs to DefinedTerm @ids for this page */ ]
}
```

---

### Service entity (page-specific)

Pick a name from the list below that matches the bucket. Customize `serviceType[0]` for the specific page subject. For City pages, set `areaServed` to the specific city.

```json
{
  "@type": "Service",
  "@id": "[URL]#service",
  "name": "[See name suggestions by bucket below]",
  "serviceType": ["[Primary service for this page]","Recovery housing referral","Sober living placement support","Recovery housing resources"],
  "provider": { "@id": "https://soberlivinglocal.com/#organization" },
  "areaServed": [ { "@type": "City", "name": "[CITY or leave California]" }, { "@type": "State", "name": "California" }, { "@type": "Country", "name": "United States" } ],
  "audience": { "@type": "Audience", "audienceType": "Individuals in recovery, families, and referral sources seeking safe, structured sober living and recovery housing" },
  "offers": {
    "@type": "Offer",
    "name": "[Page-specific offer name]",
    "price": "0",
    "priceCurrency": "USD",
    "description": "Free help connecting individuals and families with vetted sober living homes and recovery housing. Sober Living Local is a referral and resource service, not a treatment provider, and does not guarantee placement or recovery outcomes."
  },
  "termsOfService": "https://soberlivinglocal.com/terms-and-conditions/",
  "serviceOutput": ["sober living home matches","recovery housing options","placement guidance","cost and insurance information","recovery resource referrals"]
}
```

**Name suggestions by bucket:**
- City / Location: "Sober Living Home Referral in [City], CA" / "[City] Recovery Housing Placement Help"
- Demographic / Specialty: "Women's Sober Living Referral Help" / "Men's Sober Living Referral Help" / "LGBTQ Sober Living Referral Help" / "Pet-Friendly Sober Living Referral Help" / "Luxury Sober Living Referral Help" / "Dual Diagnosis Housing Referral Help" / "MAT-Friendly Sober Living Referral Help"
- Guides / FAQs: "Sober Living Resource and Guidance Help" / "Sober Living Cost and Insurance Guidance"
- Placement / Admissions: "Emergency Sober Living Placement Help" / "Same-Day Recovery Housing Placement Help"
- Housing Type / Definitions: "Recovery Housing Information and Referral Help" / "Transitional Housing Referral Help"

---

### Breadcrumb variants

```json
{
  "@type": "BreadcrumbList",
  "@id": "[URL]#breadcrumb",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://soberlivinglocal.com/" },
    { "@type": "ListItem", "position": 2, "name": "[PARENT NAME]", "item": "[PARENT URL]" },
    { "@type": "ListItem", "position": 3, "name": "[PAGE TITLE]", "item": "[URL]" }
  ]
}
```

| Bucket | Parent name | Parent URL |
|---|---|---|
| City / Location | Sober Living by Location | `https://soberlivinglocal.com/sober-living-by-location/` |
| Demographic / Specialty Housing | Specialty Sober Living | `https://soberlivinglocal.com/specialty-sober-living/` |
| Guides / FAQs | Sober Living Resources | `https://soberlivinglocal.com/sober-living-resources/` |
| Placement / Admissions | Sober Living Resources | `https://soberlivinglocal.com/sober-living-resources/` |
| Housing Type / Definitions | Recovery Housing Guides | `https://soberlivinglocal.com/recovery-housing-guides/` |

---

### DefinedTerm catalog

Shape for each term:
```json
{ "@type": "DefinedTerm", "@id": "[URL]#<term-slug>", "name": "[Term name]", "description": "[Cautious, informational description]", "inDefinedTermSet": { "@id": "[URL]#terms" }, "url": "[optional — confirmed Sober Living Local page only]" }
```

| Slug | Name | Description | URL |
|---|---|---|---|
| `sober-living-home` | Sober living home | A substance-free residence that provides structure, accountability, and peer support for people in recovery, typically following rules such as curfews and drug testing. | — |
| `recovery-residence` | Recovery residence | A broad term for substance-free housing that supports recovery, ranging from peer-run homes to clinically supervised residences. | — |
| `transitional-housing` | Transitional housing | Temporary housing that helps individuals move from a treatment setting or unstable situation toward independent living. | — |
| `halfway-house` | Halfway house | A type of supervised residence, sometimes court- or program-affiliated, that supports people transitioning back into the community, often with required stays. | — |
| `structured-recovery-housing` | Structured recovery housing | Recovery housing with defined rules, schedules, and accountability measures intended to support sustained sobriety. | — |
| `dual-diagnosis-housing` | Dual diagnosis housing | Recovery housing designed to support people managing both a substance use disorder and a co-occurring mental health condition. | — |
| `mat-friendly-housing` | MAT-friendly housing | Recovery housing that permits residents to use medication-assisted treatment prescribed for substance use disorders. | — |
| `house-manager` | House manager | A staff member or senior resident who oversees daily operations, enforces house rules, and supports residents in a sober living home. | — |
| `drug-testing` | Drug testing | Routine or random testing used in many recovery residences to support accountability and a substance-free environment. | — |
| `curfew` | Curfew | A house rule setting a time by which residents must return, commonly used in sober living homes to support structure and safety. | — |
| `relapse` | Relapse | A return to substance use after a period of abstinence; many recovery residences have policies describing how relapse is handled. | — |
| `medication-assisted-treatment` | Medication-assisted treatment | The use of FDA-approved medications, often combined with counseling, to treat substance use disorders. | — |
| `intensive-outpatient-program` | Intensive outpatient program | A structured outpatient treatment program that allows participants to live at home or in recovery housing while attending scheduled sessions. | — |
| `detox` | Detox | A medically supervised process of clearing substances from the body, typically completed before entering ongoing treatment or recovery housing. | — |
| `peer-support` | Peer support | Mutual support among people in recovery, a core feature of most sober living environments. | — |

### DefinedTerm note
This catalog covers concepts. None currently map to a confirmed standalone Sober Living Local page, so the `url` field is omitted for all terms by default. Add a `url` only after a matching page is confirmed in Verified Valid Links (e.g., link `halfway-house` to `/halfway-houses-california/` once that page is live and verified).

---

### Thing entity catalog

Shape for each thing:
```json
{ "@type": "Thing", "@id": "[URL]#<term-slug>", "name": "[Concept name]", "description": "[Short description]", "sameAs": [ /* authoritative sources only */ ] }
```

Always include `#primary-topic`:
```json
{ "@type": "Thing", "@id": "[URL]#primary-topic", "name": "[PRIMARY TOPIC — usually the H1 subject]", "description": "[1–2 sentence description of the main page topic]" }
```

| Slug | Name | Suggested sameAs |
|---|---|---|
| `sober-living` | Sober living | `https://en.wikipedia.org/wiki/Sober_living_house` |
| `recovery-residence` | Recovery residence | `https://narronline.org/` |
| `transitional-housing` | Transitional housing | — |
| `halfway-house` | Halfway house | `https://en.wikipedia.org/wiki/Halfway_house` |
| `dual-diagnosis` | Dual diagnosis | `https://www.samhsa.gov/` |
| `medication-assisted-treatment` | Medication-assisted treatment | `https://www.samhsa.gov/medications-substance-use-disorders` |
| `substance-use-disorder` | Substance use disorder | `https://www.samhsa.gov/`, `https://www.nih.gov/` |
| `addiction-recovery` | Addiction recovery | `https://www.samhsa.gov/find-help/recovery` |
| `intensive-outpatient-program` | Intensive outpatient program | — |
| `detox` | Detox | — |

---

### Topic-bucket → entity-inclusion map

Use only the entities for the page's bucket.

**City / Location bucket**
- DefinedTerms: sober-living-home, recovery-residence, transitional-housing, structured-recovery-housing, house-manager, drug-testing, curfew, peer-support
- Things: primary-topic, sober-living, recovery-residence, addiction-recovery

**Demographic / Specialty Housing bucket**
- DefinedTerms: sober-living-home, recovery-residence, structured-recovery-housing, peer-support + the relevant specialty term (dual-diagnosis-housing, mat-friendly-housing, etc.)
- Things: primary-topic, sober-living, recovery-residence, addiction-recovery + dual-diagnosis / medication-assisted-treatment where relevant

**Guides / FAQs bucket**
- DefinedTerms: sober-living-home, house-manager, drug-testing, curfew, relapse, peer-support + cost/insurance terms where relevant
- Things: primary-topic, sober-living, addiction-recovery

**Placement / Admissions bucket**
- DefinedTerms: sober-living-home, transitional-housing, detox, intensive-outpatient-program, recovery-residence
- Things: primary-topic, sober-living, recovery-residence, detox, intensive-outpatient-program

**Housing Type / Definitions bucket**
- DefinedTerms: sober-living-home, recovery-residence, transitional-housing, halfway-house, structured-recovery-housing, dual-diagnosis-housing
- Things: primary-topic, sober-living, recovery-residence, halfway-house, transitional-housing, dual-diagnosis

---

## Verified Valid Links

Only use links from this list. Never invent or guess URLs.

### Sober Living Local internal pages (CONFIRMED LIVE)
- `https://soberlivinglocal.com/`
- `https://soberlivinglocal.com/about/`

> Every other page slug (city pages, specialty pages, guides, etc.) must be confirmed live before being added here. The url.md page map lists planned slugs, but a planned slug is NOT a verified link. As pages are published, move their confirmed URLs into this list. Until then, do not place them in `significantLink` or DefinedTerm `url` fields.

### Compliance / utility pages (CONFIRM BEFORE USE)
The following are standard WordPress pages that likely exist but were not individually verified. Confirm each returns a live page before linking:
- `https://soberlivinglocal.com/contact/`
- `https://soberlivinglocal.com/privacy-policy/`
- `https://soberlivinglocal.com/terms-and-conditions/`
- `https://soberlivinglocal.com/disclaimer/`

### Social profiles (Organization sameAs only — CONFIRM EXACT URLS)
The home page links to Facebook, Instagram, and YouTube, but the exact profile URLs were not captured. Confirm and insert the real profile URLs, or omit any that cannot be verified. Do not guess handles.
- Facebook — (confirm URL)
- Instagram — (confirm URL)
- YouTube — (confirm URL)

### Authoritative external sources (Thing sameAs only)
- `https://www.samhsa.gov/` — substance use disorder, dual diagnosis, recovery, MAT
- `https://www.samhsa.gov/medications-substance-use-disorders` — medication-assisted treatment
- `https://www.samhsa.gov/find-help/recovery` — addiction recovery
- `https://narronline.org/` — recovery residences / national standards
- `https://www.nih.gov/` — substance use disorder (general medical authority)
- `https://en.wikipedia.org/wiki/Sober_living_house` — sober living (general reference)
- `https://en.wikipedia.org/wiki/Halfway_house` — halfway house (general reference)

### Logo / icon
- `https://soberlivinglocal.com/wp-content/uploads/2025/11/cropped-Sober-Living-Local-Icon-270x270.png`

### Link usage rules
- If the user's pasted content includes a link not on this list, leave it out unless it's an obvious match for a confirmed page (e.g., same URL with/without trailing slash).
- Never link to `https://soberlivinglocal.com/blog/...` paths, category archives, or tag pages unless confirmed.
- Compliance links belong in WebPage `significantLink` when relevant, not in every entity.
- When `sameAs` is optional and you have no confirmed authoritative source, omit the field.
