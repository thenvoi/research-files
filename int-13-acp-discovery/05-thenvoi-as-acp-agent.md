# Thenvoi as ACP Agent: Implementation Analysis

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

Thenvoi has a strong architectural fit for becoming an ACP-compliant agent. The platform's existing multi-agent orchestration, MCP server, and Python SDK provide a foundation to expose Thenvoi's capabilities to any ACP-compatible editor (Zed, Neovim, JetBrains, etc.). This document analyzes how Thenvoi could implement ACP, what value it would provide, and the recommended approach.

## Key Findings

### 1. Architectural Alignment

Thenvoi's existing architecture maps well to ACP concepts:

| Thenvoi Concept | ACP Concept | Mapping Notes |
|-----------------|-------------|---------------|
| **Agent** | ACP Agent | Thenvoi agents become selectable ACP agents |
| **AgentExecution** | ACP Session | Execution tracks session state |
| **ChatMessage** | Prompt/Response | Message format compatible |
| **Tool** | MCP Tool | Already implemented in thenvoi-mcp-server |
| **is_external** | N/A | Could route to ACP vs internal |

**Data Flow:**

```
┌─────────────────────────────────────────────────────────────┐
│                    ACP Client (Editor)                       │
└─────────────────────────┬───────────────────────────────────┘
                          │ ACP Protocol (JSON-RPC/stdio)
┌─────────────────────────▼───────────────────────────────────┐
│                 Thenvoi ACP Server Layer                     │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  session/new    → Create AgentExecution                 ││
│  │  session/prompt → Route to Agent, return response       ││
│  │  session/cancel → Cancel AgentExecution                 ││
│  │  fs/read_text   → Proxy to MCP or native               ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────┬───────────────────────────────────┘
                          │ Internal API
┌─────────────────────────▼───────────────────────────────────┐
│                   Thenvoi Platform                           │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────────────┐ │
│  │  Agents  │  │  Executions  │  │  Tools (MCP Server)    │ │
│  └──────────┘  └──────────────┘  └────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

**Confidence:** High (based on architecture analysis)

### 2. Value Proposition

**For ACP Users:**

| Benefit | Description |
|---------|-------------|
| **Multi-Agent Access** | Choose from multiple Thenvoi agents within one editor |
| **Orchestration** | Thenvoi handles agent coordination invisibly |
| **Tool Ecosystem** | Access Thenvoi's tool integrations |
| **Persistence** | Conversations persist in Thenvoi platform |
| **Enterprise Features** | Multi-tenant, auth, audit (existing platform features) |

**For Thenvoi:**

| Benefit | Description |
|---------|-------------|
| **Distribution** | Reach any ACP-compatible editor user |
| **Ecosystem Play** | Participate in growing ACP ecosystem |
| **Differentiation** | First multi-agent orchestration platform with ACP |
| **Protocol Coverage** | Add ACP to existing A2A and MCP support |

**Confidence:** High (strategic analysis)

### 3. Implementation Approaches

#### Approach A: Unified Super-Agent

Present Thenvoi as a single ACP agent that orchestrates internally:

```
Editor → Thenvoi ACP → [Agent Selection] → Internal Orchestration
```

**Pros:**
- Simplest ACP integration
- One config for users
- Thenvoi controls routing

**Cons:**
- Agent selection UX limited
- Hidden complexity
- Less flexibility

#### Approach B: Multi-Agent Exposure

Expose each Thenvoi agent as a separate ACP agent:

```
Editor → Thenvoi ACP → /agents/research
                    → /agents/code
                    → /agents/doc
```

**Pros:**
- Users choose specific agents
- Better maps to ACP model
- More transparent

**Cons:**
- More configuration
- May hit ACP limitations
- Agent discovery needed

#### Approach C: Proxy/Orchestrator Pattern

Follow Symposium model - Thenvoi as ACP proxy:

```
Editor → Thenvoi ACP Proxy → [Routing Logic] → Multiple ACP Agents
                          → Other ACP Agents (external)
                          → MCP Tools
