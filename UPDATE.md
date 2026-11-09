# Daily refresh procedure

Run once per day (America/Chicago). Goal: 1–3 genuinely useful new items, not volume.

## 1. Find candidates

Scan a short list of reputable sources (examples):

- One Useful Thing (Ethan Mollick)
- DeepLearning.AI / Andrew Ng letters
- Wharton@Work / Knowledge at Wharton
- HBR free articles or podcasts
- Zapier free guides (no affiliate pitch)
- Other free manager/AI explainers you already trust

Prefer items from the last 30–60 days for “This week’s picks.”

## 2. Verify every new URL

```bash
curl -sL -o /dev/null -w "%{http_code} %{url_effective}\n" -A "Mozilla/5.0" "URL"
```

Keep only **200** (or clear content pages). Drop 404/403/soft-404s. Record drops under `dropped_links` in `resources.json` with the reason and date.

## 3. Edit `resources.json`

For each keeper, add:

- `title`, `url`, `source`, `date` (YYYY-MM or YYYY-MM-DD if known), `why` (1–2 plain sentences)

Rules:

- Move aging “this week” items into `workflows`, `leadership`, or `smb` when they are no longer current.
- Cap sizes: `this_week` ≤ 8, each category ≤ 12, `people` = curated people only (update rarely).
- Do not invent stats, personal stories, employer details, or income claims.
- Do not add affiliate links.
- Prompts: only change if improving clarity; keep them original and labeled as Brian’s.

## 4. Prune

- Re-check a few older category links each week.
- Remove dead links; optionally note them in `dropped_links`.

## 5. Stamp and rebuild

1. Set `meta.last_updated` to today’s date (`YYYY-MM-DD`).
2. Run `python3 build.py`.
3. Open `index.html` and spot-check the new cards and a couple of links.
4. Commit / deploy when the GitHub Pages repo is ready (not part of this folder’s automated publish).

## Done when

- New items are real and verified.
- Caps respected.
- `last_updated` matches today.
- `index.html` rebuilt successfully.
