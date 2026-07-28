import os
import requests
import json
from datetime import datetime

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
GITHUB_API_URL = "https://api.github.com"
USERNAME = "SreejithSH"

def get_github_stats():
    stats = {
        "stars": 42,
        "commits": 1337,
        "repos": 15,
        "followers": 10
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

        stats["commits"] = "1.2k+"

    except Exception as e:
        print(f"Error fetching GitHub stats: {e}")

    return stats

def generate_hero_svg():
    svg = f"""<svg width="840" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      @keyframes type {{ from {{ width: 0; }} to {{ width: 100%; }} }}
      .cursor {{ animation: blink 1s step-end infinite; fill: #64ffda; }}
      .text {{ font-family: 'Courier New', Courier, monospace; font-size: 18px; fill: #e6edf3; }}
      .prompt {{ fill: #3fb950; }}
      .glow {{ filter: drop-shadow(0 0 8px rgba(100,255,218,0.6)); }}
      .mac-btn {{ rx: 6; ry: 6; width: 12px; height: 12px; }}
    </style>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0f18" />
      <stop offset="100%" stop-color="#111827" />
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="840" height="200" rx="12" fill="url(#bgGrad)" stroke="#1f2937" stroke-width="2"/>

  <!-- Title bar -->
  <rect width="840" height="40" rx="12" fill="#0d1117" />
  <rect y="20" width="840" height="20" fill="#0d1117" /> <!-- Straight bottom edge for title bar -->
  <line x1="0" y1="40" x2="840" y2="40" stroke="#30363d" stroke-width="1"/>

  <!-- Mac Buttons -->
  <rect class="mac-btn" x="16" y="14" fill="#ff5f56" />
  <rect class="mac-btn" x="36" y="14" fill="#ffbd2e" />
  <rect class="mac-btn" x="56" y="14" fill="#27c93f" />

  <text x="420" y="25" fill="#8b949e" font-family="monospace" font-size="14" text-anchor="middle">guest@sreejith: ~/portfolio</text>

  <!-- Content -->
  <g transform="translate(30, 80)">
    <text class="text glow" y="0"><tspan class="prompt">$</tspan> whoami</text>
    <text class="text" y="30" fill="#a5d6ff">Sreejith S H - Full Stack Software Engineer</text>
    <text class="text glow" y="70"><tspan class="prompt">$</tspan> status --current</text>
    <text class="text" y="100">Building products and turning bugs into features <rect x="425" y="85" width="10" height="18" class="cursor"/></text>
  </g>
</svg>"""
    with open("assets/hero.svg", "w") as f:
        f.write(svg)

def generate_stats_svg(stats):
    svg = f"""<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .text {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
      .title {{ font-size: 16px; font-weight: bold; fill: #8b949e; }}
      .stat-val {{ font-size: 28px; font-weight: 800; fill: #64ffda; filter: drop-shadow(0 0 5px rgba(100,255,218,0.4)); }}
      .stat-label {{ font-size: 12px; fill: #8b949e; text-transform: uppercase; letter-spacing: 1px; }}
    </style>
    <linearGradient id="cardGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#112240" />
      <stop offset="100%" stop-color="#0a192f" />
    </linearGradient>
  </defs>

  <rect width="400" height="200" rx="12" fill="url(#cardGrad)" stroke="#233554" stroke-width="2"/>

  <rect x="20" y="20" width="8" height="8" rx="4" fill="#64ffda" filter="drop-shadow(0 0 4px #64ffda)"/>
  <text x="40" y="28" class="text title" dominant-baseline="middle">System Statistics</text>
  <line x1="20" y1="45" x2="380" y2="45" stroke="#233554" stroke-width="1"/>

  <!-- Stars -->
  <g transform="translate(40, 90)">
    <text class="text stat-val">{stats['stars']}</text>
    <text y="20" class="text stat-label">Stars</text>
  </g>

  <!-- Commits -->
  <g transform="translate(140, 90)">
    <text class="text stat-val">{stats['commits']}</text>
    <text y="20" class="text stat-label">Commits</text>
  </g>

  <!-- Repos -->
  <g transform="translate(260, 90)">
    <text class="text stat-val">{stats['repos']}</text>
    <text y="20" class="text stat-label">Repos</text>
  </g>

  <!-- Followers -->
  <g transform="translate(40, 160)">
    <text class="text stat-val">{stats['followers']}</text>
    <text y="20" class="text stat-label">Followers</text>
  </g>
</svg>"""
    with open("assets/stats.svg", "w") as f:
        f.write(svg)

def generate_skills_svg():
    svg = f"""<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .text {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
      .title {{ font-size: 16px; font-weight: bold; fill: #8b949e; }}
      .tag {{ font-size: 14px; font-weight: 600; fill: #64ffda; }}
    </style>
    <linearGradient id="cardGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#112240" />
      <stop offset="100%" stop-color="#0a192f" />
    </linearGradient>
  </defs>

  <rect width="400" height="200" rx="12" fill="url(#cardGrad2)" stroke="#233554" stroke-width="2"/>

  <rect x="20" y="20" width="8" height="8" rx="4" fill="#bd93f9" filter="drop-shadow(0 0 4px #bd93f9)"/>
  <text x="40" y="28" class="text title" dominant-baseline="middle">Tech Stack</text>
  <line x1="20" y1="45" x2="380" y2="45" stroke="#233554" stroke-width="1"/>

  <g transform="translate(20, 70)">
    <!-- Python -->
    <rect x="0" y="0" width="90" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="45" y="20" class="text tag" text-anchor="middle">Python</text>

    <!-- C/C++ -->
    <rect x="100" y="0" width="80" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="140" y="20" class="text tag" text-anchor="middle">C/C++</text>

    <!-- Java -->
    <rect x="190" y="0" width="70" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="225" y="20" class="text tag" text-anchor="middle">Java</text>

    <!-- Full Stack -->
    <rect x="0" y="45" width="110" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="55" y="65" class="text tag" text-anchor="middle">Full Stack</text>

    <!-- Git -->
    <rect x="120" y="45" width="60" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="150" y="65" class="text tag" text-anchor="middle">Git</text>

    <!-- React (implied by Full Stack usually, but cool to add) -->
    <rect x="190" y="45" width="75" height="30" rx="15" fill="rgba(100,255,218,0.1)" stroke="#64ffda" stroke-width="1"/>
    <text x="227.5" y="65" class="text tag" text-anchor="middle">React</text>
  </g>
</svg>"""
    with open("assets/skills.svg", "w") as f:
        f.write(svg)

def main():
    print("Starting profile generation...")
    os.makedirs("assets", exist_ok=True)

    stats = get_github_stats()

    generate_hero_svg()
    generate_stats_svg(stats)
    generate_skills_svg()

    print("Successfully generated SVGs in assets/")

if __name__ == "__main__":
    main()
