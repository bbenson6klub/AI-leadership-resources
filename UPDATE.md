# How to refresh this library (daily)

Keep it a **static** GitHub Pages site. Edit data, rebuild, commit. Do not hotlink heavy remote images.

## Files that matter

| File | Role |
|------|------|
| `resources.json` | Source of truth (articles, prompts, people, **videos**, tags) |
| `build.py` | Generates `index.html` (search, chips, copy, lazy videos, SVG icons) |
| `index.html` | Published page (regenerate; do not hand-edit) |
| `assets/` | Local images/SVGs only (e.g. `hero-header.jpg`) |
| `UPDATE.md` | This checklist |
| `README.md` | Repo blurb |

Do **not** publish `preview-desktop.png`, `preview-mobile.png`, or other preview screenshots.

## Schema notes (`resources.json`)

- **Sections:** `this_week`, `workflows`, `prompts`, `leadership`, `smb`, `healthcare`, `industries`, `videos`, `people`, `archive` (plus `industry_groups` metadata)
- **Common fields:** `title`, `url` (or `prompt` for prompts), `why`, `tags` (array)
- **Tags:** topic chips — `workflows`, `prompts`, `leadership`, `smb`, `healthcare`, `videos`, `people` — plus audience — `managers`, `aspiring`, `smb`
- **Healthcare & pharma:** use tag `healthcare` on all health/life-sciences items. Set `"subgroup": "regulatory"` + tag `healthcare-regulatory` for FDA/EMA/WHO ethics/clinical/device items; set `"subgroup": "commercial"` + tag `pharma-commercial` for AI *inside* pharma companies (sales/HCP engagement, marketing + MLR, market access/HEOR, medical affairs, commercial ops/analytics). Prefer ZS/IQVIA/Accenture/ISPOR/FDA OPDP and similar public pieces. No employer- or brand-specific content; no patient data.
- **Filter chips:** `healthcare` (whole section), `pharma-commercial`, `healthcare-regulatory`.
- **AI by industry (`industries`, page section id `industries`, nav label "By industry"):** one array of items; each item has `"subgroup"` set to one of the industry ids below and tags `["industries", "<industry id>", "managers", ...]`. The industry id doubles as the subgroup anchor (`#ind-retail`) and its filter chip. Labels/blurbs live in `industry_groups` (order there = display order). Keep **3–5 items per industry**; when adding a newer piece past 5, move the oldest into `archive[]` with `"archived_from": "industries"` (keep its `id`, `subgroup`, tags).
  | id | Label | Focus |
  |----|-------|-------|
  | `ind-medtech` | Medical devices & biotech | field sales, reimbursement, commercial leaders (shown first, next to Healthcare & pharma) |
  | `ind-finance` | Financial services & insurance | claims, underwriting, compliance, advisor productivity |
  | `ind-retail` | Retail & consumer goods | store/district managers, forecasting, customer service |
  | `ind-manufacturing` | Manufacturing & supply chain | plant supervisors, quality, safety, scheduling, planning |
  | `ind-proservices` | Small business & professional services | owners/small firms: marketing, bookkeeping, client follow-up |
  | `ind-education` | Education & nonprofits | principals, district leaders, program leads |
  | `ind-sales` | Sales leadership | cross-industry coaching, call prep, account/territory planning |
  - Industry item ids are explicit: `"id": "ind-" + sha1(url)[:10]`. Set it on every new industry item so ids stay stable even if an item changes subgroup.
  - Pharma/health-system items still go in `healthcare`, not `industries`. General small-business automation stays in `smb`; `ind-proservices` is for owner/firm-specific AI-adoption pieces.
  - Industry items added 2026-11-09 carry `"new": true` and `"added": "2026-11-09"`. Clear `new` on them on or after **2026-11-16**. For later additions, set `"new": true` + `"added"` and clear after ~7 days.
  - Prefer free-to-read sources (McKinsey, Deloitte, BCG, Bain, MIT Sloan, RAND, FINRA, SBA, trade pubs). HBR is metered (a few free articles/month) — fine but don't let it dominate a group.
  - Known bot-blocked but live in browsers: `mckinsey.com` (curl times out → verify with WebFetch), `mddionline.com` (Cloudflare 403 → verify with WebFetch). Don't drop these on a curl failure alone.
