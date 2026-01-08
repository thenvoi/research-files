# Research Files - Claude Instructions

## About This Repository

This is Thenvoi's research repository for market analysis, opportunity discovery, and integration planning.

**Thenvoi** is a startup building a platform for agent-to-agent communication. The platform enables AI agents built on different frameworks to communicate, collaborate, and orchestrate complex workflows.

## Architecture & Technical Context

For detailed information about Thenvoi systems:
- Read `../architecture-hub/README.md` for repository overview
- Use `.arch.md` files in `../architecture-hub/` for specific systems
- Key repos: `thenvoi-platform`, `thenvoi-sdk-python`, `thenvoi-mcp`

Do NOT clone or fetch from actual GitHub repos - the `.arch.md` files contain comprehensive documentation.

## Research Output Format

Research in this repo follows a structured format. See existing folders for reference:
- `a2a-thenvoi-integration/` - A2A protocol integration research
- `int-13-acp-discovery/` - ACP protocol discovery research

Each research project should include:
- `executive-summary.md` or `00-executive-summary.md` - TL;DR and ranked opportunities
- Numbered deep-dive files (`01-*.md`, `02-*.md`, etc.)
- Clear tables for comparisons, mappings, and prioritization

---

## Opportunity Research Methodology

When researching a new opportunity for Thenvoi, follow this workflow:

### Phase 1: Discovery & Scoping

1. **Clarify the opportunity**
   - Ask clarifying questions before starting
   - Define: What is the technology/market/protocol?
   - Define: Why might this matter to Thenvoi?

2. **Initial web research**
   - Search for official documentation, specs, GitHub repos
   - Find recent news, adoption metrics, ecosystem partners
   - Identify key players and competing solutions

3. **Create research folder**
   - Name: descriptive slug (e.g., `a2a-thenvoi-integration`)
   - Create initial structure with placeholder files

### Phase 2: Deep Analysis

4. **Technical deep-dive**
   - Core architecture and concepts
   - API/protocol specifications
   - SDK availability and language support
   - Integration patterns and examples

5. **Thenvoi alignment analysis**
   - Read relevant `.arch.md` files from `~/codebase/architecture-hub/`
   - Map concepts: How does X map to Thenvoi entities?
   - Identify architectural fit and gaps
   - Estimate implementation complexity

6. **Competitive landscape**
   - Who else is doing this?
   - What's their approach?
   - Where are the gaps Thenvoi can fill?

### Phase 3: Synthesis & Recommendations

7. **Opportunity ranking**
   - Create a ranked table: Opportunity | Value | Feasibility | Priority
   - Be specific about what "value" means (revenue, market position, users)

8. **Implementation roadmap**
   - Phase the work (start simple, add complexity)
   - Identify dependencies and prerequisites
   - Note open questions requiring human judgment

9. **Executive summary**
   - Write this LAST after all research is complete
   - Lead with TL;DR (3-5 bullets)
   - Include ranked opportunities table
   - List key findings by area with links to deep-dives
   - End with recommended next steps

### Research Best Practices

- **Use tables** for comparisons, mappings, status tracking
- **Include diagrams** (ASCII or mermaid) for architecture
- **Link to sources** - official docs, GitHub, announcements
- **Separate facts from opinions** - be clear about what's speculation
- **Note confidence levels** - especially for market predictions
- **Keep summaries scannable** - busy readers should get value in 2 minutes
- **Update as you learn** - research files are living documents

### Key Questions for Every Opportunity

Answer these in your executive summary:

1. **What is it?** (1-2 sentences)
2. **Why does it matter for Thenvoi?** (strategic value)
3. **What's the competitive landscape?**
4. **What would integration look like?** (high-level)
5. **What's the effort/value tradeoff?**
6. **What are the risks?**
7. **What decisions need human input?**

### Critical: User Value Analysis

**Every research MUST address this fundamental question:**

> Should Thenvoi integrate with this product/protocol at all? If yes, how would the integration create value for the product's existing users?

This is NOT about Thenvoi's benefit - analyze from the end-user's perspective:

- **What problem do users have today?** (without Thenvoi)
- **How would Thenvoi integration solve or improve it?**
- **What new capabilities would users gain?**
- **Is the value proposition clear and compelling?**
- **Would users actually want/pay for this?**

If you cannot articulate clear user value, flag this as a major risk. An integration that only benefits Thenvoi but not the product's users is unlikely to succeed.

---

## Web Research Tips

When gathering market intelligence:

- **Official sources first**: specs, docs, GitHub, company blogs
- **Check ecosystem**: partners, integrations, community projects
- **Find adoption signals**: stars, downloads, funding, enterprise users
- **Look for gaps**: unmet needs, community complaints, missing features
- **Verify recency**: AI/agent space moves fast - check dates

## Output Quality Checklist

Before marking research complete:

- [ ] Executive summary is self-contained and scannable
- [ ] All claims have sources or are marked as analysis
- [ ] Opportunities are ranked with clear criteria
- [ ] **User value is clearly articulated** (not just Thenvoi benefit)
- [ ] Thenvoi-specific integration is addressed
- [ ] Open questions and risks are documented
- [ ] Implementation phases are realistic
- [ ] File naming is consistent and logical
