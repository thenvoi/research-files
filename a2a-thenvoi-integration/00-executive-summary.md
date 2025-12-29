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

| A2A        | Thenvoi          | Notes                                         |
| ---------- | ---------------- | --------------------------------------------- |
| A2A Server | Agent            | Each agent = A2A endpoint                     |
| Agent Card | Agent + metadata | Auto-generate                                 |
| Task       | AgentExecution   | Task is per-request, Execution is per-session |
| Message    | ChatMessage      | Role-based                                    |
| Skill      | Tool             | Derive from agent tools                       |

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

### Why This Order?

**Phase 1 (Outbound) before Phase 2 (Inbound)**:
- Outbound is simpler: we just need to call external A2A agents
- Inbound is harder: we need to expose our agents, handle various request formats, streaming, etc.
- Outbound gives immediate value: Thenvoi agents can start using external A2A agents right away

### Phase 1: A2A Outbound (TBD)

**Goal**: Thenvoi agents can call external A2A agents

**What we're building**: When a Thenvoi agent needs to use an external A2A agent, it calls out via HTTP.

**Key Deliverables**:
- [ ] Add `a2a_remote_url` field to Agent schema
- [ ] A2A Client module (fetch cards, send messages)
- [ ] Message Adapter (Thenvoi ↔ A2A format)
- [ ] Router update (check `a2a_remote_url` before routing)
- [ ] Agent Card caching
- [ ] UI field for A2A URL

**How routing works**:
```
if agent.a2a_remote_url != nil → use A2A (HTTP)
if agent.is_external → use WebSocket (current)
else → process locally
```

**Success Criteria**:
- Can configure external A2A agent URL in admin
- Thenvoi agent can call external A2A agent
- Response appears in chat
- Works with official A2A SDK samples

### Phase 2: A2A Inbound (TBD)

**Goal**: External A2A clients can discover and call Thenvoi agents

**What we're building**: External clients can fetch our Agent Cards and send messages via A2A protocol.

**Key Deliverables**:
- [ ] Agent Card Generator (build from Agent schema)
- [ ] `/.well-known/agent.json` endpoint
- [ ] A2A API endpoints (`/a2a/agents/{id}/message/send`, etc.)
- [ ] Task Adapter (Execution ↔ Task)
- [ ] SSE streaming
- [ ] Authentication
- [ ] Documentation

**Success Criteria**:
- External A2A client can fetch Agent Card
- External client can send message and get response
- Streaming works for long tasks
- Works with official A2A Python SDK

### Phase 3: Polish & Advanced (TBD)

**Goal**: Production-ready A2A integration

**Key Deliverables**:
- [ ] Error handling (map to A2A format)
- [ ] Retry logic, timeouts, circuit breaker
- [ ] Caching & performance optimization
- [ ] Push notifications (optional)
- [ ] Documentation & examples

**Success Criteria**:
- Error messages follow A2A spec
- Latency < 500ms p95
- Documentation complete

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

| Phase | Duration |
|-------|----------|
| Phase 1: A2A Outbound | TBD |
| Phase 2: A2A Inbound | TBD |
| Phase 3: Polish & Advanced | TBD |

**Total**: TBD

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
