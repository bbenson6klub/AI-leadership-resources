#!/usr/bin/env python3
"""Build a static, progressive-enhancement index.html from resources.json."""
from __future__ import annotations

import hashlib
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "resources.json").read_text(encoding="utf-8"))


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def tag_attrs(tags: list) -> str:
    return " ".join(esc(t) for t in (tags or []))


def stable_id(item: dict, kind: str = "item") -> str:
    """Stable per-item id across rebuilds (explicit id, youtube id, or URL/name hash)."""
    if item.get("id"):
        return str(item["id"])
    if item.get("youtube_id"):
        return f"yt-{item['youtube_id']}"
    seed = item.get("url") or item.get("name") or item.get("title") or kind
    digest = hashlib.sha1(str(seed).encode("utf-8")).hexdigest()[:10]
    return f"{kind}-{digest}"


def card_actions(sid: str, label: str) -> str:
    safe = esc(label)
    return f"""<div class="card-actions">
    <button type="button" class="btn-save" data-save-id="{esc(sid)}" aria-pressed="false" aria-label="Save {safe}">Save</button>
    <button type="button" class="btn-share" data-share-id="{esc(sid)}" aria-label="Share {safe}">Share</button>
  </div>"""


TAG_LABELS = {
    "workflows": "Workflows",
    "prompts": "Prompts",
    "leadership": "Leadership",
    "smb": "Small business",
    "healthcare": "Healthcare",
    "pharma-commercial": "Pharma commercial",
    "healthcare-regulatory": "Regulatory",
    "videos": "Videos",
    "people": "People",
    "managers": "Managers",
    "aspiring": "Aspiring leaders",
    "archive": "Archive",
    "saved": "Saved",
}


def tag_pills(tags: list, limit: int = 3) -> str:
    pills = []
    for t in tags or []:
        label = TAG_LABELS.get(t)
        if not label:
            continue
        pills.append(f'<span class="tag-pill tag-{esc(t)}">{esc(label)}</span>')
        if len(pills) >= limit:
            break
    if not pills:
        return ""
    return f'<div class="tag-row">{"".join(pills)}</div>'


def icon_tile(section: str) -> str:
    return f'<span class="icon-tile tone-{esc(section)}" aria-hidden="true">{ICON_SVGS.get(section, ICON_SVGS["workflows"])}</span>'

ICON_SVGS = {
    "workflows": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 6h4v2H4V6zm6 0h10v2H10V6zM4 11h4v2H4v-2zm6 0h10v2H10v-2zM4 16h4v2H4v-2zm6 0h10v2H10v-2z"/><circle cx="6" cy="7" r="1.4" fill="currentColor" opacity=".45"/><circle cx="6" cy="12" r="1.4" fill="currentColor" opacity=".45"/><circle cx="6" cy="17" r="1.4" fill="currentColor" opacity=".45"/></svg>""",
    "prompts": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H9l-4 3v-3H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm2 4v2h12V8H6zm0 4v2h8v-2H6z"/></svg>""",
    "leadership": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2l2.2 4.5 5 .7-3.6 3.5.9 5.1L12 13.8 7.5 15.8l.9-5.1L4.8 7.2l5-.7L12 2z"/></svg>""",
    "smb": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 20V9l9-5 9 5v11h-6v-6H9v6H3zm2-2h2v-4h10v4h2v-8.2L12 6.1 5 9.8V18z"/></svg>""",
    "videos": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path fill="currentColor" d="M10 9.2v5.6L15 12l-5-2.8z"/></svg>""",
    "people": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3" fill="currentColor"/><circle cx="16" cy="9" r="2.4" fill="currentColor" opacity=".7"/><path fill="currentColor" d="M3 19c0-3 3-5 6-5s6 2 6 5v1H3v-1z"/><path fill="currentColor" opacity=".7" d="M14 19c0-1.8 1.4-3.2 3.2-3.6.5-.1 1-.2 1.5-.2 1.8 0 3.3 1.2 3.3 3v1h-8v-1z"/></svg>""",
    "healthcare": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M11 3h2v6h6v2h-6v6h-2v-6H5V9h6V3z"/><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.5" opacity=".55"/></svg>""",
    "archive": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 4h16v4H4V4zm1 6h14v10H5V10zm3 2v2h8v-2H8z"/></svg>""",
    "week": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 2h2v2h6V2h2v2h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3V2zm13 8H4v10h16V10zM8 13h3v3H8v-3z"/></svg>""",
}


def card_link(item: dict, section: str) -> str:
    tags = item.get("tags") or [section]
    sid = stable_id(item, section)
    new_badge = '<span class="badge-new">New</span>' if item.get("new") else ""
    title = esc(item["title"])
    url = esc(item["url"])
    source = esc(item.get("source", ""))
    date = esc(item.get("date", ""))
    why = esc(item.get("why", ""))
    meta_bits = [source, date]
    if item.get("archived_from"):
        meta_bits.append(f"from {item.get('archived_from')}")
    if item.get("archived_date"):
        meta_bits.append(f"archived {item.get('archived_date')}")
    meta = " · ".join(x for x in meta_bits if x)
    return f"""
<article class="card tone-{esc(section)}" id="item-{esc(sid)}" data-id="{esc(sid)}" data-tags="{tag_attrs(tags)}" data-text="{esc((item.get('title','') + ' ' + item.get('source','') + ' ' + item.get('why','') + ' ' + item.get('name','')).lower())}">
  <div class="card-head">
    {icon_tile(section)}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{title}</a></h3>
      <p class="meta">{meta}</p>
    </div>
    {new_badge}
  </div>
  <p class="why">{why}</p>
  {tag_pills(tags)}
  {card_actions(sid, item.get('title') or 'resource')}
</article>"""




def card_prompt(item: dict) -> str:
    tags = item.get("tags") or ["prompts"]
    sid = stable_id(item, "prompt")
    title = esc(item["title"])
    why = esc(item.get("why", ""))
    prompt = item.get("prompt", "")
    return f"""
<article class="card prompt-card tone-prompts" id="item-{esc(sid)}" data-id="{esc(sid)}" data-tags="{tag_attrs(tags)}" data-text="{esc((item['title'] + ' ' + item.get('why','') + ' ' + prompt).lower())}">
  <div class="card-head">
    {icon_tile('prompts')}
    <div>
      <h3>{title}</h3>
      <p class="meta">Copy-ready prompt</p>
    </div>
  </div>
  <p class="why">{why}</p>
  <pre class="prompt-body" id="{esc(sid)}-text">{esc(prompt)}</pre>
  <div class="prompt-actions">
    <button type="button" class="btn-copy" data-copy-target="{esc(sid)}-text" aria-label="Copy prompt: {title}">Copy</button>
    <span class="copy-feedback" hidden aria-live="polite">Copied</span>
  </div>
  {tag_pills(tags)}
  {card_actions(sid, item.get('title') or 'prompt')}
</article>"""




