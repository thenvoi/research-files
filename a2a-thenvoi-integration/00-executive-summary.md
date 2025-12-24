# A2A + Thenvoi Integration: Executive Summary

## Document Purpose

This document provides all information needed to create an implementation plan and PRD for integrating the A2A (Agent-to-Agent) protocol with the Thenvoi platform.

---

## 1. Project Goals

### Primary Objectives

1. **Enable A2A Users to Use Thenvoi**
   - Expose Thenvoi agents as A2A-compliant servers
   - External A2A clients can discover and call Thenvoi agents
   - Full protocol compliance with A2A specification

2. **Make Thenvoi A2A-Compatible by Default**
   - Internal agent communication uses A2A protocol
   - Thenvoi agents can call external A2A agents
   - Future-proof for A2A ecosystem improvements

### Strategic Value

- **Interoperability**: Connect with agents built on any framework
- **Ecosystem Play**: Participate in growing A2A ecosystem (50+ partners)
- **Future-Proofing**: Protocol maintained by Linux Foundation
- **Competitive Advantage**: First multi-agent platform with native A2A

---

## 2. What is A2A?

### Quick Overview

- **Open protocol** for agent-to-agent communication
- **Developed by Google**, now under Linux Foundation
- **Complementary to MCP**: A2A = agent-to-agent, MCP = agent-to-tool
- **Framework-agnostic**: Works with ADK, LangGraph, CrewAI, etc.

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Agent Card** | JSON manifest at `/.well-known/agent.json` describing capabilities |
| **Task** | Unit of work with lifecycle (submitted → working → completed) |
| **Message** | Communication turn with role (user/agent) and parts |
| **Part** | Content unit (text, file, structured data) |

### Communication Patterns

1. **Synchronous**: Request → Wait → Response
2. **Streaming**: Request → SSE events → Complete
3. **Push Notifications**: Request → Return → Webhook callbacks

---

## 3. Current Thenvoi Architecture (Relevant Parts)

### Agent System

```
Agent Schema:
- id, name, description
- model_type (LLM model)
- is_external (brings own LLM)
- tools (attached capabilities)
- visibility (personal/org/global)
```

### Execution System

```
AgentExecution:
- status: new → processing → waiting → completed/failed
- messages: Chat history
- tool_calls: Recorded tool invocations
```

### Communication

```
- REST API: /api/v1/*
- WebSocket: Phoenix Channels
- External Agents: Connect via SDK, receive messages, respond via API
```

---

## 4. Integration Architecture

### High-Level Design

