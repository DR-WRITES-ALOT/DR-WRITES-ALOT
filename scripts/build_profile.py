"""Build the animated, self-updating SVG panels used by README.md.

Stdlib only. Every panel is authored here so the profile is not dependent on a
third-party stats widget, a web font, JavaScript, or a runtime image service.
"""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta

from profile_data import ROOT, collect, esc, write_svg

# ------------------------------------------------------------------ palette --

BG = "#090d1b"          # deep blue-black
PANEL = "#10162a"       # raised terminal chrome
PANEL_2 = "#141d35"     # card surface
BORDER = "#273552"      # quiet hairline
GRID = "#15213a"        # empty contribution cell
MINT = "#8cf7d6"        # primary signal
LAVENDER = "#c9a8ff"    # dreamy secondary
PEACH = "#ffd6a7"       # warm highlight
BLUE = "#8ec9ff"        # cool highlight
WHITE = "#edf2ff"
MUTED = "#71809e"
RED = "#ff7898"
AMBER = "#ffd166"
LIME = "#78f3b0"
RAMP = [GRID, "#20345a", "#3e5f91", "#7087d8", MINT]
MONO = "'SFMono-Regular',ui-monospace,'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace"

WIDE = 860


def chrome(width: int, height: int, command: str, right: str = "") -> str:
    """Reusable terminal window chrome shared by every generated panel."""
    return f'''  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{width - 2}" height="40" rx="12" fill="{PANEL}"/>
  <rect x="1" y="28" width="{width - 2}" height="13" fill="{PANEL}"/>
  <line x1="1" y1="41" x2="{width - 1}" y2="41" stroke="{BORDER}" stroke-width="1.5"/>
  <circle cx="24" cy="21" r="6" fill="{RED}" opacity=".86"/>
  <circle cx="44" cy="21" r="6" fill="{AMBER}" opacity=".86"/>
  <circle cx="64" cy="21" r="6" fill="{LIME}" opacity=".86"/>
  <text x="78" y="26" font-size="13" fill="{MUTED}" font-family="{MONO}">{esc(command)}</text>
  {f'<text x="{width - 28}" y="26" text-anchor="end" font-size="12" fill="{MUTED}" font-family="{MONO}">{esc(right)}</text>' if right else ''}'''


def svg_style() -> str:
    return f'''<defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feComponentTransfer in="blur" result="soft"><feFuncA type="linear" slope=".55"/></feComponentTransfer>
      <feMerge><feMergeNode in="soft"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="scanlines" width="3" height="4" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="{MINT}" opacity=".035"/>
    </pattern>
  </defs>'''


# --------------------------------------------------------------------- hero --


def reveal_line(y: int, delay: float, segments: list[tuple[str, str, int]]) -> str:
    spans = "".join(
        f'<tspan fill="{color}"{weight_attr}>{esc(text)}</tspan>'
        for text, color, weight in segments
        for weight_attr in [f' font-weight="{weight}"' if weight else ""]
    )
    return f'''<g opacity="0">
    <animate attributeName="opacity" values="0;1" dur=".42s" begin="{delay}s" fill="freeze"/>
    <text x="30" y="{y}" font-size="17" font-family="{MONO}">{spans}</text>
  </g>'''