def card_person(item: dict) -> str:
    tags = item.get("tags") or ["people"]
    sid = stable_id(item, "person")
    name = esc(item["name"])
    handle = esc(item.get("handle", ""))
    url = esc(item["url"])
    why = esc(item.get("why", ""))
    return f"""
<article class="card person-card tone-people" id="item-{esc(sid)}" data-id="{esc(sid)}" data-tags="{tag_attrs(tags)}" data-text="{esc((item['name'] + ' ' + item.get('handle','') + ' ' + item.get('why','')).lower())}">
  <div class="card-head">
    {icon_tile('people')}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{name}</a></h3>
      <p class="meta">{handle}</p>
    </div>
  </div>
  <p class="why">{why}</p>
  {tag_pills(tags)}
  {card_actions(sid, item.get('name') or 'person')}
</article>"""




def card_video(item: dict) -> str:
    tags = item.get("tags") or ["videos"]
    sid = stable_id(item, "video")
    vid = esc(item["youtube_id"])
    title = esc(item["title"])
    url = esc(item["url"])
    channel = esc(item.get("channel", ""))
    date = esc(item.get("date", ""))
    why = esc(item.get("why", ""))
    thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    meta = " · ".join(x for x in [channel, date] if x)
    return f"""
<article class="card video-card tone-videos" id="item-{esc(sid)}" data-id="{esc(sid)}" data-tags="{tag_attrs(tags)}" data-text="{esc((item['title'] + ' ' + item.get('channel','') + ' ' + item.get('why','')).lower())}">
  <div class="video-lazy" data-youtube-id="{vid}">
    <button type="button" class="video-poster" aria-label="Play video: {title}">
      <img src="{thumb}" alt="" width="480" height="360" loading="lazy" decoding="async">
      <span class="play-btn" aria-hidden="true"></span>
    </button>
  </div>
  <div class="card-head">
    {icon_tile('videos')}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{title}</a></h3>
      <p class="meta">{meta}</p>
    </div>
  </div>
  <p class="why">{why}</p>
  {tag_pills(tags)}
  {card_actions(sid, item.get('title') or 'video')}
</article>"""




def section_block(sid: str, heading: str, intro: str, cards_html: str, icon_key: str) -> str:
    return f"""
<section class="section reveal tone-{esc(icon_key if icon_key != 'week' else 'week')}" id="{sid}" data-section="{sid}">
  <header class="section-head">
    {icon_tile(icon_key)}
    <div>
      <h2>{esc(heading)}</h2>
      <p>{esc(intro)}</p>
    </div>
  </header>
  <div class="grid">{cards_html}</div>
</section>"""



