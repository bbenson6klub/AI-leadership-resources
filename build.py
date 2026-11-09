#!/usr/bin/env python3
"""Build a static, progressive-enhancement index.html from resources.json."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "resources.json").read_text(encoding="utf-8"))


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def tag_attrs(tags: list) -> str:
    return " ".join(esc(t) for t in (tags or []))


ICON_SVGS = {
    "workflows": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 6h4v2H4V6zm6 0h10v2H10V6zM4 11h4v2H4v-2zm6 0h10v2H10v-2zM4 16h4v2H4v-2zm6 0h10v2H10v-2z"/><circle cx="6" cy="7" r="1.2" fill="#3b82f6"/><circle cx="6" cy="12" r="1.2" fill="#3b82f6"/><circle cx="6" cy="17" r="1.2" fill="#3b82f6"/></svg>""",
    "prompts": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M4 4h16a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H9l-4 3v-3H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm2 4v2h12V8H6zm0 4v2h8v-2H6z"/></svg>""",
    "leadership": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2l2.2 4.5 5 .7-3.6 3.5.9 5.1L12 13.8 7.5 15.8l.9-5.1L4.8 7.2l5-.7L12 2z"/><path fill="#3b82f6" d="M12 2l1.1 2.2-1.1.3-1.1-.3L12 2z"/></svg>""",
    "smb": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3 20V9l9-5 9 5v11h-6v-6H9v6H3zm2-2h2v-4h10v4h2v-8.2L12 6.1 5 9.8V18z"/></svg>""",
    "videos": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="1.6"/><path fill="#3b82f6" d="M10 9.2v5.6L15 12l-5-2.8z"/></svg>""",
    "people": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="8" r="3" fill="currentColor"/><circle cx="16" cy="9" r="2.4" fill="#3b82f6"/><path fill="currentColor" d="M3 19c0-3 3-5 6-5s6 2 6 5v1H3v-1z"/><path fill="#3b82f6" d="M14 19c0-1.8 1.4-3.2 3.2-3.6.5-.1 1-.2 1.5-.2 1.8 0 3.3 1.2 3.3 3v1h-8v-1z"/></svg>""",
    "healthcare": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M11 3h2v6h6v2h-6v6h-2v-6H5V9h6V3z"/><circle cx="12" cy="12" r="9" fill="none" stroke="#3b82f6" stroke-width="1.5"/></svg>""",
    "week": """<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 2h2v2h6V2h2v2h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3V2zm13 8H4v10h16V10zM8 13h3v3H8v-3z"/></svg>""",
}


def card_link(item: dict, section: str) -> str:
    tags = item.get("tags") or [section]
    new_badge = '<span class="badge-new">New this week</span>' if item.get("new") else ""
    title = esc(item["title"])
    url = esc(item["url"])
    source = esc(item.get("source", ""))
    date = esc(item.get("date", ""))
    why = esc(item.get("why", ""))
    meta = " · ".join(x for x in [source, date] if x)
    return f"""
<article class="card" data-tags="{tag_attrs(tags)}" data-text="{esc((item['title'] + ' ' + item.get('source','') + ' ' + item.get('why','')).lower())}">
  <div class="card-head">
    {ICON_SVGS.get(section, ICON_SVGS['workflows'])}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{title}</a></h3>
      <p class="meta">{meta}</p>
    </div>
    {new_badge}
  </div>
  <p class="why">{why}</p>
</article>"""


def card_prompt(item: dict) -> str:
    tags = item.get("tags") or ["prompts"]
    pid = esc(item.get("id", "prompt"))
    title = esc(item["title"])
    why = esc(item.get("why", ""))
    prompt = item.get("prompt", "")
    return f"""
<article class="card prompt-card" data-tags="{tag_attrs(tags)}" data-text="{esc((item['title'] + ' ' + item.get('why','') + ' ' + prompt).lower())}" id="{pid}">
  <div class="card-head">
    {ICON_SVGS['prompts']}
    <div>
      <h3>{title}</h3>
      <p class="meta">Copy-ready prompt</p>
    </div>
  </div>
  <p class="why">{why}</p>
  <pre class="prompt-body" id="{pid}-text">{esc(prompt)}</pre>
  <button type="button" class="btn-copy" data-copy-target="{pid}-text" aria-label="Copy prompt: {title}">
    Copy
  </button>
  <span class="copy-feedback" hidden aria-live="polite">Copied</span>
</article>"""


