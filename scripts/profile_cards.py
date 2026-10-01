"""Generate the animated SVG panels used in the profile README.

Usage:
    python scripts/profile_cards.py static <out_dir>     # hero, about, stack, connect
    python scripts/profile_cards.py dashboard <out_dir>  # ID card + live GitHub dashboard

The dashboard reads live numbers from the GitHub GraphQL API using the
PROFILE_TOKEN environment variable. If the token is missing or the API call
fails, it falls back to the snapshot values in FALLBACK.
"""

import base64
import datetime as dt
import json
import math
import os
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USER = "MaddipatlaChetan24"
NAME = "Maddipatla Chetan"
ICONS = json.loads((Path(__file__).parent / "icons.json").read_text())

SANS = "'Segoe UI', Inter, system-ui, -apple-system, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

CYAN, BLUE, INDIGO, VIOLET = "#22d3ee", "#3b82f6", "#6366f1", "#a78bfa"
GREEN, AMBER, PINK = "#34d399", "#fbbf24", "#f472b6"
TEXT, MUTED, DIM = "#e6edf3", "#94a3b8", "#64748b"

FALLBACK = {
    "repos": 82,
    "commits": 1032,
    "prs": 112,
    "contributions": 1032,
    "streak": 4,
    "best_streak": 26,
    "since": 2025,
    "languages": [
        ("Jupyter Notebook", 86.8, "#DA5B0B"),
        ("Python", 8.4, "#3572A5"),
        ("HTML", 2.4, "#e34c26"),
        ("TypeScript", 1.0, "#3178c6"),
        ("CSS", 0.5, "#663399"),
    ],
    "avatar": None,
}


# ---------------------------------------------------------------- helpers

def t(s):
    return escape(str(s))


def base_defs(extra_css=""):
    return f"""<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1222"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".7"/><stop offset=".5" stop-color="{BLUE}" stop-opacity=".25"/><stop offset="1" stop-color="{INDIGO}" stop-opacity=".7"/></linearGradient>
<linearGradient id="brand" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#1e293b"/></pattern>
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.5"/></filter>
<style>
text{{font-family:{SANS}}}
.mono{{font-family:{MONO}}}
.tag{{font-family:{MONO};font-size:13px;letter-spacing:2.5px;font-weight:600}}
.h2{{font-size:30px;font-weight:700;fill:{TEXT}}}
.pulse{{animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
{extra_css}
</style>
</defs>"""


def panel(x, y, w, h, r=22):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#bg)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#dots)" opacity=".6"/>'
            f'<rect x="{x+.75}" y="{y+.75}" width="{w-1.5}" height="{h-1.5}" rx="{r}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>')


def svg(w, h, title, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{t(title)}">'
            f'<title>{t(title)}</title>{base_defs(css)}{body}</svg>')


def lum(hexcol):
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def icon(slug, x, y, size, fallback=None, color=None):
    """Brand icon from simple-icons, or a letter monogram if unavailable."""
    if slug in ICONS:
        ic = ICONS[slug]
        col = color or ("#" + ic["hex"] if lum(ic["hex"]) > 0.18 else TEXT)
        s = size / 24
        return f'<path transform="translate({x},{y}) scale({s:.4f})" d="{ic["path"]}" fill="{col}"/>'
    label = fallback or slug[:2].upper()
    return (f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size*.25:.1f}" fill="{color or BLUE}" opacity=".9"/>'
            f'<text x="{x+size/2}" y="{y+size*.7:.1f}" text-anchor="middle" font-size="{size*.5:.1f}" font-weight="800" fill="#0d1117">{t(label)}</text>')


def tag(x, y, label, color):
    return (f'<rect x="{x}" y="{y-9}" width="14" height="3" rx="1.5" fill="{color}"/>'
            f'<text x="{x+24}" y="{y-3}" class="tag" fill="{color}">{t(label)}</text>')


# ---------------------------------------------------------------- hero

def hero():
    W, H = 1280, 540
    roles = ["AI / ML Engineer", "Generative AI Developer", "Multi-Agent Systems Builder",
             "LLM &amp; RAG Engineer"]
    n, per = len(roles), 3.2
    total = n * per
    role_css = "".join(
        f".r{i}{{animation:role {total}s infinite;animation-delay:{i*per}s;opacity:0}}" for i in range(n))
    vis = per / total * 100
    css = f"""
@keyframes role{{0%{{opacity:0;transform:translateY(10px)}}{vis*.12:.2f}%{{opacity:1;transform:translateY(0)}}{vis*.85:.2f}%{{opacity:1;transform:translateY(0)}}{vis:.2f}%{{opacity:0;transform:translateY(-8px)}}100%{{opacity:0}}}}
{role_css}
.caret{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.under{{animation:under 4s ease-in-out infinite alternate}}@keyframes under{{from{{width:90px}}to{{width:220px}}}}
{SCENE_CSS}
.orb{{animation:orb 9s ease-in-out infinite alternate}}@keyframes orb{{to{{transform:translate(40px,30px)}}}}
"""
    body = [panel(0, 0, W, H, 26)]
    body.append(f'<g class="orb"><circle cx="160" cy="120" r="220" fill="{CYAN}" opacity=".07" filter="url(#soft)"/></g>')
    body.append(f'<circle cx="420" cy="470" r="200" fill="{INDIGO}" opacity=".06"/>')
    # status pill
    body.append(f'<rect x="64" y="62" width="218" height="34" rx="17" fill="#0f2a24" stroke="{GREEN}" stroke-opacity=".45"/>'
                f'<circle class="pulse" cx="86" cy="79" r="5.5" fill="{GREEN}"/>'
                f'<text x="102" y="84" class="mono" font-size="13" letter-spacing="2" font-weight="700" fill="{GREEN}">AI · ML · GENAI</text>')
    body.append(f'<text x="64" y="162" font-size="34" fill="{TEXT}" font-weight="500">Hi there, I&#8217;m</text>')
    body.append(f'<text x="62" y="240" font-size="64" font-weight="800" fill="url(#brand)" filter="url(#glow)" letter-spacing="-1">{t(NAME)}</text>')
    body.append(f'<rect class="under" x="64" y="262" width="160" height="4" rx="2" fill="url(#brand)"/>')
    body.append(f'<text x="64" y="322" class="mono" font-size="24" font-weight="700" fill="{CYAN}">&gt;</text>')
    for i, r in enumerate(roles):
        body.append(f'<text class="r{i} mono" x="92" y="322" font-size="24" fill="{TEXT}">{r}</text>')
    body.append(f'<text x="64" y="378" font-size="19" fill="{MUTED}">I build LLM applications, RAG pipelines and multi-agent systems,</text>')
    body.append(f'<text x="64" y="406" font-size="19" fill="{MUTED}">and ship them with FastAPI, Docker and tested code.</text>')
    meta = [(CYAN, "B.Tech CSE (Core)"), (VIOLET, "LLMs · RAG · Multi-agent systems")]
    x = 64
    for col, label in meta:
        body.append(f'<circle cx="{x+7}" cy="447" r="6" fill="none" stroke="{col}" stroke-width="2"/><circle cx="{x+7}" cy="447" r="2" fill="{col}"/>'
                    f'<text x="{x+22}" y="452" class="mono" font-size="14" fill="{MUTED}">{t(label)}</text>')
        x += 32 + len(label) * 8.6
    # right: me at my desk
    body.append(desk_scene(760, 40))
    return svg(W, H, f"Hi, I'm {NAME} — AI Engineer", "".join(body), css)


SKIN, SKIN_SHADE, HAIR = "#f2c9a0", "#d9a77c", "#16161f"
SCENE_CSS = """
.blink{transform-box:fill-box;transform-origin:center;animation:blink 4.5s infinite}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.1)}}
.nod{transform-box:fill-box;transform-origin:50% 100%;animation:nod 3.2s ease-in-out infinite}
@keyframes nod{0%,100%{transform:rotate(0)}50%{transform:rotate(2deg)}}
.type{animation:type .35s ease-in-out infinite alternate}
.type2{animation:type .35s ease-in-out infinite alternate-reverse}
@keyframes type{to{transform:translateY(3px)}}
.steam{stroke-dasharray:30;animation:steam 2.6s linear infinite}
@keyframes steam{0%{stroke-dashoffset:30;opacity:0}30%{opacity:.8}100%{stroke-dashoffset:-30;opacity:0}}
.glow{animation:glow 2.2s ease-in-out infinite alternate}
@keyframes glow{from{opacity:.25}to{opacity:.6}}
.fl{animation:fl 4s ease-in-out infinite alternate}
@keyframes fl{to{transform:translateY(-12px)}}
.code{animation:code 6s linear infinite}
@keyframes code{0%{opacity:0}10%,80%{opacity:1}90%,100%{opacity:0}}
.status{animation:pulse 2s ease-in-out infinite}
"""


