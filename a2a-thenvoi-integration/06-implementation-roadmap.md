# A2A Integration Implementation Roadmap

## Overview

This document provides a simplified implementation plan for integrating A2A protocol with Thenvoi. The plan is organized in 3 phases, starting with the most practical deliverable first.

---

## Why This Order?

**Phase 1 (Outbound) before Phase 2 (Inbound)**:
- Outbound is simpler: we just need to call external A2A agents
- Inbound is harder: we need to expose our agents, handle various request formats, streaming, etc.
- Outbound gives immediate value: Thenvoi agents can start using external A2A agents right away

---

## Phase 1: A2A Outbound (Thenvoi Calls External A2A Agents)

**Duration**: TBD

**Goal**: Thenvoi agents can call external A2A agents as a tool

### What We're Building

When a Thenvoi agent needs to use an external A2A agent, it will:
1. Look up the agent's capabilities (fetch Agent Card)
2. Send a message using A2A protocol
3. Get the response back

### Key Deliverables

#### 1.1 Schema Change

Add a field to know where external A2A agents live:

```elixir
# Agent schema
%Agent{
  is_external: true,
  a2a_remote_url: "http://localhost:5050"  # NEW FIELD
}
```

**Decision logic**:
- `a2a_remote_url` is set → use A2A protocol to call this agent
- `a2a_remote_url` is nil + `is_external` → agent connects via WebSocket (current behavior)
- `is_external` is false → internal agent, process locally

#### 1.2 A2A Client Module

A module that can:
- Fetch Agent Card from `{url}/.well-known/agent.json`
- Send messages to `{url}/message/send`
- Handle responses

```elixir
# Pseudocode
defmodule ThenvoiCom.A2A.Client do
  def fetch_agent_card(url) do
    # GET {url}/.well-known/agent.json
  end

  def send_message(url, message) do
    # POST {url}/message/send with A2A-formatted message
  end
end
```

#### 1.3 Router Update

Update the agent message router to check if we should use A2A:

```elixir
def route_to_agent(agent, message) do
  cond do
    # External A2A agent - call via HTTP
    agent.a2a_remote_url != nil ->
      A2AClient.send_message(agent.a2a_remote_url, message)

    # External WebSocket agent - do nothing, they're listening
    agent.is_external ->
      :noop

    # Internal agent - process locally
    true ->
      Executor.process(agent, message)
  end
end
```

#### 1.4 Message Adapter

Convert Thenvoi messages to A2A format and back:

```elixir
# Thenvoi → A2A
%{content: "Hello", sender_type: "User"}
→
%{role: "user", parts: [%{type: "text", text: "Hello"}]}

# A2A → Thenvoi
%{role: "agent", parts: [%{type: "text", text: "Hi!"}]}
→
%{content: "Hi!", sender_type: "Agent"}
```

### Tasks

| Task | Description |
|------|-------------|
| Add `a2a_remote_url` field to Agent schema | Database migration |
| Create A2A Client module | HTTP client for A2A protocol |
| Create Message Adapter | Convert message formats |
| Update router logic | Check `a2a_remote_url` before routing |
| Add Agent Card caching | Don't fetch card every time |
| Add UI field for A2A URL | Let users configure external A2A agents |
| Write tests | Unit and integration tests |

### Success Criteria

- [ ] Can add external A2A agent URL in admin UI
- [ ] Thenvoi agent can send message to external A2A agent
- [ ] Response from A2A agent appears in chat
- [ ] Works with official A2A SDK samples

---

## Phase 2: A2A Inbound (External Clients Call Thenvoi Agents)

**Duration**: TBD

**Goal**: External A2A clients can discover and call Thenvoi agents

### What We're Building

When an external A2A client wants to use a Thenvoi agent:
1. Client fetches Agent Card from Thenvoi
2. Client sends message via A2A protocol
3. Thenvoi processes and returns response

### Key Deliverables

#### 2.1 Agent Card Generator

Generate A2A Agent Card from Thenvoi Agent data:

```json
GET /a2a/agents/{id}/.well-known/agent.json

{
  "name": "Research Agent",
  "description": "Deep research on any topic",
  "url": "https://app.thenvoi.com/a2a/agents/{id}/",
  "version": "1.0.0",
  "protocolVersion": "0.3",
  "capabilities": {
    "streaming": true
  },
  "skills": [
    {
      "id": "research",
      "name": "Research",
      "description": "Research any topic deeply"
    }
  ]
}
```

#### 2.2 A2A API Endpoints

New endpoints for A2A protocol:

```
POST /a2a/agents/{id}/message/send     # Send message, get response
POST /a2a/agents/{id}/message/stream   # Send message, get SSE stream
GET  /a2a/agents/{id}/tasks/{task_id}  # Get task status
```

#### 2.3 Task Adapter

Map A2A Task to Thenvoi AgentExecution:

