# AgentCore + Thenvoi Integration: Executive Summary

**Research Period:** 2026-01-08
**Status:** Complete

---

## TL;DR

- **Amazon Bedrock AgentCore** is AWS's managed platform for deploying AI agents at scale (GA Oct 2025, 2M+ SDK downloads)
- **Strong Protocol Alignment**: AgentCore supports A2A protocol - Thenvoi's A2A integration work directly enables AgentCore compatibility
- **User Value**: AgentCore handles infrastructure; Thenvoi adds multi-agent orchestration, human-in-the-loop, and cross-framework collaboration
- **Three Integration Paths**: A2A server on Runtime, MCP server via Gateway, SDK adapter for Strands
- **Marketplace Opportunity**: List Thenvoi on AWS Bedrock Marketplace as A2A server and/or MCP server
- **Timing**: AgentCore is new (< 1 year), ecosystem building - first-mover advantage available

---

## Ranked Opportunities

| # | Opportunity | User Value | Feasibility | Priority | Notes |
|---|-------------|------------|-------------|----------|-------|
| 1 | **Thenvoi A2A Server on AgentCore Runtime** | High | High | **P0** | Leverages existing A2A work, direct marketplace listing |
| 2 | **Thenvoi MCP Server via Gateway** | High | High | **P0** | Expose Thenvoi orchestration as tools for any agent |
| 3 | **Python SDK Strands/AgentCore Adapter** | Medium | Medium | **P1** | Enable Thenvoi agents to run natively on AgentCore |
| 4 | **Multi-Agent Orchestration Templates** | Medium | Medium | **P1** | Pre-built patterns for AgentCore users |
| 5 | **Human-in-the-Loop for AgentCore** | High | Medium | **P2** | Approval workflows, human oversight for agent actions |
| 6 | **AgentCore Memory Bridge** | Medium | Low | **P3** | Sync Thenvoi memory with AgentCore Memory service |

---

## What is Amazon Bedrock AgentCore?

AgentCore is AWS's agentic platform for building, deploying, and operating AI agents at scale. Launched preview April 2025, GA October 2025.

### 9 Core Services

| Service | Purpose |
|---------|---------|
| **Runtime** | Serverless execution environment (up to 8 hours, session isolation) |
| **Gateway** | Transform APIs/Lambda/MCP servers into agent-compatible tools |
| **Memory** | Persistent context, episodic memory, learning from interactions |
| **Identity** | Secure access to AWS resources and third-party services |
| **Browser** | Cloud-based browser for web interactions |
| **Code Interpreter** | Secure sandbox for code execution |
| **Policy** | Real-time guardrails for agent actions (preview) |
| **Evaluations** | Quality assessment and monitoring (preview) |
| **Observability** | CloudWatch dashboards, OpenTelemetry integration |

### Key Stats
- 2M+ SDK downloads in 5 months
- Enterprise customers: Amazon, Cox Automotive, PGA TOUR, Thomson Reuters, Workday, S&P Global
- 80% of agents in AWS AI hackathon built on AgentCore

---

## User Value Analysis

### Why Would AgentCore Users Want Thenvoi?

| User Pain Point | AgentCore Limitation | Thenvoi Solution |
|-----------------|---------------------|------------------|
| **Multi-agent coordination** | A2A support exists but basic | Full orchestration patterns (supervisor, collaborative, hierarchical) |
| **Human oversight** | No native human-in-the-loop | Human participants in agent sessions, approval workflows |
| **Cross-framework teams** | Framework-agnostic but no orchestration layer | Adapters for LangGraph, Anthropic, PydanticAI, Claude SDK |
| **Real-time visibility** | CloudWatch metrics only | LiveView UI showing agent conversations in real-time |
| **Session management** | Memory service for context | Full chat system with multi-participant rooms |
| **Enterprise auth** | IAM-based | Multi-tenant SaaS with FusionAuth, RBAC |

### Compelling User Stories

1. **"I have agents built on LangGraph and CrewAI that need to collaborate"**
   - AgentCore runs them both but they can't easily communicate
   - Thenvoi provides the orchestration layer for agent collaboration

