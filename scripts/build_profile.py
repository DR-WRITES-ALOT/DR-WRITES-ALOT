"""Generate an original moonlit-atlas profile system for README.md.

The output is intentionally image-led: every visual is a local SVG generated
from public GitHub data, so the profile feels authored rather than assembled
from external widgets.
"""

from __future__ import annotations

import math
from datetime import date, timedelta

from profile_data import collect, esc, write_svg

# A warm celestial palette: dreamy, but with enough contrast to feel like a
# designed portfolio rather than a collection of badges.
NIGHT = "#0c0a22"
INK = "#181437"
PANEL = "#211b4c"
PANEL_2 = "#2b235b"
LINE = "#514375"
TEXT = "#f6f1ff"
MUTED = "#b7acce"
LILAC = "#c7a7ff"
PINK = "#f4a9c5"
GOLD = "#ffd69a"
ICE = "#a9ddff"
MINT = "#a9f3d4"
RAMP = ["#19143a", "#332864", "#55458f", "#8d70cf", LILAC]
SERIF = "Georgia,'Times New Roman',serif"
SANS = "'Avenir Next','Segoe UI',Arial,sans-serif"
MONO = "'SFMono-Regular',ui-monospace,'JetBrains Mono',Consolas,monospace"


def common_defs() -> str:
    return f'''<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{NIGHT}"/><stop offset=".58" stop-color="#211842"/><stop offset="1" stop-color="#4d2859"/></linearGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#302866" stop-opacity=".9"/><stop offset="1" stop-color="#1a153b" stop-opacity=".9"/></linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff1bf"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
  <linearGradient id="rose" x1="0" y1="0" x2="1" y2="0"><stop stop-color="{PINK}"/><stop offset="1" stop-color="{LILAC}"/></linearGradient>
  <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <style>
    .twinkle {{ animation: twinkle 3.8s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .twinkle.alt {{ animation-delay: -1.4s; }}
    .twinkle.late {{ animation-delay: -2.7s; }}
    .float {{ animation: float 6s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .float.alt {{ animation-delay: -2.3s; }}
    .float.late {{ animation-delay: -4.1s; }}
    .orbit {{ animation: orbit 18s linear infinite; transform-box: fill-box; transform-origin: 700px 176px; }}
    .orbit.slow {{ animation-duration: 28s; animation-direction: reverse; }}
    .reveal {{ animation: reveal 1.1s ease-out both; }}
    .reveal.late {{ animation-delay: .22s; }}
    .pulse {{ animation: pulse 3.2s ease-in-out infinite; transform-box: fill-box; transform-origin: center; }}
    .pulse.alt {{ animation-delay: -1.6s; }}
    @keyframes twinkle {{ 0%,100% {{ opacity:.28; transform:scale(.7); }} 48% {{ opacity:1; transform:scale(1.22); }} }}
    @keyframes float {{ 0%,100% {{ transform:translateY(0) rotate(0deg); }} 50% {{ transform:translateY(-7px) rotate(1deg); }} }}
    @keyframes orbit {{ to {{ transform:rotate(360deg); }} }}
    @keyframes reveal {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.42; transform:scale(.86); }} 50% {{ opacity:1; transform:scale(1.08); }} }}
    @media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ animation-duration:.001ms !important; animation-iteration-count:1 !important; }} }}
  </style>
</defs>'''


def starfield() -> str:
    stars = [
        (46, 48, 2.2, ""), (98, 116, 1.5, "alt"), (171, 40, 1.8, "late"),
        (244, 101, 2.1, "alt"), (315, 52, 1.4, ""), (389, 126, 1.7, "late"),
        (480, 39, 2.1, "alt"), (547, 92, 1.5, ""), (602, 43, 1.8, "late"),
        (805, 45, 1.5, ""), (853, 119, 2.1, "alt"), (52, 305, 1.6, "late"),
        (200, 347, 1.8, ""), (422, 322, 1.5, "alt"), (558, 354, 2.1, "late"),
        (833, 328, 1.6, "alt"),
    ]
    result = []
    for index, (x, y, radius, variant) in enumerate(stars):
        shape = f'<path d="M{x} {y - radius * 2.5} l{radius * .7} {radius * 1.8} l{radius * 1.8} {radius * .7} l-{radius * 1.8} {radius * .7} l-{radius * .7} {radius * 1.8} l-{radius * .7} -{radius * 1.8} l-{radius * 1.8} -{radius * .7} l{radius * 1.8} -{radius * .7}z" fill="{GOLD}" class="twinkle {variant}" style="animation-delay:-{(index % 7) * .37:.2f}s"/>'
        result.append(shape)
    return "\n  ".join(result)


