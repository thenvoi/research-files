# README-to-Fern Documentation Sync - Implementation Plan

## Summary
Build a custom GitHub Action that syncs READMEs from selected thenvoi repositories to Fern documentation, running twice weekly (Sunday and Wednesday), creating PRs for review.

## Selected Configuration

| Setting | Value |
|---------|-------|
| **Approach** | Option 1: Custom GitHub Action (Pull Pattern) |
| **Trigger** | Scheduled: Sunday and Wednesday |
| **Review Flow** | Create PR for review (not direct commit) |
| **Repositories** | thenvoi-mcp, thenvoi-sdk-python, phoenix-channels-python-client-alpha, n8n-nodes-thenvoi (private) |
| **Navigation** | Custom per-repo page rules (each repo defines its own page splits) |

## Repositories to Sync

| Repository | Visibility | Description |
|------------|------------|-------------|
| `thenvoi-mcp` | Public | MCP server for AI integration (~670 line README) |
| `thenvoi-sdk-python` | Public | Python SDK for external agents (~280 line README) |
| `phoenix-channels-python-client-alpha` | Public | Phoenix channels client |
| `n8n-nodes-thenvoi` | **Private** | n8n nodes integration (requires PAT with repo scope) |

## Key Constraints
- Fern uses MDX format with YAML frontmatter (title, subtitle, slug, description)
- No native "include" or "import" directive for markdown files in Fern
- READMEs may be split into multiple pages (not 1:1 mapping)
- Private repo access requires GitHub token with `repo` scope

---

## Architecture

```
Source Repos (thenvoi-mcp, thenvoi-sdk-python, phoenix-channels, n8n-nodes)
    │
    └── README.md (source of truth)
            │
            ▼
┌─────────────────────────────────────────────────────────────┐
│  Fern Repo - .github/workflows/sync-readmes.yml            │
│  ───────────────────────────────────────────────────────   │
│  Schedule: 0 0 * * 0,3 (Sunday & Wednesday at midnight)    │
│                                                             │
│  1. Fetch READMEs via GitHub API (public + private)        │
│  2. Parse & transform: MD → MDX with frontmatter           │
│  3. Optionally split into multiple pages                   │
│  4. Handle images (convert to absolute GitHub URLs)        │
│  5. Create PR with changes                                 │
│  6. Assign reviewer                                        │
└─────────────────────────────────────────────────────────────┘
            │
            ▼
    PR Review → Merge → publish-docs.yml → docs.thenvoi.com
```

---

## Implementation Steps

### Step 1: Create Configuration File
**File**: `readme-sync-config.yml`

Each repository has custom page extraction rules - the README is split based on predefined patterns (section headers, markers, or line ranges) unique to each repo.

```yaml
repositories:
  - owner: thenvoi
    repo: thenvoi-mcp
    readme_path: README.md
    output_dir: docs/pages/integrations/mcp/synced
    pages:
      - filename: overview.mdx
        title: "MCP Overview"
        extract:
          start: "# Thenvoi MCP Server"
          end: "## Quick Start"
      - filename: quick-start.mdx
        title: "Quick Start"
        extract:
          start: "## 🚀 Quick Start"
          end: "## 📦 Install in Your IDE"
      - filename: ide-setup.mdx
        title: "IDE Setup"
        extract:
          start: "## 📦 Install in Your IDE"
          end: "## 🔨 Available Tools"
      - filename: tools-reference.mdx
        title: "Available Tools"
        extract:
          start: "## 🔨 Available Tools"
          end: "## 💡 Usage Examples"
      - filename: examples.mdx
        title: "Usage Examples"
        extract:
          start: "## 💡 Usage Examples"
          end: "## ⚙️ Configuration"

  - owner: thenvoi
    repo: thenvoi-sdk-python
    readme_path: README.md
    output_dir: docs/pages/integrations/sdks/synced
    pages:
      - filename: overview.mdx
        title: "Python SDK Overview"
        extract:
          start: "# Thenvoi Python SDK"
          end: "## Prerequisites"
      - filename: installation.mdx
        title: "Installation"
        extract:
          start: "## Prerequisites"
          end: "## Creating External Agents"
      - filename: setup.mdx
        title: "Creating External Agents"
        extract:
          start: "## Creating External Agents"
          end: "## Package Structure"

  - owner: thenvoi
    repo: phoenix-channels-python-client-alpha
    readme_path: README.md
    output_dir: docs/pages/integrations/phoenix/synced
    pages:
      - filename: index.mdx
        title: "Phoenix Channels Client"
        extract: all  # Include entire README as single page

  - owner: thenvoi
    repo: n8n-nodes-thenvoi
    readme_path: README.md
    output_dir: docs/pages/integrations/n8n/synced
    private: true
    pages:
      - filename: index.mdx
        title: "n8n Integration"
        extract: all

defaults:
  frontmatter_template: |
    ---
    title: "{title}"
    description: "Auto-synced from {repo} repository"
    ---
```