CSS = r"""
:root {
  --navy: #0b1f3a;
  --navy-2: #122a4a;
  --indigo: #312e81;
  --teal: #0d9488;
  --violet: #7c3aed;
  --amber: #d97706;
  --green: #059669;
  --rose: #e11d48;
  --coral: #f43f5e;
  --sky: #0284c7;
  --blue: #2563eb;
  --blue-soft: #93c5fd;
  --ink: #0f172a;
  --muted: #475569;
  --line: #d7e0ee;
  --bg: #f3f6fb;
  --card: #ffffff;
  --ok: #059669;
  --radius: 16px;
  --shadow: 0 10px 28px rgba(11, 31, 58, 0.08);
  --shadow-hover: 0 16px 36px rgba(11, 31, 58, 0.14);
  --max: 1100px;
  --focus: 0 0 0 3px rgba(37, 99, 235, 0.45);
  --tone: #2563eb;
  --tone-soft: #dbeafe;
  --tone-ink: #1e3a8a;
}
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color: var(--ink);
  background:
    radial-gradient(1200px 500px at 10% -10%, rgba(45, 212, 191, 0.12), transparent 55%),
    radial-gradient(900px 420px at 100% 0%, rgba(129, 140, 248, 0.14), transparent 50%),
    var(--bg);
  line-height: 1.55;
}
a { color: var(--blue); }
a:hover { color: #1d4ed8; }
img { max-width: 100%; height: auto; display: block; }
.skip {
  position: absolute; left: -999px; top: 0;
  background: var(--navy); color: #fff; padding: .6rem 1rem; z-index: 100;
}
.skip:focus { left: 0; }

/* Section tone tokens */
.tone-week, .tone-this-week { --tone: #0284c7; --tone-soft: #e0f2fe; --tone-ink: #075985; }
.tone-workflows { --tone: #0d9488; --tone-soft: #ccfbf1; --tone-ink: #115e59; }
.tone-prompts { --tone: #7c3aed; --tone-soft: #ede9fe; --tone-ink: #5b21b6; }
.tone-leadership { --tone: #d97706; --tone-soft: #ffedd5; --tone-ink: #9a3412; }
.tone-smb { --tone: #059669; --tone-soft: #d1fae5; --tone-ink: #065f46; }
.tone-healthcare { --tone: #e11d48; --tone-soft: #ffe4e6; --tone-ink: #9f1239; }
.tone-videos { --tone: #f43f5e; --tone-soft: #ffe4e6; --tone-ink: #9f1239; }
.tone-people { --tone: #2563eb; --tone-soft: #dbeafe; --tone-ink: #1e3a8a; }
.tone-archive { --tone: #64748b; --tone-soft: #e2e8f0; --tone-ink: #334155; }
.tone-saved { --tone: #0d9488; --tone-soft: #ccfbf1; --tone-ink: #115e59; }

.hero {
  background:
    radial-gradient(700px 280px at 18% 20%, rgba(45, 212, 191, 0.28), transparent 60%),
    radial-gradient(560px 260px at 85% 10%, rgba(99, 102, 241, 0.35), transparent 55%),
    radial-gradient(420px 220px at 70% 90%, rgba(244, 63, 94, 0.18), transparent 60%),
    linear-gradient(145deg, #071527 0%, #0b1f3a 38%, #1e1b4b 72%, #134e4a 100%);
  color: #fff;
  position: relative;
  overflow: hidden;
}
.hero-mesh {
  position: absolute; inset: 0; pointer-events: none; opacity: .55;
  background:
    radial-gradient(circle at 20% 30%, rgba(255,255,255,.08) 0 1px, transparent 2px),
    radial-gradient(circle at 70% 60%, rgba(255,255,255,.07) 0 1px, transparent 2px);
  background-size: 42px 42px, 56px 56px;
  animation: meshDrift 28s linear infinite;
}
.hero-glow {
  position: absolute; width: 340px; height: 340px; border-radius: 50%;
  right: -80px; top: -100px;
  background: radial-gradient(circle, rgba(96,165,250,.35), transparent 70%);
  filter: blur(8px);
  animation: glowPulse 6s ease-in-out infinite;
  pointer-events: none;
}
@keyframes meshDrift {
  from { background-position: 0 0, 0 0; }
  to { background-position: 84px 42px, -56px 56px; }
}
@keyframes glowPulse {
  0%, 100% { opacity: .55; transform: scale(1); }
  50% { opacity: .9; transform: scale(1.08); }
}
.hero-inner {
  max-width: var(--max);
  margin: 0 auto;
  padding: 2.5rem 1.25rem 2.6rem;
  position: relative;
  z-index: 1;
}
.network {
  position: absolute;
  right: -30px;
  top: 52%;
  transform: translateY(-50%);
  width: min(42vw, 320px);
  height: 220px;
  opacity: 0.38;
  pointer-events: none;
  z-index: 0;
}
.hero h1 {
  margin: 0 0 .45rem;
  font-size: clamp(1.85rem, 4.6vw, 2.65rem);
  letter-spacing: -0.03em;
  line-height: 1.15;
  font-weight: 800;
}
.hero .tagline {
  margin: 0 0 1rem;
  color: #99f6e4;
  font-weight: 700;
  font-size: clamp(1.02rem, 2.2vw, 1.2rem);
}
.hero .intro { max-width: 42rem; margin: 0 0 1.15rem; color: #dbeafe; }
.hero .meta-line { font-size: .9rem; color: #bfdbfe; margin: 0 0 1.1rem; }
.stat-pills {
  display: flex; flex-wrap: wrap; gap: .5rem;
}
.stat-pill {
  display: inline-flex; align-items: center; gap: .4rem;
  background: rgba(255,255,255,.1);
  border: 1px solid rgba(255,255,255,.22);
  backdrop-filter: blur(8px);
  color: #fff;
  border-radius: 999px;
  padding: .4rem .8rem;
  font-size: .86rem;
  font-weight: 700;
}
.stat-pill strong {
  color: #99f6e4;
  font-size: .95rem;
}

.sticky-bar {
  position: sticky; top: 0; z-index: 40;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--line);
}
.sticky-inner {
  max-width: var(--max);
  margin: 0 auto;
  padding: .7rem 1.25rem .8rem;
  display: grid;
  gap: .65rem;
}
.nav-scroll {
  display: flex; gap: .45rem; overflow-x: auto; padding-bottom: .15rem;
  scrollbar-width: thin;
}
.nav-scroll a {
  flex: 0 0 auto;
  text-decoration: none;
  color: var(--nav-ink, var(--navy));
  background: var(--nav-bg, #eef4ff);
  border: 1px solid var(--nav-border, #cfe0ff);
  border-radius: 999px;
  padding: .38rem .78rem;
  font-size: .84rem;
  font-weight: 700;
  transition: transform .15s ease, box-shadow .15s ease;
}
.nav-scroll a:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(11,31,58,.08); }
.nav-scroll a[href="#workflows"] { --nav-bg:#ccfbf1; --nav-border:#99f6e4; --nav-ink:#115e59; }
.nav-scroll a[href="#prompts"] { --nav-bg:#ede9fe; --nav-border:#ddd6fe; --nav-ink:#5b21b6; }
.nav-scroll a[href="#leadership"] { --nav-bg:#ffedd5; --nav-border:#fed7aa; --nav-ink:#9a3412; }
.nav-scroll a[href="#smb"] { --nav-bg:#d1fae5; --nav-border:#a7f3d0; --nav-ink:#065f46; }
.nav-scroll a[href="#healthcare"] { --nav-bg:#ffe4e6; --nav-border:#fecdd3; --nav-ink:#9f1239; }
.nav-scroll a[href="#videos"] { --nav-bg:#ffe4e6; --nav-border:#fecdd3; --nav-ink:#be123c; }
.nav-scroll a[href="#people"] { --nav-bg:#dbeafe; --nav-border:#bfdbfe; --nav-ink:#1e3a8a; }
.nav-scroll a[href="#this-week"] { --nav-bg:#e0f2fe; --nav-border:#bae6fd; --nav-ink:#075985; }
.nav-scroll a:focus-visible, .chip:focus-visible, .btn-copy:focus-visible, .video-poster:focus-visible, #q:focus-visible {
  outline: none; box-shadow: var(--focus);
}
.controls { display: grid; gap: .55rem; }
#q {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: .75rem 1rem;
  font-size: 1rem;
  background: #fff;
  box-shadow: 0 1px 2px rgba(11,31,58,.04);
}
.chips { display: flex; flex-wrap: wrap; gap: .4rem; }
.chip {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--navy);
  border-radius: 999px;
  padding: .36rem .72rem;
  font-size: .82rem;
  font-weight: 650;
  cursor: pointer;
  transition: background .15s ease, color .15s ease, border-color .15s ease, transform .15s ease;
}
.chip:hover { transform: translateY(-1px); }
.chip[aria-pressed="true"] {
  background: var(--navy);
  color: #fff;
  border-color: var(--navy);
}
.chip[data-filter="workflows"][aria-pressed="true"] { background: var(--teal); border-color: var(--teal); }
.chip[data-filter="prompts"][aria-pressed="true"] { background: var(--violet); border-color: var(--violet); }
.chip[data-filter="leadership"][aria-pressed="true"] { background: var(--amber); border-color: var(--amber); }
.chip[data-filter="smb"][aria-pressed="true"] { background: var(--green); border-color: var(--green); }
.chip[data-filter="healthcare"][aria-pressed="true"],
.chip[data-filter="pharma-commercial"][aria-pressed="true"],
.chip[data-filter="healthcare-regulatory"][aria-pressed="true"] { background: var(--rose); border-color: var(--rose); }
.chip[data-filter="videos"][aria-pressed="true"] { background: var(--coral); border-color: var(--coral); }
.chip[data-filter="people"][aria-pressed="true"] { background: var(--blue); border-color: var(--blue); }

.wrap { max-width: var(--max); margin: 0 auto; padding: 1.25rem; }
.start {
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1.2rem 1.25rem 1.35rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.35rem;
}
.start h2 { margin: 0 0 .35rem; font-size: 1.2rem; color: var(--navy); }
.start p { margin: 0; color: var(--muted); }
.steps {
  display: grid;
  gap: .65rem;
  grid-template-columns: 1fr;
  margin-top: .95rem;
  align-items: stretch;
}
@media (min-width: 720px) {
  .steps {
    grid-template-columns: 1fr auto 1fr auto 1fr;
    align-items: center;
    gap: .45rem;
  }
}
.step {
  border-radius: 14px;
  padding: 1rem 1.05rem;
  color: #fff;
  box-shadow: var(--shadow);
  border: 1px solid rgba(255,255,255,.14);
  background: #0b1f3a;
}
.steps .step:nth-child(1) { background: linear-gradient(145deg, #0f766e 0%, #0b1f3a 78%); }
.steps .step:nth-child(3) { background: linear-gradient(145deg, #4f46e5 0%, #0b1f3a 78%); }
.steps .step:nth-child(5) { background: linear-gradient(145deg, #be123c 0%, #0b1f3a 78%); }
.step .num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 1.75rem; height: 1.75rem; border-radius: 999px;
  background: #fff;
  color: #0b1f3a; font-weight: 800; font-size: .82rem;
  margin-bottom: .45rem;
  box-shadow: 0 0 0 3px rgba(255,255,255,.18);
}
.step strong { display: block; color: #fff; margin-bottom: .25rem; font-size: .98rem; }
.step span { color: #dbeafe; font-size: .88rem; }
.step-arrow {
  display: none;
  color: #64748b;
  font-size: 1.35rem;
  font-weight: 700;
  text-align: center;
  line-height: 1;
}
@media (min-width: 720px) {
  .step-arrow { display: block; }
}

.section {
  margin: 1.35rem 0 1.8rem;
  padding: 1.05rem 1rem 1.15rem;
  border-radius: 18px;
  background: color-mix(in srgb, var(--tone-soft) 42%, transparent);
  border: 1px solid color-mix(in srgb, var(--tone) 14%, var(--line));
}
.section:nth-of-type(even) {
  background: color-mix(in srgb, var(--tone-soft) 58%, #fff);
}
.section-head {
  display: flex; gap: .85rem; align-items: flex-start;
  margin-bottom: .95rem;
}
.section-head h2 { margin: 0; color: var(--navy); font-size: 1.35rem; }
.section-head p { margin: .25rem 0 0; color: var(--muted); }
.subgroup { margin: 1.15rem 0 .7rem; }
.subgroup h3 {
  margin: 0 0 .25rem;
  font-size: 1.05rem;
  color: var(--navy);
}
.subgroup p {
  margin: 0 0 .75rem;
  color: var(--muted);
  font-size: .92rem;
}

.icon-tile {
  display: inline-flex; align-items: center; justify-content: center;
  width: 2.45rem; height: 2.45rem; border-radius: 12px;
  background: var(--tone-soft);
  color: var(--tone);
  flex: 0 0 auto;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--tone) 18%, transparent);
}
.ico { width: 22px; height: 22px; display: block; }
.card .icon-tile { width: 2.1rem; height: 2.1rem; border-radius: 10px; }
.card .ico { width: 18px; height: 18px; }

.grid {
  display: grid;
  gap: .95rem;
  grid-template-columns: 1fr;
}
@media (min-width: 700px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
.card {
  --tone: #2563eb;
  --tone-soft: #dbeafe;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1rem 1.05rem 1.05rem;
  box-shadow: var(--shadow);
  position: relative;
  overflow: hidden;
  transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
}
.card::before {
  content: "";
  position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
  background: linear-gradient(180deg, var(--tone), color-mix(in srgb, var(--tone) 40%, #0b1f3a));
}
.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
  border-color: color-mix(in srgb, var(--tone) 35%, var(--line));
}
.card[hidden], .section.is-empty { display: none !important; }
.card-head { display: flex; gap: .7rem; align-items: flex-start; position: relative; }
.card-head h3 { margin: 0; font-size: 1.02rem; line-height: 1.35; }
.card-head h3 a { color: var(--navy); text-decoration: none; }
.card-head h3 a:hover { color: var(--tone); text-decoration: underline; }
.meta { margin: .2rem 0 0; color: var(--muted); font-size: .84rem; }
.why { margin: .7rem 0 0; color: #334155; }
.card-head > div { flex: 1 1 auto; min-width: 0; }
.badge-new {
  position: static;
  margin-left: auto;
  align-self: flex-start;
  background: linear-gradient(135deg, #f97316, #ef4444);
  color: #fff;
  border: 0;
  font-size: .72rem; font-weight: 800;
  padding: .22rem .55rem; border-radius: 999px;
  white-space: nowrap;
  flex: 0 0 auto;
  letter-spacing: .02em;
  box-shadow: 0 4px 12px rgba(239, 68, 68, .28);
}
.tag-row { display: flex; flex-wrap: wrap; gap: .35rem; margin-top: .75rem; }
.tag-pill {
  display: inline-flex;
  border-radius: 999px;
  padding: .18rem .55rem;
  font-size: .72rem;
  font-weight: 700;
  background: var(--tone-soft);
  color: var(--tone-ink);
  border: 1px solid color-mix(in srgb, var(--tone) 22%, transparent);
}
.tag-workflows { --tone:#0d9488; --tone-soft:#ccfbf1; --tone-ink:#115e59; }
.tag-prompts { --tone:#7c3aed; --tone-soft:#ede9fe; --tone-ink:#5b21b6; }
.tag-leadership { --tone:#d97706; --tone-soft:#ffedd5; --tone-ink:#9a3412; }
.tag-smb { --tone:#059669; --tone-soft:#d1fae5; --tone-ink:#065f46; }
.tag-healthcare, .tag-pharma-commercial, .tag-healthcare-regulatory { --tone:#e11d48; --tone-soft:#ffe4e6; --tone-ink:#9f1239; }
.tag-videos { --tone:#f43f5e; --tone-soft:#ffe4e6; --tone-ink:#9f1239; }
.tag-people { --tone:#2563eb; --tone-soft:#dbeafe; --tone-ink:#1e3a8a; }
.tag-managers { --tone:#0369a1; --tone-soft:#e0f2fe; --tone-ink:#075985; }
.tag-aspiring { --tone:#7c3aed; --tone-soft:#f3e8ff; --tone-ink:#6b21a8; }

.prompt-body {
  margin: .75rem 0 .65rem;
  padding: .8rem .85rem;
  background: linear-gradient(160deg, #0b1f3a, #1e1b4b);
  color: #e2e8f0;
  border-radius: 12px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: .86rem;
  line-height: 1.45;
  max-height: 220px;
  overflow: auto;
  border: 1px solid rgba(148,163,184,.25);
}
.prompt-actions { display: flex; align-items: center; gap: .45rem; margin-bottom: .15rem; }
.btn-copy {
  border: 0;
  background: linear-gradient(135deg, #7c3aed, #2563eb);
  color: #fff;
  font-weight: 800;
  border-radius: 999px;
  padding: .48rem .95rem;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(37, 99, 235, .25);
}
.btn-copy:hover { filter: brightness(1.06); }
.copy-feedback {
  color: var(--ok);
  font-weight: 700;
  font-size: .9rem;
}
.video-lazy {
  margin: -.2rem -.2rem .8rem;
  border-radius: 12px;
  overflow: hidden;
  background: #0b1f3a;
  aspect-ratio: 16/9;
  box-shadow: inset 0 0 0 1px rgba(255,255,255,.08);
}
.video-poster {
  position: relative; display: block; width: 100%; height: 100%;
  border: 0; padding: 0; cursor: pointer; background: #0b1f3a;
}
.video-poster img { width: 100%; height: 100%; object-fit: cover; opacity: .94; transition: transform .25s ease, opacity .25s ease; }
.video-card:hover .video-poster img { transform: scale(1.03); opacity: 1; }
.play-btn {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%);
  width: 58px; height: 58px; border-radius: 999px;
  background: linear-gradient(145deg, rgba(244,63,94,.95), rgba(11,31,58,.9));
  border: 2px solid #fff;
  box-shadow: 0 8px 22px rgba(0,0,0,.35);
}
.play-btn::before {
  content: "";
  position: absolute; left: 23px; top: 17px;
  border-style: solid; border-width: 12px 0 12px 18px;
  border-color: transparent transparent transparent #fff;
}
.video-lazy iframe { width: 100%; height: 100%; border: 0; aspect-ratio: 16/9; display: block; }
.person-card .card-head h3 { font-size: 1.05rem; }
.empty {
  display: none;
  margin: 1rem 0 2rem;
  padding: 1rem;
  background: #fff;
  border: 1px dashed var(--line);
  border-radius: 12px;
  color: var(--muted);
}
.empty.show { display: block; }
footer {
  max-width: var(--max);
  margin: 0 auto 2.2rem;
  padding: 0 1.25rem;
  color: var(--muted);
  font-size: .92rem;
}
noscript .note {
  max-width: var(--max); margin: .75rem auto; padding: 0 1.25rem;
  color: var(--muted); font-size: .9rem;
}

/* Reveal on scroll — visible by default without JS */
.reveal {
  opacity: 1;
  transform: none;
}
.js .reveal {
  opacity: 0;
  transform: translateY(12px);
  transition: opacity .45s ease, transform .45s ease;
}
.js .reveal.is-visible {
  opacity: 1;
  transform: none;
}


.card-actions {
  display: flex; flex-wrap: wrap; gap: .4rem;
  margin-top: .75rem;
}
.btn-save, .btn-share {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--navy);
  font-weight: 700;
  font-size: .82rem;
  border-radius: 999px;
  padding: .38rem .75rem;
  cursor: pointer;
}
.btn-save[aria-pressed="true"] {
  background: linear-gradient(135deg, #0d9488, #0284c7);
  color: #fff;
  border-color: transparent;
}
.btn-save:hover, .btn-share:hover { filter: brightness(1.03); }
.btn-share:focus-visible, .btn-save:focus-visible {
  outline: none; box-shadow: var(--focus);
}
.count-badge {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 1.35rem; height: 1.35rem;
  padding: 0 .4rem;
  margin-left: .35rem;
  border-radius: 999px;
  background: var(--tone-soft, #dbeafe);
  color: var(--tone-ink, #1e3a8a);
  font-size: .75rem;
  font-weight: 800;
  vertical-align: middle;
}
.nav-scroll a .count-badge {
  background: rgba(11,31,58,.1);
  color: inherit;
  margin-left: .25rem;
}
.nav-scroll a[href="#saved"] .count-badge {
  background: #0d9488; color: #fff;
}
.saved-empty, .archive-empty {
  margin: .5rem 0 0;
  padding: .9rem 1rem;
  border: 1px dashed var(--line);
  border-radius: 12px;
  color: var(--muted);
  background: color-mix(in srgb, #fff 70%, transparent);
}
.archive-details { border: 0; }
.archive-summary {
  list-style: none;
  cursor: pointer;
  display: flex;
  gap: .85rem;
  align-items: flex-start;
}
.archive-summary::-webkit-details-marker { display: none; }
.archive-summary::after {
  content: "Show";
  margin-left: auto;
  align-self: center;
  font-size: .82rem;
  font-weight: 700;
  color: var(--blue);
  background: #eef4ff;
  border-radius: 999px;
  padding: .3rem .7rem;
}
.archive-details[open] .archive-summary::after { content: "Hide"; }
.archive-month { margin-top: 1rem; }
.archive-month h3 {
  margin: 0 0 .65rem;
  font-size: 1rem;
  color: var(--navy);
}
.card.is-deep-link {
  box-shadow: 0 0 0 3px rgba(13, 148, 136, .45), var(--shadow-hover);
  border-color: #0d9488;
}
.chip[data-filter="saved"][aria-pressed="true"] { background: #0d9488; border-color: #0d9488; }
.nav-scroll a[href="#saved"] { --nav-bg:#ccfbf1; --nav-border:#99f6e4; --nav-ink:#115e59; }
.nav-scroll a[href="#archive"] { --nav-bg:#e2e8f0; --nav-border:#cbd5e1; --nav-ink:#334155; }

@media (prefers-color-scheme: dark) {
  .btn-save, .btn-share { background: #0f1b2d; color: #dbeafe; border-color: #2b3d55; }
  .saved-empty, .archive-empty { background: #0f1b2d; }
  .archive-summary::after { background: #1e293b; color: #93c5fd; }
}

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .hero-mesh, .hero-glow { animation: none !important; }
  .card, .nav-scroll a, .chip, .video-poster img { transition: none !important; }
  .js .reveal, .reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
}

@media (prefers-color-scheme: dark) {
  :root {
    --ink: #e5eefc;
    --muted: #9fb0c7;
    --line: #243549;
    --bg: #07111f;
    --card: #0f1b2d;
    --shadow: 0 10px 28px rgba(0,0,0,.35);
    --shadow-hover: 0 16px 36px rgba(0,0,0,.45);
    --focus: 0 0 0 3px rgba(96, 165, 250, 0.5);
  }
  body {
    background:
      radial-gradient(1000px 420px at 10% -10%, rgba(45, 212, 191, 0.08), transparent 55%),
      radial-gradient(800px 380px at 100% 0%, rgba(129, 140, 248, 0.1), transparent 50%),
      var(--bg);
  }
  .sticky-bar { background: rgba(7, 17, 31, 0.88); }
  #q, .chip, .empty, .start { background: #0f1b2d; color: var(--ink); }
  .chip { border-color: #2b3d55; color: #dbeafe; }
  .section { border-color: #243549; }
  .card-head h3 a { color: #e8eef8; }
  .why { color: #c6d3e5; }
  .nav-scroll a { color: var(--nav-ink, #dbeafe); }
  footer { color: #9fb0c7; }
}
"""