# ---------------------------------------------------------------------- hero


def build_hero(data: dict[str, object]) -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="420" viewBox="0 0 900 420" role="img" aria-labelledby="title desc">
  <title id="title">Sreejith SH — moonlit atlas</title>
  <desc id="desc">A celestial editorial hero introducing Sreejith SH, a VIT computer science student and aspiring web developer.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="416" rx="30" fill="url(#sky)" stroke="#806ca8" stroke-opacity=".55" stroke-width="2"/>
  <circle cx="162" cy="80" r="118" fill="{PINK}" opacity=".08" filter="url(#blur)"/>
  <circle cx="760" cy="342" r="160" fill="{LILAC}" opacity=".12" filter="url(#blur)"/>
  <circle cx="615" cy="16" r="100" fill="{ICE}" opacity=".06" filter="url(#blur)"/>
  <g aria-hidden="true">{starfield()}</g>
  <path d="M48 270 C165 220 255 302 362 251 S557 220 650 266 S789 313 866 247" fill="none" stroke="url(#rose)" stroke-opacity=".28" stroke-width="1.5" stroke-dasharray="2 10"/>
  <path d="M80 210 L171 168 L244 205 L315 139 L389 176" fill="none" stroke="{ICE}" stroke-opacity=".24" stroke-width="1"/>
  <g fill="{GOLD}" class="pulse"><circle cx="80" cy="210" r="3"/><circle cx="171" cy="168" r="2.5"/><circle cx="244" cy="205" r="3"/><circle cx="315" cy="139" r="2.5"/><circle cx="389" cy="176" r="3"/></g>

  <g class="reveal" transform="translate(58 55)">
    <text x="0" y="0" fill="{GOLD}" font-size="11" font-weight="700" letter-spacing="2.7" font-family="{MONO}">FIELD NOTE 01 / 04 · SREEJITH SH</text>
    <text x="0" y="76" fill="{TEXT}" font-size="48" font-weight="700" font-family="{SERIF}">Building small worlds</text>
    <text x="0" y="130" fill="url(#rose)" font-size="48" font-weight="700" font-family="{SERIF}">with curious edges.</text>
    <text x="0" y="174" fill="{TEXT}" opacity=".9" font-size="17" font-family="{SANS}">Computer Science student at VIT ’29 · aspiring web developer</text>
    <text x="0" y="202" fill="{MUTED}" font-size="15" font-family="{SANS}">Turning questions into interfaces, tools, simulations, and side quests.</text>
    <rect x="0" y="230" width="187" height="30" rx="15" fill="#ffffff" fill-opacity=".07" stroke="{PINK}" stroke-opacity=".52"/>
    <text x="93.5" y="250" text-anchor="middle" fill="{TEXT}" font-size="12" font-weight="600" font-family="{SANS}">web · systems · wonder</text>
    <text x="0" y="310" fill="{MUTED}" font-size="11" letter-spacing="1" font-family="{MONO}">DR-WRITES-ALOT / 2026</text>
  </g>

  <g transform="translate(700 177)" aria-hidden="true">
    <ellipse rx="143" ry="68" fill="none" stroke="{LILAC}" stroke-opacity=".25" stroke-width="1.5" transform="rotate(-18)"/>
    <ellipse rx="116" ry="49" fill="none" stroke="{ICE}" stroke-opacity=".2" stroke-width="1" transform="rotate(33)"/>
    <circle r="68" fill="url(#gold)" filter="url(#glow)" class="float"/>
    <circle cx="25" cy="-21" r="68" fill="#2b2352"/>
    <circle cx="-21" cy="22" r="7" fill="#d3b68d" opacity=".27"/>
    <circle cx="-38" cy="-20" r="4" fill="#d3b68d" opacity=".23"/>
    <circle cx="12" cy="31" r="3" fill="#d3b68d" opacity=".3"/>
    <g class="orbit"><circle cx="143" cy="0" r="7" fill="{PINK}" stroke="{TEXT}" stroke-opacity=".7"/></g>
    <g class="orbit slow"><circle cx="-116" cy="0" r="5" fill="{ICE}"/></g>
    <path d="M-8 91 q18 13 36 0" fill="none" stroke="{GOLD}" stroke-opacity=".65" stroke-width="1.5"/>
    <text x="0" y="118" text-anchor="middle" fill="{MUTED}" font-size="11" letter-spacing="1.7" font-family="{MONO}">MOONLIT ATLAS</text>
  </g>
  <path d="M30 386 H870" stroke="url(#rose)" stroke-opacity=".38"/>
  <circle cx="449" cy="386" r="4" fill="{GOLD}" class="twinkle"/>
