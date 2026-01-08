# README-to-Fern Documentation Sync Research

## Problem Statement
Sync READMEs from public thenvoi repositories into Fern documentation automatically, keeping documentation close to code while presenting it in a unified documentation site.

## Existing Tools & Solutions Researched

### 1. Repo File Sync Action
**URL**: https://github.com/marketplace/actions/repo-file-sync-action

**How it works**: Syncs files between repositories via PRs. Runs in your main repository when code is pushed, reads a `sync.yml` config to determine which files to sync where.

**Pros**:
- Battle-tested with active maintenance
- Creates PRs for review before merging
- Supports file renaming during sync
- Template support (Nunjucks) for transformations

**Cons**:
- Requires setup in EACH source repository
- PAT with write access required
- Distributed config (harder to manage centrally)

---

### 2. MkDocs Multirepo Plugin
**URL**: https://github.com/jdoiro3/mkdocs-multirepo-plugin

**How it works**: Enables building documentation from multiple repos into one site. Uses `!import` statement in nav config to pull docs from specified repos at build time.

**Pros**:
- No duplication - always pulls fresh at build time
- Supports monorepos and multiple docs directories
- Async processing for fast imports

**Cons**:
- MkDocs-specific, not compatible with Fern
- Requires nav configuration changes

---

### 3. Git Submodules Approach
**How it works**: Add source repos as Git submodules, use build-time script to extract and transform READMEs.

**Pros**:
- Built into Git, version pinning available
- READMEs always pulled at build time (freshest)
- No PAT needed for public repos

**Cons**:
- Submodules are confusing for many developers
- Requires `--recurse-submodules` on clone
- Submodule updates need manual bumping

---

### 4. Custom GitHub Actions (Pull Pattern) - SELECTED
**How it works**: Build a custom workflow that periodically fetches READMEs from specified repos via GitHub API, transforms them to MDX, and creates a PR.

**Pros**:
- Full control over transformation logic
- Central configuration
- No changes needed in source repositories
- Matches existing Fern workflow patterns (similar to OpenAPI fetch)

**Cons**:
- Custom development required
- Need to maintain transformation script

---

## Community Patterns (from research)

### Federated Documentation Pattern
- Documentation distributed across code repositories
- Central docs repo pulls content from each code repo at build time
- Creates single site with unified structure
- Examples: OpenTelemetry docs, CentOS (uses Antora)

### Clone-and-Extract Pattern
- CI script clones repos, extracts docs, builds site
- Simple but adds clone overhead
- Use `--depth 1` for shallow clones

### Dispatch Triggers Pattern
- Source repos trigger central docs rebuild on changes via `repository_dispatch`
- Near real-time updates
- More complex setup

---

## Fern-Specific Considerations

### What Fern Supports
- MDX format with YAML frontmatter
- `<Code>` component for embedding GitHub code snippets (but not full READMEs)
- Auto-generated API Reference from OpenAPI specs
- Environment-aware deployments (dev/staging/prod)

### What Fern Doesn't Support
- No native `import` or `include` directive for markdown files
- No templating system for dynamic content injection
- Must manually manage markdown includes

### Existing Automation in Fern Repo
- OpenAPI spec auto-downloads from live API at build time
- Environment-aware publishing (dev/staging/prod)
- PR preview workflows
- Strong GitHub Actions foundation

---

## Sources

- [Repo File Sync Action](https://github.com/marketplace/actions/repo-file-sync-action)
- [MkDocs Multirepo Plugin](https://github.com/jdoiro3/mkdocs-multirepo-plugin)
- [Docs-as-Code Topologies](https://passo.uno/docs-as-code-topologies/)
- [Documentation as Code: Multi-Repo (Medium)](https://medium.com/@harryalexdunn/documentation-as-code-method-to-centralise-documentation-across-multiple-repositories-within-89f6485695f9)
- [Fern Documentation](https://buildwithfern.com/learn/docs/content/write-markdown)
