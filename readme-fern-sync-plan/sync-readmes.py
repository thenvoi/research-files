#!/usr/bin/env python3
"""
README Sync Script

Fetches README files from configured repositories, extracts sections based on
configuration rules, and generates MDX files with frontmatter for Fern documentation.

Usage:
    python scripts/sync-readmes.py

Environment variables:
    GITHUB_TOKEN: GitHub token for API access (required for private repos)
"""

import os
import re
import sys
from pathlib import Path
from typing import Any

import requests
import yaml


def load_config(config_path: str = "readme-sync-config.yml") -> dict[str, Any]:
    """Load the sync configuration file."""
    with open(config_path) as f:
        return yaml.safe_load(f)


def fetch_readme(owner: str, repo: str, readme_path: str, private: bool = False) -> str:
    """Fetch README content from GitHub API."""
    token = os.environ.get("GITHUB_TOKEN")

    if private and not token:
        raise ValueError(f"GITHUB_TOKEN required for private repo: {owner}/{repo}")

    headers = {"Accept": "application/vnd.github.v3.raw"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{readme_path}"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text


def extract_section(content: str, extract_config: dict | str) -> str:
    """Extract a section from the README based on configuration."""
    if extract_config == "all":
        return content

    if isinstance(extract_config, dict):
        # Line range extraction
        if "lines" in extract_config:
            lines = content.split("\n")
            start_line, end_line = extract_config["lines"]
            return "\n".join(lines[start_line - 1:end_line])

        # Regex extraction
        if "regex" in extract_config:
            pattern = extract_config["regex"]
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(0)
            return ""

        # Start/end marker extraction
        start_marker = extract_config.get("start")
        end_marker = extract_config.get("end")

        if start_marker:
            # Find start position
            start_idx = content.find(start_marker)
            if start_idx == -1:
                print(f"  Warning: Start marker not found: {start_marker}")
                return ""

            # Find end position
            if end_marker:
                end_idx = content.find(end_marker, start_idx + len(start_marker))
                if end_idx == -1:
                    # If end marker not found, take until end of file
                    extracted = content[start_idx:]
                else:
                    extracted = content[start_idx:end_idx]
            else:
                # No end marker, take until end of file
                extracted = content[start_idx:]

            return extracted.strip()

    return content


def convert_relative_images(content: str, owner: str, repo: str, branch: str = "main") -> str:
    """Convert relative image paths to absolute GitHub raw URLs."""
    # Pattern for markdown images: ![alt](path)
    md_img_pattern = r"!\[([^\]]*)\]\((?!https?://|/)([^)]+)\)"

    def replace_md_img(match):
        alt = match.group(1)
        path = match.group(2)
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        return f"![{alt}]({raw_url})"

    content = re.sub(md_img_pattern, replace_md_img, content)

    # Pattern for HTML images: src="path"
    html_img_pattern = r'src=["\'](?!https?://|/)([^"\']+)["\']'

    def replace_html_img(match):
        path = match.group(1)
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
        return f'src="{raw_url}"'

    content = re.sub(html_img_pattern, replace_html_img, content)

    return content


def convert_relative_links(content: str, owner: str, repo: str, branch: str = "main") -> str:
    """Convert relative links to absolute GitHub URLs."""
    # Pattern for markdown links to files: [text](path.ext) or [text](path)
    # Exclude anchors (#), absolute URLs (http://, https://), and root paths (/)
    md_link_pattern = r"\[([^\]]+)\]\((?!https?://|#|/)([^)#]+)(#[^)]+)?\)"

    def replace_md_link(match):
        text = match.group(1)
        path = match.group(2)
        anchor = match.group(3) or ""

        # Check if it's a documentation link (markdown file)
        if path.endswith((".md", ".mdx")):
            github_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{path}{anchor}"
        else:
            # Could be a file or directory
            github_url = f"https://github.com/{owner}/{repo}/blob/{branch}/{path}{anchor}"

        return f"[{text}]({github_url})"

    content = re.sub(md_link_pattern, replace_md_link, content)

    return content


def strip_emoji_from_headers(content: str) -> str:
    """Remove emoji from markdown headers for cleaner MDX."""
    # Pattern: ## 🚀 Header -> ## Header
    emoji_header_pattern = r"^(#{1,6})\s*[\U0001F300-\U0001F9FF\U00002600-\U000027BF]+\s*"

    def replace_emoji_header(match):
        return match.group(1) + " "

    content = re.sub(emoji_header_pattern, replace_emoji_header, content, flags=re.MULTILINE)

    return content


def generate_frontmatter(page_config: dict, repo_config: dict, defaults: dict) -> str:
    """Generate YAML frontmatter for MDX file."""
    title = page_config.get("title", "Untitled")
    subtitle = page_config.get("subtitle", "")
    repo = repo_config.get("repo", "")
    owner = repo_config.get("owner", "")

    frontmatter_lines = [
        "---",
        f'title: "{title}"',
    ]

    if subtitle:
        frontmatter_lines.append(f'subtitle: "{subtitle}"')

    frontmatter_lines.append(f'description: "Auto-synced from {repo} repository"')
    frontmatter_lines.append("---")

    return "\n".join(frontmatter_lines)


def generate_notice(repo_config: dict, defaults: dict) -> str:
    """Generate the auto-sync notice for the top of the page."""
    notice_template = defaults.get("notice", "")
    if not notice_template:
        return ""

    owner = repo_config.get("owner", "")
    repo = repo_config.get("repo", "")

    notice = notice_template.format(owner=owner, repo=repo)
    return notice


def process_repository(repo_config: dict, defaults: dict, base_path: Path) -> list[str]:
    """Process a single repository and generate MDX files."""
    owner = repo_config["owner"]
    repo = repo_config["repo"]
    readme_path = repo_config.get("readme_path", "README.md")
    output_dir = repo_config.get("output_dir", f"fern/docs/pages/{repo}")
    private = repo_config.get("private", False)
    pages = repo_config.get("pages", [])

    print(f"\nProcessing {owner}/{repo}...")

    # Fetch README
    try:
        readme_content = fetch_readme(owner, repo, readme_path, private)
        print(f"  Fetched README ({len(readme_content)} chars)")
    except requests.exceptions.HTTPError as e:
        print(f"  Error fetching README: {e}")
        return []

    # Create output directory
    output_path = base_path / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    generated_files = []

    for page in pages:
        filename = page.get("filename", "index.mdx")
        extract_config = page.get("extract", "all")

        print(f"  Extracting: {filename}")

        # Extract section
        section_content = extract_section(readme_content, extract_config)

        if not section_content:
            print(f"    Warning: No content extracted for {filename}")
            continue

        # Convert relative paths to absolute
        section_content = convert_relative_images(section_content, owner, repo)
        section_content = convert_relative_links(section_content, owner, repo)

        # Optionally strip emoji from headers
        # section_content = strip_emoji_from_headers(section_content)

        # Generate frontmatter
        frontmatter = generate_frontmatter(page, repo_config, defaults)

        # Generate notice
        notice = generate_notice(repo_config, defaults)

        # Combine into final MDX content
        mdx_content = frontmatter + "\n\n"
        if notice:
            mdx_content += notice.strip() + "\n\n"
        mdx_content += section_content

        # Write file
        file_path = output_path / filename
        with open(file_path, "w") as f:
            f.write(mdx_content)

        generated_files.append(str(file_path))
        print(f"    Generated: {file_path}")

    return generated_files


def main():
    """Main entry point."""
    # Determine base path (repository root)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent  # Go up from scripts/ to repo root

    # Load configuration
    config_path = base_path / "readme-sync-config.yml"
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}")
        sys.exit(1)

    print(f"Loading configuration from: {config_path}")
    config = load_config(config_path)

    defaults = config.get("defaults", {})
    repositories = config.get("repositories", [])

    if not repositories:
        print("No repositories configured.")
        sys.exit(0)

    print(f"Found {len(repositories)} repositories to sync")

    # Process each repository
    all_generated_files = []
    for repo_config in repositories:
        files = process_repository(repo_config, defaults, base_path)
        all_generated_files.extend(files)

    # Summary
    print(f"\n{'=' * 50}")
    print(f"Sync complete! Generated {len(all_generated_files)} files:")
    for f in all_generated_files:
        print(f"  - {f}")

    # Write manifest for GitHub Action to use
    manifest_path = base_path / "readme-sync-manifest.txt"
    with open(manifest_path, "w") as f:
        f.write("\n".join(all_generated_files))
    print(f"\nManifest written to: {manifest_path}")


if __name__ == "__main__":
    main()