```
┌─────────────────────────────────────────────────────────────┐
│                    External A2A Agents                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ A2A Protocol
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Thenvoi Platform                        │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   A2A Layer (NEW)                        ││
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐││
│  │  │ Agent Card  │ │ A2A Server  │ │ A2A Client Manager  │││
│  │  │ Generator   │ │ (Expose)    │ │ (Connect to External│││
│  │  └─────────────┘ └─────────────┘ └─────────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Existing Platform                      ││
│  │  Agents → Executor → Tools → Chat System                ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

### New Components Required

| Component | Purpose |
|-----------|---------|
| **Agent Card Generator** | Create A2A cards from Agent schema |
| **A2A Request Router** | Handle incoming A2A requests |
| **Message Adapter** | Convert A2A ↔ Thenvoi message formats |
| **Task Adapter** | Map A2A Task ↔ AgentExecution |
| **A2A Client Manager** | Manage external A2A agent connections |
| **Remote Agent Tool** | Let agents call external A2A agents |

---

## 5. Concept Mapping

### Entity Mapping

| A2A | Thenvoi | Notes |
|-----|---------|-------|
| A2A Server | Agent | Each agent = A2A endpoint |
| Agent Card | Agent + metadata | Auto-generate |
| Task | AgentExecution | 1:1 mapping |
| Message | ChatMessage | Role-based |
| Skill | Tool | Derive from agent tools |

### Status Mapping

| A2A State | Thenvoi Status |
|-----------|----------------|
| SUBMITTED | new |
| WORKING | processing |
| INPUT_REQUIRED | waiting |
| COMPLETED | completed |
| FAILED | failed |
| CANCELLED | *(new)* |
| REJECTED | *(new)* |

---

## 6. Implementation Phases

### Phase 1: A2A Server (4-6 weeks)

**Goal**: External A2A clients can call Thenvoi agents

**Deliverables**:
- [ ] Agent Card Generator
- [ ] A2A API endpoints (`/a2a/agents/{id}/...`)
- [ ] Message Adapter (A2A → Thenvoi)
- [ ] Task Adapter (Execution → Task)
- [ ] SSE streaming support
- [ ] Documentation

**Success Criteria**:
- External A2A SDK can discover Thenvoi agents
- Messages processed and responses returned
- Streaming works for long-running tasks

### Phase 2: A2A Client (3-4 weeks)

**Goal**: Thenvoi agents can call external A2A agents

**Deliverables**:
- [ ] A2A Client Manager
- [ ] Remote Agent Tool (call_remote_agent)
- [ ] Agent discovery and caching
- [ ] Message Adapter (Thenvoi → A2A)
- [ ] Error handling and retries

**Success Criteria**:
- Thenvoi agent can call external A2A agent via tool
- Results returned and incorporated into execution
- Works with official A2A SDK samples

### Phase 3: Internal A2A (2-3 weeks)

**Goal**: Internal agent-to-agent uses A2A

**Deliverables**:
- [ ] Internal A2A routing
- [ ] Optimized local transport
- [ ] Full protocol compliance
- [ ] Migration path for existing flows

**Success Criteria**:
- Agent handoffs use A2A internally
- No performance regression
- Protocol-compliant messages

### Phase 4: Advanced Features (4-6 weeks)

**Goal**: Full ecosystem participation

**Deliverables**:
- [ ] Push notifications
- [ ] Agent Card signing
- [ ] Extended Agent Cards
- [ ] gRPC binding (optional)
- [ ] Agent registry integration

---

## 7. API Design Summary

### New Endpoints

```
# Agent Card Discovery
GET  /a2a/agents/{id}/.well-known/agent.json

# A2A Protocol
POST /a2a/agents/{id}/              # JSON-RPC
POST /a2a/agents/{id}/message/send  # Send message
POST /a2a/agents/{id}/message/stream # Streaming
GET  /a2a/agents/{id}/tasks/{tid}   # Task status

