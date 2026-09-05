"""Public-profile data for the generated README artwork.

The profile deliberately uses GitHub's public REST endpoints and the public
contribution calendar only. All callers get deterministic, non-empty layout
data even when the API is unavailable, while never fabricating activity.
"""

from __future__ import annotations

import html
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOGIN = "DR-WRITES-ALOT"
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

_TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
_CACHE: dict[str, object] = {}

# Last-known public values keep the layout useful during a transient API outage.
# They are replaced on every successful scheduled build.
_FALLBACK = {
    "repos": 4,
    "followers": 5,
    "stars": 0,
    "languages": [("TypeScript", 85), ("Rust", 11), ("Python", 2), ("HTML", 1), ("CSS", 1)],
}


def _request(url: str, accept: str = "application/vnd.github+json") -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "DR-WRITES-ALOT-moonlit-atlas",
            "Accept": accept,
        },
    )
    if _TOKEN and "api.github.com" in url:
        request.add_header("Authorization", f"Bearer {_TOKEN}")
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode("utf-8", "replace")


def api(path: str):
    if path in _CACHE:
        return _CACHE[path]
    try:
        value = json.loads(_request(f"https://api.github.com{path}"))
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"[warn] GitHub API {path}: {error}")
        value = None
    _CACHE[path] = value
    return value


