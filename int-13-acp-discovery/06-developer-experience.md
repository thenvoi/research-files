# Developer Experience Analysis

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

The ACP developer experience varies significantly between agent developers and end users. Agent developers face a rapidly evolving protocol with limited documentation and examples, while end users experience inconsistent setup processes across editors. Key pain points include configuration complexity, adapter requirements for major agents, and missing features for external agents. Thenvoi has an opportunity to provide a smoother developer experience through comprehensive documentation and turnkey setup.

## Key Findings

### 1. Agent Developer Experience

**Current State:**

| Aspect | Quality | Notes |
|--------|---------|-------|
| **SDKs** | Good | Python, TypeScript, Rust, Kotlin available |
| **Documentation** | Fair | Basic docs exist, advanced patterns missing |
| **Examples** | Fair | Basic examples, complex patterns absent |
| **Testing tools** | Poor | No standard test harness |
| **Schema stability** | Evolving | Frequent releases (v0.10.6 current) |

**Developer Journey (Building an ACP Agent):**
1. ✅ Install SDK (`pip install agent-client-protocol`)
2. ✅ Follow quickstart guide
3. ⚠️ Implement required methods (some gaps in docs)
4. ⚠️ Test manually with Zed (no automated testing)
5. ❌ Debug issues (limited tooling)
6. ❌ Handle edge cases (sparse documentation)
7. ❌ Distribution (no clear path)

**Pain Points for Agent Developers:**
- Schema versions evolve rapidly (may break compatibility)
- No mock editor for testing
- Limited real-world examples
- MCP integration not well documented
- No certification/validation process

**Confidence:** High (SDK analysis, GitHub issues)

### 2. End User Experience

**Current State:**

| Editor | Setup Difficulty | Notes |
|--------|-----------------|-------|
| **Zed** | Easy | Native support, built-in agents |
| **Neovim** | Moderate | Plugin installation required |
| **Emacs** | Moderate | Plugin setup required |
| **VS Code** | Hard | No native support, extension only |
| **JetBrains** | N/A | Coming soon |

**User Journey (Using an ACP Agent in Zed):**
1. ✅ Open Zed preferences
2. ✅ Select built-in agent (Claude, Gemini, Codex)
3. ⚠️ Configure authentication (varies by agent)
4. ⚠️ Custom agents require JSON editing
5. ❌ Agent discovery (manual process)
6. ❌ Multi-agent workflow (not supported)

**Pain Points for End Users:**
- Different auth flows for each agent
- No agent marketplace/discovery
- Custom agent setup requires JSON editing
- No way to compare agent capabilities
- Missing features for external agents (editing, history)

**Confidence:** High (Zed documentation, community feedback)

### 3. Configuration Complexity

**Built-in Agents:**
```json
// Easy - just select from UI
```

**Custom Agents:**
```json
{
  "agent_servers": {
    "My Custom Agent": {
      "type": "custom",
      "command": "python",
      "args": ["-m", "my_agent"],
      "env": {
        "API_KEY": "...",
        "MODEL": "...",
        "BASE_URL": "..."
      }
    }
  }
}
```

**Issues:**
- No config validation
- No schema hints in editors
- Environment variable handling varies
- No secure credential storage

**Community Feedback (Goose Discussion):**
> "Config is a bit of a mess... each client that knows about goose may want to interact with the config system, which isn't currently covered in ACP."

**Confidence:** High (documentation, community discussions)

### 4. Adapter Complexity

Major agents require adapters rather than native ACP:

| Agent | Native ACP | Adapter Required | Maintained By |
|-------|------------|-----------------|---------------|
| Claude Code | ❌ | `@zed-industries/claude-code-acp` | Zed |
| Codex CLI | ❌ | `codex-acp` | Zed |
| Gemini CLI | ✅ | None | Google |
| Goose | ✅ | None | Block |

**Implications:**
- Adapter maintenance overhead
- Version compatibility issues
- Feature lag behind native
- Multiple installation steps

**Confidence:** High (Zed documentation)

### 5. Feature Gaps for External Agents

From Zed documentation:
> "Message editing, thread resumption from history, and checkpointing remain unavailable across all external agents."

**Feature Matrix:**

