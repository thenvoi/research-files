# Implementation Roadmap: Thenvoi + AgentCore

## Overview

This roadmap outlines the phased implementation of Thenvoi integration with Amazon Bedrock AgentCore, from initial prototype to full marketplace listing.

---

## Phase 0: Prerequisites & Research (Complete)

### Deliverables

- [x] Research AgentCore capabilities
- [x] Understand A2A protocol requirements on AgentCore
- [x] Document marketplace listing requirements
- [x] Analyze competitive landscape
- [x] Validate user value proposition

### Outputs

- This research folder
- Clear integration paths identified
- Go/no-go decision inputs

---

## Phase 1: MCP Server via Gateway

**Duration:** 2-3 weeks
**Priority:** P0
**Dependencies:** Existing thenvoi-mcp

### Goal

Expose Thenvoi orchestration capabilities as MCP tools through AgentCore Gateway.

### Why First

- Lowest effort (extend existing thenvoi-mcp)
- Immediate value (tools available to all Gateway users)
- Tests Thenvoi-AgentCore connectivity
- No marketplace registration needed yet

### Tasks

#### Week 1: Extend thenvoi-mcp

- [ ] Review Gateway MCP requirements (port 8000, `/mcp` endpoint)
- [ ] Add Gateway-compatible HTTP transport to thenvoi-mcp
- [ ] Define new tool schemas:
  - `thenvoi_create_session`
  - `thenvoi_add_agent`
  - `thenvoi_send_message`
  - `thenvoi_wait_for_human`
  - `thenvoi_list_agents`
  - `thenvoi_get_session_status`
- [ ] Implement tool handlers connecting to Thenvoi platform API

#### Week 2: Testing & Documentation

- [ ] Local testing with MCP client
- [ ] Test with AgentCore Gateway (requires AWS account)
- [ ] Write integration guide
- [ ] Create example workflows
- [ ] Performance testing

#### Week 3: Polish & Release

- [ ] Error handling improvements
- [ ] Logging and observability
- [ ] Publish updated thenvoi-mcp
- [ ] Announce availability

### Success Criteria

- [ ] MCP tools listed in Gateway catalog
- [ ] End-to-end workflow working (create session → send message → get response)
- [ ] Documentation complete
- [ ] At least one external user testing

---

## Phase 2: A2A Server on AgentCore Runtime

**Duration:** 3-4 weeks
**Priority:** P0
**Dependencies:** Thenvoi A2A implementation (from existing A2A roadmap)

### Goal

Deploy Thenvoi as an A2A-compliant server on AgentCore Runtime, enabling agent-to-agent discovery and communication.

### Why This Phase

- Enables agent discovery via Agent Cards
- Opens Bedrock Marketplace listing
- Leverages existing A2A implementation work
- Higher visibility than MCP-only

### Tasks

#### Week 1: A2A Server Container

- [ ] Create new repo/package: `thenvoi-agentcore-a2a`
- [ ] Implement server (FastAPI or similar):
  - `/ping` health check
  - `/.well-known/agent-card.json` generator
  - `/` JSON-RPC handler
- [ ] Connect to Thenvoi platform (REST + WebSocket)
- [ ] Dockerfile for ARM64

#### Week 2: AgentCore Compatibility

- [ ] Test locally on port 9000
- [ ] Test with `agentcore configure --protocol A2A`
- [ ] Test deployment to AgentCore Runtime
- [ ] Verify agent discovery from other agents
- [ ] Message flow testing

#### Week 3: Marketplace Preparation

- [ ] Register as AWS Marketplace seller (if not already)
- [ ] Prepare listing content:
  - Product name, descriptions
  - Logo assets
  - Pricing strategy
- [ ] Complete Foundational Technical Review (FTR)
- [ ] Push container to ECR

#### Week 4: Listing & Launch

- [ ] Submit marketplace listing
- [ ] Address AWS review feedback
- [ ] Prepare launch communications
- [ ] Go live on marketplace

### Success Criteria

- [ ] A2A server running on AgentCore Runtime
- [ ] Agent Card discoverable by other agents
- [ ] End-to-end message flow working
- [ ] Listed on AWS Marketplace
- [ ] At least 5 early adopters

---

## Phase 3: Python SDK AgentCore Adapter

**Duration:** 2-3 weeks
**Priority:** P1
**Dependencies:** Phase 1 or 2 complete

### Goal

Add AgentCore/Strands adapter to thenvoi-sdk-python for native Python integration.

### Why This Phase

- Enables Python developers to use Thenvoi natively
- Complements existing SDK adapters
- Not required for marketplace but enhances DX

### Tasks

#### Week 1: Adapter Implementation

- [ ] Create `src/thenvoi/adapters/agentcore.py`
- [ ] Implement `AgentCoreAdapter` class
- [ ] Add Strands-compatible tool generation
- [ ] Unit tests

#### Week 2: Integration & Examples

- [ ] Integration tests with Thenvoi platform
- [ ] Create examples:
  - Basic orchestration
  - Human-in-the-loop
  - Multi-framework
- [ ] Update SDK documentation

#### Week 3: Release

- [ ] Code review and polish
- [ ] Update PyPI package
- [ ] Announce adapter availability
- [ ] Gather feedback

### Success Criteria

- [ ] Adapter published in thenvoi-sdk-python
- [ ] At least 3 working examples
- [ ] Documentation complete
- [ ] PyPI package updated

---

## Phase 4: Templates & Patterns