def card_person(item: dict) -> str:
    tags = item.get("tags") or ["people"]
    name = esc(item["name"])
    handle = esc(item.get("handle", ""))
    url = esc(item["url"])
    why = esc(item.get("why", ""))
    return f"""
<article class="card person-card" data-tags="{tag_attrs(tags)}" data-text="{esc((item['name'] + ' ' + item.get('handle','') + ' ' + item.get('why','')).lower())}">
  <div class="card-head">
    {ICON_SVGS['people']}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{name}</a></h3>
      <p class="meta">{handle}</p>
    </div>
  </div>
  <p class="why">{why}</p>
</article>"""


def card_video(item: dict) -> str:
    tags = item.get("tags") or ["videos"]
    vid = esc(item["youtube_id"])
    title = esc(item["title"])
    url = esc(item["url"])
    channel = esc(item.get("channel", ""))
    date = esc(item.get("date", ""))
    why = esc(item.get("why", ""))
    thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    meta = " · ".join(x for x in [channel, date] if x)
    return f"""
<article class="card video-card" data-tags="{tag_attrs(tags)}" data-text="{esc((item['title'] + ' ' + item.get('channel','') + ' ' + item.get('why','')).lower())}">
  <div class="video-lazy" data-youtube-id="{vid}">
    <button type="button" class="video-poster" aria-label="Play video: {title}">
      <img src="{thumb}" alt="" width="480" height="360" loading="lazy" decoding="async">
      <span class="play-btn" aria-hidden="true"></span>
    </button>
  </div>
  <div class="card-head">
    {ICON_SVGS['videos']}
    <div>
      <h3><a href="{url}" rel="noopener noreferrer">{title}</a></h3>
      <p class="meta">{meta}</p>
    </div>
  </div>
  <p class="why">{why}</p>
</article>"""