def build_hero(data: dict[str, object]) -> None:
    repos = data["repos"]
    followers = data["followers"]
    stars = data["stars"]
    lines = [
        reveal_line(88, .15, [("sreejith@vit", MINT, 700), (":", MUTED, 0), ("~", LAVENDER, 0), ("$ ", MUTED, 0), ("./whoami --proof", WHITE, 0)]),
        reveal_line(118, .55, [("[*] ", MUTED, 0), ("resolving identity ", WHITE, 0), ("·········· ", MUTED, 0), ("ok", MINT, 700)]),
        reveal_line(148, .95, [("role  ", MINT, 0), (" : ", MUTED, 0), ("computer science student · web developer", WHITE, 0)]),
        reveal_line(178, 1.35, [("base  ", MINT, 0), (" : ", MUTED, 0), ("VIT '29 · learning in public", WHITE, 0)]),
        reveal_line(208, 1.75, [("mode  ", MINT, 0), (" : ", MUTED, 0), ("local-first tools · web experiments · side quests", WHITE, 0)]),
        reveal_line(238, 2.15, [("proof ", MINT, 0), (" : ", MUTED, 0), ("SnapHarbor · FLOW · Unity", WHITE, 0)]),
        reveal_line(268, 2.55, [("[+] ", MINT, 0), ("profile loaded", MINT, 700), ("  ", MUTED, 0), (f"{repos} repos · {followers} followers · {stars}★", BLUE, 0)]),
    ]
    name_y = 337
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="378" viewBox="0 0 860 378" role="img" aria-labelledby="title desc">
  <title id="title">Sreejith SH — dreamy terminal profile</title>
  <desc id="desc">A moonlit terminal window introducing Sreejith SH, a VIT computer science student and aspiring web developer.</desc>
  {svg_style()}
  <defs><linearGradient id="horizon" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset=".5" stop-color="{LAVENDER}" stop-opacity=".3"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient></defs>
  {chrome(860, 378, 'sreejith@vit: ~/profile — zsh')}
  <circle cx="714" cy="113" r="135" fill="{LAVENDER}" opacity=".08" filter="url(#glow)"/>
  <circle cx="775" cy="98" r="64" fill="{PEACH}" opacity=".09" filter="url(#glow)"/>
  <rect x="1" y="42" width="858" height="86" fill="url(#horizon)" opacity=".34"/>
  <rect x="2" y="42" width="856" height="334" fill="url(#scanlines)"/>

  <!-- a single boot-time scan, followed by a quiet blinking cursor -->
  <g opacity="0">
    <animateTransform attributeName="transform" type="translate" values="-80 0;860 0" dur="2.5s" begin=".1s" fill="freeze"/>
    <animate attributeName="opacity" values="0;.5;.5;0" keyTimes="0;.08;.85;1" dur="2.5s" begin=".1s" fill="freeze"/>
    <rect x="0" y="42" width="58" height="334" fill="url(#horizon)"/>
  </g>

  {''.join(lines)}
  <g opacity="0">
    <animate attributeName="opacity" values="0;1" dur=".55s" begin="3.05s" fill="freeze"/>
    <text x="30" y="{name_y}" font-size="40" font-weight="700" fill="{MINT}" filter="url(#glow)" font-family="{MONO}">Sreejith SH</text>
    <text x="30" y="{name_y}" font-size="40" font-weight="700" fill="{MINT}" font-family="{MONO}">Sreejith SH<tspan fill="{MINT}"> █<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;.49;.5;1" dur="1.05s" begin="3.4s" repeatCount="indefinite"/></tspan></text>
    <text x="830" y="{name_y}" text-anchor="end" font-size="14" fill="{MUTED}" font-family="{MONO}">// DR-WRITES-ALOT · page 01</text>
  </g>
  <path d="M30 300 H830" stroke="url(#horizon)" stroke-opacity=".5" stroke-dasharray="3 8"/>
  <path d="M14 16 V8 H26 M846 350 V362 H834" fill="none" stroke="{MINT}" stroke-opacity=".45"/>
</svg>
'''
    write_svg("hero.svg", svg)


# --------------------------------------------------------------- banners ----


def build_banner(filename: str, title: str, subtitle: str) -> None:
    title = title.upper()
    start = 42 + len(title) * 13.2 + 28
    ticks = "".join(
        f'<line x1="{x}" y1="30" x2="{x}" y2="36" stroke="{MINT}" stroke-opacity=".26"/>'
        for x in range(int(start) + 18, 682, 26)
    )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="52" viewBox="0 0 860 52" role="img" aria-label="{esc(title)} {esc(subtitle)}">
  <text x="14" y="39" font-size="13" font-weight="700" fill="{MINT}" font-family="{MONO}">&gt;&gt;</text>
  <text x="42" y="39" font-size="20" font-weight="700" fill="{MINT}" font-family="{MONO}" letter-spacing="2">{esc(title)}</text>
  <line x1="{start:.1f}" y1="33" x2="682" y2="33" stroke="{MINT}" stroke-opacity=".23" stroke-width="1.5"/>
  {ticks}
  <rect x="694" y="26" width="9" height="9" fill="{PEACH}"><animate attributeName="opacity" values="1;.18;1" dur="1.6s" repeatCount="indefinite"/></rect>
  <text x="710" y="39" font-size="12" fill="{MUTED}" font-family="{MONO}">{esc(subtitle)}</text>
</svg>
'''
    write_svg(filename, svg)