JS = r"""
(function () {
  var STORAGE_KEY = 'ai-leadership-saved-v1';
  var q = document.getElementById('q');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var empty = document.getElementById('no-results');
  var active = 'all';
  var savedGrid = document.getElementById('saved-grid');
  var savedEmpty = document.getElementById('saved-empty');
  var savedCountEls = document.querySelectorAll('[data-saved-count]');

  function allCards() {
    return Array.prototype.slice.call(document.querySelectorAll('main .card'));
  }

  function loadSaved() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr.filter(Boolean) : [];
    } catch (err) {
      return [];
    }
  }

  function storeSaved(ids) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
  }

  function syncSaveButtons(ids) {
    document.querySelectorAll('.btn-save').forEach(function (btn) {
      var id = btn.getAttribute('data-save-id');
      var on = ids.indexOf(id) !== -1;
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      btn.textContent = on ? 'Saved' : 'Save';
    });
  }

  function updateSavedCount(ids) {
    savedCountEls.forEach(function (el) {
      el.textContent = String(ids.length);
      el.hidden = false;
    });
  }

  function rebuildSavedSection(ids) {
    if (!savedGrid) return;
    savedGrid.innerHTML = '';
    var shown = 0;
    ids.forEach(function (id) {
      var src = document.querySelector('main .card[data-id="' + id + '"]:not(#saved-grid .card)');
      // Prefer canonical card outside saved grid
      if (!src) src = document.querySelector('article.card[data-id="' + id + '"]');
      if (!src) return;
      // Skip if this node already lives only in saved grid duplicates: find original in content sections
      var original = document.querySelector('#this-week .card[data-id="' + id + '"], #workflows .card[data-id="' + id + '"], #prompts .card[data-id="' + id + '"], #leadership .card[data-id="' + id + '"], #smb .card[data-id="' + id + '"], #healthcare .card[data-id="' + id + '"], #videos .card[data-id="' + id + '"], #people .card[data-id="' + id + '"], #archive .card[data-id="' + id + '"]');
      var node = (original || src).cloneNode(true);
      node.removeAttribute('hidden');
      node.classList.remove('is-deep-link');
      // Avoid duplicate element ids in clones
      if (node.id) node.id = 'saved-clone-' + node.getAttribute('data-id');
      node.querySelectorAll('[id]').forEach(function (el) {
        el.id = 'saved-clone-' + el.id;
      });
      node.querySelectorAll('.btn-copy').forEach(function (btn) {
        var t = btn.getAttribute('data-copy-target');
        if (t) btn.setAttribute('data-copy-target', 'saved-clone-' + t);
      });
      savedGrid.appendChild(node);
      shown += 1;
    });
    if (savedEmpty) savedEmpty.hidden = shown > 0;
    savedGrid.hidden = shown === 0;
    syncSaveButtons(ids);
  }

  function refreshSavedUI() {
    var ids = loadSaved();
    updateSavedCount(ids);
    syncSaveButtons(ids);
    rebuildSavedSection(ids);
  }

  function apply() {
    var term = (q && q.value || '').trim().toLowerCase();
    var ids = loadSaved();
    var shown = 0;
    allCards().forEach(function (card) {
      var inSavedGrid = !!(card.closest && card.closest('#saved-grid'));
      var tags = (card.getAttribute('data-tags') || '').split(/\s+/);
      var text = card.getAttribute('data-text') || '';
      var id = card.getAttribute('data-id') || '';
      var textOk = !term || text.indexOf(term) !== -1;

      // My saved shelf: keep clones visible; topic chips do not hide them
      if (inSavedGrid) {
        if (active === 'saved') {
          card.hidden = !(ids.indexOf(id) !== -1 && textOk);
        } else {
          card.hidden = !textOk; // search can still narrow the shelf
        }
        return;
      }

      var ok;
      if (active === 'saved') {
        ok = false; // originals hidden; shelf shows clones
      } else {
        var tagOk = active === 'all' || tags.indexOf(active) !== -1;
        ok = tagOk && textOk;
      }
      card.hidden = !ok;
      if (ok) shown += 1;
    });
    document.querySelectorAll('main .section').forEach(function (sec) {
      if (sec.id === 'saved') {
        sec.classList.remove('is-empty');
        return;
      }
      if (sec.id === 'archive' && !sec.querySelector('.card')) {
        sec.classList.remove('is-empty');
        return;
      }
      if (active === 'saved') {
        sec.classList.add('is-empty');
        return;
      }
      var any = sec.querySelector('.card:not([hidden])');
      sec.classList.toggle('is-empty', !any);
    });
    if (empty) {
      if (active === 'saved') {
        var anySaved = document.querySelector('#saved-grid .card:not([hidden])');
        empty.classList.toggle('show', !anySaved && loadSaved().length > 0 && !!term);
        if (loadSaved().length === 0) empty.classList.remove('show');
      } else {
        empty.classList.toggle('show', shown === 0);
      }
    }
  }

  if (q) q.addEventListener('input', apply);
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      active = chip.getAttribute('data-filter') || 'all';
      chips.forEach(function (c) {
        c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
      });
      apply();
      if (active === 'saved') {
        var savedSec = document.getElementById('saved');
        if (savedSec) savedSec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  document.addEventListener('click', function (e) {
    var saveBtn = e.target.closest('.btn-save');
    if (saveBtn) {
      var id = saveBtn.getAttribute('data-save-id');
      if (!id) return;
      var ids = loadSaved();
      var idx = ids.indexOf(id);
      if (idx === -1) ids.push(id); else ids.splice(idx, 1);
      storeSaved(ids);
      refreshSavedUI();
      apply();
      return;
    }
    var shareBtn = e.target.closest('.btn-share');
    if (shareBtn) {
      var sid = shareBtn.getAttribute('data-share-id');
      if (!sid) return;
      var url = window.location.origin + window.location.pathname + window.location.search + '#item-' + encodeURIComponent(sid);
      var titleEl = document.querySelector('#item-' + sid.replace(/"/g, '') + ' h3');
      var title = titleEl ? titleEl.textContent.trim() : 'AI leadership resource';
      function copied() {
        var prev = shareBtn.textContent;
        shareBtn.textContent = 'Link copied';
        setTimeout(function () { shareBtn.textContent = prev; }, 1400);
      }
      if (navigator.share) {
        navigator.share({ title: title, url: url }).catch(function () {
          if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(copied);
          }
        });
      } else if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(copied);
      } else {
        var ta = document.createElement('textarea');
        ta.value = url; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); copied(); } catch (err) {}
        document.body.removeChild(ta);
      }
      return;
    }
  });

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.btn-copy');
    if (!btn) return;
    var id = btn.getAttribute('data-copy-target');
    var el = id && document.getElementById(id);
    if (!el) return;
    var text = el.textContent || '';
    function done() {
      var fb = btn.parentElement.querySelector('.copy-feedback');
      if (fb) {
        fb.hidden = false;
        setTimeout(function () { fb.hidden = true; }, 1400);
      }
      btn.textContent = 'Copied';
      setTimeout(function () { btn.textContent = 'Copy'; }, 1400);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done).catch(function () {
        var ta = document.createElement('textarea');
        ta.value = text; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (err) {}
        document.body.removeChild(ta); done();
      });
    } else {
      var ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (err) {}
      document.body.removeChild(ta); done();
    }
  });

  document.addEventListener('click', function (e) {
    var poster = e.target.closest('.video-poster');
    if (!poster) return;
    var wrap = poster.closest('.video-lazy');
    if (!wrap) return;
    var id = wrap.getAttribute('data-youtube-id');
    if (!id) return;
    var iframe = document.createElement('iframe');
    iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0';
    iframe.title = 'YouTube video';
    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
    iframe.allowFullscreen = true;
    iframe.loading = 'lazy';
    wrap.innerHTML = '';
    wrap.appendChild(iframe);
  });

  function highlightDeepLink() {
    var hash = window.location.hash || '';
    if (hash.indexOf('#item-') !== 0) return;
    var id = decodeURIComponent(hash.slice(6));
    var el = document.getElementById('item-' + id);
    if (!el) return;
    el.classList.add('is-deep-link');
    el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    setTimeout(function () { el.classList.remove('is-deep-link'); }, 3200);
  }

  refreshSavedUI();
  apply();
  highlightDeepLink();
  window.addEventListener('hashchange', highlightDeepLink);

  document.documentElement.classList.add('js');
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var revealEls = document.querySelectorAll('.reveal');
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0, rootMargin: '0px 0px -5% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    } else {
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    }
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }

})();
"""


