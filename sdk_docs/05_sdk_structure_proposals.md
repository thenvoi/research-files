# SDK Documentation Structure Proposals

Based on research of:
1. Current Fern SDK docs (mostly stubs)
2. MCP section structure (the model to follow)
3. python-sdk and thenvoi-sdk-python repos
4. PR #39 tutorials (LangGraph workshop, SDK integration)

---

## Option A: Mirror MCP Structure (Minimal)

Directly mirrors the MCP section with 4 pages.

```
SDKs/
├── Overview           # What is the SDK, comparison of integration approaches
├── Quick Start        # Get running in 5 minutes (simple agent)
├── Connect Your Agent # Tutorial: connect LangGraph/custom agents
└── Reference          # Complete API reference, configuration, troubleshooting
```

**Pros:**
- Simple, consistent with MCP
- Easy to maintain
- Clear learning path

**Cons:**
- May be too condensed for SDK complexity
- Less room for framework-specific content
- Reference page could get very long

---

## Option B: Framework-Focused Structure

Organizes by agent framework with shared foundation.

```
SDKs/
├── Overview                    # What is the SDK, integration patterns
├── Installation & Setup        # Prerequisites, installation, configuration
├── Tutorials/
│   ├── Quick Start             # Simple agent in 5 minutes
│   ├── LangGraph Integration   # Complete LangGraph tutorial (from PR #39)
│   └── Custom Tools & Agents   # Adding tools, custom instructions
└── Reference                   # API reference, configuration, troubleshooting
```

**Pros:**
- Room for detailed tutorials
- Framework-specific guidance
- Matches PR #39 workshop structure

**Cons:**
- More pages to maintain
- LangGraph-heavy (CrewAI not ready yet)

---

## Option C: Progressive Learning Structure

Organizes by complexity level, similar to LangGraph workshop stages.

```
SDKs/
├── Overview                # What is the SDK, when to use it
├── Getting Started/
│   ├── Installation        # Setup, prerequisites, environment
│   └── Your First Agent    # Simple agent tutorial
├── Building Agents/
│   ├── Custom Tools        # Adding tools to agents
│   ├── Custom Instructions # Personality and prompts
│   └── Advanced Patterns   # Sub-graphs, delegation, custom graphs
└── Reference               # API reference, configuration, troubleshooting
```

**Pros:**
- Clear progression from simple to complex
- Matches workshop learning stages
- Room to grow with new frameworks

**Cons:**
- Deeper navigation nesting
- May overwhelm new users

---

## Option D: Use-Case Focused Structure (Recommended)

Mirrors MCP's approach of different paths for different use cases.

```
SDKs/
├── Overview                    # What is the SDK, two integration patterns
│                               # (like MCP's AI Assistant vs External Agent)
├── Simple Agent Setup          # Built-in agent architecture (quick start)
├── Custom Agent Integration    # Bring your own LangGraph (advanced)
└── Reference                   # API reference, config, troubleshooting
```

**Explanation:**

1. **Overview** (like MCP Overview)
   - What is the Thenvoi SDK
   - Two integration patterns with Mermaid diagrams:
     - Pattern 1: Use built-in agent (simple, fast)
     - Pattern 2: Bring your own LangGraph (full control)
   - Comparison table
   - CardGroup navigation to setup guides

2. **Simple Agent Setup** (like MCP AI Assistant Setup)
   - Prerequisites
   - Installation with Tabs (Python/TypeScript)
   - Create agent on platform
   - Configure environment
   - Run your first agent
   - Add custom tools
   - Add custom instructions
   - Verification and testing

3. **Custom Agent Integration** (like MCP External Agents)
   - Prerequisites
   - When to use custom graphs
   - ThenvoiPlatformClient setup
   - Getting platform tools
   - Building your custom graph
   - Connecting to platform
   - Advanced patterns (sub-graphs as tools)

4. **Reference** (like MCP Reference)
   - Core classes and functions
   - Configuration reference
   - Platform tools reference
   - Troubleshooting
   - Getting help

**Pros:**
- Directly mirrors MCP structure (user's goal)
- Clear paths for different user needs
- Scalable for future frameworks
- Not too deep, not too shallow

**Cons:**
- TypeScript SDK content is sparse currently
- May need to expand as frameworks are added

---

## Comparison Summary

| Option | Pages | MCP Similarity | Complexity Support | Maintenance |
|--------|-------|----------------|-------------------|-------------|
| A: Minimal | 4 | High | Low | Easy |
| B: Framework | 6 | Medium | Medium | Medium |
| C: Progressive | 7 | Low | High | Hard |
| **D: Use-Case** | **4** | **High** | **Medium** | **Easy** |

---

## Recommendation: Option D (Use-Case Focused)

This best matches the user's goal of making SDK look like MCP, while providing:
- Clear overview with two integration patterns
- Separate setup guides for different use cases
- Comprehensive reference page
- Room to grow (add CrewAI setup page later)

---

## Content Sources for Each Page

### Overview
- Current `python-reference.mdx` architecture section
- SDK repo README introduction
- Create Mermaid diagrams (like MCP overview)

### Simple Agent Setup
- PR #39 LangGraph workshop stages 1-3
- SDK examples `01_simple_agent.py`, `02_custom_tools.py`, `03_custom_personality.py`
- Current `python.mdx` (expand from stub)

### Custom Agent Integration
- PR #39 LangGraph workshop stages 4-5
- SDK examples `20_custom_agent_with_instructions.py`, `21_custom_graph.py`
- Current `python-reference.mdx` Layer 2-3 content

### Reference
- Current `python-reference.mdx` (most of it)
- SDK repo code documentation
- Add troubleshooting section (like MCP reference)