def scrape_contributions() -> list[dict[str, object]] | None:
    """Read the public contribution calendar without requiring GraphQL."""
    try:
        page = _request(f"https://github.com/users/{LOGIN}/contributions", "text/html")
    except (OSError, urllib.error.URLError) as error:
        print(f"[warn] contribution calendar: {error}")
        return None

    cells: list[dict[str, object]] = []
    for match in re.finditer(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*', page):
        tag = match.group(0)
        level_match = re.search(r'data-level="(\d)"', tag)
        cells.append(
            {
                "date": match.group(1),
                "level": int(level_match.group(1)) if level_match else 0,
            }
        )

    # GitHub has used both attribute orders over time.
    if not cells:
        for match in re.finditer(
            r'data-level="(\d)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', page
        ):
            cells.append({"date": match.group(2), "level": int(match.group(1))})

    return cells or None


def empty_calendar() -> list[dict[str, object]]:
    """Return a real-date empty grid when the calendar endpoint is offline."""
    today = datetime.now(timezone.utc).date()
    sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    start = sunday - timedelta(weeks=52)
    return [
        {"date": (start + timedelta(days=index)).isoformat(), "level": 0}
        for index in range(53 * 7)
    ]


def esc(value: object) -> str:
    """Escape text for SVG nodes and attributes."""
    return html.escape(str(value), quote=True)


def shorten(value: object, limit: int) -> str:
    text = str(value or "").splitlines()[0].strip()
    return text if len(text) <= limit else f"{text[: limit - 1]}…"


def _language_snapshot(repositories: list[dict[str, object]]) -> list[tuple[str, int]]:
    """Rank languages by bytes, matching GitHub's language breakdown behavior."""
    bytes_by_language: dict[str, int] = {}
    owned = [repo for repo in repositories if not repo.get("fork")]

    for repo in owned[:30]:
        name = repo.get("name")
        if not name:
            continue
        language_data = api(f"/repos/{LOGIN}/{name}/languages")
        if isinstance(language_data, dict):
            for language, count in language_data.items():
                bytes_by_language[language] = bytes_by_language.get(language, 0) + int(count)

    # The primary language fallback keeps the panel useful if a language API
    # request is rate-limited.
    if not bytes_by_language:
        for repo in owned:
            language = repo.get("language")
            if language:
                bytes_by_language[language] = bytes_by_language.get(language, 0) + max(
                    int(repo.get("size", 1) or 1), 1
                )

    if not bytes_by_language:
        return []

    total = sum(bytes_by_language.values()) or 1
    ranked = sorted(bytes_by_language.items(), key=lambda item: item[1], reverse=True)
    return [(language, round(count * 100 / total)) for language, count in ranked[:5]]


def _activity_feed(repositories: list[dict[str, object]]) -> list[dict[str, str]]:
    events = api(f"/users/{LOGIN}/events/public?per_page=100")
    feed: list[dict[str, str]] = []

    if isinstance(events, list):
        for event in events:
            event_type = event.get("type")
            if event_type not in {"PushEvent", "IssuesEvent", "PullRequestEvent", "CreateEvent", "WatchEvent"}:
                continue

            full_repo = str(event.get("repo", {}).get("name", "unknown/unknown"))
            repo_name = full_repo.split("/")[-1]
            created = str(event.get("created_at", ""))[:10]
            payload = event.get("payload") or {}

            if event_type == "PushEvent":
                action = "push"
                commits = payload.get("commits") or []
                message = commits[-1].get("message", "pushed changes") if commits else "pushed changes"
            elif event_type == "IssuesEvent":
                action = "issue"
                message = (payload.get("issue") or {}).get("title", "updated an issue")
            elif event_type == "PullRequestEvent":
                action = "pr"
                message = (payload.get("pull_request") or {}).get("title", "updated a pull request")
            elif event_type == "CreateEvent":
                action = "create"
                message = f"created {payload.get('ref_type', 'repository')}"
            else:
                action = "star"
                message = "starred a repository"

            feed.append(
                {
                    "date": created,
                    "action": action,
                    "repo": shorten(repo_name, 20),
                    "message": shorten(message, 34),
                }
            )
            if len(feed) >= 7:
                break

    if feed:
        return feed

    # If the events feed is unavailable, show repository freshness rather than
    # inventing commit messages.
    for repo in repositories:
        if repo.get("fork"):
            continue
        feed.append(
            {
                "date": str(repo.get("pushed_at", ""))[:10],
                "action": "repo",
                "repo": shorten(repo.get("name", "unknown"), 20),
                "message": shorten(repo.get("description") or "recently updated", 34),
            }
        )
        if len(feed) >= 7:
            break
    return feed


def collect() -> dict[str, object]:
    if _CACHE.get("profile"):
        return _CACHE["profile"]  # type: ignore[return-value]

    now = datetime.now(timezone.utc)
    user = api(f"/users/{LOGIN}") or {}
    if not isinstance(user, dict):
        user = {}
    repositories = api(f"/users/{LOGIN}/repos?per_page=100&type=owner&sort=pushed") or []
    if not isinstance(repositories, list):
        repositories = []

    owned = [repo for repo in repositories if not repo.get("fork")]
    repo_by_name = {str(repo.get("name")): repo for repo in repositories}
    stars = sum(int(repo.get("stargazers_count", 0) or 0) for repo in owned) if repositories else _FALLBACK["stars"]
    languages = _language_snapshot(repositories) if repositories else []
    if not languages:
        languages = list(_FALLBACK["languages"])
    calendar = scrape_contributions() or empty_calendar()

    profile = {
        "login": LOGIN,
        "name": "Sreejith SH",
        "followers": int(user.get("followers", _FALLBACK["followers"]) or _FALLBACK["followers"]),
        "following": int(user.get("following", 0) or 0),
        "repos": int(user.get("public_repos", _FALLBACK["repos"]) or _FALLBACK["repos"]),
        "stars": stars,
        "languages": languages,
        "activity": _activity_feed(repositories),
        "calendar": calendar,
        "contrib_total": sum(1 for cell in calendar if int(cell.get("level", 0) or 0) > 0),
        "generated": now.strftime("%Y-%m-%d %H:%M UTC"),
        "generated_date": now.strftime("%Y-%m-%d"),
        "repo_by_name": repo_by_name,
    }
    _CACHE["profile"] = profile
    return profile


def write_svg(filename: str, content: str) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    path = ASSETS / filename
    # Keep generated files pleasant to review and make CI diff checks useful.
    content = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    path.write_text(content, encoding="utf-8")
    print(f"[ok] wrote {path.relative_to(ROOT)} ({len(content)} bytes)")