def section_block(sid: str, heading: str, intro: str, cards_html: str, icon_key: str) -> str:
    return f"""
<section class="section" id="{sid}" data-section="{sid}">
  <header class="section-head">
    {ICON_SVGS.get(icon_key, '')}
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
  --blue: #3b82f6;
  --blue-soft: #60a5fa;
  --ink: #0f172a;
  --muted: #475569;
  --line: #dbe3f0;
  --bg: #f4f7fb;
  --card: #ffffff;
  --ok: #059669;
  --radius: 14px;
  --shadow: 0 8px 24px rgba(11, 31, 58, 0.08);
  --max: 1100px;
  --focus: 0 0 0 3px rgba(59, 130, 246, 0.45);
}
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  color: var(--ink);
  background: var(--bg);
  line-height: 1.55;
}
a { color: var(--blue); }
a:hover { color: #2563eb; }
img { max-width: 100%; height: auto; display: block; }
.skip {
  position: absolute; left: -999px; top: 0;
  background: var(--navy); color: #fff; padding: .6rem 1rem; z-index: 100;
}
.skip:focus { left: 0; }
.hero {
  background: linear-gradient(160deg, var(--navy) 0%, var(--navy-2) 55%, #163a66 100%);
  color: #fff;
  position: relative;
  overflow: hidden;
}
.hero-inner {
  max-width: var(--max);
  margin: 0 auto;
  padding: 2.25rem 1.25rem 2.35rem;
  position: relative;
  z-index: 1;
}
.network {
  position: absolute;
  right: -40px;
  top: 55%;
  transform: translateY(-50%);
  width: min(40vw, 300px);
  height: 210px;
  opacity: 0.32;
  pointer-events: none;
  z-index: 0;
}
.hero-inner { text-shadow: none; }
.hero h1, .hero .tagline { text-shadow: none; -webkit-font-smoothing: antialiased; }
.hero h1 {
  margin: 0 0 .4rem;
  font-size: clamp(1.6rem, 4vw, 2.3rem);
  letter-spacing: -0.02em;
}
.hero .tagline { margin: 0 0 1rem; color: var(--blue-soft); font-weight: 600; }
.hero .intro { max-width: 42rem; margin: 0 0 1rem; color: #dbeafe; }
.hero .meta-line { font-size: .9rem; color: #93c5fd; }

.sticky-bar {
  position: sticky; top: 0; z-index: 40;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--line);
}
.sticky-inner {
  max-width: var(--max);
  margin: 0 auto;
  padding: .65rem 1.25rem .75rem;
  display: grid;
  gap: .65rem;
}
.nav-scroll {
  display: flex; gap: .5rem; overflow-x: auto; padding-bottom: .15rem;
  scrollbar-width: thin;
}
.nav-scroll a {
  flex: 0 0 auto;
  text-decoration: none;
  color: var(--navy);
  background: #eef4ff;
  border: 1px solid #cfe0ff;
  border-radius: 999px;
  padding: .35rem .75rem;
  font-size: .85rem;
  font-weight: 600;
}
.nav-scroll a:focus-visible, .chip:focus-visible, .btn-copy:focus-visible, .video-poster:focus-visible, #q:focus-visible {
  outline: none; box-shadow: var(--focus);
}
.controls { display: grid; gap: .55rem; }
#q {
  width: 100%;
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: .7rem .9rem;
  font-size: 1rem;
  background: #fff;
}
.chips { display: flex; flex-wrap: wrap; gap: .4rem; }
.chip {
  border: 1px solid var(--line);
  background: #fff;
  color: var(--navy);
  border-radius: 999px;
  padding: .35rem .7rem;
  font-size: .82rem;
  cursor: pointer;
}
.chip[aria-pressed="true"] {
  background: var(--navy);
  color: #fff;
  border-color: var(--navy);
}
.wrap { max-width: var(--max); margin: 0 auto; padding: 1.25rem; }
.start {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1.1rem 1.2rem 1.25rem;
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
}
.start h2 { margin: 0 0 .35rem; font-size: 1.15rem; color: var(--navy); }
.start p { margin: 0 0 1rem; color: var(--muted); }
.steps {
  display: grid;
  gap: .65rem;
  grid-template-columns: 1fr;
  margin-top: .85rem;
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
  border-radius: 12px;
  padding: .95rem 1rem;
  background: var(--navy);
  color: #fff;
  box-shadow: var(--shadow);
}
.step .num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 1.55rem; height: 1.55rem; border-radius: 999px;
  background: var(--blue); color: #fff; font-weight: 700; font-size: .8rem;
  margin-bottom: .4rem;
}
.step strong { display: block; color: #fff; margin-bottom: .25rem; font-size: .98rem; }
.step span { color: #93c5fd; font-size: .88rem; }
.step-arrow {
  display: none;
  color: var(--blue);
  font-size: 1.4rem;
  font-weight: 700;
  text-align: center;
  line-height: 1;
}
@media (min-width: 720px) {
  .step-arrow { display: block; }
}
.section-head h2 { margin: 0; color: var(--navy); font-size: 1.35rem; }
.section-head p { margin: .2rem 0 0; color: var(--muted); }
.ico { width: 28px; height: 28px; flex: 0 0 auto; color: var(--navy); margin-top: .15rem; }
.grid {
  display: grid;
  gap: .9rem;
  grid-template-columns: 1fr;
}
@media (min-width: 700px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1rem 1.05rem 1.05rem;
  box-shadow: var(--shadow);
}
.card[hidden], .section.is-empty { display: none !important; }
.card-head { display: flex; gap: .65rem; align-items: flex-start; position: relative; }
.card-head h3 { margin: 0; font-size: 1.02rem; line-height: 1.35; }
.card-head h3 a { color: var(--navy); text-decoration: none; }
.card-head h3 a:hover { color: var(--blue); text-decoration: underline; }
.meta { margin: .2rem 0 0; color: var(--muted); font-size: .84rem; }
.why { margin: .7rem 0 0; color: #334155; }
.badge-new {
  position: static;
  margin-left: auto;
  align-self: flex-start;
  background: #dbeafe; color: #1e3a8a;
  border: 1px solid #93c5fd;
  font-size: .72rem; font-weight: 700;
  padding: .15rem .45rem; border-radius: 999px;
  white-space: nowrap;
  flex: 0 0 auto;
}
.card-head > div { flex: 1 1 auto; min-width: 0; }
.prompt-body {
  margin: .75rem 0 .65rem;
  padding: .75rem .8rem;
  background: #0b1f3a;
  color: #e2e8f0;
  border-radius: 10px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: .86rem;
  line-height: 1.45;
  max-height: 220px;
  overflow: auto;
}
.btn-copy {
  border: 0;
  background: var(--blue);
  color: #fff;
  font-weight: 700;
  border-radius: 999px;
  padding: .45rem .9rem;
  cursor: pointer;
}
.btn-copy:hover { background: #2563eb; }
.copy-feedback {
  margin-left: .5rem;
  color: var(--ok);
  font-weight: 700;
  font-size: .9rem;
}
.video-lazy { margin: -.15rem -.15rem .75rem; border-radius: 10px; overflow: hidden; background: #0b1f3a; aspect-ratio: 16/9; }
.video-poster {
  position: relative; display: block; width: 100%; height: 100%;
  border: 0; padding: 0; cursor: pointer; background: #0b1f3a;
}
.video-poster img { width: 100%; height: 100%; object-fit: cover; opacity: .92; }
.play-btn {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%);
  width: 56px; height: 56px; border-radius: 999px;
  background: rgba(11,31,58,.88); border: 2px solid #fff;
  box-shadow: 0 6px 18px rgba(0,0,0,.35);
}
.play-btn::before {
  content: "";
  position: absolute; left: 22px; top: 17px;
  border-style: solid; border-width: 11px 0 11px 18px;
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
  margin: 0 auto 2rem;
  padding: 0 1.25rem;
  color: var(--muted);
  font-size: .9rem;
}
footer a { color: var(--navy); }
noscript .note {
  max-width: var(--max); margin: .75rem auto; padding: 0 1.25rem;
  color: var(--muted); font-size: .9rem;
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
"""

