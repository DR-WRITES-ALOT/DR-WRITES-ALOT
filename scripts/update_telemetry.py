import os
import json
import urllib.request
import urllib.error
import math
from datetime import datetime

def fetch_json(url, token):
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not found. Exiting.")
        return

    # In GitHub actions, GITHUB_REPOSITORY is "username/repo"
    repo_name = os.environ.get("GITHUB_REPOSITORY", "DR-WRITES-ALOT/DR-WRITES-ALOT")
    username = repo_name.split("/")[0]

    print(f"Fetching data for {username}...")

    # 1. User Profile Stats
    user_data = fetch_json(f"https://api.github.com/users/{username}", token)
    if not user_data:
        return

    followers = user_data.get("followers", 0)
    public_repos = user_data.get("public_repos", 0)

    # 2. Fetch Repos for Stars and Languages
    repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100&type=owner", token)
    if not repos:
        repos = []

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    
    # Calculate Language Distribution
    langs = {}
    for repo in repos:
        if repo.get("fork"): continue
        lang = repo.get("language")
        if lang:
            langs[lang] = langs.get(lang, 0) + 1

    # Sort languages by count
    sorted_langs = sorted(langs.items(), key=lambda item: item[1], reverse=True)
    
    # Fallbacks if < 3 languages
    while len(sorted_langs) < 3:
        sorted_langs.append(("N/A", 0))

    top_3_langs = sorted_langs[:3]
    total_lang_repos = sum(count for _, count in sorted_langs) or 1 # avoid div by zero

    # 3. Fetch Recent Activity
    events = fetch_json(f"https://api.github.com/users/{username}/events/public?per_page=20", token)
    recent_logs = []
    
    if events:
        for event in events:
            # We want meaningful events like PushEvent, IssuesEvent, PullRequestEvent, CreateEvent
            if event["type"] in ["PushEvent", "IssuesEvent", "PullRequestEvent", "CreateEvent", "WatchEvent"]:
                repo_name = event["repo"]["name"].split("/")[-1]
                created_at = event["created_at"]
                
                # Format Date nicely
                try:
                    dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                    date_str = dt.strftime("%b %d")
                except:
                    date_str = created_at.split("T")[0]

                # Determine action and description
                event_type = event["type"]
                if event_type == "PushEvent":
                    action = "push"
                    commits = event.get("payload", {}).get("commits", [])
                    desc = commits[0]["message"] if commits else "Pushed to branch"
                elif event_type == "IssuesEvent":
                    action = "issue"
                    desc = event.get("payload", {}).get("issue", {}).get("title", "Opened issue")
                elif event_type == "PullRequestEvent":
                    action = "pr"
                    desc = event.get("payload", {}).get("pull_request", {}).get("title", "Opened PR")
                elif event_type == "CreateEvent":
                    action = "create"
                    desc = f"Created {event.get('payload', {}).get('ref_type', 'repo')}"
                elif event_type == "WatchEvent":
                    action = "star"
                    desc = "Starred the repository"
                
                # Clean up description (truncate if too long)
                desc = desc.split("\n")[0]
                if len(desc) > 35: desc = desc[:32] + "..."

                recent_logs.append({
                    "date": date_str,
                    "action": action,
                    "repo": repo_name,
                    "desc": desc
                })

                if len(recent_logs) >= 3:
                    break

    # Fallbacks if < 3 logs
    while len(recent_logs) < 3:
        recent_logs.append({"date": "N/A", "action": "none", "repo": "N/A", "desc": "No recent activity"})

    # 4. Inject into Template
    template_path = "assets/jules-telemetry-template.svg"
    output_path = "assets/jules-telemetry.svg"
    
    with open(template_path, "r", encoding="utf-8") as f:
        svg_content = f.read()

    # Replacements
    svg_content = svg_content.replace("{{STARS}}", str(total_stars))
    svg_content = svg_content.replace("{{REPOS}}", str(public_repos))
    svg_content = svg_content.replace("{{FOLLOWERS}}", str(followers))

    for i in range(3):
        lang_name, lang_count = top_3_langs[i]
        pct = (lang_count / total_lang_repos) * 100 if lang_count > 0 else 0
        
        # Max width of the SVG bar is 220px
        bar_width = max(10, int((pct / 100) * 220)) if pct > 0 else 0
        
        svg_content = svg_content.replace(f"{{{{LANG{i+1}_NAME}}}}", lang_name)
        svg_content = svg_content.replace(f"{{{{LANG{i+1}_PCT}}}}", str(int(pct)))
        svg_content = svg_content.replace(f"{{{{LANG{i+1}_WIDTH}}}}", str(bar_width))

    for i in range(3):
        log = recent_logs[i]
        svg_content = svg_content.replace(f"{{{{LOG{i+1}_DATE}}}}", log["date"])
        svg_content = svg_content.replace(f"{{{{LOG{i+1}_TYPE}}}}", log["action"])
        
        # Ensure repo name isn't too long to break layout
        repo_disp = log["repo"]
        if len(repo_disp) > 16: repo_disp = repo_disp[:14] + ".."
        svg_content = svg_content.replace(f"{{{{LOG{i+1}_REPO}}}}", repo_disp)
        
        svg_content = svg_content.replace(f"{{{{LOG{i+1}_MSG}}}}", log["desc"])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
        
    print("Telemetry SVG generated successfully!")

if __name__ == "__main__":
    main()
