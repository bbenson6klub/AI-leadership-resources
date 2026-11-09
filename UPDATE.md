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

- **Sections:** `this_week`, `workflows`, `prompts`, `leadership`, `smb`, `healthcare`, `videos`, `people`
- **Common fields:** `title`, `url` (or `prompt` for prompts), `why`, `tags` (array)
- **Tags:** topic chips — `workflows`, `prompts`, `leadership`, `smb`, `healthcare`, `videos`, `people` — plus audience — `managers`, `aspiring`, `smb`
- **Healthcare & pharma:** use tag `healthcare` on all health/life-sciences items. Set `"subgroup": "regulatory"` + tag `healthcare-regulatory` for FDA/EMA/WHO ethics/clinical/device items; set `"subgroup": "commercial"` + tag `pharma-commercial` for AI *inside* pharma companies (sales/HCP engagement, marketing + MLR, market access/HEOR, medical affairs, commercial ops/analytics). Prefer ZS/IQVIA/Accenture/ISPOR/FDA OPDP and similar public pieces. No employer- or brand-specific content; no patient data.
- **Filter chips:** `healthcare` (whole section), `pharma-commercial`, `healthcare-regulatory`.
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

## Daily checklist

1. **Scan** for 1–3 new, free, high-quality pieces (practical AI for managers / aspiring leaders / SMB, leadership judgment, **healthcare & pharma** regulatory/clinical AI, or **pharma commercial** AI for sales/marketing/market access/medical affairs). Prefer primary sources over listicles.
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
   for key in ("this_week","workflows","leadership","smb","healthcare","videos","people"):
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
4. **Edit** `resources.json`: move last week’s “new” items into permanent sections or drop; set `"new": true` only on truly fresh `this_week` items; update `meta.last_updated` (America/Chicago date).
5. **Rebuild:**
   ```bash
   python3 build.py
   ```
6. **Spot-check** locally: open `index.html`, try search, a topic chip, a prompt Copy button, and one video click-to-play.
7. **Commit** (when Brian asks to publish): `resources.json`, `build.py`, `index.html`, `assets/`, `UPDATE.md`, `README.md`. Exclude preview PNGs.

## Voice

Human, non-hype. No employer or family details. Explain *why* in one plain sentence. Prefer workflows + human checkpoints over “10 tools that will transform everything.”

## GitHub Pages

Repo: `https://github.com/bbenson6klub/AI-leadership-resources`  
Likely site: `https://bbenson6klub.github.io/AI-leadership-resources/`  
Static only: relative asset paths, no server runtime. Inline CSS/JS is fine.