- **New badge:** `"new": true` on `this_week` items (clear when they age out)
- **Videos:**
  ```json
  {
    "youtube_id": "xxxxxxxxxxx",
    "title": "Exact title from oEmbed",
    "url": "https://www.youtube.com/watch?v=xxxxxxxxxxx",
    "channel": "Exact author_name from oEmbed",
    "date": "2026-10",
    "why": "One line why watch",
    "tags": ["videos", "managers"]
  }
  ```
- Record dropped URLs in `dropped_links` with a reason.
- **Archive:** `archive[]` holds items rotated out of `this_week` or trimmed past a section cap. Each entry keeps its fields plus `"archived_date": "YYYY-MM-DD"` and `"archived_from": "this_week"` (or the source section). **Do not delete** rotated items—append to `archive`. Dead links (404/gone) go to `dropped_links`, not archive. The Archive section on the site is collapsed by default and grouped by month.
- **Save (client-only):** visitors can bookmark cards in `localStorage` (`ai-leadership-saved-v1`). No server/login. Stable item ids come from explicit `id`, `youtube_id`, or a SHA1 of the URL/name (see `stable_id()` in `build.py`).

## Daily checklist

1. **Scan** for 1–3 new, free, high-quality pieces (practical AI for managers / aspiring leaders / SMB, leadership judgment, **healthcare & pharma** regulatory/clinical AI, **pharma commercial** AI for sales/marketing/market access/medical affairs, or one of the seven **AI by industry** groups). Prefer primary sources over listicles. Rotate through the industries so each gets a fresh look about once a week (e.g., Mon medtech, Tue finance, Wed retail, Thu manufacturing, Fri pro services, Sat education/nonprofits, Sun sales).
2. **Videos (optional each day):** If adding a YouTube video, verify it exists:
   ```bash
   curl -sL -o /dev/null -w "%{http_code}\n" \
     "https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DVIDEO_ID&format=json"
   ```
   Must be `200`. Then pull **real** title and channel:
   ```bash
   curl -sL "https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DVIDEO_ID&format=json" | python3 -m json.tool
   ```
   Use `title` and `author_name` exactly. Write a one-line `why`. Prefer recent (2025–2026) practical content. Keep the library at ~6–10 videos; rotate older ones out.
3. **Verify links** before keeping anything:
   ```bash
   python3 - <<'PY'
   import json, urllib.request
   data = json.load(open("resources.json"))
   urls = []
   for key in ("this_week","workflows","leadership","smb","healthcare","industries","videos","people"):
       for item in data[key]:
           urls.append(item["url"])
   for u in urls:
       try:
           req = urllib.request.Request(u, method="HEAD", headers={"User-Agent":"Mozilla/5.0"})
           with urllib.request.urlopen(req, timeout=15) as r:
               print(r.status, u)
       except Exception as e:
           # fallback GET
           try:
               req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
               with urllib.request.urlopen(req, timeout=15) as r:
                   print(r.status, u)
           except Exception as e2:
               print("FAIL", u, e2)
   PY
   ```
   Drop 404s / hard failures. Note 403s (sometimes bot-blocked but live in browsers)—prefer replace if unsure.
4. **Edit** `resources.json`: clear `"new"` on aging `this_week` items; move rotated-out This week items (or anything trimmed past a section cap) into `archive[]` with `archived_date` + `archived_from`—do **not** delete them. Dead links → `dropped_links`, not archive. Set `"new": true` only on truly fresh `this_week` items; update `meta.last_updated` (America/Chicago date).
5. **Rebuild:**
   ```bash
   python3 build.py
   ```
6. **Spot-check** locally: open `index.html`, try search, a topic chip, a prompt Copy button, and one video click-to-play.
7. **Commit** (when Brian asks to publish): `resources.json`, `build.py`, `index.html`, `assets/`, `UPDATE.md`, `README.md`. Exclude preview PNGs.


## Voice

Human, non-hype. No employer or family details. Explain *why* in one plain sentence. Prefer workflows + human checkpoints over “10 tools that will transform everything.”

Keep the page built for everyone: no "curated for" line, no owner name or personal X handle in visible page text.

## GitHub Pages

Repo: `https://github.com/bbenson6klub/AI-leadership-resources`  
Likely site: `https://bbenson6klub.github.io/AI-leadership-resources/`  
Static only: relative asset paths, no server runtime. Inline CSS/JS is fine.

