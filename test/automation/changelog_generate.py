"""
[Release automation, do not use in production]
This script fetches all releases from a specified GitHub repository and generates a CHANGELOG.md
file with the release notes, commit SHAs, and release types.

Base code generated with Google Gemini, linted by Pylint and tweaked by Boss-1s
"""
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
import requests
from packaging.version import Version, InvalidVersion
from rich.console import Console
from md_toc import api as md_toc

# 1. SETUP CONFIGURATION
REPO_OWNER = "Boss-1s"
REPO_NAME = "key_multivalue_storage"
changelog_path = "docs/CHANGELOG.md"

# Provide token directly or ensure $GITHUB_TOKEN is exported in terminal
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def get_release_type(current_tag, prior_tag=None):
    """
    Determine the type of update by comparing the current version against the version directly
    before the current one.
    """
    try:
        curr_ver = Version(current_tag.lstrip('vV'))
        release_type: str = ""

        # 1. Check if the current version itself is a pre-release build
        if curr_ver.is_prerelease:
            release_type = "Pre-release - "

        # 2. If there is no older version to compare against, it's the initial release
        if not prior_tag:
            release_type = "Initial Release"
        else:
            prior_ver = Version(prior_tag.lstrip('vV'))

            # 3. Handle a promotion from a pre-release directly to
            # its stable version (e.g., 1.0.0a1 -> 1.0.0)
            if prior_ver.is_prerelease:
                if not curr_ver.is_prerelease:
                    if curr_ver.base_version == prior_ver.base_version:
                        release_type += "Stable Promotion - "

            # 4. Standard SemVer delta checking
            if curr_ver.major > prior_ver.major:
                release_type += "Major Update"
            elif curr_ver.minor > prior_ver.minor:
                release_type += "Minor Update"
            elif curr_ver.micro > prior_ver.micro:
                release_type += "Major Patch"
            else:
                release_type += "Minor Patch"
        return release_type
    except InvalidVersion:
        return "Legacy Tag"

def sort_key(release):
    """Sort key that safely handles non-SemVer tags by placing them at the bottom."""
    tag_name = release['tag'].lstrip('vV')
    try:
        return (1, Version(tag_name))
    except InvalidVersion:
        return (0, tag_name)

def get_commit_sha_from_tag(owner, repo, tag_name, auth_token):
    """Fetches the actual 40-character commit HEAD SHA for a specific tag name."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/ref/tags/{tag_name}"

    # User-Agent prevents firewall from throwing 406 Not Acceptable errors
    headers = {
        "Accept": "application/json",
        "User-Agent": "ChangelogGenerator-PythonApp"
    }
    headers["Authorization"] = f"Bearer {auth_token}"

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return "Unknown HEAD"

    data = response.json()
    obj_type = data.get("object", {}).get("type")
    sha = data.get("object", {}).get("sha")

    if obj_type == "tag":
        tag_url = data.get("object", {}).get("url")
        tag_response = requests.get(tag_url, headers=headers, timeout=10)
        if tag_response.status_code == 200:
            return tag_response.json().get("object", {}).get("sha", sha)

    return sha

def fetch_github_releases(owner, repo, token):
    """
    Fetch all releases from the GitHub API, handling pagination and rate limits,
    with requests.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    headers = {
        "Accept": "application/json",
        "User-Agent": "ChangelogGenerator-PythonApp"
    }
    headers["Authorization"] = f"Bearer {token}"

    raw_data_items = []
    page = 1

    # 1. Fetch release list pages sequentially
    while True:
        response = requests.get(url,
                                headers=headers,
                                params={"page": page, "per_page": 100},
                                timeout=10
        )
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"GitHub API Error: {response.status_code} - {response.text}"
            )

        data = response.json()
        if not data:
            break
        raw_data_items.extend(data)
        page += 1

    # Inline worker function to execute processing in parallel threads
    def worker(item):
        tag_name = item.get("tag_name")
        print(f"Processing details for tag: {tag_name}...")
        commit_head = get_commit_sha_from_tag(owner, repo, tag_name, token)
        return {
            "tag": tag_name,
            "title": item.get("name") or tag_name,
            "type": get_release_type(tag_name), # Kept signature for raw API input tracking
            "commit": commit_head,
            "body": item.get("body") or "No release notes provided."
        }

    # 2. Concurrently process individual tag metadata resolving blocks
    with ThreadPoolExecutor(max_workers=15) as executor:
        all_releases = list(executor.map(worker, raw_data_items))

    return all_releases

def clean_and_demote_headers(body_text):
    """Prevents breaking page layouts by shifting internal headers down."""
    if not body_text:
        return ""
    cleaned_lines = []
    for line in body_text.splitlines():
        match = re.match(r"^(#{1,4})\s+(.*)", line)
        if match:
            cleaned_lines.append(f"##{match.group(1)} {match.group(2)}")
        else:
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def generate_changelog():
    """Main method to generate changelog."""
    print(f"Connecting to api.github.com for {REPO_OWNER}/{REPO_NAME}...")
    releases = fetch_github_releases(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)

    # Sort releases in descending order by SemVer value
    releases.sort(key=sort_key, reverse=True)

    for _, rel in enumerate(releases):
        if "Unknown" in rel['commit']:
            print(f"Warning: Could not resolve commit SHA for tag {rel['tag']}")
            print("Removing this release....")
            releases.remove(rel)

    # Write formatted payload data to CHANGELOG.md
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\n\n")
        f.write("## Table Of Contents\n\n")
        f.write("<!--TOC-->\n\n")
        # Enumerate to peek at the older release adjacent to the current one
        for i, rel in enumerate(releases):
            # The chronologically prior release is the next element in a descending list
            prior_rel = releases[i + 1] if (i + 1) < len(releases) else None
            prior_tag = prior_rel["tag"] if prior_rel else None

            # --- CALCULATE UPDATE TYPE BASED ON PREVIOUS SEMVER HERE ---
            rel_type = get_release_type(rel["tag"], prior_tag)

            f.write(f"## 📦 {rel['tag']} — *{rel['title']}*\n\n")
            f.write(f"⚙ **Target Node Commit:** `{rel['commit'][:8]}`\n\n")
            f.write(f"📝 **Release Type:** {rel_type}\n\n")

            flattened_body = clean_and_demote_headers(rel['body'])
            f.write(f"{flattened_body}\n\n")
            f.write("---\n\n")

    toc = md_toc.build_toc(changelog_path, keep_header_levels=2, skip_lines=4)
    md_toc.write_string_on_file_between_markers(changelog_path, toc, '<!--TOC-->')

    print(f"\n🎉 {changelog_path} successfully generated!")

if __name__ == "__main__":
    try:
        generate_changelog()
    except Exception as e:
        console = Console()
        console.print_exception(show_locals=True)
        console.print(f"[b red]Error creating file '{changelog_path}': {e}")
        sys.exit(1)
