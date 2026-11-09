#!/usr/bin/env python3
"""Build index.html from resources.json. Daily refresh: edit JSON, run this script."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "resources.json"
OUT = ROOT / "index.html"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def resource_card(item: dict) -> str:
    title = esc(item["title"])
    url = esc(item["url"])
    source = esc(item.get("source", ""))
    date = esc(item.get("date", ""))
    why = esc(item.get("why", ""))
    meta = " · ".join(x for x in (source, date) if x)
    return f"""
        <article class="card">
          <h3><a href="{url}" rel="noopener noreferrer" target="_blank">{title}</a></h3>
          <p class="meta">{meta}</p>
          <p class="why">{why}</p>
        </article>"""


def prompt_card(item: dict) -> str:
    title = esc(item["title"])
    why = esc(item.get("why", ""))
    prompt = esc(item["prompt"])
    pid = esc(item.get("id", title))
    return f"""
        <article class="card prompt" id="{pid}">
          <h3>{title}</h3>
          <p class="why">{why}</p>
          <p class="label">Copy this prompt</p>
          <pre class="prompt-text">{prompt}</pre>
        </article>"""


def person_card(item: dict) -> str:
    name = esc(item["name"])
    handle = esc(item["handle"])
    url = esc(item["url"])
    why = esc(item.get("why", ""))
    return f"""
        <article class="card person">
          <h3><a href="{url}" rel="noopener noreferrer" target="_blank">{name}</a></h3>
          <p class="meta">{handle}</p>
          <p class="why">{why}</p>
        </article>"""


def section(heading: str, sid: str, body: str, lead: str = "") -> str:
    lead_html = f'<p class="section-lead">{esc(lead)}</p>' if lead else ""
    return f"""
      <section id="{esc(sid)}" class="section">
        <h2>{esc(heading)}</h2>
        {lead_html}
        <div class="grid">
          {body}
        </div>
      </section>"""


def build(data: dict) -> str:
    meta = data["meta"]
    last = esc(meta["last_updated"])
    title = esc(meta["title"])
    tagline = esc(meta.get("tagline", ""))
    intro = esc(meta.get("intro", ""))
    bio = esc(meta.get("bio", ""))
    x_url = esc(meta.get("x_profile", "https://x.com/BBenson6"))

    this_week = "".join(resource_card(i) for i in data.get("this_week", []))
    workflows = "".join(resource_card(i) for i in data.get("workflows", []))
    prompts = "".join(prompt_card(i) for i in data.get("prompts", []))
    leadership = "".join(resource_card(i) for i in data.get("leadership", []))
    smb = "".join(resource_card(i) for i in data.get("smb", []))
    people = "".join(person_card(i) for i in data.get("people", []))

    nav = """
      <nav class="nav" aria-label="Sections">
        <a href="#this-week">This week</a>
        <a href="#workflows">Workflows</a>
        <a href="#prompts">Prompts</a>
        <a href="#leadership">Leadership</a>
        <a href="#smb">Small business</a>
        <a href="#people">People</a>
      </nav>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Resources</title>
  <meta name="description" content="{intro}" />
  <meta name="author" content="Brian Benson" />
  <style>
    :root {{
      --navy: #0b1f3a;
      --navy-2: #122a4a;
      --navy-3: #1a3658;
      --blue: #6eb6ff;
      --blue-soft: #9ec9f5;
      --muted: #a8b8cc;
      --paper: #f5f8fc;
      --card: #ffffff;
      --ink: #122033;
      --line: #d7e2ef;
      --radius: 14px;
      --shadow: 0 8px 24px rgba(11, 31, 58, 0.08);
      --max: 920px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.55;
    }}
    a {{ color: #1a5fb4; text-decoration-thickness: 1px; text-underline-offset: 2px; }}
    a:hover {{ color: #0d3f7a; }}
    .hero {{
      background: linear-gradient(105deg, #081528 0%, var(--navy) 45%, #163a63 100%);
      color: #fff;
      padding: 2.4rem 1.25rem 2rem;
      border-bottom: 1px solid rgba(110, 182, 255, 0.25);
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      right: -40px;
      top: -20px;
      width: 280px;
      height: 220px;
      background:
        radial-gradient(circle at 30% 40%, rgba(110,182,255,0.45) 0 3px, transparent 4px),
        radial-gradient(circle at 55% 25%, rgba(158,201,245,0.35) 0 2px, transparent 3px),
        radial-gradient(circle at 70% 60%, rgba(110,182,255,0.4) 0 2.5px, transparent 3.5px),
        radial-gradient(circle at 40% 75%, rgba(158,201,245,0.3) 0 2px, transparent 3px);
      opacity: 0.9;
      pointer-events: none;
    }}
    .hero-inner {{ max-width: var(--max); margin: 0 auto; position: relative; z-index: 1; }}
    .hero h1 {{
      margin: 0 0 0.35rem;
      font-size: clamp(1.6rem, 4vw, 2.2rem);
      letter-spacing: -0.02em;
      font-weight: 700;
    }}
    .hero .tagline {{
      margin: 0 0 1rem;
      color: var(--blue-soft);
      font-size: 1.05rem;
    }}
    .hero .intro {{
      margin: 0;
      max-width: 40rem;
      color: #d9e6f5;
      font-size: 0.98rem;
    }}
    .meta-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem 1.25rem;
      align-items: center;
      margin-top: 1.25rem;
      font-size: 0.9rem;
      color: var(--muted);
    }}
    .badge {{
      display: inline-block;
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
      border: 1px solid rgba(110,182,255,0.35);
      color: var(--blue);
      background: rgba(110,182,255,0.08);
    }}
    .wrap {{ max-width: var(--max); margin: 0 auto; padding: 1.25rem; }}
    .nav {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin: 0.25rem 0 1.5rem;
    }}
    .nav a {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 999px;
      padding: 0.4rem 0.8rem;
      color: var(--navy);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
    }}
    .nav a:hover {{ border-color: var(--blue); color: #0d3f7a; }}
    .section {{ margin: 0 0 2rem; }}
    .section h2 {{
      margin: 0 0 0.4rem;
      font-size: 1.35rem;
      color: var(--navy);
      letter-spacing: -0.01em;
    }}
    .section-lead {{
      margin: 0 0 1rem;
      color: #4a5d73;
      font-size: 0.96rem;
    }}
    .grid {{
      display: grid;
      gap: 0.9rem;
    }}
    .card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 1rem 1.1rem;
      box-shadow: var(--shadow);
    }}
    .card h3 {{
      margin: 0 0 0.35rem;
      font-size: 1.05rem;
      line-height: 1.35;
    }}
    .card h3 a {{ color: var(--navy); text-decoration: none; }}
    .card h3 a:hover {{ color: #1a5fb4; text-decoration: underline; }}
    .meta {{
      margin: 0 0 0.55rem;
      color: #5b6f86;
      font-size: 0.84rem;
    }}
    .why {{ margin: 0; color: #2b3c50; font-size: 0.95rem; }}
    .label {{
      margin: 0.85rem 0 0.35rem;
      font-size: 0.78rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: #5b6f86;
      font-weight: 700;
    }}
    .prompt-text {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      background: #0b1f3a;
      color: #e8f1fb;
      border-radius: 10px;
      padding: 0.9rem 1rem;
      font-size: 0.86rem;
      line-height: 1.45;
      overflow-x: auto;
    }}
    .bio-box {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 1rem 1.1rem;
      margin-bottom: 1.25rem;
      box-shadow: var(--shadow);
    }}
    .bio-box strong {{ color: var(--navy); }}
    footer {{
      background: var(--navy);
      color: #c9d7e8;
      padding: 1.5rem 1.25rem 2rem;
      margin-top: 1rem;
    }}
    footer .inner {{ max-width: var(--max); margin: 0 auto; font-size: 0.92rem; }}
    footer a {{ color: var(--blue); }}
    footer p {{ margin: 0.35rem 0; }}
    @media (min-width: 720px) {{
      .grid {{ grid-template-columns: 1fr 1fr; }}
      .prompt {{ grid-column: 1 / -1; }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <h1>{title}</h1>
      <p class="tagline">{tagline}</p>
      <p class="intro">{intro}</p>
      <div class="meta-bar">
        <span class="badge">Last updated {last}</span>
        <span>For managers, aspiring leaders, and small-business owners</span>
      </div>
    </div>
  </header>

  <main class="wrap">
    {nav}
    <div class="bio-box">
      <strong>About this page.</strong> Built to sit behind the X bio for <a href="{x_url}" rel="noopener noreferrer" target="_blank">@BBenson6</a>:
      “{bio}” Links are free to open. Prompts below are original drafts for Brian’s readers—edit them to fit your team’s tools and policies.
    </div>

    {section("This week's picks", "this-week", this_week, "Recent, high-signal reads and tools. Older picks move into the categories below.")}
    {section("AI workflows & tools for managers", "workflows", workflows, "Repeatable ways to use AI without giving up ownership of the outcome.")}
    {section("Prompts & templates", "prompts", prompts, "Original prompts from Brian. Replace the placeholders, then review every output before you send or decide.")}
    {section("Leadership & career growth", "leadership", leadership, "Judgment, rethinking, and how work is changing as agents arrive.")}
    {section("Small-business automation", "smb", smb, "Start with one process. Document it, then automate the boring handoffs.")}
    {section("People worth following", "people", people, "Verified public X profiles (people, not company accounts). Follow in the X app.")}
  </main>

  <footer>
    <div class="inner">
      <p><strong>Practical AI. Better Leadership.</strong> — curated by Brian Benson.</p>
      <p>Follow on X: <a href="{x_url}" rel="noopener noreferrer" target="_blank">https://x.com/BBenson6</a></p>
      <p>Last updated {last}. No affiliate links. No income guarantees. Use your organization’s policies for data and AI tools.</p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    OUT.write_text(build(data), encoding="utf-8")
    n = (
        len(data.get("this_week", []))
        + len(data.get("workflows", []))
        + len(data.get("prompts", []))
        + len(data.get("leadership", []))
        + len(data.get("smb", []))
        + len(data.get("people", []))
    )
    print(f"Wrote {OUT} ({n} items across sections)")


if __name__ == "__main__":
    main()
