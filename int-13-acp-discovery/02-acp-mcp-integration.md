# ACP-MCP Integration Patterns

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

ACP (Agent Client Protocol) and MCP (Model Context Protocol) are complementary protocols designed to work together. ACP handles editor-to-agent communication, while MCP handles agent-to-tool communication. When an ACP session starts, the editor passes available MCP server endpoints and credentials to the agent, giving it access to a toolkit of capabilities. This integration pattern is critical for understanding how Thenvoi (which already has MCP support) can participate in the ACP ecosystem.

## Key Findings

### 1. Protocol Relationship: Complementary, Not Competing

ACP and MCP solve different problems in the AI coding assistant stack:

| Protocol | Purpose | Communication Pattern |
|----------|---------|----------------------|
| **ACP** | Editor ↔ Agent | User prompts, streaming responses, file access |
| **MCP** | Agent ↔ Tools | Tool invocation, resource access, structured I/O |

> "ACP is designed to work hand-in-hand with the Model Context Protocol for tool use." - [PromptLayer Blog](https://blog.promptlayer.com/agent-client-protocol-the-lsp-for-ai-coding-agents/)

**The Stack:**
```
┌─────────────────────────────────────┐
│           User / Developer          │
└─────────────────┬───────────────────┘
                  │ User Input
┌─────────────────▼───────────────────┐
│        Editor / IDE (ACP Client)     │
│   - VS Code, Zed, Neovim, etc.       │
└─────────────────┬───────────────────┘
                  │ ACP (JSON-RPC/stdio)
┌─────────────────▼───────────────────┐
│        AI Agent (ACP Server)         │
│   - Claude Code, Gemini CLI, etc.    │
└─────────────────┬───────────────────┘
                  │ MCP (JSON-RPC)
┌─────────────────▼───────────────────┐
│          MCP Servers (Tools)         │
│   - Filesystem, Database, APIs       │
└─────────────────────────────────────┘
```

**Confidence:** High (multiple sources confirm)

### 2. MCP Server Handoff Pattern

When an ACP session initializes, the editor provides MCP server configuration:

**Flow:**
1. Editor starts agent process
2. During `initialize`, editor provides MCP server endpoints
3. Agent connects to MCP servers
4. Agent uses MCP tools during session
5. Tool calls require user permission via ACP

> "When an ACP session starts, the client (Editor/IDE) passes available MCP server endpoints and their credentials to the agent, giving it a toolkit of capabilities." - [PromptLayer](https://blog.promptlayer.com/agent-client-protocol-the-lsp-for-ai-coding-agents/)

**Capability Negotiation:**
```json
{
  "method": "initialize",
  "params": {
    "capabilities": {
      "mcp": {
        "servers": [
          {
            "name": "filesystem",
            "endpoint": "stdio://...",
            "credentials": {...}
          }
        ]
      }
    }
  }
}
```

**Confidence:** High (documentation confirmed)

### 3. Tool Execution Flow

Tools are provided to ACP agents through MCP servers, not through the ACP protocol directly:

**Execution Pattern:**
1. Agent decides to use a tool
2. Agent calls MCP server with tool request
3. ACP may request user permission (`session/request_permission`)
4. MCP server executes tool
5. Result flows back through agent to editor

> "Tools are called and executed by the ACP agent, and results are reported back through the AI SDK's streaming interface." - [AI SDK Docs](https://ai-sdk.dev/providers/community-providers/acp)

**Permission Model:**
> "The client maintains control over actions the agent can perform by asking the user for permission before executing any tool calls."

**Confidence:** High (SDK documentation)

### 4. JSON Schema Reuse

ACP explicitly reuses MCP's JSON schema definitions where applicable:

| ACP Component | MCP Reuse |
|---------------|-----------|
| Content types | TextPart, ImagePart similar to MCP |
| Tool results | Compatible with MCP tool response format |
| Resource references | URI patterns align |
| Error codes | JSON-RPC standard shared |

This design decision:
- Reduces implementation complexity
- Enables tooling reuse
- Maintains ecosystem compatibility

**Confidence:** High (specification analysis)

### 5. AI SDK Integration Pattern

The [Vercel AI SDK](https://ai-sdk.dev/providers/community-providers/acp) provides an ACP provider that demonstrates MCP integration:

**Key Features:**
- MCP Server Integration: Connect MCP servers to enhance agent capabilities
- Tool Execution: Agents execute tools and report results through streaming
- Process Management: Automatic spawning and lifecycle management

**Code Pattern (from AI SDK):**
```typescript
import { acp } from '@ai-sdk/acp';
import { streamText } from 'ai';

const result = streamText({
  model: acp('claude-code'),
  prompt: 'Refactor this function',
  experimental_providerMetadata: {
    acp: {
      mcpServers: [
        { name: 'filesystem', ... }
      ]
    }
  }
});
```

**Confidence:** High (official SDK documentation)

### 6. Thenvoi's Existing MCP Implementation

Thenvoi already has MCP integration through `thenvoi-mcp-server`:

**Current Capabilities:**
- Agent management tools
- Chat management tools
- Message handling tools
- Participant management tools
- LangChain/LangGraph integration examples

**Architecture:**
```
┌─────────────────────────────────────┐
│    LangChain/LangGraph Agent         │
└─────────────────┬───────────────────┘
                  │ MCP Protocol
┌─────────────────▼───────────────────┐
│      thenvoi-mcp-server              │
│  ┌─────────────────────────────────┐ │
│  │ Tools: agents, chats, messages  │ │
│  └─────────────────────────────────┘ │
└─────────────────┬───────────────────┘
                  │ REST API
┌─────────────────▼───────────────────┐
│        Thenvoi Platform              │
└─────────────────────────────────────┘
```

**Confidence:** High (internal documentation)

## Community Signals

### Protocol Convergence

> "On September 1, 2025, something unprecedented happened. IBM's ACP team merged with Google's A2A team under Linux Foundation governance." - [Hyperdev](https://hyperdev.matsuoka.com/p/do-you-know-acp-you-will)

This convergence suggests:
- Industry moving toward standardization
- MCP/ACP/A2A ecosystem consolidating
- Opportunity for early integrators

### Developer Experience Focus

The AI SDK integration demonstrates:
- Framework providers adding ACP support
- MCP as the de facto tool protocol
- Streaming as expected pattern

## Gaps Identified

### Integration Gaps

1. **No standard MCP discovery** - Editors don't automatically find MCP servers
2. **Credential management** - How MCP credentials flow through ACP unclear
3. **Tool permission UX** - Each editor implements differently
4. **MCP server lifecycle** - Who manages MCP server processes?

### Documentation Gaps

1. **ACP MCP page 404** - Official docs missing MCP integration page
2. **Example patterns** - Limited real-world integration examples
3. **Multi-MCP orchestration** - Using multiple MCP servers unclear

### Thenvoi-Specific Gaps

1. **ACP server capability** - Thenvoi doesn't expose ACP interface yet
2. **Bidirectional flow** - Only outbound (Thenvoi calls tools), not inbound
3. **MCP credential passthrough** - No mechanism for ACP clients to auth to Thenvoi MCP

## Implications for Thenvoi

### Opportunity 1: Thenvoi as MCP Provider to ACP Agents

Any ACP-compatible agent could use Thenvoi's MCP server:

```
ACP Editor → ACP Agent → Thenvoi MCP Server → Thenvoi Platform
```

**Value:** Expose Thenvoi's multi-agent orchestration as MCP tools to any ACP agent.

**Implementation:**
1. Ensure thenvoi-mcp-server is fully MCP-compliant
2. Document integration with popular ACP agents
3. Publish to MCP server registries

### Opportunity 2: Thenvoi as ACP Agent with MCP Passthrough

Thenvoi could implement ACP server interface and expose its own agents:

```
ACP Editor → Thenvoi (ACP Server) → Internal Agents → MCP Tools
```

**Value:** Editors get access to Thenvoi's orchestrated agents via ACP.

**Implementation:**
1. Implement ACP server in Thenvoi platform or SDK
2. Accept MCP server configs from editors
3. Orchestrate between Thenvoi agents and external MCP tools

### Opportunity 3: Bridge Pattern (ACP + A2A + MCP)

Thenvoi could be the hub connecting all three protocols:

```
┌───────────────────────────────────────────────────────┐
│                    Thenvoi Platform                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ ACP Server  │  │ A2A Server  │  │ MCP Server  │   │
│  │ (Editors)   │  │ (Agents)    │  │ (Tools)     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘   │
│         │                │                │          │
│         └────────────────┼────────────────┘          │
│                          │                           │
│              ┌───────────▼───────────┐               │
│              │   Orchestration Core   │               │
│              │   (Multi-Agent)        │               │
│              └───────────────────────┘               │
└───────────────────────────────────────────────────────┘
```

**Value:** First platform to unify editor, agent, and tool protocols.

### Opportunity 4: Enhanced MCP Server

Extend thenvoi-mcp-server with ACP-aware features:

- Session context awareness
- User permission integration
- Streaming result support
- Multi-tenant credentials

## Sources Consulted

- [x] [PromptLayer: ACP as LSP for AI](https://blog.promptlayer.com/agent-client-protocol-the-lsp-for-ai-coding-agents/) - Integration overview
- [x] [AI SDK: ACP Provider](https://ai-sdk.dev/providers/community-providers/acp) - SDK integration patterns
- [x] [CodeStandup: ACP Explained](https://codestandup.com/posts/2025/agent-client-protocol-acp-explained/) - Technical deep-dive
- [x] [Hyperdev: Do You Know ACP?](https://hyperdev.matsuoka.com/p/do-you-know-acp-you-will) - Protocol convergence
- [x] thenvoi-mcp-server.arch.md - Internal MCP implementation
- [ ] agentclientprotocol.com/concepts/mcp - Page returns 404

## Related Research Files

- [01-acp-architecture.md](./01-acp-architecture.md) - Full ACP protocol analysis
- [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) - Implementation approach
- Existing Thenvoi MCP: `~/codebase/architecture-hub/thenvoi-mcp-server.arch.md`
