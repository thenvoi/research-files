# Custom Agent Integration Patterns

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

Integrating a custom agent into the ACP ecosystem requires implementing the ACP server interface. Agents communicate via JSON-RPC over stdio with ACP clients (editors). The Python SDK provides the most accessible path for custom agent development, with Pydantic models, asyncio transports, and helper builders. Zed supports custom agents through `settings.json` configuration, and the adapter pattern is used for wrapping existing CLI tools.

## Key Findings

### 1. Agent Integration Architecture

Custom agents integrate through the ACP server interface:

```
┌─────────────────────────────────────┐
│     Editor (ACP Client)              │
│  - Zed, Neovim, Emacs, etc.          │
└─────────────────┬───────────────────┘
                  │ JSON-RPC over stdio
┌─────────────────▼───────────────────┐
│     Custom Agent (ACP Server)        │
│  - Implements ACP protocol           │
│  - Handles session/prompt/cancel     │
│  - Optionally uses MCP tools         │
└─────────────────────────────────────┘
```

**Communication:**
- **Protocol:** JSON-RPC 2.0
- **Transport:** stdio (stdin/stdout)
- **Format:** JSON messages, Markdown text

**Confidence:** High (official documentation)

### 2. Zed Configuration for Custom Agents

Custom agents are configured in Zed's `settings.json`:

```json
{
  "agent_servers": {
    "My Custom Agent": {
      "type": "custom",
      "command": "node",
      "args": ["~/projects/agent/index.js", "--acp"],
      "env": {
        "API_KEY": "...",
        "MODEL": "claude-3"
      }
    }
  }
}
```

**Configuration Options:**
| Field | Purpose |
|-------|---------|
| `type` | Must be "custom" for custom agents |
| `command` | Executable to run |
| `args` | Command-line arguments |
| `env` | Environment variables |