def build_divider() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="24" viewBox="0 0 860 24" role="img" aria-label="animated data stream divider">
  <defs><linearGradient id="packet" x1="0" x2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset=".5" stop-color="{PEACH}"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient></defs>
  <line x1="0" y1="12" x2="860" y2="12" stroke="{MINT}" stroke-opacity=".18"/>
  <path d="M423 12 L430 5 L437 12 L430 19Z" fill="{BG}" stroke="{LAVENDER}" stroke-opacity=".75"/>
  <rect x="-90" y="10" width="90" height="3" fill="url(#packet)"><animate attributeName="x" values="-90;860;860" keyTimes="0;.72;1" dur="5s" repeatCount="indefinite"/></rect>
  <circle cx="112" cy="12" r="2" fill="{PEACH}"><animate attributeName="opacity" values=".25;1;.25" dur="2.8s" repeatCount="indefinite"/></circle>
  <circle cx="748" cy="12" r="2" fill="{LAVENDER}"><animate attributeName="opacity" values="1;.2;1" dur="2.1s" repeatCount="indefinite"/></circle>
</svg>
'''
    write_svg("divider.svg", svg)


# ------------------------------------------------------------------ cards ----

ICONS = {
    "anchor": '<path d="M430 32v82M398 64h64M390 114c8 31 27 46 40 46s32-15 40-46M389 114h-22M471 114h22" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><circle cx="430" cy="25" r="8" fill="none" stroke="currentColor" stroke-width="3"/>',
    "route": '<path d="M122 112c45-74 94 72 143-2 40-62 94-31 147-67" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-dasharray="9 8"/><circle cx="120" cy="112" r="9" fill="none" stroke="currentColor" stroke-width="3"/><path d="m406 37 9 6-7 9" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>',
    "drone": '<path d="M360 86h140l-18 34H378zM384 120v24m92-24v24M344 78h-35m192 0h35" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"/><circle cx="300" cy="78" r="14" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="580" cy="78" r="14" fill="none" stroke="currentColor" stroke-width="3"/><path d="M360 86 314 78m186 8 46-8" fill="none" stroke="currentColor" stroke-width="3"/>',
}


def chip(x: float, y: int, text: str, accent: str = MINT) -> tuple[str, float]:
    width = max(42, len(text) * 7.2 + 18)
    markup = f'''<rect x="{x:.1f}" y="{y}" width="{width:.1f}" height="20" rx="4" fill="{accent}" fill-opacity=".08" stroke="{accent}" stroke-opacity=".55"/>
  <text x="{x + width / 2:.1f}" y="{y + 14}" text-anchor="middle" font-size="11" fill="{accent}" font-family="{MONO}">{esc(text)}</text>'''
    return markup, x + width + 8


def build_card(filename: str, index: str, project: dict[str, object], data: dict[str, object]) -> None:
    repo_name = str(project["repo"]).split("/")[-1]
    repo = data["repo_by_name"].get(repo_name, {})
    star_chip = f"{int(repo.get('stargazers_count', 0) or 0)}★"
    tags = [star_chip] + list(project["tags"])
    chips = ""
    x = 92.0
    for tag_index, tag in enumerate(tags):
        color = BLUE if tag_index == 0 else MINT
        rendered, x = chip(x, 131, str(tag), color)
        chips += rendered

    icon = ICONS[str(project["icon"])].replace("currentColor", MINT)
    gradient_id = f"sweep{index}"
    clip_id = f"clip{index}"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="174" viewBox="0 0 860 174" role="img" aria-label="{esc(project['name'])} — {esc(project['brief'])}">
  <defs>
    <linearGradient id="{gradient_id}" x1="0" x2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset=".5" stop-color="{MINT}" stop-opacity=".07"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient>
    <clipPath id="{clip_id}"><rect x="1" y="1" width="858" height="172" rx="11"/></clipPath>
    <filter id="iconGlow"><feGaussianBlur stdDeviation="3"/></filter>
  </defs>
  <rect x="1" y="1" width="858" height="172" rx="11" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="2" y="2" width="5" height="168" fill="{MINT}"><animate attributeName="opacity" values=".9;.35;.9" dur="3s" repeatCount="indefinite"/></rect>
  <g opacity=".16" filter="url(#iconGlow)" fill="none" stroke="{LAVENDER}" stroke-width="5">{icon}</g>
  <g opacity=".10" fill="none" stroke="{MINT}" stroke-width="2">{icon}</g>
  <text x="34" y="90" font-size="48" font-weight="700" fill="{MINT}" fill-opacity=".13" font-family="{MONO}">{esc(index)}</text>
  <text x="92" y="50" font-size="22" font-weight="700" fill="{MINT}" font-family="{MONO}">{esc(project['name'])}</text>
  <text x="92" y="72" font-size="12" fill="{MUTED}" font-family="{MONO}">› github.com/{esc(project['repo'])}</text>
  <text x="92" y="98" font-size="13" fill="{WHITE}" font-family="{MONO}">{esc(project['brief'][0])}</text>
  <text x="92" y="116" font-size="13" fill="{WHITE}" font-family="{MONO}">{esc(project['brief'][1])}</text>
  {chips}
  <text x="830" y="28" text-anchor="end" font-size="11" fill="{PEACH}" font-family="{MONO}">{esc(project['status'])}</text>
  <path d="M14 16 V8 H26 M846 150 V162 H834" fill="none" stroke="{MINT}" stroke-opacity=".52"/>
  <g clip-path="url(#{clip_id})"><rect x="-210" y="1" width="210" height="172" fill="url(#{gradient_id})"><animate attributeName="x" values="-210;860;860" keyTimes="0;.62;1" dur="6s" begin="{int(index) * 1.1}s" repeatCount="indefinite"/></rect></g>
</svg>
'''
    write_svg(filename, svg)


