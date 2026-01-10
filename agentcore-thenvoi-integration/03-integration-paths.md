# Integration Paths: Thenvoi + AgentCore

## Overview

Three primary integration paths enable Thenvoi to work with AgentCore:

| Path | Description | Effort | Value |
|------|-------------|--------|-------|
| **A2A Server** | Deploy Thenvoi as A2A server on AgentCore Runtime | Medium | High |
| **MCP Server** | Expose Thenvoi via AgentCore Gateway | Low | High |
| **SDK Adapter** | AgentCore/Strands adapter for thenvoi-sdk-python | Medium | Medium |

---

## Path 1: A2A Server on AgentCore Runtime

### Architecture

```
┌────────────────────────────────────────────────────────────┐
│                AWS Bedrock AgentCore                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               AgentCore Runtime                       │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │           Thenvoi A2A Server                     │ │  │
│  │  │                                                  │ │  │
│  │  │  Endpoints:                                      │ │  │
│  │  │  - /ping (health check)                          │ │  │
│  │  │  - /.well-known/agent-card.json (discovery)      │ │  │
│  │  │  - / (JSON-RPC message handling)                 │ │  │
│  │  │                                                  │ │  │
│  │  │  Port: 9000                                      │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
                              ↑
                              │ A2A Protocol
                              │
┌────────────────────────────────────────────────────────────┐
│              Other Agents on AgentCore                      │
│  (Strands, LangGraph, CrewAI, Custom)                      │
└────────────────────────────────────────────────────────────┘
```

### Technical Requirements

**Container Requirements:**
- ARM64 architecture
- Docker container
- Listen on `0.0.0.0:9000`
- Stateless design

**Endpoints:**

1. **`GET /ping`** - Health check
   ```json
   {"status": "Healthy"}
   ```

2. **`GET /.well-known/agent-card.json`** - Agent discovery
   ```json
   {
     "name": "Thenvoi Orchestration Agent",
     "description": "Multi-agent orchestration with human-in-the-loop",
     "url": "https://runtime.agentcore.aws/...",
     "version": "1.0.0",
     "protocolVersion": "0.3",
     "capabilities": {
       "streaming": true,
       "pushNotifications": true
     },
     "skills": [
       {
         "id": "orchestrate",
         "name": "Orchestrate Agents",
         "description": "Coordinate multiple agents on a task"
       },
       {
         "id": "human_loop",
         "name": "Human in the Loop",
         "description": "Request human approval or input"
       }
     ],
     "securitySchemes": {
       "apiKey": {
         "type": "apiKey",
         "in": "header",
         "name": "X-Thenvoi-API-Key"
       }
     }
   }
   ```

3. **`POST /`** - JSON-RPC message handling
   ```json
   // Request
   {
     "jsonrpc": "2.0",
     "id": "req-001",
     "method": "message/send",
     "params": {
       "message": {
         "role": "user",
         "parts": [{"kind": "text", "text": "Orchestrate analysis task"}],
         "messageId": "msg-123"
       }
     }
   }

   // Response
   {
     "jsonrpc": "2.0",
     "id": "req-001",
     "result": {
       "artifacts": [
         {
           "parts": [{"kind": "text", "text": "Task orchestrated..."}]
         }
       ]
     }
   }
   ```

### Implementation Steps

1. **Create A2A Server Package**
   ```
   thenvoi-agentcore/
   ├── Dockerfile
   ├── src/
   │   ├── server.py          # FastAPI/AIOHTTP server
   │   ├── a2a_handler.py     # JSON-RPC handling
   │   ├── agent_card.py      # Card generation
   │   └── thenvoi_client.py  # Connect to Thenvoi platform
   ├── requirements.txt
   └── agentcore.yaml         # AgentCore config
   ```

2. **Connect to Thenvoi Platform**
   - Receive A2A message
   - Create/join Thenvoi session
   - Forward to appropriate agent
   - Stream response back via A2A

### Data Flow: Agent-to-Agent via Thenvoi

```
AgentCore Runtime
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  ┌──────────────┐                   ┌──────────────┐      │
│  │   Agent 1    │                   │   Agent 2    │      │
│  │  (LangGraph) │                   │   (CrewAI)   │      │
│  └──────┬───────┘                   └───────▲──────┘      │
│         │                                   │              │
│         │ 1. A2A request                    │ 4. A2A call  │
│         ▼                                   │              │
│  ┌──────────────────────────────────────────┴───────────┐ │
│  │              thenvoi-agentcore-a2a                    │ │
│  │              (Adapter Container)                      │ │
│  │                                                       │ │
│  │  • Receives A2A messages from agents                  │ │
│  │  • Translates to Thenvoi Platform API                 │ │
│  │  • Routes responses back to requesting agents         │ │
│  └───────────────────────┬───────────────────────────────┘ │
│                          │                                  │
└──────────────────────────┼──────────────────────────────────┘
                           │ 2. REST + WebSocket
                           ▼
              ┌─────────────────────────┐
              │    Thenvoi Platform     │
              │                         │
              │  • Session management   │
              │  • Orchestration logic  │
              │  • Human-in-the-loop    │
              │  • History & context    │
              │  • LiveView UI          │
              └────────────┬────────────┘
                           │
                           │ 3. Orchestration decision:
                           │    "Route to Agent 2"
                           ▼
              (Response flows back up)
```

