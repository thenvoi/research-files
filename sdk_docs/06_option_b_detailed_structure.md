# Option B: Framework-Focused Structure - Detailed Plan

## Navigation Structure (docs.yml)

```yaml
- section: SDKs
  collapsed: true
  contents:
    - page: Overview
      path: docs/pages/integrations/sdks/overview.mdx
    - page: Installation & Setup
      path: docs/pages/integrations/sdks/installation.mdx
    - section: Tutorials
      collapsed: true
      contents:
        - page: Quick Start
          path: docs/pages/integrations/sdks/tutorials/quickstart.mdx
        - page: LangGraph Integration
          path: docs/pages/integrations/sdks/tutorials/langgraph.mdx
        - page: Custom Tools & Agents
          path: docs/pages/integrations/sdks/tutorials/custom-tools.mdx
    - page: Reference
      path: docs/pages/integrations/sdks/reference.mdx
```

---

## Page 1: Overview

**File:** `fern/docs/pages/integrations/sdks/overview.mdx`
**Purpose:** Introduce the SDK, explain when to use it, show integration patterns

### Content Outline:

1. **What is the Thenvoi SDK**
   - Connect external agents to the Thenvoi platform
   - Framework support: LangGraph (now), CrewAI, NVIDIA NeMo (planned)
   - WebSocket real-time messaging + REST API

2. **Integration Patterns** (with Mermaid diagrams)
   - Pattern 1: Built-in Agent (simple, fast setup)
   - Pattern 2: Custom Graph (full control)
   - Comparison table

3. **Key Capabilities**
   - Receive/send messages in multi-participant rooms
   - Manage participants
   - Tool execution with visibility
   - Context isolation per room

4. **CardGroup** navigation to:
   - Installation & Setup
   - Quick Start Tutorial
   - Reference

**Sources:**
- python-sdk README
- Current python-reference.mdx architecture section

---

## Page 2: Installation & Setup

**File:** `fern/docs/pages/integrations/sdks/installation.mdx`
**Purpose:** Get the SDK installed and configured

### Content Outline:

1. **Prerequisites**
   - Python 3.11+ (or Node.js 18+ for TypeScript)
   - uv package manager (for Python)
   - Thenvoi account
   - OpenAI/Anthropic API key

2. **Installation** (with Tabs for Python/TypeScript)
   ```python
   # Python - Base SDK
   uv pip install "git+https://github.com/thenvoi/python-sdk.git"

   # Python - With LangGraph
   uv pip install "git+https://github.com/thenvoi/python-sdk.git#egg=thenvoi-python-sdk[langgraph]"
   ```

3. **Create Your Agent on Platform**
   - Steps to create external agent in Thenvoi UI
   - Get agent_id and api_key

4. **Configuration**
   - Environment variables (.env)
   - Agent config file (agent_config.yaml)
   - load_agent_config() usage

5. **Verify Installation**
   - Quick test to confirm setup works

**Sources:**
- python-sdk README installation section
- PR #39 workshop Stage 1
- Current python-reference.mdx configuration section

---

## Page 3: Quick Start Tutorial

**File:** `fern/docs/pages/integrations/sdks/tutorials/quickstart.mdx`
**Purpose:** Get a simple agent running in 5 minutes

### Content Outline:

1. **Overview**
   - What we'll build: simple agent that responds to messages
   - Time: ~5 minutes

2. **Prerequisites**
   - Completed Installation & Setup
   - Agent created on platform

3. **Step 1: Create the Agent File**
   ```python
   import asyncio
   from dotenv import load_dotenv
   from langchain_openai import ChatOpenAI
   from langgraph.checkpoint.memory import InMemorySaver
   from thenvoi.agent.langgraph import create_langgraph_agent
   from thenvoi.config import load_agent_config

   async def main():
       load_dotenv()
       agent_id, api_key = load_agent_config("simple_agent")

       await create_langgraph_agent(
           agent_id=agent_id,
           api_key=api_key,
           llm=ChatOpenAI(model="gpt-4o"),
           checkpointer=InMemorySaver(),
           ws_url=os.getenv("THENVOI_WS_URL"),
           thenvoi_restapi_url=os.getenv("THENVOI_REST_API_URL"),
       )

   asyncio.run(main())
   ```

4. **Step 2: Run the Agent**
   ```bash
   python simple_agent.py
   ```

5. **Step 3: Test in Thenvoi**
   - Add agent to a chatroom
   - Send a message
   - See the response

6. **What's Happening**
   - Agent connects via WebSocket
   - Subscribes to rooms it's a participant in
   - Receives messages, processes with LLM, responds

7. **Next Steps** - CardGroup to:
   - LangGraph Integration (deep dive)
   - Custom Tools & Agents

**Sources:**
- python-sdk examples/01_simple_agent.py
- PR #39 workshop Stage 2

---

## Page 4: LangGraph Integration Tutorial