def build_cards(data: dict[str, object]) -> None:
    projects = [
        {
            "name": "SnapHarbor",
            "repo": "DR-WRITES-ALOT/SnapHarbor",
            "brief": ("local-first photo + video vault with smart SHA-256 deduplication,", "device sync, timeline galleries, and automation that stays on your machine."),
            "tags": ["typescript", "rust + tauri", "sqlite"],
            "icon": "anchor",
            "status": "DESKTOP / V1",
        },
        {
            "name": "FLOW",
            "repo": "DR-WRITES-ALOT/FLOW",
            "brief": ("deterministic transit simulation that watches connection confidence", "and recovers a safer route before the journey falls apart."),
            "tags": ["next.js", "typescript", "prisma"],
            "icon": "route",
            "status": "WEB / LIVE DEMO",
        },
        {
            "name": "rapid response · drone mapper",
            "repo": "DR-WRITES-ALOT/rapid-response-dronemapper",
            "brief": ("hackathon vision tool that turns aerial imagery into severity", "scores, hazard summaries, GPS-aware maps, and rapid incident awareness."),
            "tags": ["python", "streamlit", "gemma 4"],
            "icon": "drone",
            "status": "HACKATHON / FIELD",
        },
    ]
    for index, project in enumerate(projects, start=1):
        build_card(f"card_{['snapharbor', 'flow', 'drone_mapper'][index - 1]}.svg", f"0{index}", project, data)


# ------------------------------------------------------------------- stats --


