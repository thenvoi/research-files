# Multi-Agent Gap Analysis in ACP

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

ACP (Agent Client Protocol) is fundamentally designed for **single-agent, editor-centric** workflows. It standardizes communication between one code editor and one coding agent at a time. There is **no native support** for multi-agent orchestration, agent-to-agent communication, or parallel agent execution within the protocol. This represents a significant gap and opportunity for platforms like Thenvoi that specialize in multi-agent orchestration.

## Key Findings

### 1. ACP's Single-Agent Architecture

ACP is explicitly designed around a user-editor-agent triad, not multi-agent systems.

> "The user is primarily in their editor, and wants to reach out and use agents to assist them with specific tasks" - [ACP Introduction](https://agentclientprotocol.com/overview/introduction)

**Protocol Evidence:**
- Session management is 1:1 between client and agent
- `session/new`, `session/prompt`, `session/cancel` operate on single sessions
- No concept of agent-to-agent messaging in the schema
- No task delegation or handoff mechanisms

**Confidence:** High (based on official specification)

### 2. Active Community Demand for Parallel Agent Execution

The [Zed GitHub Discussion #37791](https://github.com/zed-industries/zed/discussions/37791) reveals strong community demand:

**Pain Points:**
- Users must wait for one agent to complete before starting another
- Developers open multiple Zed instances as a workaround
- Breaks Zed's "speed of thought" philosophy

**Community Signal:**
- 26 positive reactions on the proposal
- Comments express "urgent" demand
- Cited as competitive advantage for Cursor over Zed

**Proposed Workarounds:**
- Response queue system
- Alt+Send to remain with current agent
- Natural isolation via git worktrees
- Multi-targeting input bar

**Confidence:** High (direct community evidence)

### 3. No Agent-to-Agent Protocol in ACP

Unlike Google's A2A (Agent-to-Agent) protocol, ACP has **no mechanism** for agents to communicate with each other.

| Aspect | ACP | A2A |
|--------|-----|-----|
| **Primary Communication** | Editor ↔ Agent | Agent ↔ Agent |
| **Multi-Agent Support** | None native | Native design goal |
| **Task Delegation** | Not supported | Core feature |
| **Agent Discovery** | Registry (draft RFD) | Agent Cards |

**Community Discussion:**
> "There is no such protocol in the market that can provide the capability to work with multiple agents" - [Community feedback](https://ainativedev.io/news/zed-debuts-agent-client-protocol-to-connect-ai-coding-agents-to-any-editor)

**Confidence:** High (protocol comparison analysis)

### 4. Proxy Chains RFD Indicates Recognition of Gap

The ACP team has recognized this limitation through [RFD: Proxy Chains: Composable Agent Architectures](https://agentclientprotocol.com/rfds).

This draft RFD proposes a mechanism for chaining multiple agents, indicating:
- The team acknowledges the need for multi-agent patterns
- Solution is still in draft/design phase
- No timeline for implementation

**Confidence:** Medium (RFD is draft status)

### 5. Symposium Project: Emerging Multi-Agent Pattern

The [Symposium project](https://github.com/symposium-dev/symposium) (proposed for ACP organization) demonstrates community-driven multi-agent patterns:

> "Symposium enables library ecosystems where packages come with their own agent integration, creating extensible agents that users can customize with domain-specific capabilities."

**Key Features:**
- ACP proxy for Rust development
- Orchestrates specialized sub-proxies
- Intelligent selection based on dependencies and context
- Works with any ACP-supported editor

**Implication:** The community is building multi-agent solutions on top of ACP, validating the gap.

**Confidence:** High (active project, recent RFD submission)

### 6. Docker cagent Multi-Agent Runtime

Docker's [cagent](https://www.docker.com/blog/docker-jetbrains-and-zed-building-a-common-language-for-agents-and-ides/) provides a multi-agent runtime that supports ACP:

> "An open-source multi-agent runtime, already supports ACP, alongside Claude Code, Codex CLI, and Gemini CLI."

This shows:
- Enterprise players building multi-agent on ACP
- Validation of market demand
- Potential partnership/integration opportunity

**Confidence:** High (Docker official blog)

## Community Signals

### Feature Requests Across Major Projects

| Project | Issue | Reactions | Date |
|---------|-------|-----------|------|
| OpenAI Codex | [#2785](https://github.com/openai/codex/issues/2785) | 138 thumbs-up | Aug 2025 |
| Amazon Q | [#2703](https://github.com/aws/amazon-q-developer-cli/issues/2703) | 49 thumbs-up, 17 rockets | Aug 2025 |
| Claude Code | [#6686](https://github.com/anthropics/claude-code/issues/6686) | Active discussion | Aug 2025 |
| Warp Terminal | [#7326](https://github.com/warpdotdev/Warp/issues/7326) | Growing interest | Sep 2025 |

### User Workarounds (Reveal Unmet Needs)

1. **Multiple editor instances** - Users run parallel Zed/VS Code windows
2. **Git worktrees** - Manual isolation for concurrent agent work
3. **External orchestration** - Using separate tools to coordinate agents
4. **Custom adapters** - Building bespoke integrations (Claude Code, Codex required adapters)

## Gaps Identified

### Protocol-Level Gaps

1. **No multi-session coordination** - Cannot link or orchestrate multiple agent sessions
2. **No agent discovery/selection** - Registry RFD is still draft
3. **No task delegation** - Cannot handoff between agents
4. **No shared context** - Agents cannot access each other's state
5. **No parallel execution** - Protocol is inherently serial

### Ecosystem Gaps

1. **No orchestration layer** - Each editor implements its own (limited) solution
2. **No agent composition** - Cannot combine agent capabilities
3. **No workflow definition** - No declarative multi-step agent workflows
4. **No centralized state** - Each agent session is isolated

### Developer Experience Gaps

1. **Manual switching** - Users must explicitly change agents
2. **Context loss** - Switching agents loses conversation context
3. **No intelligent routing** - Cannot auto-select best agent for task
4. **Limited parallelism** - Significant productivity bottleneck

## Implications for Thenvoi

### Opportunity 1: ACP Orchestration Layer

Thenvoi could provide a multi-agent orchestration layer that:
- Sits between ACP clients and multiple ACP agents
- Routes requests to optimal agents
- Manages parallel execution
- Maintains shared context

**Value Proposition:** Enable ACP editors to access Thenvoi's multi-agent capabilities without protocol changes.

### Opportunity 2: Thenvoi as "Super Agent"

Thenvoi could expose itself as a single ACP agent that:
- Internally orchestrates multiple specialized agents
- Presents unified interface to editors
- Handles task decomposition and delegation
- Aggregates results

**Value Proposition:** Any ACP-compatible editor gets multi-agent capabilities "for free."

### Opportunity 3: ACP Proxy (Symposium Pattern)

Following the Symposium model, Thenvoi could offer:
- Domain-specific agent composition
- Intelligent agent selection
- Extensible agent ecosystem
- Works with all ACP clients

**Value Proposition:** Ecosystem play - developers add Thenvoi agents to their workflow.

### Opportunity 4: Bridge to A2A

Thenvoi already has A2A research completed. Could bridge:
- ACP (editor-to-Thenvoi) + A2A (Thenvoi-to-agents)
- Unified interface for both protocols
- First platform to truly solve multi-agent for IDE users

**Value Proposition:** Protocol unification - be the hub connecting all agent protocols.

## Sources Consulted

- [x] [ACP Specification](https://agentclientprotocol.com/overview/introduction) - Confirms single-agent design
- [x] [ACP Schema](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/schema/schema.json) - No multi-agent primitives
- [x] [Zed Discussion #37791](https://github.com/zed-industries/zed/discussions/37791) - Parallel execution demand
- [x] [ACP RFDs](https://agentclientprotocol.com/rfds) - Proxy Chains shows recognition of gap
- [x] [Symposium RFD](https://github.com/agentclientprotocol/agent-client-protocol/pull/359) - Multi-agent proxy pattern
- [x] [Docker cagent Blog](https://www.docker.com/blog/docker-jetbrains-and-zed-building-a-common-language-for-agents-and-ides/) - Enterprise multi-agent runtime
- [x] [AI Native Dev Article](https://ainativedev.io/news/zed-debuts-agent-client-protocol-to-connect-ai-coding-agents-to-any-editor) - Community sentiment
- [x] [ACP GitHub Issues](https://github.com/agentclientprotocol/agent-client-protocol/issues) - Active development priorities
- [ ] Discord/Zulip discussions - Not accessed (requires account)

## Related Research Files

- [01-acp-architecture.md](./01-acp-architecture.md) - Full ACP protocol analysis
- [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) - How Thenvoi could implement ACP
- Existing A2A research: `/Users/roishikler/codebase/research_files/a2a-thenvoi-integration/`