| A2A Task State | Thenvoi Execution Status |
|----------------|--------------------------|
| SUBMITTED | new |
| WORKING | processing |
| INPUT_REQUIRED | waiting |
| COMPLETED | completed |
| FAILED | failed |
| CANCELLED | cancelled (new) |

Note: A2A Task is per-request, but we create an AgentExecution for tracking.

#### 2.4 SSE Streaming

For long-running tasks, stream updates via Server-Sent Events:

```
Client: POST /a2a/agents/{id}/message/stream

Server: event: status
        data: {"state": "working"}

Server: event: artifact
        data: {"parts": [{"text": "Partial result..."}]}

Server: event: status
        data: {"state": "completed"}
```

### Tasks

| Task | Description |
|------|-------------|
| Create Agent Card Generator | Build card from Agent schema |
| Add `/.well-known/agent.json` endpoint | Discovery endpoint |
| Add `a2a_enabled` flag to Agent | Let users opt-in per agent |
| Create A2A Router/Controller | Handle incoming A2A requests |
| Create Task Adapter | Map Execution ↔ Task |
| Implement `/message/send` endpoint | Synchronous message handling |
| Implement `/message/stream` endpoint | SSE streaming |
| Implement `/tasks/{id}` endpoint | Task status lookup |
| Add authentication | API key validation |
| Write tests | Unit and integration tests |
| Documentation | How to use Thenvoi agents via A2A |

### Success Criteria

- [ ] External A2A client can fetch Agent Card
- [ ] External client can send message and get response
- [ ] Streaming works for long tasks
- [ ] Works with official A2A Python SDK

---

## Phase 3: Polish & Advanced Features

**Duration**: TBD

**Goal**: Production-ready A2A integration

### Key Deliverables

#### 3.1 Error Handling & Reliability

- Proper error mapping to A2A error format
- Retry logic for external agent calls
- Timeout configuration
- Circuit breaker for failing agents

#### 3.2 Caching & Performance

- Agent Card caching with TTL
- Connection pooling for outbound calls
- Response time optimization

#### 3.3 Push Notifications (Optional)

For long-running tasks, callback to client when done:

```json
// Client provides callback URL
{
  "pushNotificationConfig": {
    "url": "https://client.com/webhook",
    "authentication": {...}
  }
}

// Thenvoi calls back when task completes
POST https://client.com/webhook
{
  "taskId": "123",
  "state": "completed",
  "result": {...}
}
```

#### 3.4 Documentation & Examples

- API documentation
- Integration guide
- Example implementations

### Tasks

| Task | Description |
|------|-------------|
| Add error handling | Map errors to A2A format |
| Add retry logic | For external agent calls |
| Add rate limiting | Prevent abuse |
| Implement caching | Agent Cards, connections |
| Add push notifications | Webhook callbacks (optional) |
| Performance testing | Ensure <500ms latency |
| Security review | Authentication, data exposure |
| Write documentation | API docs, integration guide |
| Create examples | Sample A2A integrations |

### Success Criteria

- [ ] Error messages follow A2A spec
- [ ] Latency < 500ms p95
- [ ] Documentation complete
- [ ] Example integrations working

---

## Summary

| Phase | What | Why | Duration |
|-------|------|-----|----------|
| 1. Outbound | Thenvoi agents call external A2A agents | Simplest, immediate value | TBD |
| 2. Inbound | External clients call Thenvoi agents | Ecosystem participation | TBD |
| 3. Polish | Error handling, caching, docs | Production readiness | TBD |

---

## Key Technical Decisions

### Routing Logic

All agent-to-agent communication goes through Thenvoi (hub model):

```
Agent A → Thenvoi Platform → Agent B
              ↓
        Check a2a_remote_url
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
  A2A HTTP          WebSocket
(if url set)       (if nil)
```

### When to Use A2A vs WebSocket

| Scenario | Protocol | Why |
|----------|----------|-----|
| External A2A agent | A2A (HTTP) | Agent has own URL, stateless |
| External SDK agent | WebSocket | Agent connects to us, maintains connection |
| Internal agent | Local call | No network needed |

### Schema Changes

```sql
-- Phase 1
ALTER TABLE agents ADD COLUMN a2a_remote_url TEXT;

-- Phase 2
ALTER TABLE agents ADD COLUMN a2a_enabled BOOLEAN DEFAULT false;
ALTER TABLE agents ADD COLUMN a2a_skills JSONB DEFAULT '[]';
ALTER TABLE agent_executions ADD COLUMN a2a_task_id TEXT;
```

---

## Risks

| Risk | Mitigation |
|------|------------|
| A2A protocol changes | Abstract A2A layer, easy to update |
| Performance overhead | Caching, connection pooling |
| Security exposure | API key auth, allow-lists |
| External agent failures | Timeouts, circuit breaker |
