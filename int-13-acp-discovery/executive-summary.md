# INT-13: ACP Discovery - Executive Summary

**Research Period:** 2026-01-06
**Status:** Complete

---

## TL;DR

- **ACP (Agent Client Protocol)** is an emerging standard for connecting code editors to AI coding agents, with strong momentum (Zed, JetBrains, Google, Docker backing)
- **Critical Gap**: ACP has **no native multi-agent support** - this is Thenvoi's primary opportunity
- **Strong Architectural Fit**: Thenvoi's existing MCP server, Python SDK, and multi-agent platform align well with ACP integration
- **First-Mover Advantage**: No multi-agent orchestration platform has ACP support yet - Thenvoi could be first
- **Recommended Action**: Build Thenvoi ACP agent using Python SDK, starting with "Super-Agent" pattern that exposes orchestrated agents to any ACP-compatible editor

---

## Ranked Opportunities

| # | Opportunity | Value | Feasibility | Priority | Notes |
|---|-------------|-------|-------------|----------|-------|
| 1 | **Thenvoi as ACP "Super-Agent"** | High | High | **P0** | Single ACP agent exposing multi-agent orchestration |
| 2 | **Multi-Agent Orchestration Layer** | High | Medium | **P1** | Proxy pattern for routing to multiple agents |
| 3 | **ACP + A2A Bridge** | High | Medium | **P1** | Connect ACP editors to A2A agent networks |
| 4 | **Enhanced MCP Integration** | Medium | High | **P2** | Expose Thenvoi tools to any ACP agent |
| 5 | **Zed Extension Distribution** | Medium | Medium | **P2** | Marketplace presence for discovery |
| 6 | **Enterprise Security Layer** | Medium | Medium | **P2** | SSO, RBAC, audit for enterprise ACP users |

---

## Key Findings by Area

### [ACP Architecture](./01-acp-architecture.md)
- JSON-RPC over stdio protocol, similar design philosophy to LSP
- Strong ecosystem momentum: Zed native, JetBrains coming, Neovim/Emacs plugins
- SDKs available in Python, TypeScript, Rust, Kotlin
- Protocol actively evolving (v0.10.6, 11 draft RFDs)

### [ACP-MCP Integration](./02-acp-mcp-integration.md)
- ACP and MCP are complementary: ACP for editor↔agent, MCP for agent↔tools
- Editors pass MCP server configs to agents during initialization
- Thenvoi's existing MCP server can be used by any ACP agent
- Opportunity to bridge ACP clients to Thenvoi's tool ecosystem

### [Multi-Agent Gap](./03-multi-agent-gap.md) ⭐ **Highest Priority Finding**
- ACP is fundamentally single-agent, editor-centric
- Active community demand for parallel agent execution (26+ reactions on Zed discussion)
- No native agent-to-agent communication (unlike A2A)
- Symposium project and Docker cagent show community building multi-agent on top
- **Thenvoi would be first multi-agent platform with ACP support**

### [Custom Agent Integration](./04-custom-agent-integration.md)
- Python SDK provides accessible path for custom agents
- Adapter pattern used for major agents (Claude Code, Codex)
- External agents have feature limitations (no editing, history)
- Zed configuration via JSON, extension marketplace emerging

### [Thenvoi as ACP Agent](./05-thenvoi-as-acp-agent.md)
- Strong architectural alignment: Agent↔ACP Agent, AgentExecution↔Session
- Recommended: Start with Super-Agent pattern, evolve to Proxy
- Implementation via Python SDK aligns with existing stack
- Agent selection via slash commands, modes, and smart routing

### [Developer Experience](./06-developer-experience.md)
- Varied DX: smooth for built-in agents, friction for custom
- Pain points: configuration complexity, adapter requirements, testing gaps
- Opportunity: Thenvoi can provide turnkey setup, configuration wizard, comprehensive docs
- Target: < 5 minute setup vs current 15-30 minutes

### [Security & Permissions](./07-security-permissions.md)
- Process isolation as primary security boundary
- User-consent permission model via `session/request_permission`
- Authentication currently out-of-band (API keys in env vars)
- Enterprise gaps: no SSO, RBAC, standardized audit
- Thenvoi can add enterprise security layer

