"""Refresh the generated GitHub observatory card used by the profile README."""

import html
import json
import os
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = ROOT / "assets" / "storybook-telemetry-template.svg"
OUTPUT_PATH = ROOT / "assets" / "storybook-telemetry.svg"


def fetch_json(url: str, token: str | None):
    request = urllib.request.Request(url)
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"Could not fetch {url}: {error}")
        return None


def xml_text(value) -> str:
    """Escape values before placing API data into an SVG text node."""
    return html.escape(str(value), quote=False)


def short(value: str, limit: int) -> str:
    value = (value or "").splitlines()[0].strip()
    return value if len(value) <= limit else f"{value[: limit - 3]}..."


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY", "DR-WRITES-ALOT/DR-WRITES-ALOT")
    username = repository.split("/", 1)[0]

    print(f"Refreshing observatory data for {username}...")
    user_data = fetch_json(f"https://api.github.com/users/{username}", token)
    if not user_data:
        print("Profile data was unavailable; keeping the existing telemetry card.")
        return

    followers = user_data.get("followers", 0)
    public_repos = user_data.get("public_repos", 0)

    repos = fetch_json(
        f"https://api.github.com/users/{username}/repos?per_page=100&type=owner&sort=updated",
        token,
    ) or []

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

    # Count the primary language of each non-fork repository. This keeps the
    # chart legible and matches the language snapshot shown on GitHub profiles.
    languages: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork"):
            continue
        language = repo.get("language")
        if language:
            languages[language] = languages.get(language, 0) + 1

    sorted_languages = sorted(languages.items(), key=lambda item: item[1], reverse=True)
    while len(sorted_languages) < 3:
        sorted_languages.append(("N/A", 0))
    top_languages = sorted_languages[:3]
    total_language_repos = sum(count for _, count in sorted_languages) or 1

    events = fetch_json(f"https://api.github.com/users/{username}/events/public?per_page=30", token) or []
    recent_logs: list[dict[str, str]] = []
    interesting_events = {
        "PushEvent",
        "IssuesEvent",
        "PullRequestEvent",
        "CreateEvent",
        "WatchEvent",
    }

    for event in events:
        event_type = event.get("type")
        if event_type not in interesting_events:
            continue

        repo_name = event.get("repo", {}).get("name", "").split("/")[-1] or "N/A"
        created_at = event.get("created_at", "")
        try:
            date_value = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            date_label = date_value.strftime("%b %d")
        except ValueError:
            date_label = created_at.split("T")[0] if created_at else "N/A"

        payload = event.get("payload", {})
        if event_type == "PushEvent":
            action = "push"
            commits = payload.get("commits", [])
            description = commits[0].get("message", "Pushed to branch") if commits else "Pushed to branch"
        elif event_type == "IssuesEvent":
            action = "issue"
            description = payload.get("issue", {}).get("title", "Opened issue")
        elif event_type == "PullRequestEvent":
            action = "pr"
            description = payload.get("pull_request", {}).get("title", "Opened pull request")
        elif event_type == "CreateEvent":
            action = "create"
            description = f"Created {payload.get('ref_type', 'repository')}"
        else:
            action = "star"
            description = "Starred a repository"

        recent_logs.append(
            {
                "date": date_label,
                "action": action,
                "repo": short(repo_name, 16),
                "desc": short(description, 35),
            }
        )
        if len(recent_logs) == 3:
            break

    while len(recent_logs) < 3:
        recent_logs.append(
            {"date": "N/A", "action": "quiet", "repo": "N/A", "desc": "No recent public activity"}
        )

    svg = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{STARS}}": xml_text(total_stars),
        "{{REPOS}}": xml_text(public_repos),
        "{{FOLLOWERS}}": xml_text(followers),
    }

    for index, (language, count) in enumerate(top_languages, start=1):
        percentage = (count / total_language_repos) * 100 if count else 0
        bar_width = round((percentage / 100) * 312) if percentage else 0
        replacements.update(
            {
                f"{{{{LANG{index}_NAME}}}}": xml_text(language),
                f"{{{{LANG{index}_PCT}}}}": str(round(percentage)),
                f"{{{{LANG{index}_WIDTH}}}}": str(bar_width),
            }
        )

    for index, log in enumerate(recent_logs, start=1):
        replacements.update(
            {
                f"{{{{LOG{index}_DATE}}}}": xml_text(log["date"]),
                f"{{{{LOG{index}_TYPE}}}}": xml_text(log["action"]),
                f"{{{{LOG{index}_REPO}}}}": xml_text(log["repo"]),
                f"{{{{LOG{index}_MSG}}}}": xml_text(log["desc"]),
            }
        )

    for placeholder, value in replacements.items():
        svg = svg.replace(placeholder, value)

    OUTPUT_PATH.write_text(svg, encoding="utf-8")
    print(f"Observatory SVG generated at {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