**Duration:** Ongoing
**Priority:** P1
**Dependencies:** Phases 1-3

### Goal

Provide pre-built templates and patterns for common AgentCore + Thenvoi use cases.

### Templates to Create

1. **Supervisor Agent Pattern**
   - Central coordinator + specialist agents
   - Automatic task routing
   - Result aggregation

2. **Human Approval Workflow**
   - Agent proposes action
   - Session waits for human
   - Human approves/rejects
   - Agent continues

3. **Cross-Framework Collaboration**
   - LangGraph + CrewAI + custom
   - Shared session context
   - Unified outputs

4. **Customer Support Escalation**
   - Tier 1-3 agent handoffs
   - Human agent integration
   - Context preservation

### Tasks

- [ ] Design template structure
- [ ] Implement each template
- [ ] Test with real AgentCore deployments
- [ ] Document setup and customization
- [ ] Create video walkthroughs

### Success Criteria

- [ ] 4+ templates available
- [ ] Each template documented
- [ ] At least 10 users using templates
- [ ] Positive feedback on ease of use

---

## Phase 5: Advanced Features

**Duration:** 3-4 weeks
**Priority:** P2
**Dependencies:** Phases 1-3

### Goal

Add enterprise and advanced features for AgentCore integration.

### Features

1. **AgentCore Memory Bridge**
   - Sync Thenvoi sessions with AgentCore Memory service
   - Unified context management
   - Episodic memory integration

2. **AgentCore Identity Integration**
   - Use AgentCore Identity for Thenvoi auth
   - SSO federation
   - Cross-service authorization

3. **Enhanced Observability**
   - Push Thenvoi metrics to CloudWatch
   - OpenTelemetry integration
   - Unified dashboards

4. **VPC/PrivateLink Support**
   - Private network deployment
   - No public internet exposure
   - Enterprise security requirements

### Tasks

- [ ] Prioritize features based on customer demand
- [ ] Implement highest priority features
- [ ] Test in enterprise environments
- [ ] Document enterprise setup

### Success Criteria

- [ ] At least 2 advanced features shipped
- [ ] Enterprise customer using advanced features
- [ ] Documentation for enterprise deployment

---

## Timeline Summary

```
Month 1:
├── Week 1-2: Phase 1 (MCP Server)
└── Week 3-4: Phase 2 Start (A2A Server)

Month 2:
├── Week 1-2: Phase 2 Continue (Marketplace prep)
├── Week 3: Phase 2 Complete (Listing live)
└── Week 4: Phase 3 Start (SDK Adapter)

Month 3:
├── Week 1-2: Phase 3 Complete
└── Week 3-4: Phase 4 Start (Templates)

Month 4+:
├── Phase 4 Continue (Templates)
└── Phase 5 (Advanced Features)
```

---

## Resource Estimates

### Phase 1: MCP Server

| Role | Time |
|------|------|
| Backend Engineer | 2 weeks |
| DevOps | 0.5 weeks |
| Technical Writer | 0.5 weeks |

### Phase 2: A2A Server + Marketplace

| Role | Time |
|------|------|
| Backend Engineer | 3 weeks |
| DevOps | 1 week |
| Business (Marketplace) | 1 week |
| Technical Writer | 0.5 weeks |

### Phase 3: SDK Adapter

| Role | Time |
|------|------|
| Backend Engineer | 2 weeks |
| Technical Writer | 0.5 weeks |

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| AWS review delays | Medium | Medium | Start FTR early, buffer time |
| A2A work delayed | Medium | High | Phase 1 provides value independently |
| Low marketplace adoption | Medium | Medium | Focus on direct sales initially |
| AgentCore API changes | Low | High | Abstract integration layer |
| Competition from AWS | Medium | High | Focus on human-in-the-loop differentiator |

---

## Decision Points

### Before Phase 1

- [ ] Confirm thenvoi-mcp can be extended (vs new repo)
- [ ] Confirm AWS account access for testing
- [ ] Prioritize MCP tools to implement

### Before Phase 2

- [ ] Decide on pricing strategy
- [ ] Confirm A2A implementation timeline
- [ ] Register as Marketplace seller

### Before Phase 4

- [ ] Gather customer feedback on template needs
- [ ] Prioritize templates based on demand

---

## Success Metrics

| Metric | 3 Month | 6 Month | 12 Month |
|--------|---------|---------|----------|
| Marketplace listing | Live | Live | Live |
| Monthly API calls via AgentCore | 10K | 50K | 200K |
| AgentCore customers using Thenvoi | 5 | 25 | 100 |
| Enterprise deals via AgentCore | 0 | 2 | 10 |
| Template users | N/A | 20 | 100 |
| NPS from AgentCore users | N/A | 30 | 50 |

---

## Open Questions

1. **Pricing:** Usage-based, subscription, or hybrid?
2. **Priority:** MCP or A2A first if resources constrained?
3. **AWS Partnership:** Pursue ISV Accelerate immediately?
4. **A2A Dependency:** Can Phase 2 proceed without existing A2A work?
5. **Thenvoi Cloud vs Self-hosted:** Which to list first?

---

## Next Steps

1. **Product/Engineering Review:** Validate timeline and resource estimates
2. **AWS Account Setup:** Ensure access for AgentCore testing
3. **Marketplace Registration:** Start seller registration process
4. **A2A Alignment:** Coordinate with existing A2A implementation roadmap
5. **Customer Validation:** Talk to 2-3 potential AgentCore users