2. **"I need human approval before my agent takes certain actions"**
   - AgentCore Policy can block actions, but no human-in-the-loop
   - Thenvoi enables human participants who can approve/reject

3. **"I want to see what my agents are doing in real-time"**
   - AgentCore provides metrics and logs
   - Thenvoi provides live conversation UI with streaming

---

## Integration Paths

### Path 1: A2A Server on AgentCore Runtime (Recommended First)

Deploy Thenvoi as an A2A-compliant server container on AgentCore Runtime.

```
┌─────────────────────────────────────┐
│     AWS Bedrock AgentCore           │
│  ┌───────────────────────────────┐  │
│  │      AgentCore Runtime         │  │
│  │   ┌─────────────────────────┐ │  │
│  │   │  Thenvoi A2A Server     │ │  │
│  │   │  (Port 9000)            │ │  │
│  │   │  /.well-known/agent.json│ │  │
│  │   └─────────────────────────┘ │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         ↑ A2A Protocol
         │
┌─────────────────────────────────────┐
│  Other AgentCore Agents             │
│  (Strands, LangGraph, etc.)         │
└─────────────────────────────────────┘
```

**Requirements:**
- Port 9000 HTTP server
- `/ping` health check
- `/.well-known/agent-card.json` discovery
- JSON-RPC message/send endpoint
- ARM64 Docker container

**Value:** Any agent on AgentCore can discover and use Thenvoi orchestration capabilities.

### Path 2: MCP Server via AgentCore Gateway

Expose Thenvoi capabilities as MCP tools through AgentCore Gateway.

**Tools Exposed:**
- `thenvoi_create_session` - Create multi-agent collaboration session
- `thenvoi_add_agent` - Add agent to session
- `thenvoi_send_message` - Send message to session
- `thenvoi_wait_for_human` - Wait for human participant input
- `thenvoi_list_agents` - Discover available Thenvoi agents

**Value:** Any agent using AgentCore Gateway gets Thenvoi orchestration as native tools.

### Path 3: Python SDK AgentCore/Strands Adapter

Add AgentCore-native adapter to `thenvoi-sdk-python`.

```python
# New adapter in thenvoi-sdk-python
from thenvoi.adapters.agentcore import AgentCoreAdapter

adapter = AgentCoreAdapter(
    thenvoi_api_key="...",
    session_id="..."
)

# Use with Strands Agents
strands_agent = Agent(
    tools=[adapter.as_tool()],
    ...
)
```

**Value:** Thenvoi agents run natively on AgentCore Runtime with full integration.

---

## Bedrock Marketplace Listing

### Container Types Supported

| Type | Port | Path | Protocol | Thenvoi Fit |
|------|------|------|----------|-------------|
| Agent | 8080 | /invocations | HTTP JSON | Lower |
| MCP Server | 8000 | /mcp | JSON-RPC | High |
| A2A Server | 9000 | / | JSON-RPC | High |

### Listing Process

1. **Register as AWS Marketplace Seller**
2. **Complete Foundational Technical Review (FTR)**
3. **Build ARM64 Docker container** meeting requirements
4. **Push to Amazon ECR**
5. **Submit listing with documentation**
6. **ISV Accelerate Program** for co-sell support

### Pricing Options
- Usage-based (per request, per minute)
- Subscription (monthly flat fee)
- Free tier + paid features

---

## Competitive Landscape

### What AgentCore Users Use Today

| Solution | Strengths | Weaknesses vs Thenvoi |
|----------|-----------|----------------------|
| **Native A2A** | Built-in, simple | No orchestration patterns |
| **LangGraph Multi-agent** | Powerful graphs | Single framework |
| **CrewAI** | Role-based teams | No human participants |
| **Agent Squad (AWS)** | AWS-native | Basic routing only |
| **Custom solutions** | Flexible | Build from scratch |

### Thenvoi Differentiators

1. **Framework-agnostic** - Works with any AI framework
2. **Human-in-the-loop** - Unique capability
3. **Real-time UI** - LiveView for visibility
4. **A2A + MCP** - Both protocols supported
5. **Multi-tenant** - Enterprise-ready SaaS

---

## Synergies with Existing Thenvoi Work

### A2A Integration (Existing Research)