```

**Pros:**
- Maximum flexibility
- Can include external agents
- Symposium precedent in ecosystem

**Cons:**
- Most complex
- Proxy latency
- New architectural pattern

**Recommendation:** Start with **Approach A** (Super-Agent), evolve to **Approach C** (Proxy).

### 4. Technical Implementation Plan

**Phase 1: ACP Server Implementation (Python)**

```python
# thenvoi_acp/server.py
from acp.agents import BaseAgent
from acp.schema import (
    InitializeRequest, InitializeResponse,
    SessionNewRequest, SessionNewResponse,
    PromptRequest, PromptResponse
)
from thenvoi_client_rest import EnvoiClient

class ThenvoiACPAgent(BaseAgent):
    """Thenvoi platform exposed as ACP agent."""

    def __init__(self):
        self.client = EnvoiClient(
            api_key=os.environ.get('THENVOI_API_KEY'),
            base_url=os.environ.get('THENVOI_BASE_URL')
        )
        self.sessions = {}  # ACP session → Thenvoi execution

    async def handle_initialize(self, request: InitializeRequest) -> InitializeResponse:
        return InitializeResponse(
            capabilities={
                'streaming': True,
                'mcp': True,
                'sessionLoad': True
            },
            agent_info={
                'name': 'Thenvoi',
                'version': '1.0.0',
                'description': 'Multi-agent orchestration platform'
            }
        )

    async def handle_session_new(self, request: SessionNewRequest) -> SessionNewResponse:
        # Create new Thenvoi execution
        execution = await self.client.executions.create(
            agent_id=self.default_agent_id
        )
        self.sessions[execution.id] = execution
        return SessionNewResponse(sessionId=execution.id)

    async def handle_prompt(self, request: PromptRequest) -> PromptResponse:
        execution_id = request.params.sessionId
        message = request.params.prompt

        # Send to Thenvoi platform
        response = await self.client.messages.create(
            execution_id=execution_id,
            content=message
        )

        # Stream response back
        return PromptResponse(
            sessionId=execution_id,
            content=[TextContent(text=response.content)]
        )
```

**Phase 2: Zed Configuration**

```json
{
  "agent_servers": {
    "Thenvoi": {
      "type": "custom",
      "command": "python",
      "args": ["-m", "thenvoi_acp"],
      "env": {
        "THENVOI_API_KEY": "${env:THENVOI_API_KEY}",
        "THENVOI_BASE_URL": "https://app.thenvoi.com"
      }
    }
  }
}
```

**Phase 3: MCP Integration**

```python
async def handle_initialize(self, request: InitializeRequest) -> InitializeResponse:
    # Accept MCP servers from editor
    mcp_servers = request.params.capabilities.get('mcp', {}).get('servers', [])

    # Connect to editor-provided MCP servers
    for server in mcp_servers:
        await self.connect_mcp_server(server)

    # Also expose Thenvoi's own MCP tools
    return InitializeResponse(
        capabilities={
            'mcp': {
                'servers': [
                    {'name': 'thenvoi-tools', 'builtin': True}
                ]
            }
        }
    )