def desk_scene(ox, oy):
    """Illustration of me coding at a laptop (476 x 460 area)."""
    g = [f'<g transform="translate({ox},{oy})">']
    # backdrop blob + window
    g.append(f'<path d="M60 120C90 40 210 10 300 40S470 120 450 240 360 410 240 400 30 330 40 230 40 160 60 120z" fill="#111d35"/>')
    g.append(f'<rect x="300" y="52" width="120" height="96" rx="10" fill="#0b1528" stroke="#1e3a5f"/>'
             f'<path d="M360 52v96M300 100h120" stroke="#1e3a5f"/>'
             f'<circle cx="390" cy="78" r="9" fill="#e2e8f0" opacity=".8"/>')
    for i in range(5):
        g.append(f'<circle class="pulse" style="animation-delay:{i*.4:.1f}s" cx="{312+i*22}" cy="{122+(i%2)*12}" r="1.4" fill="#e2e8f0"/>')
    # floating code card
    g.append(f'<g class="fl"><rect x="34" y="70" width="150" height="92" rx="10" fill="#0d1117" stroke="{CYAN}" stroke-opacity=".5"/>'
             f'<circle cx="48" cy="84" r="3.5" fill="#ff5f57"/><circle cx="60" cy="84" r="3.5" fill="#febc2e"/><circle cx="72" cy="84" r="3.5" fill="#28c840"/>')
    code = [(CYAN, 58), (VIOLET, 96), (GREEN, 74), (PINK, 104), (AMBER, 64)]
    for i, (col, w) in enumerate(code):
        g.append(f'<rect class="code" style="animation-delay:{i*.5:.1f}s" x="{48+(i%2)*12}" y="{98+i*12}" width="{w}" height="5" rx="2.5" fill="{col}" opacity=".85"/>')
    g.append('</g>')
    # floating tags
    for i, (lbl, x, y, col) in enumerate([("LLM", 60, 212, VIOLET), ("RAG", 392, 186, CYAN), ("&lt;/&gt;", 104, 244, PINK), ("agents", 356, 236, GREEN)]):
        w = 18 + len(lbl.replace("&lt;", "<").replace("&gt;", ">")) * 9
        g.append(f'<g class="fl" style="animation-delay:{i*.7:.1f}s"><rect x="{x}" y="{y}" width="{w}" height="26" rx="13" fill="#0d1117" stroke="{col}"/>'
                 f'<text x="{x+w/2}" y="{y+17.5}" text-anchor="middle" class="mono" font-size="12.5" font-weight="700" fill="{col}">{lbl}</text></g>')
    # plant
    g.append(f'<path d="M66 352c-20-30-30-60-6-78 4 24 12 46 10 78z" fill="#15803d"/>'
             f'<path d="M74 352c4-34 22-58 44-62-10 22-22 44-34 62z" fill="#22c55e"/>'
             f'<path d="M70 352c-6-24-2-48 10-66 6 24 2 46-4 66z" fill="#16a34a"/>'
             f'<path d="M50 350h48l-6 34H56z" fill="#f472b6" opacity=".85"/>')
    # lamp
    g.append(f'<path d="M412 384v-6M412 378l-30-92 -40 22" stroke="#64748b" stroke-width="4" fill="none" stroke-linecap="round"/>'
             f'<path d="M318 300l36-26 14 20-36 24z" fill="{AMBER}"/>'
             f'<ellipse cx="412" cy="386" rx="22" ry="5" fill="#475569"/>')
    # chair back
    g.append(f'<rect x="164" y="214" width="148" height="190" rx="34" fill="#1e293b"/>')
    # body: white tee over black long sleeves, headphones round the neck
    g.append(f'<path d="M176 392c0-70 18-120 62-126s62 56 62 126z" fill="#f1f5f9"/>'
             f'<path d="M180 330c4-30 14-52 30-60l-6 46zM296 330c-4-30-14-52-30-60l6 46z" fill="#1f2937"/>'
             f'<path d="M222 270q16 12 32 0" stroke="#cbd5e1" stroke-width="3" fill="none"/>')
    # head
    g.append('<g class="nod">')
    g.append(f'<rect x="227" y="232" width="22" height="30" rx="8" fill="{SKIN_SHADE}"/>'
             f'<path d="M204 262q34 22 68 0" stroke="#111827" stroke-width="7" fill="none" stroke-linecap="round"/>'
             f'<rect x="196" y="246" width="16" height="24" rx="7" fill="#111827"/><rect x="264" y="246" width="16" height="24" rx="7" fill="#111827"/>'
             f'<rect x="200" y="252" width="8" height="12" rx="3" fill="#475569"/><rect x="268" y="252" width="8" height="12" rx="3" fill="#475569"/>'
             f'<circle cx="198" cy="206" r="9" fill="{SKIN_SHADE}"/><circle cx="278" cy="206" r="9" fill="{SKIN_SHADE}"/>'
             f'<ellipse cx="238" cy="202" rx="40" ry="42" fill="{SKIN}"/>'
             f'<path d="M194 204c-10-30 -2-56 18-66l-6 14 14-20 4 14 12-18 6 16 14-16 2 16 16-10-4 16c14 6 22 24 16 54-4-14-10-24-18-30l2 14-12-16-4 14-10-14-6 14-8-14-6 14-8-12-4 14c-8 4-14 10-20 26z" fill="{HAIR}"/>'
             f'<path d="M214 210q8-9 16 0M246 210q8-9 16 0" stroke="#1b1b26" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<ellipse cx="212" cy="222" rx="7" ry="4" fill="#f87171" opacity=".35"/><ellipse cx="264" cy="222" rx="7" ry="4" fill="#f87171" opacity=".35"/>'
             f'<path d="M224 226q14 14 28 0z" fill="#7c2d12"/><path d="M228 228q10 6 20 0" fill="#fda4af"/>')
    g.append('</g>')
    # arms reaching to keyboard
    g.append(f'<path d="M186 320c-10 22-6 46 14 56l26 4" stroke="#1f2937" stroke-width="22" fill="none" stroke-linecap="round"/>'
             f'<path d="M290 320c10 22 6 46-14 56l-26 4" stroke="#1f2937" stroke-width="22" fill="none" stroke-linecap="round"/>'
             f'<circle class="type" cx="222" cy="378" r="10" fill="{SKIN}"/><circle class="type2" cx="254" cy="378" r="10" fill="{SKIN}"/>')
    # desk + laptop (back of lid facing us)
    g.append(f'<rect x="14" y="384" width="448" height="12" rx="6" fill="#334155"/>'
             f'<path d="M60 396v28M416 396v28" stroke="#334155" stroke-width="8"/>'
             f'<path d="M176 300h124l10 84H166z" fill="#94a3b8"/>'
             f'<path d="M180 304h116l9 76H171z" fill="#cbd5e1"/>'
             f'<circle cx="238" cy="342" r="13" fill="{CYAN}" opacity=".85"/>'
             f'<text x="238" y="347" text-anchor="middle" class="mono" font-size="11" font-weight="800" fill="#0d1117">AI</text>'
             f'<rect x="150" y="380" width="176" height="8" rx="4" fill="#64748b"/>')
    # coffee
    g.append(f'<path d="M352 352h30v26a8 8 0 0 1-8 8h-14a8 8 0 0 1-8-8z" fill="#f8fafc"/>'
             f'<path d="M382 358c10 0 10 16 0 16" stroke="#f8fafc" stroke-width="4" fill="none"/>'
             f'<path class="steam" d="M360 344c-6-8 6-12 0-22" stroke="#cbd5e1" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             f'<path class="steam" style="animation-delay:1.1s" d="M372 344c-6-8 6-12 0-22" stroke="#cbd5e1" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    # status line
    g.append(f'<circle class="status" cx="22" cy="440" r="5" fill="{GREEN}"/>'
             f'<text x="34" y="445" class="mono" font-size="13" font-weight="700" letter-spacing="2" fill="{TEXT}">ONLINE</text>'
             f'<text x="456" y="445" text-anchor="end" class="mono" font-size="12" letter-spacing="1.5" fill="{MUTED}">building agents · shipping AI</text>')
    g.append('</g>')
    return "".join(g)


# ---------------------------------------------------------------- about

def about():
    W, H = 1280, 640
    lines = [
        (f'<tspan fill="{GREEN}">$</tspan> python agent.py --task "plan my study week"', TEXT),
        (f'<tspan fill="{CYAN}">▸ planner  </tspan> breaking goal into 4 sub-tasks', MUTED),
        (f'<tspan fill="{BLUE}">▸ retriever</tspan> 12 chunks from vector store (k=12)', MUTED),
        (f'<tspan fill="{VIOLET}">▸ tool_call</tspan> calendar.create_events(n=6)', MUTED),
        (f'<tspan fill="{PINK}">▸ critic   </tspan> checking plan against deadlines', MUTED),
        (f'<tspan fill="{GREEN}">✔ done</tspan> in 2.4s · 1,204 tokens · 0 errors', TEXT),
    ]
    cyc = 12
    line_css = ""
    for i in range(len(lines)):
        start = 4 + i * 9
        line_css += (f".l{i}{{animation:l{i} {cyc}s infinite}}"
                     f"@keyframes l{i}{{0%,{start}%{{opacity:0}}{start+3}%,92%{{opacity:1}}97%,100%{{opacity:0}}}}")
    slides = 4
    per = 4
    total = slides * per
    vis = 100 / slides
    slide_css = "".join(f".s{i}{{animation:slide {total}s infinite;animation-delay:{i*per}s;opacity:0}}" for i in range(slides))
    seg_css = "".join(f".g{i}{{animation:seg {total}s linear infinite;animation-delay:{i*per}s}}" for i in range(slides))
    css = f"""
{line_css}
@keyframes slide{{0%{{opacity:0}}3%{{opacity:1}}{vis-3:.2f}%{{opacity:1}}{vis:.2f}%,100%{{opacity:0}}}}
{slide_css}
@keyframes seg{{0%{{width:0}}{vis:.2f}%{{width:124px}}{vis+.01:.2f}%,100%{{width:0}}}}
{seg_css}
.cur{{animation:blink 1s steps(1) infinite}}@keyframes blink{{50%{{opacity:0}}}}
.ring{{animation:ring 3s ease-out infinite alternate}}@keyframes ring{{from{{stroke-dashoffset:113}}}}
.bob{{animation:bob 3s ease-in-out infinite alternate}}@keyframes bob{{to{{transform:translateY(-6px)}}}}
.spin{{transform-origin:968px 290px;animation:spin 10s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
.unspin{{animation:spin 10s linear infinite reverse;transform-box:fill-box;transform-origin:center}}
.scan{{animation:scan 2.4s ease-in-out infinite alternate}}@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY(190px)}}}}
.draw{{stroke-dasharray:520;animation:draw 4s ease-out infinite}}@keyframes draw{{from{{stroke-dashoffset:520}}to{{stroke-dashoffset:0}}}}
"""
    b = [panel(0, 0, 620, H, 24), panel(660, 0, 620, H, 24)]
    # ---- left: developer terminal
    b.append(f'<text x="28" y="46" class="tag" fill="{CYAN}">// AI ENGINEER</text>')
    b.append(f'<text x="28" y="88" class="h2">Systems that think &amp; act</text>')
    b.append(f'<rect x="28" y="118" width="564" height="352" rx="14" fill="#070b14" stroke="#1e293b"/>'
             f'<path d="M28 146V132a14 14 0 0 1 14-14h536a14 14 0 0 1 14 14v14z" fill="#111827"/>'
             f'<circle cx="48" cy="133" r="5.5" fill="#ff5f57"/><circle cx="66" cy="133" r="5.5" fill="#febc2e"/><circle cx="84" cy="133" r="5.5" fill="#28c840"/>'
             f'<rect x="200" y="124" width="220" height="18" rx="9" fill="#0b1222"/>'
             f'<text x="310" y="137" text-anchor="middle" class="mono" font-size="11" fill="{MUTED}">~/agents · agent.run()</text>')
    for i, (ln, col) in enumerate(lines):
        b.append(f'<text class="l{i} mono" x="48" y="{186+i*34}" font-size="14" fill="{col}" xml:space="preserve">{ln}</text>')
    b.append(f'<rect class="cur" x="48" y="{186+len(lines)*34-13}" width="9" height="16" fill="{CYAN}"/>')
    rows = [
        (CYAN, "LLM apps &amp; RAG", "LangChain, LlamaIndex, vector DBs, evaluation"),
        (VIOLET, "Agentic &amp; multi-agent systems", "LangGraph, CrewAI, Google ADK, tool calling"),
        (AMBER, "Computer vision &amp; deep learning", "PyTorch, YOLO, OpenCV, LoRA / QLoRA fine-tuning"),
    ]
    for i, (col, title, sub) in enumerate(rows):
        y = 496 + i * 48
        b.append(f'<rect x="28" y="{y}" width="38" height="38" rx="9" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>'
                 f'<circle cx="47" cy="{y+19}" r="7" fill="none" stroke="{col}" stroke-width="2"/><circle cx="47" cy="{y+19}" r="2.5" fill="{col}"/>'
                 f'<text x="82" y="{y+16}" font-size="16" font-weight="700" fill="{TEXT}">{title}</text>'
                 f'<text x="82" y="{y+34}" class="mono" font-size="12.5" fill="{MUTED}">{sub}</text>')
    # ---- right: what I build carousel
    X = 660
    b.append(f'<text x="{X+28}" y="46" class="tag" fill="{PINK}">// WHAT I BUILD</text>')
    b.append(f'<text x="{X+28}" y="88" class="h2">From research to production</text>')
    b.append(f'<rect x="{X+28}" y="118" width="564" height="352" rx="14" fill="#0a1020" stroke="#1e293b"/>')
    for i in range(slides):
        sx = X + 48 + i * 132
        b.append(f'<rect x="{sx}" y="132" width="124" height="3" rx="1.5" fill="#1e293b"/>'
                 f'<rect class="g{i}" x="{sx}" y="132" width="0" height="3" rx="1.5" fill="{TEXT}"/>')
    cx, cy = 968, 290
    # slide 0: RAG
    s0 = [f'<g class="bob">']
    for j in range(3):
        dx = 760 + j * 14
        s0.append(f'<rect x="{dx}" y="{220+j*14}" width="74" height="94" rx="8" fill="#111c33" stroke="{CYAN}" stroke-opacity=".6"/>')
        for q in range(4):
            s0.append(f'<rect x="{dx+12}" y="{238+j*14+q*16}" width="{50-q*8}" height="5" rx="2.5" fill="{CYAN}" opacity=".5"/>')
    s0.append('</g>')
    for q in range(9):
        s0.append(f'<circle class="pulse" style="animation-delay:{q*.2:.1f}s" cx="{915+(q%3)*26}" cy="{250+(q//3)*26}" r="6" fill="{[CYAN,BLUE,VIOLET][q%3]}"/>')
    s0.append(f'<path class="flow" d="M858 290H902M988 290H1032" stroke="{CYAN}" stroke-width="2" fill="none"/>')
    s0.append(f'<rect x="1040" y="236" width="150" height="56" rx="14" fill="{BLUE}" fill-opacity=".2" stroke="{BLUE}"/>'
              f'<text x="1115" y="269" text-anchor="middle" class="mono" font-size="13" fill="{TEXT}">grounded answer</text>'
              f'<rect x="1060" y="304" width="130" height="40" rx="12" fill="#1e293b"/><text x="1125" y="329" text-anchor="middle" class="mono" font-size="12" fill="{MUTED}">sources: 3</text>')
    # slide 1: agents
    s1 = [f'<circle cx="{cx}" cy="{cy}" r="92" fill="none" stroke="#1e3a5f" stroke-dasharray="4 6"/>',
          f'<circle cx="{cx}" cy="{cy}" r="40" fill="{VIOLET}" fill-opacity=".18" stroke="{VIOLET}"/>',
          f'<text x="{cx}" y="{cy+5}" text-anchor="middle" class="mono" font-size="14" font-weight="700" fill="{TEXT}">LLM</text>',
          '<g class="spin">']
    for j, (lbl, col) in enumerate([("planner", CYAN), ("researcher", BLUE), ("critic", PINK), ("tools", AMBER)]):
        ang = j * math.pi / 2
        px, py = cx + 92 * math.cos(ang), cy + 92 * math.sin(ang)
        s1.append(f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{col}" stroke-opacity=".5"/>'
                  f'<g class="unspin"><rect x="{px-46:.1f}" y="{py-15:.1f}" width="92" height="30" rx="15" fill="#0d1117" stroke="{col}"/>'
                  f'<text x="{px:.1f}" y="{py+5:.1f}" text-anchor="middle" class="mono" font-size="12" fill="{col}">{lbl}</text></g>')
    s1.append('</g>')
    # slide 2: vision
    s2 = [f'<rect x="808" y="190" width="320" height="200" rx="12" fill="#111c33" stroke="#334155"/>',
          f'<path d="M808 360l70-60 50 40 70-80 130 100v28a12 12 0 0 1-12 12H820a12 12 0 0 1-12-12z" fill="#1e3a5f"/>',
          f'<circle cx="1072" cy="236" r="18" fill="{AMBER}" opacity=".6"/>',
          f'<rect x="846" y="236" width="88" height="118" rx="4" fill="none" stroke="{GREEN}" stroke-width="2.5"/>',
          f'<rect x="846" y="218" width="104" height="18" fill="{GREEN}"/><text x="852" y="231" class="mono" font-size="11" font-weight="700" fill="#0d1117">person 0.97</text>',
          f'<rect x="968" y="282" width="118" height="78" rx="4" fill="none" stroke="{PINK}" stroke-width="2.5"/>',
          f'<rect x="968" y="264" width="92" height="18" fill="{PINK}"/><text x="974" y="277" class="mono" font-size="11" font-weight="700" fill="#0d1117">car 0.92</text>',
          f'<rect class="scan" x="808" y="190" width="320" height="3" fill="{CYAN}" opacity=".7"/>']
    # slide 3: fine-tuning loss curve
    s3 = [f'<line x1="808" y1="380" x2="1128" y2="380" stroke="#334155"/><line x1="808" y1="190" x2="808" y2="380" stroke="#334155"/>',
          f'<text x="816" y="204" class="mono" font-size="11" fill="{DIM}">loss</text><text x="1128" y="398" text-anchor="end" class="mono" font-size="11" fill="{DIM}">steps</text>',
          f'<path class="draw" d="M812 206C860 300 900 330 950 346S1060 366 1124 370" fill="none" stroke="url(#brand)" stroke-width="3.5" stroke-linecap="round"/>',
          f'<rect x="990" y="214" width="132" height="54" rx="10" fill="#0d1117" stroke="{GREEN}" stroke-opacity=".6"/>'
          f'<text x="1004" y="236" class="mono" font-size="12" fill="{GREEN}">LoRA r=16</text><text x="1004" y="256" class="mono" font-size="12" fill="{MUTED}">0.3% params</text>']
    titles = [("RAG chatbots", "Grounded answers from your own documents", CYAN),
              ("Multi-agent systems", "Planner, researcher and critic agents that collaborate", VIOLET),
              ("Real-time computer vision", "Detection and threat intelligence with YOLO", GREEN),
              ("Model fine-tuning", "Parameter-efficient LoRA / QLoRA adaptation", AMBER)]
    for i, parts in enumerate([s0, s1, s2, s3]):
        title, sub, col = titles[i]
        b.append(f'<g class="s{i}">' + "".join(parts) +
                 f'<rect x="{X+28}" y="490" width="{len(title)*9.5+40:.0f}" height="30" rx="8" fill="{col}" fill-opacity=".15"/>'
                 f'<text x="{X+44}" y="511" font-size="17" font-weight="700" fill="{col}">{t(title)}</text>'
                 f'<text x="{X+28}" y="548" font-size="15" fill="{MUTED}">{t(sub)}</text></g>')
    for i, (lbl, col) in enumerate([("Learn", GREEN), ("Build", CYAN), ("Ship", PINK)]):
        rx = X + 50 + i * 150
        b.append(f'<circle cx="{rx}" cy="598" r="18" fill="none" stroke="#1e293b" stroke-width="5"/>'
                 f'<circle class="ring" style="animation-delay:{i*.4}s" cx="{rx}" cy="598" r="18" fill="none" stroke="{col}" stroke-width="5" stroke-linecap="round" stroke-dasharray="113" stroke-dashoffset="22" transform="rotate(-90 {rx} 598)"/>'
                 f'<text x="{rx+30}" y="604" font-size="15" font-weight="600" fill="{TEXT}">{lbl}</text>')
    b.append(f'<text x="{X+592}" y="603" text-anchor="end" class="tag" fill="{DIM}">DAILY LOOP</text>')
    return svg(W, H, "What I build as an AI engineer", "".join(b), css)


# ---------------------------------------------------------------- stack

def stack():
    W, H = 1280, 480
    groups = [
        ("AI / MACHINE LEARNING", CYAN, [("python", "Python"), ("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"),
                                         ("scikitlearn", "scikit-learn"), ("huggingface", "Hugging Face"), ("opencv", "OpenCV")]),
        ("LLMS & AGENTS", VIOLET, [("langchain", "LangChain"), ("langgraph", "LangGraph"), ("llamaindex", "LlamaIndex"),
                                       ("openai", "OpenAI"), ("googlegemini", "Gemini"), ("crewai", "CrewAI")]),
        ("BACKEND & DATA", AMBER, [("fastapi", "FastAPI"), ("flask", "Flask"), ("postgresql", "PostgreSQL"),
                                       ("mongodb", "MongoDB"), ("mysql", "MySQL"), ("pandas", "Pandas")]),
        ("TOOLS & CLOUD", PINK, [("docker", "Docker"), ("kubernetes", "Kubernetes"), ("amazonwebservices", "AWS"),
                                     ("git", "Git"), ("linux", "Linux"), ("jupyter", "Jupyter")]),
    ]
    css = """
.o1{transform-origin:260px 290px;animation:spin 26s linear infinite}
.o2{transform-origin:260px 290px;animation:spin 40s linear infinite reverse}
.up1{animation:spin 26s linear infinite reverse;transform-box:fill-box;transform-origin:center}
.up2{animation:spin 40s linear infinite;transform-box:fill-box;transform-origin:center}
@keyframes spin{to{transform:rotate(360deg)}}
.core{animation:core 3s ease-in-out infinite alternate}@keyframes core{from{opacity:.55}to{opacity:1}}
.chip{animation:chip .6s ease-out both}@keyframes chip{from{opacity:0;transform:translateY(6px)}}
"""
    b = [panel(0, 0, W, H, 26)]
    b.append(f'<text x="40" y="56" class="tag" fill="{CYAN}">// TECH STACK</text>')
    b.append(f'<text x="40" y="98" class="h2">Tools I build with</text>')
    cx, cy = 260, 290
    b.append(f'<radialGradient id="halo"><stop offset="0" stop-color="{BLUE}" stop-opacity=".35"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>'
             f'<circle class="core" cx="{cx}" cy="{cy}" r="150" fill="url(#halo)"/>')
    for r in (92, 158):
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#1e3a5f" stroke-width="1.2"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="url(#brand)" opacity=".9"/>'
             f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{CYAN}" stroke-opacity=".4"/>'
             f'<text x="{cx}" y="{cy+10}" text-anchor="middle" font-size="28" font-weight="800" fill="#fff" class="mono">AI</text>')
    for cls, up, r, slugs in [("o1", "up1", 92, ["python", "pytorch", "huggingface", "langchain"]),
                              ("o2", "up2", 158, ["tensorflow", "opencv", "fastapi", "docker", "googlegemini", "mongodb"])]:
        b.append(f'<g class="{cls}">')
        for j, s in enumerate(slugs):
            a = 2 * math.pi * j / len(slugs) + (0.4 if cls == "o2" else 0)
            px, py = cx + r * math.cos(a), cy + r * math.sin(a)
            col = "#" + ICONS[s]["hex"] if s in ICONS else BLUE
            b.append(f'<g class="{up}"><circle cx="{px:.1f}" cy="{py:.1f}" r="21" fill="#0d1117" stroke="{col}" stroke-opacity=".8"/>'
                     + icon(s, round(px - 11, 1), round(py - 11, 1), 22) + '</g>')
        b.append('</g>')
    b.append('<line x1="520" y1="120" x2="520" y2="440" stroke="#1e293b"/>')
    y = 130
    k = 0
    for label, col, items in groups:
        b.append(tag(552, y, label, col))
        y += 18
        x = 552
        for slug, name in items:
            w = 40 + len(name) * 7.6
            if x + w > 1250:
                x = 552
                y += 46
            b.append(f'<g class="chip" style="animation-delay:{k*.05:.2f}s">'
                     f'<rect x="{x}" y="{y}" width="{w:.0f}" height="36" rx="9" fill="#0f172a" stroke="{col}" stroke-opacity=".35"/>'
                     + icon(slug, x + 12, y + 9, 18, fallback=name[0]) +
                     f'<text x="{x+36}" y="{y+23}" class="mono" font-size="12.5" fill="{TEXT}">{t(name)}</text></g>')
            x += w + 8
            k += 1
        y += 66
    return svg(W, H, "Tech stack", "".join(b), css)