</svg>
'''
    write_svg("atlas-hero.svg", svg)


# ------------------------------------------------------------------- divider


def build_divider() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="34" viewBox="0 0 900 34" role="img" aria-label="animated constellation divider">
  <defs><linearGradient id="trail" x1="0" x2="1"><stop stop-color="{PINK}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD}"/><stop offset="1" stop-color="{LILAC}" stop-opacity="0"/></linearGradient></defs>
  <path d="M0 17 C150 4 250 30 370 17 S620 4 900 17" fill="none" stroke="url(#trail)" stroke-width="1.5" stroke-dasharray="2 12"><animate attributeName="stroke-dashoffset" from="0" to="-220" dur="9s" repeatCount="indefinite"/></path>
  <path d="M440 17 l10 -8 10 8-10 8z" fill="{NIGHT}" stroke="{GOLD}" stroke-opacity=".8"/>
  <circle cx="130" cy="14" r="2" fill="{ICE}" class="twinkle"/><circle cx="770" cy="21" r="2" fill="{PINK}" class="twinkle alt"/>
</svg>
'''
    write_svg("atlas-divider.svg", svg)


# ---------------------------------------------------------------- field notes


def build_field_notes() -> None:
    cards = [
        (38, "NOW", "SnapHarbor", "local-first media tools", PINK),
        (318, "NEXT", "Unity mechanics", "loops · physics · C#", LILAC),
        (598, "WANDERING", "FLOW", "simulations · route recovery", GOLD),
    ]
    card_svg = []
    for x, label, title, subtitle, color in cards:
        card_svg.append(f'''<g class="float" style="animation-delay:-{(x / 300):.1f}s">
    <rect x="{x}" y="84" width="264" height="105" rx="18" fill="#ffffff" fill-opacity=".055" stroke="{color}" stroke-opacity=".35"/>
    <circle cx="{x + 24}" cy="111" r="6" fill="{color}" class="pulse"/>
    <text x="{x + 41}" y="116" fill="{color}" font-size="10" font-weight="700" letter-spacing="1.5" font-family="{MONO}">{label}</text>
    <text x="{x + 20}" y="149" fill="{TEXT}" font-size="20" font-weight="700" font-family="{SERIF}">{title}</text>
    <text x="{x + 20}" y="171" fill="{MUTED}" font-size="12" font-family="{SANS}">{subtitle}</text>
  </g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="220" viewBox="0 0 900 220" role="img" aria-labelledby="title desc">
  <title id="title">Current orbit</title><desc id="desc">Current focus, next milestone, and wandering experiments.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="216" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <circle cx="850" cy="26" r="80" fill="{LILAC}" opacity=".09" filter="url(#blur)"/>
  <text x="38" y="39" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">CURRENT ORBIT</text>
  <text x="38" y="65" fill="{TEXT}" font-size="23" font-weight="700" font-family="{SERIF}">What is moving through the workshop</text>
  {''.join(card_svg)}
</svg>
'''
    write_svg("atlas-field-notes.svg", svg)


# ---------------------------------------------------------------- projects

ICONS = {
    "harbor": '<path d="M450 54v54M426 77h48M411 111c8 28 24 42 39 42s31-14 39-42M410 111h-24M474 111h24" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="450" cy="48" r="8" fill="none" stroke="currentColor" stroke-width="4"/>',
    "flow": '<path d="M255 118c42-62 79 52 124-4 36-45 83-31 124-69" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="250" cy="122" r="10" fill="none" stroke="currentColor" stroke-width="4"/><path d="m490 42 13 4-7 12" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>',
    "drone": '<path d="M405 86h90l-12 32h-66zM420 118v23m60-23v23M395 86l-42-13m152 13 42-13" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><circle cx="339" cy="70" r="14" fill="none" stroke="currentColor" stroke-width="4"/><circle cx="561" cy="70" r="14" fill="none" stroke="currentColor" stroke-width="4"/>',
}


def chip_row(tags: list[str], y: int) -> str:
    rendered = []
    x = 190
    colors = [ICE, MINT, LILAC, GOLD]
    for index, tag in enumerate(tags):
        width = max(48, len(tag) * 7.1 + 20)
        color = colors[index % len(colors)]
        rendered.append(f'<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="22" rx="11" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".45"/><text x="{x + width / 2:.1f}" y="{y + 15}" text-anchor="middle" fill="{color}" font-size="11" font-family="{SANS}">{esc(tag)}</text>')
        x += width + 8
    return "".join(rendered)


def build_project(filename: str, index: str, project: dict[str, object], data: dict[str, object]) -> None:
    repo_name = str(project["repo"]).split("/")[-1]
    repo = data["repo_by_name"].get(repo_name, {})
    stars = int(repo.get("stargazers_count", 0) or 0)
    icon = ICONS[str(project["icon"])].replace("currentColor", str(project["color"]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="196" viewBox="0 0 900 196" role="img" aria-label="{esc(project['name'])} — {esc(project['accessible'])}">
  {common_defs()}
  <rect x="2" y="2" width="896" height="192" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <path d="M3 34 Q180 2 360 28 T710 20 T897 30 V3 H3Z" fill="{project['color']}" opacity=".06"/>
  <circle cx="87" cy="98" r="58" fill="{project['color']}" fill-opacity=".07" stroke="{project['color']}" stroke-opacity=".38" stroke-width="1.5"/>
  <circle cx="87" cy="98" r="70" fill="none" stroke="{project['color']}" stroke-opacity=".18" stroke-dasharray="2 10" class="orbit"/>
  <g fill="none" stroke="{project['color']}" stroke-width="3" opacity=".25" filter="url(#blur)">{icon}</g>
  <g fill="none" stroke="{project['color']}" stroke-width="3">{icon}</g>
  <text x="34" y="38" fill="{project['color']}" font-size="11" font-weight="700" letter-spacing="2" font-family="{MONO}">{esc(index)} / {esc(project['category'])}</text>
  <text x="190" y="57" fill="{TEXT}" font-size="27" font-weight="700" font-family="{SERIF}">{esc(project['name'])}</text>
  <text x="190" y="82" fill="{MUTED}" font-size="12" font-family="{MONO}">github.com/{esc(project['repo'])}</text>
  <text x="190" y="111" fill="{TEXT}" font-size="14" font-family="{SANS}">{esc(project['brief'][0])}</text>
  <text x="190" y="131" fill="{TEXT}" font-size="14" font-family="{SANS}">{esc(project['brief'][1])}</text>
  {chip_row([f'{stars} stars'] + list(project['tags']), 151)}
  <text x="860" y="38" text-anchor="end" fill="{project['color']}" font-size="10" font-weight="700" letter-spacing="1.5" font-family="{MONO}">{esc(project['status'])}</text>
  <circle cx="838" cy="165" r="3" fill="{GOLD}" class="twinkle"/><circle cx="855" cy="153" r="2" fill="{ICE}" class="twinkle alt"/>
</svg>
'''
    write_svg(filename, svg)


def build_projects(data: dict[str, object]) -> None:
    projects = [
        {
            "filename": "atlas-project-snapharbor.svg", "index": "01", "name": "SnapHarbor", "repo": "DR-WRITES-ALOT/SnapHarbor", "category": "DESKTOP TOOL", "icon": "harbor", "color": PINK, "status": "LOCAL-FIRST / V1",
            "brief": ("A local-first media vault for photos and video,", "with SHA-256 dedupe, device sync, and calm automation."), "tags": ["TypeScript", "Rust + Tauri", "SQLite"], "accessible": "a local-first photo and video vault with smart deduplication and automation",
        },
        {
            "filename": "atlas-project-flow.svg", "index": "02", "name": "FLOW", "repo": "DR-WRITES-ALOT/FLOW", "category": "WEB EXPERIMENT", "icon": "flow", "color": LILAC, "status": "LIVE DEMO / ROUTES",
            "brief": ("A deterministic transit simulation that watches", "connection confidence and recovers a safer route."), "tags": ["Next.js", "TypeScript", "Prisma"], "accessible": "a deterministic transit simulation with proactive route recovery",
        },
        {
            "filename": "atlas-project-drone.svg", "index": "03", "name": "Rapid Response Drone Mapper", "repo": "DR-WRITES-ALOT/rapid-response-dronemapper", "category": "HACKATHON FIELD NOTE", "icon": "drone", "color": GOLD, "status": "GEMMA 4 / VISION",
            "brief": ("A vision tool that turns aerial imagery into", "severity scores, maps, and incident awareness."), "tags": ["Python", "Streamlit", "Gemma 4"], "accessible": "an AI-assisted disaster assessment tool for drone imagery",
        },
    ]
    for project in projects:
        build_project(str(project["filename"]), str(project["index"]), project, data)


# ---------------------------------------------------------------- observatory


def build_observatory(data: dict[str, object]) -> None:
    languages = list(data["languages"])
    while len(languages) < 4:
        languages.append(("—", 0))
    metrics = [("REPOSITORIES", data["repos"], PINK), ("FOLLOWERS", data["followers"], LILAC), ("STARS", data["stars"], GOLD), ("ACTIVE DAYS", data["contrib_total"], ICE)]
    metric_svg = []
    for index, (label, value, color) in enumerate(metrics):
        x = 40 + index * 208
        metric_svg.append(f'''<g class="float" style="animation-delay:-{index * .7:.1f}s"><rect x="{x}" y="73" width="184" height="76" rx="18" fill="#ffffff" fill-opacity=".05" stroke="{color}" stroke-opacity=".28"/><text x="{x + 22}" y="111" fill="{color}" font-size="30" font-weight="700" font-family="{SERIF}">{esc(value)}</text><text x="{x + 22}" y="131" fill="{MUTED}" font-size="10" letter-spacing="1.3" font-family="{MONO}">{label}</text><circle cx="{x + 155}" cy="94" r="5" fill="{color}" class="pulse"/></g>''')
    bars = []
    for index, (language, percentage) in enumerate(languages[:4]):
        y = 183 + index * 23
        width = round(360 * int(percentage) / 100) if percentage else 0
        bars.append(f'<text x="40" y="{y + 12}" fill="{TEXT}" font-size="12" font-family="{SANS}">{esc(str(language))}</text><rect x="135" y="{y}" width="360" height="10" rx="5" fill="#171333"/><rect x="135" y="{y}" width="{width}" height="10" rx="5" fill="url(#rose)"/><text x="510" y="{y + 10}" fill="{ICE}" font-size="11" font-family="{MONO}">{int(percentage)}%</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="286" viewBox="0 0 900 286" role="img" aria-labelledby="title desc">
  <title id="title">GitHub observatory</title><desc id="desc">Live profile metrics and language distribution generated from public GitHub data.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="282" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <text x="40" y="39" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">PROFILE OBSERVATORY</text>
  <text x="40" y="62" fill="{TEXT}" font-size="23" font-weight="700" font-family="{SERIF}">A few numbers from the night sky</text>
  <text x="860" y="40" text-anchor="end" fill="{MUTED}" font-size="11" font-family="{MONO}">updated {esc(data['generated_date'])}</text>
  {''.join(metric_svg)}
  <path d="M40 164 H860" stroke="{LINE}" stroke-opacity=".65"/>
  <text x="40" y="176" fill="{MUTED}" font-size="10" letter-spacing="1.4" font-family="{MONO}">LANGUAGE CONSTELLATION · BY CODE VOLUME</text>
  {''.join(bars)}
  <circle cx="820" cy="238" r="32" fill="none" stroke="{LILAC}" stroke-opacity=".18"/><circle cx="820" cy="238" r="5" fill="{GOLD}" class="twinkle"/><path d="M786 250 Q820 218 854 250" fill="none" stroke="{PINK}" stroke-opacity=".35"/>
</svg>
'''
    write_svg("atlas-observatory.svg", svg)


# ---------------------------------------------------------------- activity


def build_activity(data: dict[str, object]) -> None:
    activity = list(data["activity"])
    if not activity:
        activity = [{"date": "", "action": "quiet", "repo": "—", "message": "no recent public activity"}]
    activity = activity[:6]
    rows = []
    for index, item in enumerate(activity):
        y = 74 + index * 28
        date_label = str(item.get("date", ""))[5:] or "--"
        action = str(item.get("action", "note"))
        color = [PINK, LILAC, GOLD, ICE, MINT, PINK][index % 6]
        rows.append(f'''<g class="reveal" style="animation-delay:{index * .08:.2f}s"><circle cx="68" cy="{y - 4}" r="6" fill="{color}" class="pulse"/><text x="91" y="{y}" fill="{MUTED}" font-size="11" font-family="{MONO}">{esc(date_label)}</text><rect x="145" y="{y - 15}" width="60" height="20" rx="10" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-opacity=".35"/><text x="175" y="{y - 1}" text-anchor="middle" fill="{color}" font-size="10" font-family="{MONO}">{esc(action)}</text><text x="227" y="{y}" fill="{TEXT}" font-size="13" font-weight="600" font-family="{SANS}">{esc(item.get('repo', '—'))}</text><text x="410" y="{y}" fill="{MUTED}" font-size="12" font-family="{SANS}">{esc(item.get('message', ''))}</text></g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="248" viewBox="0 0 900 248" role="img" aria-labelledby="title desc">
  <title id="title">Recent movements</title><desc id="desc">A timeline of recent public GitHub activity.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="244" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <text x="40" y="39" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">RECENT MOVEMENTS</text>
  <text x="40" y="62" fill="{TEXT}" font-size="23" font-weight="700" font-family="{SERIF}">The latest signals from the workshop</text>
  <path d="M68 76 V{82 + max(0, len(activity) - 1) * 28}" stroke="{LINE}" stroke-width="2"/>
  {''.join(rows)}
  <text x="860" y="226" text-anchor="end" fill="{MUTED}" font-size="10" font-family="{MONO}">public activity · refreshed {esc(data['generated_date'])}</text>
</svg>
'''
    write_svg("atlas-activity.svg", svg)


# --------------------------------------------------------------- contribution


def grid_from_calendar(calendar: list[dict[str, object]]) -> tuple[list[tuple[int, int, int]], list[tuple[int, str]]]:
    parsed: list[tuple[dict[str, object], date]] = []
    for cell in calendar:
        try:
            parsed.append((cell, date.fromisoformat(str(cell["date"]))))
        except (KeyError, ValueError):
            continue
    if not parsed:
        return [], []
    first = min(item[1] for item in parsed)
    sunday = first - timedelta(days=(first.weekday() + 1) % 7)
    latest = max(item[1] for item in parsed)
    maximum = (latest - sunday).days // 7
    cutoff = max(0, maximum - 52)
    cells = []
    for cell, current in parsed:
        column = (current - sunday).days // 7 - cutoff
        if 0 <= column <= 52:
            cells.append((column, (current.weekday() + 1) % 7, int(cell.get("level", 0) or 0)))
    months, seen = [], set()
    for _, current in sorted(parsed, key=lambda item: item[1]):
        column = (current - sunday).days // 7 - cutoff
        key = (current.year, current.month)
        if 0 <= column <= 52 and key not in seen:
            seen.add(key)
            months.append((column, current.strftime("%b").lower()))
    return cells, months


def build_contributions(data: dict[str, object]) -> None:
    cell, gap, stride, gx, gy = 11, 3, 14, 92, 80
    cells, months = grid_from_calendar(list(data["calendar"]))
    if not cells:
        cells = [(column, row, 0) for column in range(53) for row in range(7)]
    base, active = [], []
    for column, row, level in cells:
        x, y = gx + column * stride, gy + row * stride
        base.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="#19143a"/>')
        if level:
            begin = (column / 52) * 7.2
            active.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{RAMP[min(level, 4)]}" opacity=".45"><animate attributeName="opacity" values=".35;1;.5;.35" dur="3.7s" begin="-{begin:.2f}s" repeatCount="indefinite"/></rect>')
    month_text = "".join(f'<text x="{gx + column * stride}" y="66" fill="{MUTED}" font-size="9" font-family="{MONO}">{esc(label)}</text>' for column, label in months)
    week_text = "".join(f'<text x="{gx - 9}" y="{gy + row * stride + 9}" text-anchor="end" fill="{MUTED}" font-size="9" font-family="{MONO}">{label}</text>' for row, label in ((1, "mon"), (3, "wed"), (5, "fri")))
    legend = ''.join(f'<rect x="{650 + index * 16}" y="235" width="11" height="11" rx="3" fill="{RAMP[index + 1]}"/>' for index in range(4))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="274" viewBox="0 0 900 274" role="img" aria-labelledby="title desc">
  <title id="title">Contribution constellation</title><desc id="desc">An animated calendar of public contribution days.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="270" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <text x="40" y="39" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">CONTRIBUTION CONSTELLATION</text>
  <text x="40" y="62" fill="{TEXT}" font-size="23" font-weight="700" font-family="{SERIF}">Every small signal still belongs to the map</text>
  <text x="860" y="40" text-anchor="end" fill="{ICE}" font-size="11" font-family="{MONO}">{data['contrib_total']} active days</text>
  {month_text}{week_text}
  <path d="M90 157 C240 96 370 213 520 145 S720 103 842 158" fill="none" stroke="{PINK}" stroke-opacity=".13" stroke-width="1" stroke-dasharray="2 8"/>
  <g>{''.join(base)}</g><g>{''.join(active)}</g>
  <path d="M82 74 V178 H842" fill="none" stroke="{LILAC}" stroke-opacity=".18"/>
  <text x="606" y="244" fill="{MUTED}" font-size="10" font-family="{MONO}">quiet</text>{legend}<text x="723" y="244" fill="{MUTED}" font-size="10" font-family="{MONO}">bright</text>
</svg>
'''
    write_svg("atlas-contributions.svg", svg)


# --------------------------------------------------------------------- stack


def build_stack() -> None:
    rows = [
        ("LANGUAGES", [(116, "C", "systems"), (296, "C++", "systems"), (476, "Java", "systems"), (656, "Python", "data")], PINK),
        ("WEB + UI", [(116, "TypeScript", "interfaces"), (296, "JavaScript", "motion"), (476, "React", "components"), (656, "Next.js", "routes")], LILAC),
        ("BUILD + PLAY", [(116, "Rust", "native"), (296, "Tauri", "desktop"), (476, "Unity", "physics"), (656, "SQL · Git", "ship it")], GOLD),
    ]
    lane_svg = []
    for row_index, (label, nodes, color) in enumerate(rows):
        y = 117 + row_index * 82
        lane_svg.append(f'<text x="40" y="{y + 5}" fill="{color}" font-size="9" letter-spacing="1.4" font-family="{MONO}">{label}</text>')
        for node_index, (x, name, sub) in enumerate(nodes):
            if node_index < len(nodes) - 1:
                lane_svg.append(f'<path d="M{x + 63} {y} C{x + 86} {y - 18} {x + 98} {y + 18} {x + 117} {y}" fill="none" stroke="{color}" stroke-opacity=".28" stroke-dasharray="3 5"/>')
            lane_svg.append(f'<g class="float" style="animation-delay:-{(row_index + node_index) * .45:.2f}s"><rect x="{x - 56}" y="{y - 24}" width="112" height="48" rx="24" fill="#ffffff" fill-opacity=".055" stroke="{color}" stroke-opacity=".42"/><circle cx="{x - 34}" cy="{y}" r="6" fill="{color}" class="pulse"/><text x="{x - 20}" y="{y + 4}" fill="{TEXT}" font-size="12" font-weight="600" font-family="{SANS}">{esc(name)}</text><text x="{x - 20}" y="{y + 19}" fill="{MUTED}" font-size="9" font-family="{SANS}">{esc(sub)}</text></g>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="332" viewBox="0 0 900 332" role="img" aria-labelledby="title desc">
  <title id="title">Constellation of tools</title><desc id="desc">A connected map of languages, web tools, and building tools.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="328" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <circle cx="836" cy="26" r="84" fill="{LILAC}" opacity=".08" filter="url(#blur)"/>
  <text x="40" y="39" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">CONSTELLATION OF TOOLS</text>
  <text x="40" y="65" fill="{TEXT}" font-size="23" font-weight="700" font-family="{SERIF}">The things I use to give ideas a shape</text>
  <path d="M40 82 H860" stroke="{LINE}"/>
  {''.join(lane_svg)}
  <path d="M40 292 C180 266 316 306 470 282 S720 264 860 292" fill="none" stroke="url(#rose)" stroke-opacity=".3" stroke-dasharray="2 9"/>
</svg>
'''
    write_svg("atlas-stack.svg", svg)


# ------------------------------------------------------------------- contact


def build_contact() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="210" viewBox="0 0 900 210" role="img" aria-labelledby="title desc">
  <title id="title">Coordinates for a hello</title><desc id="desc">Contact information for Sreejith SH through GitHub and LinkedIn.</desc>
  {common_defs()}
  <rect x="2" y="2" width="896" height="206" rx="24" fill="url(#glass)" stroke="{LINE}" stroke-width="2"/>
  <g transform="translate(112 104)" aria-hidden="true">
    <circle r="64" fill="{PINK}" fill-opacity=".08" stroke="{PINK}" stroke-opacity=".42"/>
    <ellipse rx="84" ry="28" fill="none" stroke="{LILAC}" stroke-opacity=".4" transform="rotate(-20)"/>
    <g class="orbit"><circle cx="84" cy="0" r="6" fill="{GOLD}"/></g>
    <path d="M-30 -15 Q0 -40 30 -15 V20 Q0 43 -30 20Z" fill="none" stroke="{TEXT}" stroke-opacity=".85" stroke-width="2"/>
    <path d="M-29 -14 L0 8 29 -14" fill="none" stroke="{TEXT}" stroke-opacity=".85" stroke-width="2"/>
  </g>
  <text x="220" y="52" fill="{GOLD}" font-size="10" font-weight="700" letter-spacing="2.4" font-family="{MONO}">COORDINATES FOR A HELLO</text>
  <text x="220" y="84" fill="{TEXT}" font-size="27" font-weight="700" font-family="{SERIF}">Bring a question. Leave a constellation.</text>
  <text x="220" y="116" fill="{MUTED}" font-size="14" font-family="{SANS}">The best routes are usually the ones that begin with curiosity.</text>
  <text x="220" y="151" fill="{PINK}" font-size="13" font-weight="700" font-family="{MONO}">GITHUB</text><text x="306" y="151" fill="{TEXT}" font-size="13" font-family="{MONO}">@DR-WRITES-ALOT</text>
  <text x="220" y="177" fill="{LILAC}" font-size="13" font-weight="700" font-family="{MONO}">LINKEDIN</text><text x="306" y="177" fill="{TEXT}" font-size="13" font-family="{MONO}">/sreejith-s-h-810803243</text>
</svg>
'''
    write_svg("atlas-contact.svg", svg)


def main() -> None:
    data = collect()
    print("== building moonlit atlas profile ==")
    build_hero(data)
    build_divider()
    build_field_notes()
    build_projects(data)
    build_observatory(data)
    build_activity(data)
    build_contributions(data)
    build_stack()
    build_contact()
    print("== moonlit atlas ready ==")


if __name__ == "__main__":
    main()