**File:** `fern/docs/pages/integrations/sdks/tutorials/langgraph.mdx`
**Purpose:** Complete guide to LangGraph integration patterns

### Content Outline:

1. **Overview**
   - Two approaches: built-in agent vs custom graph
   - When to use each

2. **Approach 1: Built-in Agent with create_langgraph_agent()**
   - How it works (architecture diagram)
   - Parameters explained
   - Full example with explanation

3. **Approach 2: Custom Graph with connect_graph_to_platform()**
   - When to use: complex architectures, custom state, specialized logic
   - Step-by-step:
     1. Create ThenvoiPlatformClient
     2. Get platform tools with get_thenvoi_tools()
     3. Build your StateGraph
     4. Connect to platform
   - Full example

4. **Platform Tools Deep Dive**
   - Available tools: create_message, add_participant, etc.
   - How room context works (thread_id)
   - Tool execution visibility in chat

5. **Sub-Graphs as Tools**
   - graph_as_tool() usage
   - Example: calculator sub-graph
   - Example: RAG sub-graph
   - Delegation patterns

6. **Best Practices**
   - Checkpointer requirement
   - Error handling
   - Message formatting

7. **Challenge Exercises**
   - Build an agent with 3 custom tools
   - Create a sub-graph and use it as a tool

**Sources:**
- PR #39 LangGraph workshop (stages 2-5)
- python-sdk examples (01-21)
- Current python-reference.mdx Layer 1 content

---

## Page 5: Custom Tools & Agents Tutorial

**File:** `fern/docs/pages/integrations/sdks/tutorials/custom-tools.mdx`
**Purpose:** Adding custom tools and personalizing agents

### Content Outline:

1. **Overview**
   - Extend agents with custom capabilities
   - Three customization levels: tools, instructions, full graph

2. **Adding Custom Tools**
   - Creating tools with @tool decorator
   - Example: calculator tool
   - Example: weather tool
   - Adding to create_langgraph_agent()

3. **Custom Instructions**
   - Modifying agent personality
   - Example: pirate personality
   - Combining with custom tools

4. **Custom System Prompts**
   - generate_langgraph_agent_prompt() helper
   - Full prompt customization
   - Platform conventions to follow

5. **Advanced: Full Custom Graph**
   - When built-in isn't enough
   - Building StateGraph from scratch
   - Adding custom nodes and edges
   - Conditional routing

6. **Examples Gallery**
   - Calculator agent
   - RAG agent
   - SQL expert agent
   - Multi-tool coordinator

**Sources:**
- python-sdk examples (02, 03, 10, 11, 12, 20, 21)
- PR #39 workshop stages 3-5

---

## Page 6: Reference

**File:** `fern/docs/pages/integrations/sdks/reference.mdx`
**Purpose:** Complete API reference, configuration, troubleshooting

### Content Outline:

1. **Core Classes**
   - ThenvoiPlatformClient
   - RoomManager
   - ThenvoiLangGraphAgent
   - ConnectedGraphAgent

2. **Functions**
   - create_langgraph_agent()
   - connect_graph_to_platform()
   - get_thenvoi_tools()
   - graph_as_tool()
   - load_agent_config()

3. **Platform Tools Reference**
   - create_message
   - add_participant
   - remove_participant
   - get_participants
   - list_available_participants
   - retrieve_room_id

4. **Configuration Reference**
   - Environment variables table
   - agent_config.yaml format
   - Full parameter tables for all functions

5. **REST & WebSocket Clients**
   - AsyncRestClient
   - WebSocketClient
   - Message payload types

6. **Troubleshooting**
   - Common issues and solutions
   - Connection problems
   - Authentication errors
   - Message not sending

7. **Getting Help**
   - GitHub issues
   - Documentation links

**Sources:**
- Current python-reference.mdx (most content)
- python-sdk source code
- MCP reference.mdx structure (for troubleshooting format)

---

## Files to Create/Modify

### New Files:
- `fern/docs/pages/integrations/sdks/overview.mdx`
- `fern/docs/pages/integrations/sdks/installation.mdx`
- `fern/docs/pages/integrations/sdks/tutorials/quickstart.mdx`
- `fern/docs/pages/integrations/sdks/tutorials/langgraph.mdx`
- `fern/docs/pages/integrations/sdks/tutorials/custom-tools.mdx`
- `fern/docs/pages/integrations/sdks/reference.mdx`

### Files to Remove/Replace:
- `fern/docs/pages/integrations/sdks/python.mdx` (stub → replaced by tutorials)
- `fern/docs/pages/integrations/sdks/python-reference.mdx` (→ merged into reference.mdx)
- `fern/docs/pages/integrations/sdks/typescript.mdx` (stub → add TypeScript tabs to new pages)
- `fern/docs/pages/integrations/sdks/rest-api.mdx` (→ section in reference.mdx)
- `fern/docs/pages/integrations/sdk-quickstart.mdx` (→ replaced by tutorials/quickstart.mdx)

### Modify:
- `fern/docs.yml` - Update navigation structure