def archive_section_html(items: list) -> str:
    """Collapsed Archive section, grouped by archived month."""
    from collections import defaultdict

    groups: dict[str, list] = defaultdict(list)
    for item in items or []:
        ad = str(item.get("archived_date") or item.get("date") or "Unknown")
        # Prefer YYYY-MM
        month = ad[:7] if len(ad) >= 7 and ad[4:5] == "-" else ad
        groups[month].append(item)

    if not groups:
        body = """
  <p class="archive-empty">Older picks land here when the daily refresh rotates them out of This week or trims a list. Nothing has been archived yet.</p>"""
        count_label = "0"
    else:
        parts = []
        for month in sorted(groups.keys(), reverse=True):
            cards = "".join(
                card_link({**item, "tags": list(dict.fromkeys((item.get("tags") or []) + ["archive"]))},
                          item.get("archived_from") or "week")
                for item in groups[month]
            )
            parts.append(f"""
  <div class="archive-month">
    <h3>{esc(month)}</h3>
    <div class="grid">{cards}</div>
  </div>""")
        body = "".join(parts)
        count_label = str(sum(len(v) for v in groups.values()))

    return f"""
<section class="section reveal tone-week" id="archive" data-section="archive">
  <details class="archive-details">
    <summary class="section-head archive-summary">
      {icon_tile('archive')}
      <div>
        <h2>Archive <span class="count-badge" id="archive-count">{esc(count_label)}</span></h2>
        <p>Rotated-out reads, kept for later. Dead links are removed, not archived.</p>
      </div>
    </summary>
    {body}
  </details>
</section>"""



