# A2A:
### Core Concepts

| Concept        | Description                                                        |
| -------------- | ------------------------------------------------------------------ |
| **Agent Card** | JSON manifest at `/.well-known/agent.json` describing capabilities |
| **Task**       | Unit of work with lifecycle (submitted → working → completed)      |
| **Message**    | Communication turn with role (user/agent) and parts                |
| **Part**       | Content unit (text, file, structured data)                         |

### Communication Patterns

1. **Synchronous**: Request → Wait → Response
2. **Streaming**: Request → SSE events → Complete
3. **Push Notifications**: Request → Return → Webhook callbacks

# Thenvoi:
Current Thenvoi Architecture (Relevant Parts)

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

Integration Architecture

# High-Level Design

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

# Thoughts

- A2A Task has an "input-required" status, but Thenvoi's AgentExecution doesn't have an equivalent status

## Concept Clarification

### A2A Task

- What it is: A single unit of work in A2A
- Lifecycle: submitted → working → input_required → completed/failed
- Represents: One request-response cycle with an agent
- Contains: status, artifacts (results), message history

### Thenvoi AgentExecution

- What it is: The execution state for an agent processing messages in a chat room
- Lifecycle: new → processing → waiting → completed/failed
- Represents: Agent's work session, can span multiple messages
- Contains: status, messages array, tool_calls, errors

### Thenvoi Task

- What it is: A user-facing task/work item (like a todo or ticket)
- Different concept: More like a project management task
- Associated with: Chat rooms (optional), users, agents
- Contains: title, summary, status, business context

## Model Comparison

```
A2A Model:
┌─────────────────────────────────────┐
│ Task (work unit)                    │
│  ├─ status: working                 │
│  ├─ contextId: "conversation-123"   │
│  ├─ history: [messages...]          │
│  └─ artifacts: [results...]         │
└─────────────────────────────────────┘

Thenvoi Model:
┌─────────────────────────────────────┐
│ Task (business item) ─ optional     │
│  └─ title, summary, zendesk_id...   │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ ChatRoom (conversation container)   │
│  ├─ participants                    │
│  └─ messages                        │
└─────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────┐
│ AgentExecution (agent work state)   │  ← Maps to A2A Task
│  ├─ status: processing              │
│  ├─ messages: [history...]          │
│  ├─ tool_calls: {...}               │
│  └─ agent_specific_output: {...}    │
└─────────────────────────────────────┘
```

## History Scope Comparison

| Aspect              | Thenvoi Execution         | A2A Task                |
|---------------------|---------------------------|-------------------------|
| Scope               | LLM-relevant messages     | Task-specific messages  |
| Includes tool calls | Yes                       | Yes (as parts)          |
| Configurable        | Via context window limits | Via historyLength param |
| Full room history?  | No (prepared subset)      | No (task-scoped)        |

## Execution Lifecycle Deep Dive

### One Execution Per Agent Per Chat Room

All message exchanges use the SAME execution. The execution is a long-lived state container for an agent's participation in a chat room.

```
ChatRoom: "Project Discussion"
  └── Agent: "Research Agent"
        └── AgentExecution: ONE execution (persists across all messages)
```

### Status Flow for Multiple Messages

```
Message 1: User sends "Hello"
  Execution: new → processing → waiting ✓

Message 2: User sends "Research AI trends"
  Execution: waiting → processing → waiting ✓

Message 3: User sends "More details"
  Execution: waiting → processing → waiting ✓

... (more messages) ...

Message 10: User sends "Thanks, that's all"
  Execution: waiting → processing → waiting ✓
                                      │
                                      └── Still waiting for more!
```

### Key Insight: Executions Rarely Reach "completed"

| Status     | Meaning                                          |
|------------|--------------------------------------------------|
| new        | Just created, not yet processed                  |
| processing | Currently running LLM reasoning cycle            |
| waiting    | Finished current cycle, waiting for next message |
| completed  | Conversation explicitly ended (rare)             |
| failed     | Unrecoverable error                              |
| handoff    | Delegated to another agent                       |

### When Does "completed" Actually Happen?

1. **Explicit task completion** - Agent determines the task is done
2. **Handoff completion** - Child execution finishes
3. **Room archival** - Chat room is closed/archived
4. **Manual completion** - System/admin marks it done

NOT after every message exchange.

## A2A Roadmap - Planned Features

The A2A roadmap mentions planned enhancements:

| Feature             | Status    | Description                             |
|---------------------|-----------|-----------------------------------------|
| Agent Registry      | Planned   | Centralized directory of agents         |
| Dynamic Discovery   | Planned   | Query for agents by capability          |
| DNS-based Discovery | Discussed | Like service discovery in microservices |

From the A2A spec roadmap:
> "Agent Discovery: Formalize inclusion of authorization schemes and optional credentials directly within the AgentCard"

# Key Recommendations

## 1. Unify Lifecycle Status

Align status values between A2A and Thenvoi:

| A2A Status     | Current Thenvoi Status | Recommended Thenvoi Status |
| -------------- | ---------------------- | -------------------------- |
| submitted      | new                    | submitted                  |
| working        | processing             | working                    |
| input-required | (none)                 | input-required             |
| completed      | completed              | completed                  |
| failed         | failed                 | failed                     |
| canceled       | (none)                 | canceled                   |

# Things to Consider

## Configurable History Length

Consider making the history length adjustable so that not all chat history is exposed to all agents. This would allow:

- Fine-grained control over what context each agent receives
- Privacy/security boundaries between agents in the same conversation
- Performance optimization by limiting context size per agent

## Status Naming Alignment

Consider renaming Thenvoi execution statuses to better align with A2A and clarify meaning:

| Current Status | Proposed Status | Rationale                                              |
| -------------- | --------------- | ------------------------------------------------------ |
| waiting        | ready           | Better reflects that execution is ready for next input |
| processing     | working         | Aligns with A2A terminology                            |
| (none)         | input-required  | New status for when agent explicitly needs user input  |

This would give us a clearer status flow:
- `new` → `working` → `ready` (waiting for next message)
- `ready` → `working` → `input-required` (explicitly needs input)
- `ready` → `completed` (conversation ended)

## A2A Endpoint Hierarchy

Where should `/a2a/agents/{id}/.well-known/agent.json` live?

| Option                | Structure                             | Considerations                                                                       |
| --------------------- | ------------------------------------- | ------------------------------------------------------------------------------------ |
| A: Separate namespace | `/a2a/agents/{id}/...`                | Clean separation, each agent gets own base URL, easy A2A-specific middleware         |
| B: Under existing API | `/api/v1/agents/{id}/.well-known/...` | Reuses existing routing, but mixes REST with A2A protocol                            |
| C: Root well-known    | `/.well-known/a2a/agents/{id}.json`   | Centralized discovery, but doesn't follow A2A convention of card at agent's base URL |

**Option A structure:**
```
Existing REST:     /api/v1/agents/{id}
A2A Protocol:      /a2a/agents/{id}/
  ├── .well-known/agent.json    # Agent Card
  ├── message/send              # POST
  ├── message/stream            # POST
  └── tasks/{task_id}           # GET
```