# ---------------------------------------------------------------- connect

def connect():
    W, H = 1280, 230
    css = """
.wave{animation:wave 8s ease-in-out infinite alternate}@keyframes wave{to{transform:translateX(-120px)}}
.float{animation:float 5s ease-in-out infinite alternate}@keyframes float{to{transform:translateY(-14px)}}
"""
    b = [panel(0, 0, W, H, 24)]
    b.append(f'<g class="wave" opacity=".5"><path d="M0 180C160 140 320 220 480 180S800 140 960 180 1280 220 1440 180V230H0z" fill="{BLUE}" opacity=".15"/>'
             f'<path d="M0 200C160 170 320 230 480 200S800 170 960 200 1280 230 1440 200V230H0z" fill="{CYAN}" opacity=".12"/></g>')
    for i in range(14):
        b.append(f'<circle class="float" style="animation-delay:{i*.37:.2f}s" cx="{80+i*88}" cy="{40+(i*53)%120}" r="{1.5+(i%3)}" fill="{[CYAN,BLUE,VIOLET][i%3]}" opacity=".6"/>')
    b.append(f'<text x="640" y="74" text-anchor="middle" class="tag" fill="{CYAN}">// LET&#8217;S CONNECT</text>')
    b.append(f'<text x="640" y="124" text-anchor="middle" font-size="36" font-weight="800" fill="url(#brand)">Let&#8217;s build something intelligent together</text>')
    b.append(f'<text x="640" y="160" text-anchor="middle" font-size="17" fill="{MUTED}">Open to internships, collaborations and AI projects &#8212; reach out below.</text>')
    return svg(W, H, "Let's connect", "".join(b), css)