def healthcare_section_html(items: list) -> str:
    """Healthcare & pharma with Regulatory vs Pharma commercial subgroups."""
    regulatory = [i for i in items if i.get("subgroup") == "regulatory" or (
        "healthcare-regulatory" in (i.get("tags") or []) and i.get("subgroup") != "commercial"
    )]
    commercial = [i for i in items if i.get("subgroup") == "commercial" or "pharma-commercial" in (i.get("tags") or [])]
    # de-dupe if an item matched both lists: prefer commercial listing for dual-tagged OPDP etc.
    reg_urls = {i["url"] for i in commercial}
    regulatory = [i for i in regulatory if i["url"] not in reg_urls]
    # keep stable order from JSON
    def cards(group):
        return "".join(card_link(i, "healthcare") for i in group)

    body = f"""
  <div class="subgroup" id="healthcare-regulatory">
    <h3>Regulatory &amp; clinical</h3>
    <p>FDA/EMA/WHO guidance, ethics, and clinical AI leadership—governance before pilots.</p>
    <div class="grid">{cards(regulatory)}</div>
  </div>
  <div class="subgroup" id="pharma-commercial">
    <h3>Pharma commercial: sales, marketing, market access</h3>
    <p>Using AI inside pharma companies—field/HCP engagement, content + MLR, HEOR/access, medical affairs, and commercial ops—with compliance and measurement in mind.</p>
    <div class="grid">{cards(commercial)}</div>
  </div>"""
    return f"""
<section class="section reveal tone-healthcare" id="healthcare" data-section="healthcare">
  <header class="section-head">
    {icon_tile('healthcare')}
    <div>
      <h2>Healthcare &amp; pharma</h2>
      <p>AI for health systems and life-sciences companies—regulatory context plus commercial functions. No employer-specific content; no patient data.</p>
    </div>
  </header>
  {body}
</section>"""