---

## Recommended Next Steps

### Immediate (Next Sprint)

1. **Prototype ACP Agent**
   - Use Python SDK (`agent-client-protocol`)
   - Implement `initialize`, `session/new`, `session/prompt`
   - Connect to Thenvoi platform via REST API
   - Test with Zed editor

2. **Document Integration**
   - Zed configuration guide
   - Authentication setup
   - Troubleshooting FAQ

### Short-Term (1-2 Sprints)

3. **Add Streaming Support**
   - Bridge Phoenix Channels to ACP `session/update`
   - Implement tool call streaming
   - Add MCP passthrough

4. **Multi-Agent UX**
   - Slash commands for agent selection
   - Session modes for persistent selection
   - Smart routing (optional)

### Medium-Term (3-4 Sprints)

5. **Distribution**
   - Package as Zed extension
   - Submit to ACP registry
   - Neovim/Emacs documentation

6. **Enterprise Features**
   - OAuth flow (replace API keys)
   - Server-side permissions
   - Audit logging

---

## Open Questions

These require human/product judgment:

1. **Positioning**: Should Thenvoi ACP be free (growth) or paid (revenue)?
2. **Agent Selection**: Should we expose all Thenvoi agents or curated set?
3. **Priority**: ACP integration vs completing A2A integration first?
4. **Resources**: Dedicated team or part of existing SDK work?
5. **Partnership**: Pursue Zed/JetBrains partnership or independent?

---

## Success Metrics

| Metric                       | 3 Month Target | 6 Month Target |
| ---------------------------- | -------------- | -------------- |
| Editor integrations          | Zed            | Zed + 2 others |
| Monthly active users via ACP | TBD            | TBD            |
| First token latency (p95)    | TBD            | < TBD          |
| Setup time                   | TBD            | TBD            |
| Documentation NPS            | TBD            | TBD            |

---

## All Research Files

| File | Description |
|------|-------------|
| [01-acp-architecture.md](./01-acp-architecture.md) | Full ACP protocol analysis |
| [02-acp-mcp-integration.md](./02-acp-mcp-integration.md) | ACP and MCP complementary usage |
| [03-multi-agent-gap.md](./03-multi-agent-gap.md) | Multi-agent limitations and opportunity |
| [04-custom-agent-integration.md](./04-custom-agent-integration.md) | Building custom ACP agents |
| [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) | Thenvoi implementation approach |
| [06-developer-experience.md](./06-developer-experience.md) | DX analysis and recommendations |
| [07-security-permissions.md](./07-security-permissions.md) | Security model and enterprise features |

---

## Key Sources

- [ACP Official Site](https://zed.dev/acp)
- [ACP GitHub](https://github.com/agentclientprotocol/agent-client-protocol)
- [ACP Python SDK](https://github.com/agentclientprotocol/python-sdk)
- [Zed External Agents Docs](https://zed.dev/docs/ai/external-agents)
- [Zed Parallel Agents Discussion](https://github.com/zed-industries/zed/discussions/37791)
- [Docker cagent Blog](https://www.docker.com/blog/docker-jetbrains-and-zed-building-a-common-language-for-agents-and-ides/)
- [ACP Progress Report](https://zed.dev/blog/acp-progress-report)

---

## Comparison: ACP vs A2A

Since Thenvoi has existing A2A research, here's how the protocols differ:

| Aspect | ACP | A2A |
|--------|-----|-----|
| **Purpose** | Editor ↔ Agent | Agent ↔ Agent |
| **Primary User** | Developer in IDE | Agent orchestrator |
| **Multi-Agent** | Not native | Native design |
| **Transport** | stdio/HTTP | HTTP |
| **Ecosystem** | Zed, JetBrains, Google | Google ADK, LangChain |
| **Maturity** | Early (v0.10.x) | Early (v0.3) |

**Recommendation**: Implement both ACP and A2A to maximize reach:
- ACP for developer-facing (IDE) users
- A2A for agent-facing (orchestration) users
- Thenvoi as the hub connecting both ecosystems

---

*Research compiled by Claude Code for Thenvoi*
*Last updated: 2026-01-06*
