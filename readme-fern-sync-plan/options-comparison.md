# README Sync Options Comparison

## Summary

Three approaches for syncing READMEs from thenvoi repositories to Fern documentation.

---

## Option 1: Custom GitHub Action (SELECTED)

**Pattern**: Pull-based - Fern repo pulls READMEs on schedule

```
Source Repos → GitHub API → Transform Script → PR → Fern Docs
```

| Aspect | Details |
|--------|---------|
| Setup Location | Fern repo only |
| Trigger | Schedule (Sunday & Wednesday) + manual |
| Changes Flow | PR for review |
| Complexity | Medium |
| Control | High (central config) |

**Best for**: Central control, no changes to source repos, flexible transformation

---

## Option 2: Repo File Sync Action

**Pattern**: Push-based - Each source repo pushes to Fern

```
Source Repo Push → repo-file-sync-action → PR to Fern
```

| Aspect | Details |
|--------|---------|
| Setup Location | Each source repo |
| Trigger | On push to main |
| Changes Flow | PR for review |
| Complexity | High (distributed) |
| Control | Low (config per repo) |

**Best for**: Real-time sync, when source repos can be modified

---

## Option 3: Git Submodules

**Pattern**: Build-time extraction

```
Fern Repo (with submodules) → Build Script → Extract READMEs → Fern Docs
```

| Aspect | Details |
|--------|---------|
| Setup Location | Fern repo only |
| Trigger | At build time |
| Changes Flow | Direct (no PR) |
| Complexity | Medium-High |
| Control | High |

**Best for**: Version pinning, always-fresh builds

---

## Comparison Matrix

| Criteria | Option 1 | Option 2 | Option 3 |
|----------|----------|----------|----------|
| Setup complexity | Medium | High | Medium |
| Maintenance | Medium | Low (per repo) | High |
| Freshness | Near real-time | On push | Build time |
| Central control | High | Low | High |
| PR review flow | Yes | Yes | No |
| External deps | None | Action | None |
| Fits Fern patterns | Yes | Partially | No |

---

## Decision: Option 1 Selected

Reasons:
1. Matches existing Fern workflow patterns (similar to OpenAPI fetch)
2. All configuration centralized in Fern repo
3. No modifications needed to source repositories
4. Full flexibility for custom transformation logic
5. PR review flow ensures quality control