def build() -> Path:
    m = DATA["meta"]
    week = "".join(card_link(i, "week") for i in DATA["this_week"])
    workflows = "".join(card_link(i, "workflows") for i in DATA["workflows"])
    prompts = "".join(card_prompt(i) for i in DATA["prompts"])
    leadership = "".join(card_link(i, "leadership") for i in DATA["leadership"])
    smb = "".join(card_link(i, "smb") for i in DATA["smb"])
    videos = "".join(card_video(i) for i in DATA["videos"])
    people = "".join(card_person(i) for i in DATA["people"])
    healthcare = healthcare_section_html(DATA.get("healthcare", []))
    archive = archive_section_html(DATA.get("archive", []))

    n_prompts = len(DATA.get("prompts", []))
    n_videos = len(DATA.get("videos", []))
    n_resources = (
        len(DATA.get("this_week", []))
        + len(DATA.get("workflows", []))
        + n_prompts
        + len(DATA.get("leadership", []))
        + len(DATA.get("smb", []))
        + len(DATA.get("healthcare", []))
        + n_videos
        + len(DATA.get("people", []))
    )

    network_svg = """
<svg class="network" viewBox="0 0 320 220" aria-hidden="true">
  <g fill="none" stroke="#60a5fa" stroke-width="1.25" opacity="0.95">
    <path d="M30 170 C90 40, 150 190, 250 55"/>
    <path d="M50 35 C110 100, 180 25, 300 130"/>
    <path d="M15 95 C100 140, 190 80, 290 180"/>
    <path d="M80 200 C140 120, 200 160, 280 90"/>
  </g>
  <g fill="#93c5fd">
    <circle cx="50" cy="35" r="4"/><circle cx="100" cy="105" r="3"/><circle cx="180" cy="50" r="4"/>
    <circle cx="250" cy="55" r="3.5"/><circle cx="290" cy="180" r="4"/><circle cx="30" cy="170" r="3"/>
    <circle cx="140" cy="150" r="3"/><circle cx="280" cy="90" r="3.5"/><circle cx="200" cy="120" r="2.5"/>
  </g>
</svg>"""

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(m['title'])} — AI leadership resources</title>
<meta name="description" content="{esc(m['intro'])}">
<meta name="theme-color" content="#0b1f3a">
<link rel="canonical" href="https://bbenson6klub.github.io/AI-leadership-resources/">
<style>
{CSS}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hero">
  <div class="hero-mesh" aria-hidden="true"></div>
  <div class="hero-glow" aria-hidden="true"></div>
  {network_svg}
  <div class="hero-inner">
    <h1>{esc(m['title'])}</h1>
    <p class="tagline">{esc(m['tagline'])}</p>
    <p class="intro">{esc(m['intro'])}</p>
    <p class="meta-line">Updated {esc(m['last_updated'])} · Updated daily</p>
    <div class="stat-pills" aria-label="Library snapshot">
      <span class="stat-pill"><strong>{n_resources}</strong> resources</span>
      <span class="stat-pill"><strong>{n_prompts}</strong> prompts</span>
      <span class="stat-pill"><strong>{n_videos}</strong> videos</span>
    </div>
  </div>