def build_stats(data: dict[str, object]) -> None:
    languages = list(data["languages"])
    while len(languages) < 5:
        languages.append(("—", 0))
    bars = []
    for index, (language, percentage) in enumerate(languages[:5]):
        y = 157 + index * 23
        width = round(220 * int(percentage) / 100) if percentage else 0
        bars.append(
            f'<text x="20" y="{y + 12}" font-size="13" fill="{WHITE}" font-family="{MONO}">{esc(str(language).lower()[:13])}</text>'
            f'<rect x="132" y="{y}" width="220" height="14" rx="3" fill="{GRID}"/>'
            f'<rect x="132" y="{y}" width="{width}" height="14" rx="3" fill="{MINT}"/>'
            f'<text x="360" y="{y + 12}" font-size="12" fill="{BLUE}" font-family="{MONO}">{int(percentage)}%</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="430" height="300" viewBox="0 0 430 300" role="img" aria-label="live stats: {data['stars']} stars, {data['repos']} repositories, {data['followers']} followers">
  {chrome(430, 300, '~/stats $ ./metrics --live')}
  <text x="78" y="86" text-anchor="middle" font-size="30" font-weight="700" fill="{MINT}" font-family="{MONO}">{data['stars']}★</text><text x="78" y="104" text-anchor="middle" font-size="11" fill="{MUTED}" font-family="{MONO}">stars</text>
  <text x="215" y="86" text-anchor="middle" font-size="30" font-weight="700" fill="{MINT}" font-family="{MONO}">{data['repos']}</text><text x="215" y="104" text-anchor="middle" font-size="11" fill="{MUTED}" font-family="{MONO}">repos</text>
  <text x="352" y="86" text-anchor="middle" font-size="30" font-weight="700" fill="{MINT}" font-family="{MONO}">{data['followers']}</text><text x="352" y="104" text-anchor="middle" font-size="11" fill="{MUTED}" font-family="{MONO}">followers</text>
  <line x1="20" y1="124" x2="410" y2="124" stroke="{BORDER}"/>
  <text x="20" y="146" font-size="12" fill="{MUTED}" font-family="{MONO}">// language distribution</text>
  {''.join(bars)}
  <text x="20" y="286" font-size="11" fill="{MUTED}" font-family="{MONO}">last sync · {esc(data['generated'])}</text>
</svg>
'''
    write_svg("stats.svg", svg)


# --------------------------------------------------------------------- ops --


def build_ops(data: dict[str, object]) -> None:
    activity = list(data["activity"])
    if not activity:
        activity = [{"date": "", "action": "quiet", "repo": "—", "message": "no recent public activity"}]
    while len(activity) < 7:
        activity.append({"date": "", "action": "—", "repo": "—", "message": "waiting for the next signal"})
    rows = []
    for index, item in enumerate(activity[:7]):
        y = 60 + index * 31
        mmdd = str(item.get("date", ""))[5:] or "--"
        rows.append(
            f'<text x="20" y="{y}" font-size="13" font-family="{MONO}"><tspan fill="{MUTED}">[{esc(mmdd)}] </tspan><tspan fill="{MINT}">{esc(item.get("action", "—"))} </tspan><tspan fill="{WHITE}">{esc(item.get("repo", "—"))}</tspan></text>'
            f'<text x="78" y="{y + 15}" font-size="11" fill="{MUTED}" font-family="{MONO}">{esc(item.get("message", ""))}</text>'
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="430" height="300" viewBox="0 0 430 300" role="img" aria-label="recent public activity feed">
  {chrome(430, 300, '~/ops $ tail activity.log')}
  {''.join(rows)}
  <circle cx="26" cy="282" r="4" fill="{MINT}"><animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/></circle>
  <text x="38" y="286" font-size="11" fill="{MUTED}" font-family="{MONO}">live · rebuilt {esc(data['generated_date'])}</text>
</svg>
'''
    write_svg("ops.svg", svg)


# --------------------------------------------------------------- contrib ----


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
    max_col = (latest - sunday).days // 7
    cutoff = max(0, max_col - 52)
    cells: list[tuple[int, int, int]] = []
    for cell, current in parsed:
        column = (current - sunday).days // 7 - cutoff
        if 0 <= column <= 52:
            row = (current.weekday() + 1) % 7
            cells.append((column, row, int(cell.get("level", 0) or 0)))

    months: list[tuple[int, str]] = []
    seen: set[tuple[int, int]] = set()
    for _, current in sorted(parsed, key=lambda pair: pair[1]):
        column = (current - sunday).days // 7 - cutoff
        key = (current.year, current.month)
        if 0 <= column <= 52 and key not in seen:
            seen.add(key)
            months.append((column, current.strftime("%b").lower()))
    return cells, months


def build_contrib(data: dict[str, object]) -> None:
    cell, gap, gx, gy, cols, period = 11, 3, 44, 60, 53, 8.0
    stride = cell + gap
    cells, months = grid_from_calendar(list(data["calendar"]))
    if not cells:
        cells = [(column, row, 0) for column in range(cols) for row in range(7)]
    max_column = max((item[0] for item in cells), default=52)
    sweep_width = max_column * stride + cell
    width, height = 806, 208

    base = []
    reveal = []
    for column, row, level in cells:
        x, y = gx + column * stride, gy + row * stride
        base.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{GRID}"/>')
        if level > 0:
            begin = round((column / max(max_column, 1)) * period * .84, 3)
            reveal.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{RAMP[min(level, 4)]}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1;0;0" keyTimes="0;.03;.46;1" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/></rect>'
            )

    month_labels = "".join(
        f'<text x="{gx + column * stride}" y="52" font-size="9" fill="{MUTED}" font-family="{MONO}">{esc(label)}</text>'
        for column, label in months
    )
    week_labels = "".join(
        f'<text x="{gx - 8}" y="{gy + row * stride + cell - 1}" text-anchor="end" font-size="9" fill="{MUTED}" font-family="{MONO}">{label}</text>'
        for row, label in ((1, "mon"), (3, "wed"), (5, "fri"))
    )
    legend_x = 606
    legend = f'<text x="{legend_x}" y="194" font-size="10" fill="{MUTED}" font-family="{MONO}">less</text>' + "".join(
        f'<rect x="{legend_x + 30 + index * 15}" y="185" width="11" height="11" rx="2" fill="{RAMP[index + 1]}"/>'
        for index in range(4)
    ) + f'<text x="{legend_x + 94}" y="194" font-size="10" fill="{MUTED}" font-family="{MONO}">more</text>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="806" height="208" viewBox="0 0 806 208" role="img" aria-label="contribution chart scanned by a sweep line: {data['contrib_total']} active days">
  <defs>
    <linearGradient id="beam" x1="0" x2="1"><stop offset="0" stop-color="{MINT}" stop-opacity="0"/><stop offset=".5" stop-color="{MINT}" stop-opacity=".9"/><stop offset="1" stop-color="{MINT}" stop-opacity="0"/></linearGradient>
    <pattern id="crt" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="{MINT}" opacity=".045"/></pattern>
    <clipPath id="gridclip"><rect x="{gx - 4}" y="{gy - 4}" width="{sweep_width + 8}" height="106"/></clipPath>
  </defs>
  {chrome(806, 208, '~/contrib $ ./scan --year', f"{data['contrib_total']} active days")}
  {month_labels}
  {week_labels}
  <g>{''.join(base)}</g>
  <g clip-path="url(#gridclip)">
    {''.join(reveal)}
    <g>
      <animateTransform attributeName="transform" type="translate" values="0 0;{sweep_width} 0;{sweep_width} 0" keyTimes="0;.85;1" dur="{period}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values=".9;.9;0;0" keyTimes="0;.85;.86;1" dur="{period}s" repeatCount="indefinite"/>
      <rect x="{gx - 10}" y="{gy - 4}" width="21" height="103" fill="url(#beam)"/>
      <line x1="{gx + 1}" y1="{gy - 4}" x2="{gx + 1}" y2="{gy + 98}" stroke="#e3fff6" stroke-width="1.3"/>
    </g>
  </g>
  <rect x="{gx - 4}" y="{gy - 4}" width="{sweep_width + 8}" height="106" fill="url(#crt)"/>
  <path d="M34 68 V54 H48 M793 146 V160 H779" fill="none" stroke="{MINT}" stroke-opacity=".5"/>
  {legend}