**Flow Example:**
1. Agent 1 sends: "Coordinate with Agent 2 to analyze this data"
2. thenvoi-agentcore-a2a forwards to Thenvoi Platform
3. Platform creates session, determines Agent 2 should handle part of task
4. thenvoi-agentcore-a2a calls Agent 2 via A2A
5. Responses aggregate through Platform back to Agent 1

3. **Deploy to AgentCore**
   ```bash
   # Configure and deploy
   agentcore configure -e server.py --protocol A2A
   agentcore deploy
   ```

### Benefits

- Any AgentCore agent can discover and use Thenvoi
- Full A2A protocol compliance
- Serverless scaling via AgentCore
- Enterprise security (SigV4, OAuth)

---

## Path 2: MCP Server via AgentCore Gateway

### Architecture

```
┌────────────────────────────────────────────────────────────┐
│                AWS Bedrock AgentCore                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               AgentCore Gateway                       │  │
│  │                                                       │  │
│  │  Tool Catalog:                                        │  │
│  │  - thenvoi_create_session                            │  │
│  │  - thenvoi_add_agent                                 │  │
│  │  - thenvoi_send_message                              │  │
│  │  - thenvoi_wait_for_human                            │  │
│  │  - thenvoi_list_agents                               │  │
│  │                                                       │  │
│  └─────────────────────────┬────────────────────────────┘  │
│                            │ MCP Protocol                   │
│  ┌─────────────────────────▼────────────────────────────┐  │
│  │           Thenvoi MCP Server                          │  │
│  │           (Port 8000, /mcp endpoint)                  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

### Technical Requirements

**Container Requirements:**
- Listen on `0.0.0.0:8000`
- POST `/mcp` endpoint for JSON-RPC
- Implement `tools/list` and `tools/call`

**Tools to Expose:**

1. **`thenvoi_create_session`**
   ```json
   {
     "name": "thenvoi_create_session",
     "description": "Create a new multi-agent session",
     "inputSchema": {
       "type": "object",
       "properties": {
         "name": {"type": "string"},
         "agents": {"type": "array", "items": {"type": "string"}}
       },
       "required": ["name"]
     }
   }
   ```

2. **`thenvoi_send_message`**
   ```json
   {
     "name": "thenvoi_send_message",
     "description": "Send a message to a Thenvoi session",
     "inputSchema": {
       "type": "object",
       "properties": {
         "session_id": {"type": "string"},
         "message": {"type": "string"},
         "target_agent": {"type": "string"}
       },
       "required": ["session_id", "message"]
     }
   }
   ```

3. **`thenvoi_wait_for_human`**
   ```json
   {
     "name": "thenvoi_wait_for_human",
     "description": "Request human input or approval",
     "inputSchema": {
       "type": "object",
       "properties": {
         "session_id": {"type": "string"},
         "prompt": {"type": "string"},
         "options": {"type": "array", "items": {"type": "string"}}
       },
       "required": ["session_id", "prompt"]
     }
   }
   ```

### Implementation Steps

1. **Extend Existing thenvoi-mcp**
   - Already has MCP server implementation
   - Add Gateway-compatible transport
   - Expose orchestration tools

2. **Gateway Configuration**
   ```yaml
   targets:
     - name: thenvoi
       type: mcp-server
       url: https://your-thenvoi-mcp-server/mcp
       tools:
         - thenvoi_create_session
         - thenvoi_send_message
         - thenvoi_wait_for_human
   ```

3. **Register with Gateway**
   - Push container to ECR
   - Create Gateway target
   - Tools auto-discovered

### Benefits

- Any agent using Gateway gets Thenvoi tools
- Lower integration effort (existing MCP server)
- Semantic tool discovery
- Centralized credential management

---

## Path 3: Python SDK AgentCore Adapter

### Architecture

```python
# New adapter in thenvoi-sdk-python
from thenvoi.adapters.agentcore import AgentCoreAdapter, StrandsIntegration

# Option 1: Thenvoi as tool for Strands agent
adapter = AgentCoreAdapter(thenvoi_api_key="...")
strands_agent = Agent(
    name="My Agent",
    tools=[adapter.orchestration_tool()]
)

# Option 2: Run Thenvoi agent on AgentCore
from thenvoi.integrations.agentcore import ThenvoidOnAgentCore

runner = ThenvoidOnAgentCore(
    agent_config=...,
    agentcore_config=...
)
runner.deploy()
```

### Implementation

**New Files:**
```
src/thenvoi/
├── adapters/
│   └── agentcore.py        # AgentCore adapter
└── integrations/
    └── agentcore/
        ├── __init__.py
        ├── runtime.py      # Runtime integration
        ├── memory.py       # Memory service bridge
        └── tools.py        # Tool conversion