| Feature | Built-in Agents | External Agents |
|---------|-----------------|-----------------|
| Message editing | ✅ | ❌ |
| Thread resumption | ✅ | ❌ |
| Checkpointing | ✅ | ❌ |
| MCP support | ✅ | Varies |
| Streaming | ✅ | ✅ |
| Basic prompts | ✅ | ✅ |

**Impact:**
- External agents are "second class"
- Users prefer built-in for full features
- Discourages custom agent adoption

**Confidence:** High (official documentation)

### 6. Debugging Experience

**Available Tools:**
- `dev: open acp logs` in Zed (JSON-RPC inspection)
- Console logging in agent
- No remote debugging support

**Missing:**
- Structured logging standards
- Error categorization
- Performance profiling
- Test fixtures

**Confidence:** High (Zed documentation)

## Community Signals

### Frustration Points (from GitHub issues)

1. **Configuration** - No standard config management
2. **Discovery** - "How do I find agents?"
3. **Compatibility** - "Will this agent work with my editor?"
4. **Authentication** - "Each agent has different auth"
5. **Updates** - "How do I update agents?"

### Positive Signals

1. **SDK quality** - Python SDK well-received
2. **Zed integration** - Smooth for built-in agents
3. **Community growth** - Multiple adapters being built
4. **Documentation improving** - Active doc contributions

## Gaps Identified

### Documentation Gaps

1. **No end-to-end tutorial** - Building to deployment
2. **No troubleshooting guide** - Common issues/solutions
3. **No architecture deep-dive** - Advanced patterns
4. **No migration guides** - Between schema versions

### Tooling Gaps

1. **No test framework** - Automated agent testing
2. **No validator** - Config validation tool
3. **No profiler** - Performance analysis
4. **No simulator** - Mock editor for testing

### Ecosystem Gaps

1. **No marketplace** - Agent discovery
2. **No ratings/reviews** - Quality signals
3. **No certification** - Compatibility validation
4. **No analytics** - Usage insights

## Implications for Thenvoi

### DX Opportunities

**1. Turnkey Setup**
Thenvoi could provide single-command installation:
```bash
# Install Thenvoi ACP agent
curl -fsSL https://thenvoi.com/install-acp | sh

# Or via package manager
brew install thenvoi/tap/thenvoi-acp
npm install -g @thenvoi/acp-agent
```

**2. Guided Configuration**
Interactive setup wizard:
```bash
$ thenvoi-acp setup
? Enter your Thenvoi API key: ****
? Select default agent: [Research Agent]
? Enable streaming: [Yes]
✓ Configuration saved to ~/.config/thenvoi/acp.json
✓ Zed settings updated
```

**3. Comprehensive Documentation**
- Quick start (5 minutes)
- Editor-specific guides (Zed, Neovim, Emacs)
- Troubleshooting FAQ
- Video walkthroughs

**4. Testing Tools**
Provide mock editor for agent testing:
```bash
$ thenvoi-acp test
Starting mock ACP client...
> hello
[Session created: abc123]
[Response]: Hello! How can I help you today?
[Latency: 234ms]
```

### Competitive Advantage

| Aspect | Current ACP Agents | Thenvoi Opportunity |
|--------|-------------------|---------------------|
| Setup time | 15-30 minutes | < 5 minutes |
| Config | Manual JSON | Automated wizard |
| Testing | Manual | Automated tools |
| Updates | Manual | Auto-update |
| Discovery | None | Integrated |
| Support | Community | Enterprise support |

### Recommended DX Investments

| Priority | Investment | Impact |
|----------|-----------|--------|
| P0 | One-line installer | First impression |
| P0 | Zed quick start guide | Primary editor |
| P1 | Configuration wizard | Reduce friction |
| P1 | Error messages/troubleshooting | Support burden |
| P2 | Testing tools | Developer adoption |
| P2 | Editor-specific docs | Broader reach |

## Sources Consulted

- [x] [ACP Python SDK](https://github.com/agentclientprotocol/python-sdk) - Developer experience
- [x] [Zed External Agents](https://zed.dev/docs/ai/external-agents) - User experience
- [x] [Goose ACP Discussion](https://github.com/block/goose/discussions/4645) - Config feedback
- [x] [GitHub Issues](https://github.com/agentclientprotocol/agent-client-protocol/issues) - Pain points
- [x] ACP RFDs - Future improvements

## Related Research Files

- [04-custom-agent-integration.md](./04-custom-agent-integration.md) - Implementation details
- [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) - Thenvoi implementation