```

**Confidence:** High (based on SDK analysis)

### 5. Mapping ACP Methods to Thenvoi

| ACP Method                   | Thenvoi Implementation                          |
| ---------------------------- | ----------------------------------------------- |
| `initialize`                 | Return capabilities, connect client             |
| `authenticate`               | Validate THENVOI_API_KEY                        |
| `session/new`                | Create AgentExecution                           |
| `session/load`               | Load existing AgentExecution                    |
| `session/prompt`             | Send message, get response                      |
| `session/cancel`             | Cancel AgentExecution                           |
| `session/update`             | Stream via Phoenix Channels → ACP notifications |
| `fs/read_text_file`          | Proxy to MCP or deny                            |
| `fs/write_text_file`         | Proxy to MCP with permission                    |
| `terminal/*`                 | Not supported initially                         |
| `session/request_permission` | Map to Thenvoi permission system                |

### 6. Streaming Integration

Thenvoi uses Phoenix Channels for real-time updates. Map to ACP streaming:

```python
async def handle_prompt_streaming(self, request: PromptRequest):
    execution_id = request.params.sessionId

    # Connect to Thenvoi WebSocket
    async with self.client.connect_channel(f'execution:{execution_id}') as channel:
        # Send message
        await channel.send('message', {'content': request.params.prompt})

        # Stream responses as ACP updates
        async for event in channel.events():
            if event.type == 'message':
                yield SessionUpdate(
                    type='content',
                    content=TextContent(text=event.data.content)
                )
            elif event.type == 'tool_call':
                yield SessionUpdate(
                    type='tool_call',
                    toolCall=event.data
                )
            elif event.type == 'complete':
                break
```

**Confidence:** Medium (requires Phoenix Channels integration work)

### 7. Agent Selection UX

Challenge: ACP doesn't have great multi-agent selection UX.

**Options:**

1. **Slash Commands** - Use ACP slash commands to select agent
   ```
   /agent research
   /agent code
   /agent docs
   ```

2. **Session Modes** - Use ACP session modes
   ```python
   async def handle_set_mode(self, request):
       mode = request.params.mode
       self.current_agent = self.agents_by_mode[mode]
   ```

3. **Smart Routing** - Thenvoi auto-selects based on prompt
   ```python
   async def route_prompt(self, prompt: str):
       # Use classifier to select best agent
       agent = await self.classify_and_route(prompt)
       return agent.handle(prompt)
   ```

**Recommendation:** Implement all three - slash commands for explicit selection, modes for persistent selection, smart routing as default.

## Community Signals

### Market Opportunity

- **138+ reactions** on Codex ACP support shows demand
- No multi-agent ACP solution in market yet
- JetBrains partnership signals enterprise adoption coming
- Docker cagent validates multi-agent runtime approach

### Competitive Positioning

| Solution | Multi-Agent | ACP | Enterprise |
|----------|-------------|-----|------------|
| Claude Code | No | Adapter | Limited |
| Gemini CLI | No | Native | Google only |
| Goose | No | Native | Open source |
| Docker cagent | Yes | Native | Docker focus |
| **Thenvoi** | **Yes** | **Potential** | **Yes** |

Thenvoi would be **first multi-agent orchestration platform with native ACP support**.

## Gaps Identified

### Implementation Gaps

1. **No ACP server in platform** - Needs to be built
2. **Session persistence mapping** - AgentExecution vs ACP session lifecycle
3. **Streaming protocol bridge** - Phoenix Channels → ACP notifications
4. **Permission model mapping** - Thenvoi permissions to ACP permissions

### UX Gaps

1. **Agent selection** - ACP not designed for multi-agent selection
2. **Context sharing** - How to share context between agents
3. **History** - ACP external agents lack history features

### Platform Gaps

1. **Local execution** - ACP expects local process, Thenvoi is cloud
2. **Authentication** - Need to handle API key in ACP config
3. **MCP passthrough** - Editor MCP servers to Thenvoi agents

## Implications for Thenvoi

### Recommended Roadmap

**Phase 1: Prototype**
- Implement basic ACP server using Python SDK
- Support `initialize`, `session/new`, `session/prompt`
- Test with Zed editor
- Document configuration

**Phase 2: Streaming & Tools**
- Add streaming support via `session/update`
- Integrate MCP tool passthrough
- Add file system operations
- Implement permission requests

**Phase 3: Multi-Agent UX**
- Add agent selection via slash commands
- Implement session modes
- Add smart routing
- Polish documentation

**Phase 4: Distribution**
- Package as Zed extension
- Create Neovim plugin documentation
- Submit to registries
- Marketing/launch

### Success Metrics

| Metric | Target |
|--------|--------|
| Editor integrations | Zed + 2 others |
| Active users via ACP | 100+ monthly |
| Latency p95 | < 500ms for first token |
| Agent selection accuracy | > 80% (smart routing) |

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| ACP protocol changes | Use SDK, track RFDs |
| Performance (cloud latency) | Optimize API calls, caching |
| Feature parity | Prioritize core features |
| Adoption | Focus on Zed first (largest) |

## Sources Consulted

- [x] Existing A2A research - Integration patterns
- [x] thenvoi-mcp-server.arch.md - MCP implementation
- [x] thenvoi-platform (via architecture-hub) - Platform architecture
- [x] thenvoi-sdk-python (via architecture-hub) - SDK patterns
- [x] ACP Python SDK - Implementation reference
- [x] Zed External Agents docs - Integration requirements

## Related Research Files

- [01-acp-architecture.md](./01-acp-architecture.md) - Protocol foundation
- [02-acp-mcp-integration.md](./02-acp-mcp-integration.md) - Tool integration
- [03-multi-agent-gap.md](./03-multi-agent-gap.md) - Multi-agent opportunity
- [04-custom-agent-integration.md](./04-custom-agent-integration.md) - Implementation patterns
