# Practical AI. Better Leadership. — Resources

Static site for Brian Benson’s X bio link (`@BBenson6`).

## Who it’s for

Team leaders, aspiring managers, and small-business owners who want practical AI workflows and clearer leadership—without hype.

## Files

| File | Role |
| --- | --- |
| `resources.json` | Source of truth for every resource, prompt, and person |
| `build.py` | Builds `index.html` from the JSON |
| `index.html` | Deployable static page (no external CSS/JS) |
| `UPDATE.md` | Daily refresh procedure |
| `preview.png` | Local render check |

## Local build

```bash
python3 build.py
```

Open `index.html` in a browser. For GitHub Pages, publish this folder (or the repo root) after building.

## Daily updates

Edit `resources.json` only, then run `python3 build.py`. See `UPDATE.md`.

## Notes

- No affiliate links.
- No guaranteed income claims.
- Prompts are original drafts—users should adapt them to their tools and policies.
- Hosting on GitHub Pages is planned; repo not created from this folder yet.