# Platform
GET  /a2a/agents                    # List A2A agents
```

### Agent Card Example

```json
{
  "name": "Research Agent",
  "description": "Deep research on any topic",
  "url": "https://app.thenvoi.com/a2a/agents/{id}/",
  "version": "1.0.0",
  "protocolVersion": "0.3",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "research",
      "name": "Research",
      "description": "Research any topic deeply"
    }
  ],
  "securitySchemes": {
    "apiKey": {
      "type": "apiKey",
      "in": "header",
      "name": "Authorization"
    }
  }
}
```

---

## 8. Schema Changes Required

### Agent Table

```sql
ALTER TABLE agents ADD COLUMN a2a_enabled BOOLEAN DEFAULT false;
ALTER TABLE agents ADD COLUMN a2a_skills JSONB DEFAULT '[]';
ALTER TABLE agents ADD COLUMN a2a_capabilities JSONB DEFAULT '{}';
ALTER TABLE agents ADD COLUMN a2a_remote_url TEXT;  -- For external A2A agents
```

### AgentExecution Table

```sql
ALTER TABLE agent_executions ADD COLUMN a2a_task_id TEXT;
ALTER TABLE agent_executions ADD COLUMN a2a_context_id TEXT;
ALTER TABLE agent_executions ADD COLUMN a2a_callback_url TEXT;
```

### New Status Values

```elixir
# Add to valid statuses
"cancelled"     # A2A CANCELLED
"rejected"      # A2A REJECTED
"auth_required" # A2A AUTH_REQUIRED
```

---

## 9. Technical Considerations

### Performance

| Concern | Mitigation |
|---------|------------|
| Agent Card requests | Cache with TTL |
| Message conversion overhead | Optimize adapters |
| External agent latency | Async with timeouts |
| Streaming connections | Connection pooling |

### Security

| Concern | Mitigation |
|---------|------------|
| Unauthorized access | API key required |
| Data exposure | Filter sensitive fields from cards |
| External agent trust | Allow-list for external agents |
| Rate limiting | Per-caller limits |

### Compatibility

- Support A2A protocol version 0.3+
- Graceful degradation for unsupported features
- Version negotiation via headers

---

## 10. Dependencies

### External

- A2A Python SDK (`a2a-sdk`) for client implementation
- JSON-RPC library for request handling
- SSE library for streaming

### Internal

- Agent schema modifications
- Executor integration
- ServiceRegistry updates
- WebSocket channel extensions

---

## 11. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Protocol changes | Medium | High | Abstract A2A layer, version support |
| Performance impact | Low | Medium | Optimize local routing, caching |
| Security exposure | Medium | High | Strict auth, allow-lists, auditing |
| Adoption challenges | Medium | Medium | Documentation, examples, support |

---

## 12. Success Metrics

| Metric | Phase 1 Target | Phase 4 Target |
|--------|----------------|----------------|
| A2A endpoint latency (p95) | < 500ms | < 200ms |
| Agent Card response time | < 100ms | < 50ms |
| External agent call success | > 95% | > 99% |
| A2A-enabled agents | 10% | 50% |
| External A2A integrations | 5 | 50+ |

---

## 13. Resource Estimates

| Phase | Duration | Backend | Frontend | QA |
|-------|----------|---------|----------|-----|
| Phase 1 | 4-6 weeks | 2 devs | 0.5 dev | 1 dev |
| Phase 2 | 3-4 weeks | 1.5 devs | 0 | 0.5 dev |
| Phase 3 | 2-3 weeks | 1 dev | 0 | 0.5 dev |
| Phase 4 | 4-6 weeks | 1.5 devs | 0.5 dev | 1 dev |

**Total**: ~15-20 weeks with dedicated team

---

## 14. Research Files Index

| File | Description |
|------|-------------|
| `01-a2a-protocol-deep-dive.md` | Complete A2A protocol documentation |
| `02-thenvoi-platform-architecture.md` | Thenvoi architecture analysis |
| `03-thenvoi-sdk-integration.md` | SDK and integration patterns |
| `04-product-vision-overview.md` | Product vision and roadmap |
| `05-a2a-thenvoi-integration-analysis.md` | Detailed integration analysis |

---

## 15. Key Decisions Needed

### Before Implementation

1. **A2A Default Behavior**: Enabled by default for new agents?
2. **External Agent Trust**: Allow-list or open federation?
3. **Billing Model**: Usage-based for A2A calls?
4. **Feature Flags**: Gradual rollout strategy?

### Architecture Decisions

1. **Internal A2A**: Optimize for local or use full protocol?
2. **Streaming**: SSE-only or also support gRPC?
3. **Push Notifications**: Webhooks or WebSocket-based?

---

## 16. Next Steps

1. **Review this document** with engineering and product
2. **Validate architecture** with technical leads
3. **Prioritize phases** based on business needs
4. **Create detailed PRD** for Phase 1
5. **Set up development environment** with A2A SDK
6. **Prototype Agent Card generation** as proof of concept

---

## 17. References

### Official A2A Resources

- Specification: https://a2a-protocol.org/latest/specification/
- GitHub: https://github.com/a2aproject/A2A
- Python SDK: https://github.com/a2aproject/a2a-python
- Samples: https://github.com/a2aproject/a2a-samples

### Thenvoi Resources

- Platform: ~/codebase/thenvoi-platform
- Python SDK: ~/codebase/thenvoi-sdk-python
- MCP Server: ~/codebase/thenvoi-mcp
- Product Docs: ~/codebase/product-docs-vault

### Example A2A Implementations

- Multi-agent demo: ~/codebase/projects/agent2agent/
