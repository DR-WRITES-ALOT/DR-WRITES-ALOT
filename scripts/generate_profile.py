import os
import random
import requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
GITHUB_API_URL = "https://api.github.com"
USERNAME = "DR-WRITES-ALOT"
BG_COLOR = "#0D1117"
CYAN = "#00FFFF"
GREEN = "#00FF66"

def get_github_stats():
    stats = {
        "stars": 0,
        "commits": 0,
        "repos": 0,
        "followers": 0,
        "langs": {"Python": 40, "JavaScript": 30, "HTML": 20, "CSS": 10}
    }

    if not GITHUB_TOKEN:
        print("Warning: GITHUB_TOKEN not found. Using default stats.")
        return stats

    try:
        user_response = requests.get(f"{GITHUB_API_URL}/users/{USERNAME}", headers=HEADERS)
        if user_response.status_code == 200:
            user_data = user_response.json()
            stats["followers"] = user_data.get("followers", 0)
            stats["repos"] = user_data.get("public_repos", 0)

        repos_response = requests.get(f"{GITHUB_API_URL}/users/{USERNAME}/repos?per_page=100", headers=HEADERS)
        if repos_response.status_code == 200:
            repos_data = repos_response.json()
            stats["stars"] = sum(repo.get("stargazers_count", 0) for repo in repos_data)

            # Accurate commits calculation (basic summation of public repos)
            # A full accurate count requires GraphQL API or traversing all commits, but we can approximate via the API if needed.
            # GitHub's REST API doesn't easily expose total commits.
            # A common workaround for Profile READMEs without GraphQL is searching commits.
            commit_res = requests.get(f"{GITHUB_API_URL}/search/commits?q=author:{USERNAME}", headers=HEADERS)
            if commit_res.status_code == 200:
                stats["commits"] = commit_res.json().get("total_count", 0)

            lang_counts = {}
            for repo in repos_data:
                lang = repo.get("language")
                if lang:
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1

            if lang_counts:
                total = sum(lang_counts.values())
                stats["langs"] = {k: (v/total)*100 for k, v in lang_counts.items()}

    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")

    return stats

def generate_hero_svg():
    svg = f"""<svg width="840" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: {BG_COLOR}; }}
      .title {{ font-family: 'Courier New', Courier, monospace; font-size: 64px; font-weight: bold; fill: {GREEN}; filter: drop-shadow(0 0 10px {GREEN}) drop-shadow(0 0 20px {GREEN}); }}
      .sub {{ font-family: 'Courier New', Courier, monospace; font-size: 16px; fill: #8b949e; }}

      @keyframes float {{
        0% {{ transform: translateY(-20px); opacity: 0; }}
        50% {{ opacity: 1; }}
        100% {{ transform: translateY(100px); opacity: 0; }}
      }}
      .float-char {{ font-family: monospace; font-size: 14px; font-weight: bold; opacity: 0; }}

      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      .cursor-block {{ animation: blink 1s step-end infinite; fill: {GREEN}; filter: drop-shadow(0 0 10px {GREEN}); }}

      /* Base reveal animation for subtitle */
      @keyframes reveal {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
      .reveal {{ animation: reveal 0.1s forwards; opacity: 0; }}
    </style>
  </defs>
  <rect class="bg" width="100%" height="100%" rx="10" stroke="#1f2937" stroke-width="2"/>
"""
    colors = [CYAN, GREEN, "#ff007f", "#ffff00", "#bd93f9"]
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#%&"
    for i in range(40):
        x = random.randint(20, 800)
        y = random.randint(20, 150)
        char = random.choice(chars)
        color = random.choice(colors)
        delay = random.uniform(0, 3)
        duration = random.uniform(2, 5)
        if char == '&': char = '&amp;'
        elif char == '<': char = '&lt;'
        elif char == '>': char = '&gt;'

        svg += f'  <text x="{x}" y="{y}" fill="{color}" class="float-char" style="animation: float {duration}s linear {delay}s infinite;">{char}</text>\n'

    name = "DR-WRITES-ALOT"
    char_width = 39.5
    text_width = len(name) * char_width
    start_x = 80
    cursor_x = start_x + text_width + 15

    svg += f'  <text x="{start_x}" y="150" class="title" text-anchor="start">{name}</text>\n'
    svg += f'  <rect x="{cursor_x}" y="100" width="30" height="60" class="cursor-block" />\n'

    subtitle = "Algorithmic Developer & Full-Stack Engineer in Training"
    svg += '  <text x="750" y="210" class="sub" text-anchor="end">\n'
    svg += '    // DR-WRITES-ALOT • '
    for i, char in enumerate(subtitle):
        delay = 0.5 + (i * 0.05)
        if char in '<>&':
            char = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        svg += f'    <tspan class="reveal" style="animation-delay: {delay}s;">{char}</tspan>'
    svg += '  </text>\n'
    svg += "</svg>"
    with open("assets/hero.svg", "w") as f:
        f.write(svg)