Thenvoi's A2A integration research directly enables AgentCore compatibility:
- A2A Server implementation → AgentCore Runtime deployment
- A2A Client → Connect to other AgentCore agents
- Agent Card generation → AgentCore discovery

### ACP Integration (Existing Research)

ACP + AgentCore creates full coverage:
- ACP for developer-facing (IDE) users
- AgentCore/A2A for agent-facing (orchestration) users
- Thenvoi as hub connecting both ecosystems

---

## Implementation Roadmap

### Phase 1: A2A Server Container (2-3 weeks)

**Goal:** List Thenvoi on Bedrock Marketplace as A2A server

- [ ] Create AgentCore-compliant Docker container
- [ ] Implement `/ping`, `/.well-known/agent-card.json`, JSON-RPC endpoints
- [ ] Test with AgentCore Runtime locally
- [ ] Register as AWS Marketplace seller
- [ ] Submit listing

### Phase 2: MCP Server via Gateway (2-3 weeks)

**Goal:** Expose Thenvoi tools through AgentCore Gateway

- [ ] Package existing thenvoi-mcp as Gateway-compatible
- [ ] Add Gateway-specific endpoints
- [ ] Create Gateway configuration templates
- [ ] Document integration

### Phase 3: SDK Adapter (2-3 weeks)

**Goal:** Native AgentCore support in thenvoi-sdk-python

- [ ] Create `AgentCoreAdapter`
- [ ] Add Strands Agents integration
- [ ] Update examples
- [ ] Publish to PyPI

### Phase 4: Templates & Patterns (Ongoing)

**Goal:** Make Thenvoi the go-to orchestration layer

- [ ] Multi-agent pattern templates
- [ ] Human-in-the-loop examples
- [ ] Documentation and tutorials
- [ ] Partner with AWS for co-marketing

---

## Open Questions

1. **Marketplace Pricing:** Usage-based or subscription? Free tier?
2. **AWS Partnership:** Pursue ISV Accelerate or independent?
3. **Priority:** A2A first or MCP first for marketplace?
4. **Thenvoi Cloud vs Self-hosted:** Which to list on marketplace?
5. **Enterprise Features:** VPC connectivity, PrivateLink support?

---

## Success Metrics

| Metric | 3 Month Target | 6 Month Target |
|--------|----------------|----------------|
| Marketplace listing live | Yes | Yes |
| AgentCore integrations | 5 | 25 |
| Monthly API calls from AgentCore | 10K | 100K |
| Enterprise customers via AgentCore | 1 | 5 |
| Documentation completeness | 80% | 95% |

---

## Key Sources

### AWS Documentation
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore Runtime for Marketplace](https://docs.aws.amazon.com/marketplace/latest/userguide/bedrock-agentcore-runtime.html)
- [A2A Protocol in AgentCore](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
- [AgentCore Python SDK](https://github.com/aws/bedrock-agentcore-sdk-python)
- [AgentCore Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)

### A2A Protocol
- [A2A Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [A2A GitHub](https://github.com/a2aproject/A2A)
- [Google A2A Announcement](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)

### AWS Marketplace
- [ISV Accelerate Program](https://aws.amazon.com/blogs/apn/accelerating-aws-partner-success-new-initiatives-to-drive-customer-value-in-2025/)
- [Agentic AI Competency](https://aws.amazon.com/blogs/apn/powering-partner-success-2026-innovations/)

---

## Research Files Index

| File | Description |
|------|-------------|
| [01-agentcore-deep-dive.md](./01-agentcore-deep-dive.md) | Full AgentCore capabilities and architecture |
| [02-user-value-analysis.md](./02-user-value-analysis.md) | Why AgentCore users would want Thenvoi |
| [03-integration-paths.md](./03-integration-paths.md) | Technical integration options |
| [04-marketplace-listing.md](./04-marketplace-listing.md) | Bedrock Marketplace listing guide |
| [05-competitive-landscape.md](./05-competitive-landscape.md) | Alternative solutions analysis |
| [06-implementation-roadmap.md](./06-implementation-roadmap.md) | Phased implementation plan |

---

*Research compiled by Claude Code for Thenvoi*
*Last updated: 2026-01-08*