# ---------------------------------------------------------------- dashboard (live)

QUERY = """
query($login:String!){
  user(login:$login){
    createdAt avatarUrl(size:240)
    repositories(ownerAffiliations:OWNER, privacy:PUBLIC){ totalCount }
    pullRequests{ totalCount }
    langRepos: repositories(ownerAffiliations:OWNER, isFork:false, first:100){
      nodes{ languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions restrictedContributionsCount
      contributionCalendar{ totalContributions weeks{ contributionDays{ contributionCount date } } }
    }
  }
}"""


def fetch_live():
    token = os.environ.get("PROFILE_TOKEN")
    if not token:
        raise RuntimeError("PROFILE_TOKEN not set")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    u = data["data"]["user"]
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    best = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] > 0 else 0
        best = max(best, cur)
    streak = 0
    for i, d in enumerate(reversed(days)):
        if d["contributionCount"] > 0:
            streak += 1
        elif i == 0:
            continue  # today may not have contributions yet
        else:
            break
    sizes = {}
    for r in u["langRepos"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            s = sizes.setdefault(n, [0, e["node"]["color"] or "#8b949e"])
            s[0] += e["size"]
    tot = sum(v[0] for v in sizes.values()) or 1
    langs = sorted(((n, v[0] * 100 / tot, v[1]) for n, v in sizes.items()), key=lambda x: -x[1])[:5]
    avatar = None
    try:
        raw = urllib.request.urlopen(u["avatarUrl"], timeout=30).read()
        avatar = "data:image/png;base64," + base64.b64encode(raw).decode()
    except Exception as exc:  # avatar is optional
        print("avatar fetch failed:", exc)
    return {
        "repos": u["repositories"]["totalCount"],
        "commits": cc["totalCommitContributions"] + cc["restrictedContributionsCount"],
        "prs": u["pullRequests"]["totalCount"],
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "streak": streak, "best_streak": best,
        "since": int(u["createdAt"][:4]),
        "languages": langs, "avatar": avatar,
    }


def dashboard(d):
    W, H = 1280, 600
    css = f"""
.swing{{transform-origin:212px 0;animation:swing 6s ease-in-out infinite alternate}}@keyframes swing{{from{{transform:rotate(-2.5deg)}}to{{transform:rotate(2.5deg)}}}}
.sheen{{animation:sheen 5s ease-in-out infinite}}@keyframes sheen{{0%{{transform:translateX(-360px)}}60%,100%{{transform:translateX(420px)}}}}
.grow{{animation:grow 1.6s cubic-bezier(.2,.8,.2,1) both}}@keyframes grow{{from{{width:0}}}}
.fade{{animation:fade .8s ease-out both}}@keyframes fade{{from{{opacity:0;transform:translateY(8px)}}}}
"""
    b = [panel(0, 0, W, H, 26)]
    # lanyard + badge
    b.append('<g class="swing">')
    b.append(f'<rect x="196" y="-10" width="32" height="118" fill="url(#brand)"/>'
             f'<text transform="translate(217 6) rotate(90)" class="mono" font-size="10.5" letter-spacing="2.5" fill="#0d1117" font-weight="700">AI.ENGINEER · {USER.upper()[:16]}</text>'
             f'<rect x="186" y="102" width="52" height="22" rx="6" fill="#94a3b8"/><rect x="186" y="102" width="52" height="8" rx="4" fill="#cbd5e1"/>'
             f'<circle cx="212" cy="134" r="11" fill="none" stroke="#94a3b8" stroke-width="4"/>')
    bx, by, bw, bh = 58, 146, 308, 428
    b.append(f'<clipPath id="card"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="18"/></clipPath>'
             f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="18" fill="#0f172a" stroke="url(#brand)" stroke-width="2"/>'
             f'<g clip-path="url(#card)"><rect class="sheen" x="{bx}" y="{by-40}" width="70" height="{bh+80}" fill="#fff" opacity=".07" transform="skewX(-18)"/></g>'
             f'<text x="{bx+20}" y="{by+30}" class="tag" fill="{CYAN}">DEVELOPER ID</text>'
             f'<text x="{bx+bw-20}" y="{by+30}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">v3.0</text>'
             f'<rect x="{bx+22}" y="{by+56}" width="34" height="26" rx="5" fill="{AMBER}" opacity=".85"/>'
             f'<path d="M{bx+22} {by+69}h34M{bx+39} {by+56}v26" stroke="#b45309" stroke-width="1"/>')
    ax, ay, asz = bx + 84, by + 50, 140
    b.append(f'<clipPath id="av"><rect x="{ax}" y="{ay}" width="{asz}" height="{asz}" rx="18"/></clipPath>')
    if d.get("avatar"):
        b.append(f'<image href="{d["avatar"]}" x="{ax}" y="{ay}" width="{asz}" height="{asz}" clip-path="url(#av)" preserveAspectRatio="xMidYMid slice"/>')
    else:
        b.append(f'<rect x="{ax}" y="{ay}" width="{asz}" height="{asz}" rx="18" fill="url(#brand)"/>'
                 f'<text x="{ax+asz/2}" y="{ay+asz/2+18}" text-anchor="middle" font-size="52" font-weight="800" fill="#fff">MC</text>')
    b.append(f'<rect x="{ax}" y="{ay}" width="{asz}" height="{asz}" rx="18" fill="none" stroke="url(#brand)" stroke-width="2.5"/>')
    b.append(f'<text x="{bx+bw/2}" y="{by+230}" text-anchor="middle" font-size="25" font-weight="800" fill="{TEXT}">{t(NAME)}</text>'
             f'<text x="{bx+bw/2}" y="{by+254}" text-anchor="middle" class="tag" fill="{VIOLET}">AI ENGINEER</text>'
             f'<line x1="{bx+22}" y1="{by+272}" x2="{bx+bw-22}" y2="{by+272}" stroke="#1e293b"/>')
    fields = [("FOCUS", "GenAI · Agents"), ("TRACK", "B.Tech CSE"), ("STACK", "Python · PyTorch"), ("SINCE", str(d["since"]))]
    for i, (k, v) in enumerate(fields):
        fx = bx + 24 + (i % 2) * 142
        fy = by + 296 + (i // 2) * 44
        b.append(f'<text x="{fx}" y="{fy}" class="mono" font-size="10.5" letter-spacing="1.5" fill="{DIM}">{k}</text>'
                 f'<text x="{fx}" y="{fy+18}" font-size="14" font-weight="600" fill="{TEXT}">{t(v)}</text>')
    bars = "".join(f'<rect x="{bx+24+i*4.6:.1f}" y="{by+384}" width="{[1.4,2.6,1,3][i%4]}" height="20" fill="#cbd5e1"/>' for i in range(56))
    b.append(bars)
    b.append(f'<circle class="pulse" cx="{bx+28}" cy="{by+416}" r="4" fill="{GREEN}"/>'
             f'<text x="{bx+40}" y="{by+420}" class="mono" font-size="11" letter-spacing="1.5" fill="{GREEN}">OPEN TO COLLAB</text>')
    b.append('</g>')
    # dashboard
    X = 420
    b.append(f'<text x="{X}" y="56" class="tag" fill="{VIOLET}">// DEVELOPER DASHBOARD</text>'
             f'<text x="{X}" y="98" class="h2">Profile at a glance</text>'
             f'<rect x="1090" y="56" width="150" height="30" rx="15" fill="#0f2a24" stroke="{GREEN}" stroke-opacity=".45"/>'
             f'<circle class="pulse" cx="1108" cy="71" r="4.5" fill="{GREEN}"/>'
             f'<text x="1120" y="76" class="mono" font-size="11.5" letter-spacing="1.5" font-weight="700" fill="{GREEN}">LIVE · GITHUB</text>')
    stats = [(f'{d["repos"]:,}', "PUBLIC REPOS", CYAN), (f'{d["commits"]:,}', "COMMITS · 1Y", AMBER),
             (f'{d["prs"]:,}', "PULL REQUESTS", VIOLET), (f'{d["contributions"]:,}', "CONTRIBUTIONS · 1Y", PINK)]
    for i, (v, lbl, col) in enumerate(stats):
        sx = X + i * 209
        b.append(f'<g class="fade" style="animation-delay:{i*.12:.2f}s"><rect x="{sx}" y="126" width="195" height="96" rx="14" fill="#111827" stroke="#1e293b"/>'
                 f'<rect x="{sx+18}" y="140" width="22" height="3" rx="1.5" fill="{col}"/>'
                 f'<text x="{sx+18}" y="186" font-size="34" font-weight="800" fill="{TEXT}">{v}</text>'
                 f'<text x="{sx+18}" y="208" class="mono" font-size="10.5" letter-spacing="2" fill="{MUTED}">{lbl}</text></g>')
    # languages
    b.append(f'<rect x="{X}" y="240" width="462" height="306" rx="16" fill="#111827" stroke="#1e293b"/>'
             f'<text x="{X+22}" y="272" class="mono" font-size="11.5" letter-spacing="2" fill="{MUTED}">TOP LANGUAGES · BY CODE SIZE</text>')
    langs = d["languages"]
    mx = max((p for _, p, _ in langs), default=1)
    for i, (n, p, col) in enumerate(langs):
        y = 310 + i * 42
        w = max(8, 196 * p / mx)
        b.append(f'<text x="{X+22}" y="{y+5}" class="mono" font-size="13" fill="{TEXT}">{t(n[:18])}</text>'
                 f'<rect x="{X+176}" y="{y-6}" width="196" height="14" rx="7" fill="#1e293b"/>'
                 f'<rect class="grow" style="animation-delay:{i*.15:.2f}s" x="{X+176}" y="{y-6}" width="{w:.1f}" height="14" rx="7" fill="{col}"/>'
                 f'<text x="{X+440}" y="{y+5}" text-anchor="end" class="mono" font-size="12.5" font-weight="700" fill="{TEXT}">{p:.1f}%</text>')
    b.append(f'<text x="{X+22}" y="528" class="mono" font-size="11" fill="{DIM}">refreshed {dt.date.today():%d %b %Y} · github graphql</text>')
    # streak card
    RX = 896
    b.append(f'<rect x="{RX}" y="240" width="344" height="140" rx="16" fill="#111827" stroke="#1e293b"/>'
             f'<text x="{RX+22}" y="272" class="mono" font-size="11.5" letter-spacing="2" fill="{MUTED}">COMMIT STREAK</text>'
             f'<text x="{RX+22}" y="326" font-size="40" font-weight="800" fill="{AMBER}">{d["streak"]}</text>'
             f'<text x="{RX+22}" y="352" class="mono" font-size="10.5" letter-spacing="2" fill="{MUTED}">CURRENT · DAYS</text>'
             f'<text x="{RX+180}" y="326" font-size="40" font-weight="800" fill="{TEXT}">{d["best_streak"]}</text>'
             f'<text x="{RX+180}" y="352" class="mono" font-size="10.5" letter-spacing="2" fill="{MUTED}">BEST · DAYS</text>')
    focus = [("BUILDING", "Multi-agent AI systems", CYAN), ("EXPLORING", "LLM fine-tuning &amp; MLOps", VIOLET),
             ("SHIPPING", "FastAPI · Docker · tested code", PINK)]
    b.append(f'<rect x="{RX}" y="396" width="344" height="150" rx="16" fill="#111827" stroke="#1e293b"/>')
    for i, (k, v, col) in enumerate(focus):
        y = 426 + i * 42
        b.append(f'<circle cx="{RX+26}" cy="{y+8}" r="4" fill="{col}"/>'
                 f'<text x="{RX+40}" y="{y}" class="mono" font-size="10.5" letter-spacing="2" font-weight="700" fill="{col}">{k}</text>'
                 f'<text x="{RX+40}" y="{y+19}" font-size="15" fill="{TEXT}">{v}</text>')
    return svg(W, H, "Developer ID and dashboard", "".join(b), css)


# ---------------------------------------------------------------- public repo data

DATA_QUERY = """
query($login:String!){
  user(login:$login){
    pinnedItems(first:6, types:REPOSITORY){ nodes{ ... on Repository{ name } } }
    repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, first:100,
                 orderBy:{field:PUSHED_AT, direction:DESC}){
      nodes{
        name description homepageUrl stargazerCount forkCount pushedAt createdAt
        primaryLanguage{ name }
        repositoryTopics(first:10){ nodes{ topic{ name } } }
        dockerfile: object(expression:"HEAD:Dockerfile"){ id }
        compose: object(expression:"HEAD:docker-compose.yml"){ id }
        workflows: object(expression:"HEAD:.github/workflows"){ id }
        tests: object(expression:"HEAD:tests"){ id }
      }
    }
  }
}"""


def fetch_public_data():
    """Public-only facts used to keep the README accurate (no private repos)."""
    token = os.environ["PROFILE_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": DATA_QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=30))
    if data.get("errors"):
        raise RuntimeError(data["errors"])
    u = data["data"]["user"]
    repos = []
    for r in u["repositories"]["nodes"]:
        repos.append({
            "name": r["name"], "description": r["description"], "homepage": r["homepageUrl"],
            "stars": r["stargazerCount"], "forks": r["forkCount"], "pushed": r["pushedAt"][:10],
            "created": r["createdAt"][:10],
            "language": (r["primaryLanguage"] or {}).get("name"),
            "topics": [n["topic"]["name"] for n in r["repositoryTopics"]["nodes"]],
            "docker": bool(r["dockerfile"] or r["compose"]), "ci": bool(r["workflows"]),
            "tests": bool(r["tests"]),
        })
    return {"pinned": [n["name"] for n in u["pinnedItems"]["nodes"] if n],
            "repos": repos}


# ---------------------------------------------------------------- featured projects

def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + [cur] if cur else lines


def proj_anim(kind, x, y, w, h):
    """Small animated illustration for each project card (area w x h at x, y)."""
    cx, cy = x + w / 2, y + h / 2
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#070b14" stroke="#1e293b"/>']
    if kind == "guardian":
        g.append(f'<path d="M{x+20} {y+h-20}l60-44 40 28 56-58 70 52 60-30 {w-326} 52z" fill="#13213b"/>')
        g.append(f'<rect class="pa-box1" x="{x+64}" y="{y+44}" width="54" height="66" rx="3" fill="none" stroke="{GREEN}" stroke-width="2"/>'
                 f'<text class="pa-box1 mono" x="{x+64}" y="{y+40}" font-size="10" fill="{GREEN}">person 0.96</text>'
                 f'<rect class="pa-box2" x="{x+186}" y="{y+58}" width="70" height="50" rx="3" fill="none" stroke="#ef4444" stroke-width="2"/>'
                 f'<text class="pa-box2 mono" x="{x+186}" y="{y+54}" font-size="10" fill="#ef4444">loitering · 0.88</text>'
                 f'<rect class="pa-scan" x="{x}" y="{y}" width="{w}" height="2" fill="{CYAN}" opacity=".8"/>'
                 f'<circle class="pulse" cx="{x+16}" cy="{y+14}" r="4" fill="#ef4444"/><text x="{x+26}" y="{y+18}" class="mono" font-size="10" fill="{MUTED}">CAM-04 · LIVE</text>'
                 f'<text x="{x+w-112}" y="{y+18}" class="mono" font-size="10" fill="{MUTED}">THREAT</text>'
                 f'<rect x="{x+w-66}" y="{y+10}" width="52" height="8" rx="4" fill="#1e293b"/>'
                 f'<rect class="pa-threat" x="{x+w-66}" y="{y+10}" width="20" height="8" rx="4" fill="{AMBER}"/>')
    elif kind == "sentinel":
        for i, (lw, col) in enumerate([(120, CYAN), (180, MUTED), (90, VIOLET), (150, MUTED), (200, MUTED), (110, PINK)]):
            g.append(f'<text x="{x+14}" y="{y+24+i*16}" class="mono" font-size="10" fill="{DIM}">{i+1:02d}</text>'
                     f'<rect x="{x+36}" y="{y+17+i*16}" width="{lw}" height="6" rx="3" fill="{col}" opacity=".55"/>')
        g.append(f'<rect class="pa-flag" x="{x+30}" y="{y+76}" width="{w-130}" height="14" rx="3" fill="#ef4444" opacity=".25"/>'
                 f'<text class="pa-flag mono" x="{x+w-150}" y="{y+87}" font-size="9.5" fill="#fca5a5">bare except</text>'
                 f'<rect class="pa-scan2" x="{x+30}" y="{y+12}" width="{w-130}" height="2" fill="{CYAN}"/>')
        gx, gy = x + w - 46, y + h / 2
        g.append(f'<circle cx="{gx}" cy="{gy}" r="26" fill="none" stroke="#1e293b" stroke-width="6"/>'
                 f'<circle class="pa-gauge" cx="{gx}" cy="{gy}" r="26" fill="none" stroke="{GREEN}" stroke-width="6" stroke-linecap="round" stroke-dasharray="163" stroke-dashoffset="40" transform="rotate(-90 {gx} {gy})"/>'
                 f'<text x="{gx}" y="{gy+5}" text-anchor="middle" font-size="10" font-weight="700" class="mono" fill="{TEXT}">score</text>')
    elif kind == "coach":
        names = [("budget", CYAN), ("savings", GREEN), ("debt", PINK), ("goals", AMBER)]
        step = (w - 60) / 3
        for i, (n, col) in enumerate(names):
            nx = x + 30 + i * step
            if i:
                g.append(f'<line class="flow" x1="{nx-step+20}" y1="{y+40}" x2="{nx-20}" y2="{y+40}" stroke="{col}" stroke-width="2"/>')
            g.append(f'<circle class="pa-agent" style="animation-delay:{i*.6}s" cx="{nx}" cy="{y+40}" r="17" fill="{col}" fill-opacity=".15" stroke="{col}" stroke-width="2"/>'
                     f'<text x="{nx}" y="{y+44}" text-anchor="middle" class="mono" font-size="9" font-weight="700" fill="{col}">A{i+1}</text>'
                     f'<text x="{nx}" y="{y+72}" text-anchor="middle" class="mono" font-size="9.5" fill="{MUTED}">{n}</text>')
        for i, bh in enumerate([22, 34, 18, 40, 28, 46, 36]):
            g.append(f'<rect class="pa-bar" style="animation-delay:{i*.15:.2f}s" x="{x+30+i*((w-60)/7):.1f}" y="{y+h-12-bh}" width="{(w-60)/7-8:.1f}" height="{bh}" rx="2" fill="url(#brand)" opacity=".75"/>')
    elif kind == "meeting":
        n = 28
        for i in range(n):
            bh = 8 + (i * 37 % 26)
            g.append(f'<rect class="pa-wave" style="animation-delay:{(i%7)*.12:.2f}s" x="{x+16+i*6.2:.1f}" y="{cy-bh/2-12:.1f}" width="3.6" height="{bh}" rx="1.8" fill="{VIOLET}"/>')
        g.append(f'<path class="flow" d="M{x+196} {cy-12}H{x+224}" stroke="{CYAN}" stroke-width="2"/>')
        for i, (lbl, col) in enumerate([("summary", CYAN), ("action items", GREEN), ("decisions", AMBER), ("Q&amp;A (RAG)", PINK)]):
            g.append(f'<g class="pa-note" style="animation-delay:{i*.5}s"><rect x="{x+232}" y="{y+14+i*24}" width="{w-248}" height="18" rx="5" fill="{col}" fill-opacity=".14"/>'
                     f'<text x="{x+240}" y="{y+27+i*24}" class="mono" font-size="10" fill="{col}">{lbl}</text></g>')
    elif kind == "nova":
        stages = [("search", CYAN), ("read", BLUE), ("write", VIOLET), ("critic", PINK)]
        step = (w - 70) / 3
        pts = []
        for i, (n, col) in enumerate(stages):
            nx, ny = x + 35 + i * step, y + (34 if i % 2 == 0 else 74)
            pts.append((nx, ny))
            g.append(f'<rect x="{nx-30}" y="{ny-13}" width="60" height="26" rx="13" fill="#0d1117" stroke="{col}"/>'
                     f'<text x="{nx}" y="{ny+4}" text-anchor="middle" class="mono" font-size="10" fill="{col}">{n}</text>')
        path = "M" + " L".join(f"{px:.1f} {py}" for px, py in pts)
        g.insert(1, f'<path id="novapath" d="{path}" fill="none" stroke="#1e3a5f" stroke-width="2" stroke-dasharray="4 5"/>')
        g.append(f'<circle r="5" fill="{AMBER}"><animateMotion dur="3.2s" repeatCount="indefinite" path="{path}"/></circle>')
        g.append(f'<text x="{x+w-14}" y="{y+h-10}" text-anchor="end" class="mono" font-size="10" fill="{GREEN}">cited report · confidence score</text>')
    elif kind == "fleet":
        for i in range(1, 6):
            g.append(f'<line x1="{x+i*w/6:.1f}" y1="{y}" x2="{x+i*w/6:.1f}" y2="{y+h}" stroke="#13213b"/>')
        for i in range(1, 4):
            g.append(f'<line x1="{x}" y1="{y+i*h/4:.1f}" x2="{x+w}" y2="{y+i*h/4:.1f}" stroke="#13213b"/>')
        routes = [(f"M{x+20} {y+h-16} L{x+90} {y+h-16} L{x+90} {y+40} L{x+210} {y+40} L{x+210} {y+18}", CYAN, "3.4s"),
                  (f"M{x+30} {y+20} L{x+150} {y+20} L{x+150} {y+h-30} L{x+w-24} {y+h-30}", PINK, "4s"),
                  (f"M{x+w-20} {y+16} L{x+w-80} {y+16} L{x+w-80} {y+70} L{x+250} {y+70}", AMBER, "3s")]
        for d, col, dur in routes:
            g.append(f'<path class="pa-route" d="{d}" fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round"/>'
                     f'<rect x="-6" y="-4" width="12" height="8" rx="2" fill="{col}"><animateMotion dur="{dur}" repeatCount="indefinite" rotate="auto" path="{d}"/></rect>')
        for (px, py) in [(x+210, y+18), (x+w-24, y+h-30), (x+250, y+70)]:
            g.append(f'<circle class="pulse" cx="{px}" cy="{py}" r="5" fill="none" stroke="{TEXT}" stroke-width="2"/>')
        g.append(f'<text x="{x+12}" y="{y+h-28}" class="mono" font-size="10" fill="{GREEN}">VRP solved · OR-Tools</text>')
    return "".join(g)


PROJECTS = [
    ("GuardianAI", "guardian", CYAN,
     "Multi-agent CCTV surveillance: YOLOv11 + DeepSORT detection and Gemini threat reasoning with explainable decisions, built on Google ADK and MCP tools.",
     ["FastAPI", "WebSockets", "PostgreSQL", "Redis", "React"], ["Docker Compose", "pytest", "JWT/RBAC"]),
    ("CodeSentinel", "sentinel", GREEN,
     "Code review combining deterministic Python AST analysis with a pluggable LLM layer: OpenAI, Anthropic or local Ollama.",
     ["FastAPI", "SQLite", "YAML rules", "CLI"], ["Docker", "pytest", "CI gate"]),
    ("AI Financial Coach", "coach", AMBER,
     "Four Gemini agents orchestrated as a Google ADK SequentialAgent; all finance math is deterministic Python, never generated by the LLM.",
     ["Google ADK", "Gemini", "Pydantic", "Streamlit"], ["Docker", "unit tests"]),
    ("AI Meeting Assistant", "meeting", VIOLET,
     "Recording to summary, action items, decisions and RAG Q&A. Whisper + Sarvam AI transcription, Mistral via LangChain LCEL.",
     ["LangChain", "ChromaDB", "Whisper", "Mistral"], ["Docker Compose", "AWS EC2"]),
    ("Nova · Multi-Agent Research", "nova", PINK,
     "LangGraph pipeline of search, reader, writer and critic agents producing cited research reports with confidence scores.",
     ["LangGraph", "LangChain", "FastAPI"], ["agent dashboard"]),
    ("Cab Fleet Route Optimization", "fleet", BLUE,
     "Vehicle routing with capacity and time windows using Google OR-Tools, plus ML demand prediction.",
     ["OR-Tools", "FastAPI", "Pydantic v2", "scikit-learn"], ["Docker", "live on Railway"]),
]


def projects():
    W = 1280
    cw, ch, gap, top = 392, 380, 26, 130
    H = top + 2 * ch + gap + 40
    css = """
.pa-scan{animation:pscan 2.6s ease-in-out infinite alternate}@keyframes pscan{to{transform:translateY(118px)}}
.pa-scan2{animation:pscan2 3s linear infinite}@keyframes pscan2{to{transform:translateY(96px)}}
.pa-box1{animation:pbox 3s ease-in-out infinite}.pa-box2{animation:pbox 3s ease-in-out infinite 1.4s}
@keyframes pbox{0%,15%{opacity:0}25%,85%{opacity:1}100%{opacity:0}}
.pa-threat{animation:pthreat 3s ease-in-out infinite alternate}@keyframes pthreat{to{width:46px;fill:#ef4444}}
.pa-flag{animation:pflag 3s steps(1) infinite}@keyframes pflag{0%,40%{opacity:0}45%,100%{opacity:1}}
.pa-gauge{animation:pgauge 3s ease-out infinite}@keyframes pgauge{from{stroke-dashoffset:163}}
.pa-agent{animation:pagent 2.4s ease-in-out infinite}@keyframes pagent{0%,100%{fill-opacity:.1}25%{fill-opacity:.7}}
.pa-bar{transform-box:fill-box;transform-origin:bottom;animation:pbar 2.2s ease-in-out infinite alternate}@keyframes pbar{from{transform:scaleY(.35)}}
.pa-wave{transform-box:fill-box;transform-origin:center;animation:pwave .9s ease-in-out infinite alternate}@keyframes pwave{from{transform:scaleY(.25)}}
.pa-note{animation:pnote 4s ease-in-out infinite}@keyframes pnote{0%,10%{opacity:0;transform:translateX(-8px)}25%,90%{opacity:1;transform:none}100%{opacity:0}}
.pa-route{stroke-dasharray:400;animation:proute 4s ease-in-out infinite}@keyframes proute{from{stroke-dashoffset:400}50%,to{stroke-dashoffset:0}}
.flow{stroke-dasharray:6 6;animation:flow 1s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}
.trail{stroke-dasharray:120 1400;animation:trail 6s linear infinite}@keyframes trail{to{stroke-dashoffset:-1520}}
.card{animation:card .9s cubic-bezier(.2,.8,.2,1) both}@keyframes card{from{opacity:0;transform:translateY(16px)}}
.glow2{animation:glow2 3s ease-in-out infinite alternate}@keyframes glow2{from{opacity:.03}to{opacity:.10}}
"""
    b = [panel(0, 0, W, H, 26)]
    b.append(f'<text x="40" y="58" class="tag" fill="{CYAN}">// FEATURED PROJECTS</text>'
             f'<text x="40" y="100" class="h2">Systems I&#8217;ve designed, built and shipped</text>')
    for i, (name, kind, col, desc, stack_, proof) in enumerate(PROJECTS):
        cx = 40 + (i % 3) * (cw + gap)
        cy = top + (i // 3) * (ch + gap)
        per = 2 * (cw + ch)
        b.append(f'<g class="card" style="animation-delay:{i*.12:.2f}s">')
        b.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="18" fill="#0f172a" stroke="#1e293b"/>'
                 f'<rect class="glow2" x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="18" fill="{col}"/>'
                 f'<rect class="trail" style="animation-delay:-{i*1.1:.1f}s" x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="18" fill="none" stroke="{col}" stroke-width="2.2" pathLength="{per}"/>')
        b.append(proj_anim(kind, cx + 16, cy + 16, cw - 32, 128))
        b.append(f'<text x="{cx+20}" y="{cy+178}" font-size="19" font-weight="800" fill="{TEXT}">{t(name)}</text>'
                 f'<rect x="{cx+20}" y="{cy+188}" width="34" height="3" rx="1.5" fill="{col}"/>')
        for j, line in enumerate(wrap(desc, 46)[:4]):
            b.append(f'<text x="{cx+20}" y="{cy+214+j*19}" font-size="13.5" fill="{MUTED}">{t(line)}</text>')
        x0, y0 = cx + 20, cy + ch - 70
        for k, tool in enumerate(stack_):
            wd = 18 + len(tool) * 7
            if x0 + wd > cx + cw - 16:
                break
            b.append(f'<rect x="{x0}" y="{y0}" width="{wd}" height="22" rx="6" fill="#111c33" stroke="{col}" stroke-opacity=".35"/>'
                     f'<text x="{x0+9}" y="{y0+15}" class="mono" font-size="11" fill="{TEXT}">{t(tool)}</text>')
            x0 += wd + 6
        x0, y0 = cx + 20, cy + ch - 36
        for k, pf in enumerate(proof):
            wd = 30 + len(pf) * 7
            live = "live" in pf
            pc = GREEN if live else CYAN
            b.append(f'<circle class="{"pulse" if live else ""}" cx="{x0+7}" cy="{y0+8}" r="4" fill="{pc}"/>'
                     f'<text x="{x0+17}" y="{y0+12}" class="mono" font-size="11" font-weight="700" fill="{pc}">{t(pf)}</text>')
            x0 += wd
        b.append('</g>')
    return svg(W, H, "Featured projects", "".join(b), css)


# ---------------------------------------------------------------- technical skills

SKILLS = [
    ("GENERATIVE AI &amp; AGENTS", CYAN, [("langchain", "LangChain"), ("langgraph", "LangGraph"), ("adk", "Google ADK"),
        ("mcp", "MCP"), ("pinecone", "Pinecone"), ("chroma", "ChromaDB"), ("openai", "OpenAI"), ("anthropic", "Anthropic"),
        ("googlegemini", "Gemini"), ("mistralai", "Mistral"), ("groq", "Groq"), ("ollama", "Ollama")]),
    ("MODEL TRAINING", VIOLET, [("pytorch", "PyTorch"), ("tensorflow", "TensorFlow"), ("huggingface", "Transformers"),
        ("peft", "PEFT · LoRA / QLoRA"), ("trl", "TRL · RLHF / DPO"), ("scikitlearn", "scikit-learn")]),
    ("VISION &amp; SPEECH", PINK, [("yolo", "YOLOv11"), ("deepsort", "DeepSORT"), ("opencv", "OpenCV"), ("whisper", "Whisper")]),
    ("BACKEND &amp; DATA", AMBER, [("python", "Python"), ("fastapi", "FastAPI"), ("flask", "Flask"), ("pydantic", "Pydantic"),
        ("postgresql", "PostgreSQL"), ("redis", "Redis"), ("mongodb", "MongoDB"), ("sqlite", "SQLite"), ("pandas", "Pandas")]),
    ("DEPLOY &amp; QUALITY", GREEN, [("docker", "Docker"), ("compose", "Compose"), ("nginx", "Nginx"), ("aws", "AWS EC2"),
        ("railway", "Railway"), ("vercel", "Vercel"), ("githubactions", "GitHub Actions"), ("pytest", "pytest")]),
]


def skills():
    W = 1280
    lx, cx0, cx1 = 40, 336, 1240
    rows, y = [], 130
    for label, col, items in SKILLS:
        chips, x, ry = [], cx0, y
        for slug, name in items:
            w = 42 + len(name) * 7.6
            if x + w > cx1:
                x, ry = cx0, ry + 46
            chips.append((slug, name, x, ry, w))
            x += w + 8
        rows.append((label, col, chips, y, ry + 36))
        y = ry + 36 + 30
    H = y + 14
    css = """
.sweep{animation:sweep 5s ease-in-out infinite}@keyframes sweep{0%{transform:translateX(-200px)}60%,100%{transform:translateX(1100px)}}
.chip{animation:chip 4s ease-in-out infinite}@keyframes chip{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.flow{stroke-dasharray:4 8;animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}
.halo{animation:halo 2.4s ease-in-out infinite}@keyframes halo{0%,100%{r:6;opacity:.9}50%{r:11;opacity:.2}}
.in{animation:in .7s cubic-bezier(.2,.8,.2,1) both}@keyframes in{from{opacity:0;transform:translateX(-10px)}}
"""
    b = [panel(0, 0, W, H, 26)]
    b.append(f'<text x="40" y="58" class="tag" fill="{VIOLET}">// TECHNICAL SKILLS</text>'
             f'<text x="40" y="100" class="h2">Tools I use in production code</text>'
             f'<text x="{W-40}" y="100" text-anchor="end" class="mono" font-size="12" fill="{DIM}">every item is used in my repositories</text>')
    k = 0
    for label, col, chips, top, bottom in rows:
        mid = (top + min(bottom, top + 36)) / 2 + 0
        b.append(f'<clipPath id="row{k}"><rect x="{cx0-12}" y="{top-8}" width="{cx1-cx0+24}" height="{bottom-top+16}" rx="14"/></clipPath>')
        b.append(f'<rect x="{cx0-12}" y="{top-8}" width="{cx1-cx0+24}" height="{bottom-top+16}" rx="14" fill="#0b1222" stroke="#1e293b"/>'
                 f'<g clip-path="url(#row{k})"><rect class="sweep" style="animation-delay:{k*.7:.1f}s" x="{cx0-12}" y="{top-8}" width="160" height="{bottom-top+16}" fill="{col}" opacity=".10" transform="skewX(-20)"/></g>')
        b.append(f'<circle class="halo" style="animation-delay:{k*.3:.1f}s" cx="{lx+8}" cy="{top+18}" r="6" fill="none" stroke="{col}" stroke-width="2"/>'
                 f'<circle cx="{lx+8}" cy="{top+18}" r="4" fill="{col}"/>'
                 f'<text x="{lx+24}" y="{top+23}" class="tag" fill="{col}">{label}</text>'
                 f'<path class="flow" d="M{lx+24+len(label.replace("&amp;","&"))*9.6:.0f} {top+18}H{cx0-16}" stroke="{col}" stroke-width="1.6" fill="none" opacity=".7"/>')
        for j, (slug, name, x, ry, w) in enumerate(chips):
            b.append(f'<g class="in" style="animation-delay:{(k*6+j)*.04:.2f}s"><g class="chip" style="animation-delay:{(j%5)*.35:.2f}s">'
                     f'<rect x="{x:.1f}" y="{ry}" width="{w:.1f}" height="36" rx="10" fill="#0f172a" stroke="{col}" stroke-opacity=".4"/>'
                     + icon(slug, round(x + 12, 1), ry + 9, 18, fallback=name[0], color=None if slug in ICONS else col) +
                     f'<text x="{x+38:.1f}" y="{ry+23}" class="mono" font-size="12.5" fill="{TEXT}">{t(name)}</text></g></g>')
        k += 1
    return svg(W, H, "Technical skills", "".join(b), css)


# ---------------------------------------------------------------- more projects marquee

MORE = [
    ("LLM APP", CYAN, "Navigo Travel Planner", "LangGraph · Groq · PostgreSQL"),
    ("RAG", BLUE, "Medical Chatbot", "LangChain · Pinecone · Flask"),
    ("FINE-TUNING", VIOLET, "Falcon-7B QLoRA", "QLoRA · PEFT · Transformers"),
    ("FINE-TUNING", VIOLET, "LoRA Fine-Tuning", "LoRA · PEFT · TRL"),
    ("ALIGNMENT", PINK, "RLHF / DPO Training", "TRL · custom datasets"),
    ("LLM INFERENCE", CYAN, "Cache-Augmented Generation", "precomputed KV cache"),
    ("TEAM · ML", AMBER, "Amazon ML Challenge 2026", "entity resolution · transformers"),
    ("DEEP LEARNING", GREEN, "Argus Fraud Detection", "class-weighted neural net"),
    ("RECOMMENDER", PINK, "CineMind AI", "TF-IDF · hybrid ranking"),
    ("NLP", BLUE, "NLP Sentiment Analysis", "LR · SVM · LSTM · BiLSTM"),
]


def more_projects():
    W, H = 1280, 350
    cw, chh, gap = 296, 92, 16
    rows = [MORE[:5], MORE[5:]]
    setw = 5 * (cw + gap)
    css = f"""
.mq0{{animation:mq0 38s linear infinite}}@keyframes mq0{{to{{transform:translateX(-{setw}px)}}}}
.mq1{{animation:mq1 44s linear infinite}}@keyframes mq1{{from{{transform:translateX(-{setw}px)}}to{{transform:translateX(0)}}}}
.dotp{{animation:pulse 2s ease-in-out infinite}}
"""
    b = [panel(0, 0, W, H, 26)]
    b.append(f'<text x="40" y="58" class="tag" fill="{PINK}">// MORE PROJECTS</text>'
             f'<text x="40" y="100" class="h2">LLM apps, fine-tuning and machine learning</text>')
    b.append(f'<linearGradient id="fadeL" x1="0" x2="1"><stop offset="0" stop-color="#0c1220"/><stop offset="1" stop-color="#0c1220" stop-opacity="0"/></linearGradient>'
             f'<linearGradient id="fadeR" x1="1" x2="0"><stop offset="0" stop-color="#0d1117"/><stop offset="1" stop-color="#0d1117" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="mqclip"><rect x="2" y="120" width="{W-4}" height="222"/></clipPath>')
    b.append('<g clip-path="url(#mqclip)">')
    for r, items in enumerate(rows):
        y = 128 + r * (chh + 14)
        b.append(f'<g class="mq{r}">')
        for rep in range(3):
            for i, (cat, col, name, tech) in enumerate(items):
                x = 20 + rep * setw + i * (cw + gap)
                b.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{chh}" rx="14" fill="#0f172a" stroke="{col}" stroke-opacity=".45"/>'
                         f'<rect x="{x}" y="{y+16}" width="3" height="{chh-32}" rx="1.5" fill="{col}"/>'
                         f'<circle class="dotp" style="animation-delay:{(i*.4):.1f}s" cx="{x+cw-18}" cy="{y+18}" r="4" fill="{col}"/>'
                         f'<text x="{x+18}" y="{y+26}" class="mono" font-size="10.5" letter-spacing="2" font-weight="700" fill="{col}">{t(cat)}</text>'
                         f'<text x="{x+18}" y="{y+53}" font-size="16" font-weight="800" fill="{TEXT}">{t(name)}</text>'
                         f'<text x="{x+18}" y="{y+75}" class="mono" font-size="11.5" fill="{MUTED}">{t(tech)}</text>')
        b.append('</g>')
    b.append('</g>')
    b.append(f'<rect x="2" y="120" width="70" height="222" fill="url(#fadeL)"/><rect x="{W-72}" y="120" width="70" height="222" fill="url(#fadeR)"/>')
    return svg(W, H, "More projects", "".join(b), css)