def generate_terminal_svg():
    svg = f"""<svg width="840" height="220" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: #0a0a0f; }}
      .text {{ font-family: 'Courier New', Courier, monospace; font-size: 15px; fill: #ffffff; }}
      .prompt {{ fill: {GREEN}; font-weight: bold; filter: drop-shadow(0 0 2px {GREEN}); }}
      .cmd {{ fill: #ffffff; }}
      .keyword {{ fill: {CYAN}; filter: drop-shadow(0 0 2px {CYAN}); }}
      .bracket {{ fill: #ff007f; font-weight: bold; }}
      .mac-btn {{ rx: 6; ry: 6; width: 12px; height: 12px; }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      .cursor {{ animation: blink 1s step-end infinite; fill: {CYAN}; }}
      @keyframes typeLine {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
      .line1 {{ animation: typeLine 0.1s forwards; }}
      .line2 {{ opacity: 0; animation: typeLine 0.1s 0.5s forwards; }}
      .line3 {{ opacity: 0; animation: typeLine 0.1s 1.0s forwards; }}
      .line4 {{ opacity: 0; animation: typeLine 0.1s 1.5s forwards; }}
      .line5 {{ opacity: 0; animation: typeLine 0.1s 2.0s forwards; }}
      .line6 {{ opacity: 0; animation: typeLine 0.1s 2.5s forwards; }}
    </style>
  </defs>
  <rect width="840" height="220" rx="10" class="bg" stroke="#1f2937" stroke-width="2"/>
  <rect width="840" height="35" rx="10" fill="#111827" />
  <rect y="15" width="840" height="20" fill="#111827" />
  <line x1="0" y1="35" x2="840" y2="35" stroke="#30363d" stroke-width="1"/>
  <rect class="mac-btn" x="15" y="11" fill="#ff5f56" />
  <rect class="mac-btn" x="35" y="11" fill="#ffbd2e" />
  <rect class="mac-btn" x="55" y="11" fill="#27c93f" />
  <text x="420" y="22" fill="#8b949e" font-family="monospace" font-size="13" text-anchor="middle">dr-writes-alot@linux: ~/profile</text>
  <g transform="translate(20, 70)" class="text">
    <text y="0" class="line1"><tspan class="prompt">dr-writes-alot@linux:~/profile $</tspan> <tspan class="cmd">./whoami --proof</tspan></text>
    <text y="25" class="line2"><tspan class="bracket">[</tspan><tspan fill="#ffbd2e">*</tspan><tspan class="bracket">]</tspan> resolving identity ......... <tspan class="keyword">ok</tspan></text>
    <text y="50" class="line3"><tspan class="keyword">role </tspan> : software-developer . dsa-practitioner . fullstack-learner</text>
    <text y="75" class="line4"><tspan class="keyword">mode </tspan> : builds clean logic, learning scalable web architecture</text>
    <text y="100" class="line5"><tspan class="keyword">stack</tspan> : C . C++ . Java . Python</text>
    <text y="125" class="line6"><tspan class="bracket">[</tspan><tspan class="prompt">+</tspan><tspan class="bracket">]</tspan> access granted <rect x="155" y="113" width="10" height="15" class="cursor"/></text>
  </g>
</svg>"""
    with open("assets/terminal.svg", "w") as f:
        f.write(svg)


def generate_stats_svg(stats):
    langs = stats.get("langs", {"Python": 100})
    sorted_langs = sorted(langs.items(), key=lambda item: item[1], reverse=True)[:4]

    segments = ""
    current_x = 180
    total_width = 580
    colors = [GREEN, "#00cc55", "#009944", "#006622"]

    for i, (lang, percentage) in enumerate(sorted_langs):
        width = (percentage / 100) * total_width
        color = colors[i % len(colors)]
        segments += '    <rect fill="' + color + '" x="' + str(current_x) + '" y="-12" width="' + str(width) + '" height="20" filter="drop-shadow(0 0 5px ' + color + ')" class="progress"/>\n'
        current_x += width

    svg_template = '''<svg width="840" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: #0a0a0f; }}
      .title {{ font-family: 'Courier New', Courier, monospace; font-size: 22px; font-weight: bold; fill: {green}; filter: drop-shadow(0 0 5px {green}); }}
      .label {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; fill: #8b949e; text-transform: uppercase; }}
      .val {{ font-family: 'Courier New', Courier, monospace; font-size: 36px; font-weight: bold; fill: {cyan}; filter: drop-shadow(0 0 5px {cyan}); }}

      @keyframes loadBar {{ 0% {{ transform: scaleX(0); }} 100% {{ transform: scaleX(1); }} }}
      .progress {{ transform-origin: left center; animation: loadBar 1.5s ease-out forwards; }}
      .progress-bg {{ fill: #1f2937; }}
    </style>
  </defs>

  <rect width="840" height="200" rx="10" class="bg" stroke="#1f2937" stroke-width="2"/>

  <text x="30" y="45" class="title">SYSTEM_TELEMETRY.log</text>
  <line x1="30" y1="55" x2="810" y2="55" stroke="#1f2937" stroke-width="2"/>

  <!-- Stats Grid -->
  <g transform="translate(70, 110)">
    <text class="val" x="0" y="0">{stars}</text>
    <text class="label" x="0" y="25">TOTAL STARS</text>

    <text class="val" x="220" y="0">{commits}</text>
    <text class="label" x="220" y="25">COMMITS</text>

    <text class="val" x="420" y="0">{repos}</text>
    <text class="label" x="420" y="25">REPOSITORIES</text>

    <text class="val" x="620" y="0">{followers}</text>
    <text class="label" x="620" y="25">FOLLOWERS</text>
  </g>

  <!-- Language Progress Bar -->
  <g transform="translate(70, 175)">
    <text class="label" x="0" y="3">STACK DISTRIBUTION</text>
    <rect class="progress-bg" x="180" y="-12" width="580" height="20" />
{segments}
  </g>
</svg>'''

    svg = svg_template.format(
        green=GREEN,
        cyan=CYAN,
        stars=stats['stars'],
        commits=stats['commits'],
        repos=stats['repos'],
        followers=stats['followers'],
        segments=segments
    )

    with open("assets/stats.svg", "w") as f:
        f.write(svg)


def main():
    print("Starting matrix profile generation...")
    os.makedirs("assets", exist_ok=True)

    stats = get_github_stats()

    generate_hero_svg()
    generate_terminal_svg()
    generate_stats_svg(stats)

    print("Successfully generated Matrix SVGs in assets/")

if __name__ == "__main__":
    main()