</header>

<div class="sticky-bar">
  <div class="sticky-inner">
    <nav class="nav-scroll" aria-label="Sections">
      <a href="#start-here">Start here</a>
      <a href="#this-week">This week</a>
      <a href="#workflows">Workflows</a>
      <a href="#prompts">Prompts</a>
      <a href="#leadership">Leadership</a>
      <a href="#smb">Small business</a>
      <a href="#healthcare">Healthcare &amp; pharma</a>
      <a href="#videos">Videos</a>
      <a href="#people">People</a>
      <a href="#saved">Saved <span class="count-badge" data-saved-count>0</span></a>
      <a href="#archive">Archive</a>
    </nav>
    <div class="controls">
      <label for="q" class="visually-hidden" style="position:absolute;left:-9999px;">Search resources</label>
      <input id="q" type="search" placeholder="Search titles, sources, prompts…" autocomplete="off" enterkeyhint="search">
      <div class="chips" role="group" aria-label="Filter by topic">
        <button type="button" class="chip" data-filter="all" aria-pressed="true">All</button>
        <button type="button" class="chip" data-filter="workflows" aria-pressed="false">Workflows</button>
        <button type="button" class="chip" data-filter="prompts" aria-pressed="false">Prompts</button>
        <button type="button" class="chip" data-filter="leadership" aria-pressed="false">Leadership</button>
        <button type="button" class="chip" data-filter="smb" aria-pressed="false">Small business</button>
        <button type="button" class="chip" data-filter="healthcare" aria-pressed="false">Healthcare &amp; pharma</button>
        <button type="button" class="chip" data-filter="pharma-commercial" aria-pressed="false">Pharma commercial</button>
        <button type="button" class="chip" data-filter="healthcare-regulatory" aria-pressed="false">Regulatory &amp; clinical</button>
        <button type="button" class="chip" data-filter="videos" aria-pressed="false">Videos</button>
        <button type="button" class="chip" data-filter="people" aria-pressed="false">People</button>
        <button type="button" class="chip" data-filter="saved" aria-pressed="false">Saved</button>
        <button type="button" class="chip" data-filter="managers" aria-pressed="false">Managers</button>
        <button type="button" class="chip" data-filter="aspiring" aria-pressed="false">Aspiring leaders</button>
      </div>
    </div>
  </div>
</div>

<main id="main" class="wrap">
  <section class="start reveal" id="start-here">
    <h2>Start here</h2>
    <p>You do not need a stack of tools. Pick one recurring piece of work, keep a human in the loop, and track whether quality improved.</p>
    <div class="steps" role="list" aria-label="Three steps: pick one workflow, add a human checkpoint, measure">
      <div class="step" role="listitem"><span class="num">1</span><strong>Pick one workflow</strong><span>status, 1:1s, or inbox</span></div>
      <div class="step-arrow" aria-hidden="true">→</div>
      <div class="step" role="listitem"><span class="num">2</span><strong>Add a human check</strong><span>approve before send</span></div>
      <div class="step-arrow" aria-hidden="true">→</div>
      <div class="step" role="listitem"><span class="num">3</span><strong>Measure</strong><span>time saved + quality</span></div>
    </div>
  </section>

  <div id="no-results" class="empty" role="status">No resources match that search or filter. Clear search or choose All.</div>

  {section_block('this-week', 'New this week', 'Fresh reads worth a short bookmark.', week, 'week')}
  {section_block('workflows', 'Workflows', 'Practical ways to use AI on real recurring work.', workflows, 'workflows')}
  {section_block('prompts', 'Prompts', 'Copy these, swap in your notes, then edit the draft yourself.', prompts, 'prompts')}
  {section_block('leadership', 'Leadership', 'Judgment, feedback, and rethinking—skills AI does not replace.', leadership, 'leadership')}
  {section_block('smb', 'Small business', 'Automation ideas for owners who wear many hats.', smb, 'smb')}
  {healthcare}
  {section_block('videos', 'Videos', 'Click a thumbnail to play (loads YouTube privacy-enhanced embed).', videos, 'videos')}
  {section_block('people', 'People to follow', 'Accounts that stay useful on AI at work and leadership.', people, 'people')}

  <section class="section reveal tone-saved" id="saved" data-section="saved">
    <header class="section-head">
      <span class="icon-tile tone-saved" aria-hidden="true"><svg class="ico" viewBox="0 0 24 24"><path fill="currentColor" d="M6 2h12a1 1 0 0 1 1 1v19l-7-4-7 4V3a1 1 0 0 1 1-1z"/></svg></span>
      <div>
        <h2>My saved <span class="count-badge" data-saved-count>0</span></h2>
        <p>Bookmarks stay on this device only—no account, no trackers.</p>
      </div>
    </header>
    <p id="saved-empty" class="saved-empty">Tap Save on anything to keep it here. Saved on this device only.</p>
    <div id="saved-grid" class="grid" hidden></div>
  </section>

  {archive}
</main>

<footer>
  <p>Practical AI and clearer leadership, no hype. Updated daily.</p>
</footer>
<noscript><p class="note">JavaScript is off: you can still read every resource. Search, filters, copy buttons, and click-to-play videos need JS.</p></noscript>
<script>
{JS}
</script>
</body>
</html>
"""
    out = ROOT / "index.html"
    out.write_text(page, encoding="utf-8")
    return out


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")
