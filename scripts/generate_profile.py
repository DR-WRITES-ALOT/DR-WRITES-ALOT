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
        "stars": 12,
        "commits": 450,
        "repos": 5,
        "followers": 2,
        "top_langs": ["C", "C++", "Python", "Java"]
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

        stats["commits"] = "800+"

    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")

    return stats

def generate_hero_svg():
    # Big, blocky, highly legible ascii art
    ascii_art = [
        r" ___  ___   _      __ ___  ___  ___  ___  ___    _    _    ___  ___ ",
        r"|   \| _ \ | |    / /| _ \|_ _||_ _|| __|/ __|  /_\  | |  / _ \|_ _|",
        r"| |) |   / | |__ / / |   / | |  | | | _| \__ \ / _ \ | |_| (_) || | ",
        r"|___/|_|_\ |____/_/  |_|_\ |___ |___|___||___//_/ \_\|____\___/ |_| "
    ]

    svg = f"""<svg width="840" height="250" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: {BG_COLOR}; }}
      .ascii {{ font-family: 'Courier New', Courier, monospace; font-size: 16px; font-weight: 900; fill: {GREEN}; letter-spacing: 1px; filter: drop-shadow(0 0 8px {GREEN}); }}
      .sub {{ font-family: 'Courier New', Courier, monospace; font-size: 20px; font-weight: bold; fill: {CYAN}; letter-spacing: 6px; filter: drop-shadow(0 0 8px {CYAN}); }}

      @keyframes float {{
        0% {{ transform: translateY(-20px); opacity: 0; }}
        50% {{ opacity: 1; }}
        100% {{ transform: translateY(100px); opacity: 0; }}
      }}
      .float-char {{ font-family: monospace; font-size: 14px; font-weight: bold; opacity: 0; }}

      /* Matrix Glitch Animation */
      @keyframes glitch-anim-1 {{
        0% {{ clip-path: inset(20% 0 80% 0); transform: translate(-2px, 1px); }}
        20% {{ clip-path: inset(60% 0 10% 0); transform: translate(2px, -1px); }}
        40% {{ clip-path: inset(40% 0 50% 0); transform: translate(-2px, 2px); }}
        60% {{ clip-path: inset(80% 0 5% 0); transform: translate(2px, -2px); }}
        80% {{ clip-path: inset(10% 0 70% 0); transform: translate(-1px, 1px); }}
        100% {{ clip-path: inset(30% 0 50% 0); transform: translate(1px, -1px); }}
      }}
      @keyframes glitch-anim-2 {{
        0% {{ clip-path: inset(10% 0 60% 0); transform: translate(2px, -1px); }}
        20% {{ clip-path: inset(30% 0 20% 0); transform: translate(-2px, 1px); }}
        40% {{ clip-path: inset(70% 0 10% 0); transform: translate(2px, -2px); }}
        60% {{ clip-path: inset(20% 0 50% 0); transform: translate(-2px, 2px); }}
        80% {{ clip-path: inset(50% 0 30% 0); transform: translate(1px, -1px); }}
        100% {{ clip-path: inset(5% 0 80% 0); transform: translate(-1px, 1px); }}
      }}

      .glitch-layer {{ opacity: 0; }}
      .glitch-container:hover .glitch-layer {{ opacity: 0.8; }}
      .glitch-container .glitch-layer:nth-child(2) {{ animation: glitch-anim-1 2s infinite linear alternate-reverse; fill: {CYAN}; }}
      .glitch-container .glitch-layer:nth-child(3) {{ animation: glitch-anim-2 3s infinite linear alternate-reverse; fill: #ff007f; }}

      /* Base reveal animation for subtitle */
      @keyframes reveal {{ 0% {{ opacity: 0; }} 100% {{ opacity: 1; }} }}
      .reveal {{ animation: reveal 0.1s forwards; opacity: 0; }}
    </style>
  </defs>
  <rect class="bg" width="100%" height="100%" rx="10" />
"""
    # Background floating characters
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

    # Glitch Container for ASCII art
    svg += '  <g transform="translate(60, 70)" class="glitch-container">\n'

    # We render the ASCII art 3 times: Base layer, Glitch 1, Glitch 2
    for layer in range(3):
        layer_class = "ascii" if layer == 0 else "ascii glitch-layer"
        svg += f'    <g class="{layer_class}">\n'
        y_offset = 0
        for line in ascii_art:
            svg += f'      <text x="0" y="{y_offset}" text-anchor="start" xml:space="preserve">\n'
            # Escaping for XML
            line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            svg += f'        {line}\n'
            svg += '      </text>\n'
            y_offset += 20
        svg += '    </g>\n'

    svg += '  </g>\n'

    # Subtitle with typing effect
    subtitle = "Software Developer"
    svg += '  <text x="420" y="220" class="sub" text-anchor="middle">\n'
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
    svg = f"""<svg width="840" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .bg {{ fill: #0a0a0f; }}
      .title {{ font-family: 'Courier New', Courier, monospace; font-size: 16px; font-weight: bold; fill: {GREEN}; filter: drop-shadow(0 0 3px {GREEN}); }}
      .label {{ font-family: 'Courier New', Courier, monospace; font-size: 14px; fill: #8b949e; text-transform: uppercase; }}
      .val {{ font-family: 'Courier New', Courier, monospace; font-size: 32px; font-weight: bold; fill: {CYAN}; filter: drop-shadow(0 0 5px {CYAN}); }}

      @keyframes loadBar {{ 0% {{ transform: scaleX(0); }} 100% {{ transform: scaleX(1); }} }}
      .progress {{ fill: {GREEN}; filter: drop-shadow(0 0 4px {GREEN}); transform-origin: left center; animation: loadBar 1.5s ease-out forwards; }}
      .progress-bg {{ fill: #1f2937; }}

      @keyframes pulse {{ 0% {{ opacity: 0.7; }} 50% {{ opacity: 1; }} 100% {{ opacity: 0.7; }} }}
      .pulse {{ animation: pulse 2s infinite; }}
    </style>
  </defs>

  <rect width="840" height="200" rx="10" class="bg" stroke="#1f2937" stroke-width="2"/>

  <text x="20" y="30" class="title">SYSTEM_TELEMETRY.log</text>
  <line x1="20" y1="40" x2="820" y2="40" stroke="#1f2937" stroke-width="2"/>

  <!-- Stats Grid -->
  <g transform="translate(60, 90)">
    <text class="val pulse" x="0" y="0">{stats['stars']}</text>
    <text class="label" x="0" y="25">Total Stars</text>

    <text class="val pulse" x="180" y="0">{stats['commits']}</text>
    <text class="label" x="180" y="25">Commits</text>

    <text class="val pulse" x="360" y="0">{stats['repos']}</text>
    <text class="label" x="360" y="25">Repositories</text>

    <text class="val pulse" x="540" y="0">{stats['followers']}</text>
    <text class="label" x="540" y="25">Followers</text>
  </g>

  <!-- Language Progress Bar (Mockup showing distribution of the 4 langs) -->
  <g transform="translate(60, 160)">
    <text class="label" x="0" y="0">STACK DISTRIBUTION</text>
    <rect class="progress-bg" x="180" y="-12" width="540" height="15" rx="5" />
    <!-- Segmented progress bars for languages -->
    <rect fill="{CYAN}" x="180" y="-12" width="200" height="15" filter="drop-shadow(0 0 1px {CYAN})" class="progress"/>
    <rect fill="{GREEN}" x="380" y="-12" width="150" height="15" filter="drop-shadow(0 0 1px {GREEN})" class="progress"/>
    <rect fill="#ffbd2e" x="530" y="-12" width="100" height="15" filter="drop-shadow(0 0 1px #ffbd2e)" class="progress"/>
    <rect fill="#ff5f56" x="630" y="-12" width="90" height="15" rx="5" filter="drop-shadow(0 0 1px #ff5f56)" class="progress"/>
  </g>
</svg>"""
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