**Confidence:** High ([Zed Docs](https://zed.dev/docs/ai/external-agents))

### 3. Built-in Agent Patterns

Zed ships three agents that demonstrate integration patterns:

| Agent | Pattern | Key Insight |
|-------|---------|-------------|
| **Claude Code** | Adapter (`@zed-industries/claude-code-acp`) | Wraps CLI with ACP interface |
| **Gemini CLI** | Direct ACP | Native ACP implementation |
| **Codex CLI** | Adapter (`codex-acp`) | Adapter wraps existing tool |

**Adapter Pattern:**
> "Built-in agents use dedicated adapters that wrap the underlying CLI tool."

This pattern is valuable for:
- Integrating existing tools that don't natively support ACP
- Adding ACP capabilities incrementally
- Maintaining compatibility with standalone usage

**Override Pattern:**
```json
{
  "agent_servers": {
    "claude": {
      "env": {
        "CLAUDE_CODE_EXECUTABLE": "/path/to/alternate-executable"
      }
    }
  }
}
```

**Confidence:** High (Zed documentation)

### 4. Python SDK for Agent Development

The [Python SDK](https://github.com/agentclientprotocol/python-sdk) is the most accessible for custom agents:

**Installation:**
```bash
pip install agent-client-protocol
# or
uv add agent-client-protocol
```

**Key Features:**
| Feature | Description |
|---------|-------------|
| **Pydantic Models** | Type-safe ACP schema in `acp.schema` |
| **Async Base Classes** | Asyncio transports and lifecycle helpers |
| **Helper Builders** | `acp.helpers` for content blocks, tool calls |
| **Contrib Utilities** | Session accumulators, permission brokers |

**Minimal Agent Example:**
```python
from acp.agents import BaseAgent
from acp.schema import Session, PromptRequest, PromptResponse

class MyAgent(BaseAgent):
    async def handle_prompt(self, request: PromptRequest) -> PromptResponse:
        # Process user prompt
        user_message = request.params.prompt

        # Generate response
        result = await self.generate_response(user_message)

        # Return ACP-compliant response
        return PromptResponse(
            sessionId=request.params.sessionId,
            content=[TextContent(text=result)]
        )
```

**Confidence:** High (SDK documentation)

### 5. SDK Ecosystem

Official SDKs are available in multiple languages:

| Language | Package | Best For |
|----------|---------|----------|
| **Python** | `agent-client-protocol` | Rapid prototyping, AI frameworks |
| **TypeScript** | `@agentclientprotocol/sdk` | Node.js agents, VS Code extensions |
| **Rust** | `agent-client-protocol` | High-performance, native agents |
| **Kotlin** | `acp-kotlin` | JVM ecosystem, JetBrains plugins |

**Python SDK Advantages for Thenvoi:**
- Aligns with `thenvoi-sdk-python` language
- Async support matches existing patterns
- Pydantic models match API design
- LangChain/LangGraph examples available

**Confidence:** High (GitHub repositories)

### 6. Testing and Debugging

Zed provides debugging capabilities:

**ACP Log Viewer:**
```
Command: dev: open acp logs
```

This reveals:
- JSON-RPC messages exchanged
- Protocol errors
- Session lifecycle events

**Testing Approaches:**
1. **Unit tests** - Test ACP handler functions
2. **Integration tests** - Simulate editor<->agent communication
3. **Live testing** - Configure in Zed, use debug logs

**Confidence:** High (Zed documentation)

### 7. Current Limitations

From Zed documentation:

| Feature | Status |
|---------|--------|
| Message editing | Unavailable for external agents |
| Thread resumption | Unavailable |
| Checkpointing | Unavailable |
| MCP server support | Varies by agent |

> "Message editing, thread resumption from history, and checkpointing remain unavailable across all external agents."

**Implications:**
- External agents have fewer features than built-in
- Session persistence is limited
- Feature parity still developing

**Confidence:** High (official documentation)

## Community Signals

### Active Development

- Python SDK actively maintained with regular releases
- Examples cover streaming, permissions, Gemini bridge
- Community adopters like `kimi-cli` demonstrate production use

### Extension Ecosystem

> "Additional agents deploy as 'Agent Server extensions.' Discover available agents by filtering for 'Agent Servers' in Zed's extension marketplace."

This indicates:
- Growing agent marketplace
- Distribution mechanism exists
- Discoverability improving

## Gaps Identified

### Development Gaps

1. **Limited examples** - Complex multi-agent patterns not shown
2. **Testing tooling** - No standard test harness
3. **CI/CD patterns** - No standard deployment guidance
4. **Version compatibility** - Schema versions evolve rapidly

### Feature Gaps (for external agents)

1. **No message editing** - Cannot modify sent messages
2. **No thread resumption** - Cannot continue previous sessions
3. **No checkpointing** - Cannot save/restore state
4. **Variable MCP support** - Not all features available

### Ecosystem Gaps

1. **No agent marketplace** - Discovery is manual
2. **No certification** - No quality assurance process
3. **No analytics** - No usage tracking for agents

## Implications for Thenvoi

### Path 1: Python SDK Agent

Build Thenvoi ACP agent using Python SDK:

**Advantages:**
- Aligns with existing Python infrastructure
- Pydantic models match API patterns
- LangChain integration examples available
- Fastest path to prototype

**Implementation:**
```python
from acp.agents import BaseAgent
from thenvoi_client_rest import EnvoiClient

class ThenvoiAgent(BaseAgent):
    def __init__(self):
        self.client = EnvoiClient(api_key=os.environ['THENVOI_API_KEY'])

    async def handle_prompt(self, request):
        # Route to Thenvoi platform
        execution = await self.client.agents.execute(
            agent_id=self.selected_agent,
            message=request.params.prompt
        )
        return self.format_response(execution)
```

### Path 2: Adapter Pattern

Wrap existing Thenvoi SDK with ACP adapter:

**Advantages:**
- Preserves existing SDK functionality
- Minimal changes to core platform
- Can evolve independently

**Structure:**
```
thenvoi-acp-adapter/
├── src/
│   ├── adapter.py      # ACP protocol handling
│   ├── bridge.py       # Thenvoi SDK integration
│   └── cli.py          # Entry point for editors
├── examples/
│   └── zed_config.json
└── tests/
```

### Path 3: Zed Extension

Package as Zed extension for marketplace:

**Advantages:**
- Discoverable in Zed marketplace
- Auto-updates for users
- Community visibility

**Requirements:**
- Extension manifest
- ACP server implementation
- Installation/update hooks

### Recommendation

**Start with Path 1 (Python SDK)** for rapid prototyping:
1. Fastest to implement
2. Language alignment with existing SDKs
3. Can evolve to adapter or extension later
4. Test with real editors immediately

## Sources Consulted

- [x] [Zed External Agents](https://zed.dev/docs/ai/external-agents) - Integration guide
- [x] [Python SDK](https://github.com/agentclientprotocol/python-sdk) - Implementation reference
- [x] [Python SDK Docs](https://agentclientprotocol.github.io/python-sdk/) - Detailed documentation
- [x] [TypeScript SDK](https://github.com/agentclientprotocol/typescript-sdk) - Alternative implementation
- [x] [Rust SDK](https://github.com/agentclientprotocol/rust-sdk) - High-performance option

## Related Research Files

- [01-acp-architecture.md](./01-acp-architecture.md) - Protocol foundation
- [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) - Thenvoi-specific implementation
- [02-acp-mcp-integration.md](./02-acp-mcp-integration.md) - Tool integration