</svg>
'''
    write_svg("contrib.svg", svg)


# ------------------------------------------------------------------- stack --


def hex_path(cx: float, cy: float, radius: float) -> str:
    points = []
    for degree in range(0, 360, 60):
        radians = math.radians(degree)
        points.append((cx + radius * math.sin(radians), cy - radius * math.cos(radians)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"


def build_stack() -> None:
    tech = [
        ("C", "C"), ("C++", "C++"), ("Java", "JV"), ("Python", "Py"), ("TypeScript", "TS"), ("JavaScript", "JS"),
        ("React", "R"), ("Rust", "Rs"), ("Tauri", "T"), ("Unity", "U"), ("SQL", "DB"), ("Git", "G"),
    ]
    width, height, radius = 820, 312, 31
    xs = [80 + index * 132 for index in range(6)]
    ys = [105, 222]
    wires = []
    badges = []
    for index, (label, glyph) in enumerate(tech):
        x, y = xs[index % 6], ys[index // 6]
        if index % 6 < 5:
            wires.append(f'<line x1="{x + radius}" y1="{y}" x2="{xs[index % 6 + 1] - radius}" y2="{y}" stroke="{MINT}" stroke-opacity=".16" stroke-dasharray="3 5"/>')
        color = [MINT, LAVENDER, PEACH, BLUE][index % 4]
        path = hex_path(x, y, radius)
        badges.append(
            f'''<g><animate attributeName="opacity" values="1;.5;1;.78;1" keyTimes="0;.12;.28;.68;1" dur="3.8s" begin="{(index * .29):.2f}s" repeatCount="indefinite"/>
  <path d="{path}" fill="{color}" fill-opacity=".07" stroke="{color}" stroke-opacity=".72" stroke-width="1.5"/>
  <path d="{path}" fill="none" stroke="{color}" stroke-opacity=".18" stroke-width="5" filter="url(#stackGlow)"/>
  <text x="{x}" y="{y + 5}" text-anchor="middle" font-size="15" font-weight="700" fill="{color}" font-family="{MONO}">{esc(glyph)}</text>
  <text x="{x}" y="{y + 51}" text-anchor="middle" font-size="11" fill="{MUTED}" font-family="{MONO}">{esc(label)}</text></g>'''
        )
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="312" viewBox="0 0 820 312" role="img" aria-label="developer loadout: C, C++, Java, Python, TypeScript, JavaScript, React, Rust, Tauri, Unity, SQL, and Git">
  <defs><filter id="stackGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter><linearGradient id="stackSweep" x1="0" x2="0" y1="0" y2="1"><stop stop-color="{LAVENDER}" stop-opacity="0"/><stop offset=".5" stop-color="{LAVENDER}" stop-opacity=".12"/><stop offset="1" stop-color="{LAVENDER}" stop-opacity="0"/></linearGradient></defs>
  {chrome(820, 312, '~/stack $ ./loadout --modules', '12 modules online')}
  {''.join(wires)}
  {''.join(badges)}
  <rect x="2" y="42" width="816" height="50" fill="url(#stackSweep)" opacity=".5"><animate attributeName="y" values="42;250;42" dur="7s" repeatCount="indefinite"/></rect>
  <path d="M18 60 V50 H30 M802 282 V292 H790" fill="none" stroke="{MINT}" stroke-opacity=".45"/>
</svg>
'''
    write_svg("stack.svg", svg)