```

**AgentCore Adapter:**
```python
class AgentCoreAdapter(BaseAdapter):
    """Adapter for using Thenvoi with AgentCore/Strands."""

    def __init__(
        self,
        thenvoi_api_key: str,
        thenvoi_base_url: str = "https://api.thenvoi.com",
        **kwargs
    ):
        self.client = ThenvoiClient(api_key=thenvoi_api_key, base_url=thenvoi_base_url)

    def orchestration_tool(self) -> Tool:
        """Return Thenvoi orchestration as a Strands-compatible tool."""
        return Tool(
            name="thenvoi_orchestrate",
            description="Orchestrate multiple agents on a complex task",
            function=self._orchestrate
        )

    async def _orchestrate(self, task: str, agents: list[str]) -> str:
        """Execute orchestration via Thenvoi."""
        session = await self.client.create_session(agents=agents)
        result = await self.client.execute(session.id, task)
        return result.output
```

**Strands Integration:**
```python
from strands import Agent
from strands_tools import calculator
from thenvoi.adapters.agentcore import AgentCoreAdapter

# Create Thenvoi adapter
thenvoi = AgentCoreAdapter(thenvoi_api_key=os.environ["THENVOI_API_KEY"])

# Create Strands agent with Thenvoi orchestration
agent = Agent(
    name="Coordinator",
    description="Coordinates complex multi-agent tasks",
    tools=[
        calculator,
        thenvoi.orchestration_tool(),
        thenvoi.human_in_the_loop_tool()
    ]
)

# Deploy to AgentCore
# ... deployment code ...
```

### Benefits

- Native Python integration
- Works with existing Thenvoi SDK patterns
- Consistent with other adapters (LangGraph, Anthropic, etc.)
- Can run on or outside AgentCore

---

## Comparison of Paths

| Aspect | A2A Server | MCP via Gateway | SDK Adapter |
|--------|------------|-----------------|-------------|
| **Integration Type** | Container on Runtime | Container + Gateway | Python library |
| **Effort** | Medium | Low | Medium |
| **Discoverability** | Agent Cards | Tool catalog | Code-level |
| **Streaming** | Native A2A | MCP streaming | SDK streaming |
| **Best For** | Agent-to-agent | Tool-based workflows | Python developers |
| **Marketplace** | Yes | Yes | No (PyPI) |

---

## Recommended Implementation Order

### Phase 1: MCP Server via Gateway

**Why First:**
- Lowest effort (extend existing thenvoi-mcp)
- Immediate value (tools available to all agents)
- Gateway handles infrastructure

**Deliverables:**
- [ ] Update thenvoi-mcp for Gateway compatibility
- [ ] Define tool schemas
- [ ] Test with Gateway
- [ ] Document setup

### Phase 2: A2A Server on Runtime

**Why Second:**
- Enables agent-to-agent discovery
- Marketplace listing opportunity
- Leverages A2A work already planned

**Deliverables:**
- [ ] Create A2A server container
- [ ] Implement Agent Card generation
- [ ] Deploy to AgentCore Runtime
- [ ] List on Marketplace

### Phase 3: SDK Adapter

**Why Third:**
- Enables deep Python integration
- Complements other paths
- For power users

**Deliverables:**
- [ ] Create AgentCoreAdapter class
- [ ] Add Strands integration
- [ ] Write examples
- [ ] Publish to PyPI

---

## Technical Dependencies

### For All Paths

- Thenvoi platform REST API
- WebSocket streaming capability
- Authentication (API keys, OAuth)

### For A2A Server

- A2A protocol implementation (from existing A2A work)
- Docker container tooling
- AWS account with AgentCore access

### For MCP Server

- Existing thenvoi-mcp codebase
- MCP JSON-RPC handling
- Gateway configuration

### For SDK Adapter

- thenvoi-sdk-python codebase
- Strands Agents SDK (optional)
- AgentCore Python SDK

---

## Testing Strategy

### A2A Server Testing

1. **Local Testing:**
   ```bash
   docker run -p 9000:9000 thenvoi-a2a-server
   curl http://localhost:9000/ping
   curl http://localhost:9000/.well-known/agent-card.json
   ```

2. **AgentCore Testing:**
   ```bash
   agentcore configure -e server.py --protocol A2A
   agentcore test --local
   ```

3. **Integration Testing:**
   - Deploy test agent
   - Connect from another AgentCore agent
   - Verify message flow

### MCP Server Testing

1. **Local Testing:**
   ```bash
   curl -X POST http://localhost:8000/mcp \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
   ```

2. **Gateway Testing:**
   - Create Gateway target
   - Verify tool discovery
   - Test tool calls

### SDK Testing

- Unit tests for adapter
- Integration tests with Thenvoi platform
- Example script testing