# ---------------------------------------------------------------- section divider + footer

def divider(tag_text, title, col):
    W, H = 1280, 120
    css = """
.scanl{animation:scanl 4s ease-in-out infinite}@keyframes scanl{from{transform:translateX(-260px)}to{transform:translateX(1280px)}}
.blinkd{animation:pulse 1.6s ease-in-out infinite}
"""
    b = [panel(0, 0, W, H, 18),
         f'<circle class="blinkd" cx="40" cy="40" r="6" fill="{col}"/>',
         f'<text x="58" y="46" class="tag" fill="{col}">{t(tag_text)}</text>',
         f'<text x="40" y="88" font-size="30" font-weight="800" fill="{TEXT}">{t(title)}</text>',
         f'<rect x="40" y="104" width="{W-80}" height="2" rx="1" fill="#1e293b"/>',
         f'<clipPath id="dl"><rect x="40" y="100" width="{W-80}" height="10"/></clipPath>',
         f'<g clip-path="url(#dl)"><rect class="scanl" x="0" y="103" width="240" height="4" rx="2" fill="url(#brand)"/></g>']
    return svg(W, H, title, "".join(b), css)


def footer():
    W, H = 1280, 220
    css = """
.w1{animation:w 9s ease-in-out infinite alternate}.w2{animation:w 12s ease-in-out infinite alternate-reverse}
@keyframes w{to{transform:translateX(-160px)}}
.tw{animation:tw 3s ease-in-out infinite alternate}@keyframes tw{from{opacity:.2}to{opacity:1}}
"""
    b = [f'<clipPath id="fc"><rect x="0" y="0" width="{W}" height="{H}" rx="26"/></clipPath><g clip-path="url(#fc)">',
         f'<rect width="{W}" height="{H}" fill="url(#bg)"/>']
    for i in range(22):
        b.append(f'<circle class="tw" style="animation-delay:{(i*.37)%3:.2f}s" cx="{(i*157)%W}" cy="{18+(i*41)%110}" r="{1+(i%3)*.6:.1f}" fill="#e2e8f0"/>')
    b.append(f'<g class="w1"><path d="M0 150C160 110 320 190 480 150S800 110 960 150 1280 190 1440 150V220H0z" fill="{BLUE}" opacity=".35"/></g>'
             f'<g class="w2"><path d="M-160 170C0 140 160 210 320 170S640 140 800 170 1120 210 1280 170 1440 150 1440 170V220H-160z" fill="{CYAN}" opacity=".3"/></g>'
             f'<g class="w1"><path d="M0 195C200 175 400 215 600 195S1000 175 1200 195 1440 205 1440 195V220H0z" fill="{INDIGO}" opacity=".5"/></g>')
    b.append(f'<text x="{W/2}" y="70" text-anchor="middle" font-size="30" font-weight="800" fill="url(#brand)">Thanks for visiting</text>'
             f'<text x="{W/2}" y="104" text-anchor="middle" class="mono" font-size="15" letter-spacing="3" fill="{MUTED}">ALWAYS LEARNING · ALWAYS BUILDING</text>')
    b.append('</g>')
    return svg(W, H, "Thanks for visiting", "".join(b), css)


def main():
    mode, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    if mode == "static":
        for name, fn in [("hero", hero), ("projects", projects), ("skills", skills), ("more", more_projects), ("footer", footer),
                         ("div-activity", lambda: divider("// GITHUB ACTIVITY", "Live stats, contributions and the snake", GREEN))]:
            (out / f"{name}.svg").write_text(fn())
    elif mode == "dashboard":
        try:
            data = fetch_live()
        except Exception as exc:
            print("Using fallback dashboard data:", exc)
            data = FALLBACK
        (out / "dashboard.svg").write_text(dashboard(data))
    elif mode == "data":
        (out / "profile-data.json").write_text(json.dumps(fetch_public_data(), indent=1))
    else:
        raise SystemExit("mode must be 'static', 'dashboard' or 'data'")


if __name__ == "__main__":
    main()