# ----------------------------------------------------------------- contact --


def build_contact() -> None:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="174" viewBox="0 0 860 174" role="img" aria-labelledby="title desc">
  <title id="title">Sreejith SH contact console</title>
  <desc id="desc">A terminal-style contact card for GitHub and LinkedIn.</desc>
  {chrome(860, 174, '~/contact $ cat signal.txt')}
  <text x="30" y="72" font-size="16" font-family="{MONO}"><tspan fill="{MINT}" font-weight="700">github   </tspan><tspan fill="{MUTED}">: </tspan><tspan fill="{WHITE}">@DR-WRITES-ALOT</tspan></text>
  <text x="30" y="101" font-size="16" font-family="{MONO}"><tspan fill="{LAVENDER}" font-weight="700">linkedin </tspan><tspan fill="{MUTED}">: </tspan><tspan fill="{WHITE}">/sreejith-s-h-810803243</tspan></text>
  <text x="30" y="130" font-size="16" font-family="{MONO}"><tspan fill="{PEACH}" font-weight="700">status   </tspan><tspan fill="{MUTED}">: </tspan><tspan fill="{WHITE}">open to good questions, experiments, and collaboration</tspan></text>
  <text x="830" y="151" text-anchor="end" font-size="12" fill="{MUTED}" font-family="{MONO}">// no inbox automation · say hello</text>
</svg>
'''
    write_svg("contact.svg", svg)


def main() -> None:
    data = collect()
    print("== rebuilding Sreejith's profile console ==")
    build_hero(data)
    build_banner("banner_work.svg", "selected work", "// 3 dossiers")
    build_banner("banner_telemetry.svg", "telemetry", "// live · self-rebuilding")
    build_banner("banner_stack.svg", "loadout", "// 12 modules")
    build_banner("banner_contact.svg", "whois", "// reach")
    build_divider()
    build_cards(data)
    build_stats(data)
    build_ops(data)
    build_contrib(data)
    build_stack()
    build_contact()
    print("== profile console ready ==")


if __name__ == "__main__":
    main()