**Page extraction rules**:
- `extract.start` / `extract.end` - Extract content between these markers (inclusive of start, exclusive of end)
- `extract: all` - Include the entire README
- `extract.lines: [10, 50]` - Extract specific line ranges
- `extract.regex` - Match content by regex pattern

This allows full control over how each README is divided into documentation pages.

### Step 2: Create Transform Script
**File**: `scripts/sync-readmes.py`

Key capabilities:
- Fetch README via GitHub API (supports private repos with PAT)
- Parse custom extraction rules (start/end markers, line ranges, regex, or full file)
- Extract specified sections from each README based on config
- Convert markdown to MDX format
- Add YAML frontmatter with configured title/description
- Convert relative image paths to absolute GitHub URLs (raw.githubusercontent.com)
- Handle code blocks and preserve syntax highlighting

### Step 3: Create GitHub Action Workflow
**File**: `.github/workflows/sync-readmes.yml`

```yaml
name: Sync READMEs to Docs

on:
  schedule:
    - cron: '0 0 * * 0'  # Sunday midnight UTC
    - cron: '0 0 * * 3'  # Wednesday midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml requests

      - name: Sync READMEs
        env:
          GITHUB_TOKEN: ${{ secrets.README_SYNC_PAT }}
        run: python scripts/sync-readmes.py

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v6
        with:
          token: ${{ secrets.README_SYNC_PAT }}
          commit-message: "docs: sync READMEs from source repositories"
          title: "[Auto] Sync READMEs"
          body: |
            Automated sync of README files from source repositories.

            **Repositories synced:**
            - thenvoi-mcp
            - thenvoi-sdk-python
            - phoenix-channels-python-client-alpha
            - n8n-nodes-thenvoi
          branch: auto/sync-readmes
          base: main
          labels: documentation,automated
```

### Step 4: Set Up GitHub Secret
**Secret**: `README_SYNC_PAT`

Required permissions:
- `repo` scope (for private repo access)
- `workflow` scope (for creating PRs)

### Step 5: Update Navigation (Collaborative)
**File**: `fern/docs.yml`

We'll work together to decide the exact structure. Options:
- Add synced pages under existing sections (MCP, SDKs)
- Create new section for each repo
- Replace existing manual pages with synced content

---

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `readme-sync-config.yml` | Create | Configuration for repos and output paths |
| `scripts/sync-readmes.py` | Create | Python script to fetch and transform READMEs |
| `.github/workflows/sync-readmes.yml` | Create | GitHub Action workflow |
| `fern/docs.yml` | Modify | Add navigation entries for synced pages |
| `fern/docs/pages/integrations/*/synced/` | Create | Output directories for synced MDX files |

---

## GitHub Secrets Required

| Secret | Purpose |
|--------|---------|
| `README_SYNC_PAT` | GitHub PAT with `repo` + `workflow` scope for private repo access and PR creation |

---

## Next Steps

1. Create the configuration file with repo list
2. Build the transform script (Python)
3. Create the GitHub Action workflow
4. Add the PAT secret to the repository
5. Collaboratively decide on navigation structure
6. Test with a manual workflow dispatch
7. Review generated PR and iterate