JS = r"""
(function () {
  var q = document.getElementById('q');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var empty = document.getElementById('no-results');
  var active = 'all';

  function apply() {
    var term = (q && q.value || '').trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var tags = (card.getAttribute('data-tags') || '').split(/\s+/);
      var text = card.getAttribute('data-text') || '';
      var tagOk = active === 'all' || tags.indexOf(active) !== -1;
      var textOk = !term || text.indexOf(term) !== -1;
      var ok = tagOk && textOk;
      card.hidden = !ok;
      if (ok) shown += 1;
    });
    document.querySelectorAll('.section').forEach(function (sec) {
      var any = sec.querySelector('.card:not([hidden])');
      sec.classList.toggle('is-empty', !any);
    });
    if (empty) empty.classList.toggle('show', shown === 0);
  }

  if (q) {
    q.addEventListener('input', apply);
  }
  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      active = chip.getAttribute('data-filter') || 'all';
      chips.forEach(function (c) {
        c.setAttribute('aria-pressed', c === chip ? 'true' : 'false');
      });
      apply();
    });
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
})();
"""


def build() -> Path:
    m = DATA["meta"]
    week = "".join(card_link(i, "week") for i in DATA["this_week"])
    workflows = "".join(card_link(i, "workflows") for i in DATA["workflows"])
    prompts = "".join(card_prompt(i) for i in DATA["prompts"])
    leadership = "".join(card_link(i, "leadership") for i in DATA["leadership"])
    smb = "".join(card_link(i, "smb") for i in DATA["smb"])
    videos = "".join(card_video(i) for i in DATA["videos"])
    people = "".join(card_person(i) for i in DATA["people"])
    healthcare = "".join(card_link(i, "healthcare") for i in DATA.get("healthcare", []))


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
  {network_svg}
  <div class="hero-inner">
    <h1>{esc(m['title'])}</h1>
    <p class="tagline">{esc(m['tagline'])}</p>
    <p class="intro">{esc(m['intro'])}</p>
    <p class="meta-line">Updated {esc(m['last_updated'])} ({esc(m.get('timezone_note',''))}) · <a href="{esc(m['x_profile'])}" rel="noopener noreferrer" style="color:#bfdbfe">@BBenson6</a></p>
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
        <button type="button" class="chip" data-filter="videos" aria-pressed="false">Videos</button>
        <button type="button" class="chip" data-filter="people" aria-pressed="false">People</button>
        <button type="button" class="chip" data-filter="managers" aria-pressed="false">Managers</button>
        <button type="button" class="chip" data-filter="aspiring" aria-pressed="false">Aspiring leaders</button>
      </div>
    </div>
  </div>
</div>

<main id="main" class="wrap">
  <section class="start" id="start-here">
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
  {section_block('healthcare', 'Healthcare & pharma', 'Regulatory, ethics, and leadership guidance for AI in health and life sciences—no hype, no patient data here.', healthcare, 'healthcare')}
  {section_block('videos', 'Videos', 'Click a thumbnail to play (loads YouTube privacy-enhanced embed).', videos, 'videos')}
  {section_block('people', 'People to follow', 'Accounts that stay useful on AI at work and leadership.', people, 'people')}
</main>

<footer>
  <p>Built as a static site for GitHub Pages. Content curated for practical AI and clearer leadership—no hype. Source data: <code>resources.json</code>. Rebuild with <code>python3 build.py</code>.</p>
  <p><a href="{esc(m['x_profile'])}" rel="noopener noreferrer">@BBenson6 on X</a></p>
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
