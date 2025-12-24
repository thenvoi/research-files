# Python SDK Repository Research

**Location:** `/Users/roishikler/codebase/python-sdk`

## Overview

The **Thenvoi Python SDK** enables AI agents built with various frameworks (LangGraph, with CrewAI and NVIDIA NeMo planned) to connect to the Thenvoi platform for multi-participant AI agent coordination.

---

## Key Features

1. **Multiple Framework Support** - LangGraph (production ready), CrewAI/NVIDIA NeMo (planned)
2. **Dual Integration Approaches**:
   - SDK-managed agents (simplified setup)
   - Custom graph integration (bring your own LangGraph)
3. **Platform Integration** - WebSocket messaging, REST API, room management
4. **Agent Capabilities** - Receive/send messages, manage participants, tool execution tracking

---

## Installation

```bash
# Base SDK
uv pip install "git+https://github.com/thenvoi/python-sdk.git"

# With LangGraph support
uv pip install "git+https://github.com/thenvoi/python-sdk.git#egg=thenvoi-python-sdk[langgraph]"
```

**Requirements:** Python 3.11-3.12, uv package manager

---

## Architecture

```
src/thenvoi/
├── config/
│   └── loader.py                    # YAML config loading (agent_config.yaml)
├── agent/
│   ├── core/
│   │   ├── platform_client.py       # ThenvoiPlatformClient (core infrastructure)
│   │   └── room_manager.py          # RoomManager (event handling)
│   ├── langgraph/
│   │   ├── agent.py                 # ThenvoiLangGraphAgent, create_langgraph_agent()
│   │   ├── tools.py                 # get_thenvoi_tools() - platform tools
│   │   ├── graph_tools.py           # graph_as_tool() - wrap graphs as tools
│   │   ├── message_formatters.py    # Message formatting utilities
│   │   └── prompts.py               # System prompt generation
│   ├── crewai/                      # Placeholder for CrewAI adapter
│   └── letta/                       # Placeholder for Letta adapter
├── client/
│   ├── rest/                        # AsyncRestClient for REST API
│   └── streaming/                   # WebSocketClient for WebSocket streaming
```

---

## Core Classes & Functions

### 1. `create_langgraph_agent()` - Simplest Approach
```python
from thenvoi.agent.langgraph import create_langgraph_agent

agent = await create_langgraph_agent(
    agent_id=agent_id,
    api_key=api_key,
    llm=ChatOpenAI(model="gpt-4o"),
    checkpointer=InMemorySaver(),
    ws_url=ws_url,
    thenvoi_restapi_url=thenvoi_restapi_url,
    additional_tools=[custom_tool1],       # Optional
    custom_instructions="Custom prompt",   # Optional
)
```

### 2. `ThenvoiPlatformClient` - Core Infrastructure
```python
client = ThenvoiPlatformClient(
    agent_id="agent-123",
    api_key="key-456",
    ws_url="wss://platform.thenvoi.com",
    thenvoi_restapi_url="https://api.thenvoi.com"
)
await client.fetch_agent_metadata()
ws_client = await client.connect_websocket()
```

### 3. `RoomManager` - Event Handling
```python
manager = RoomManager(
    agent_id=agent_id,
    agent_name=agent_name,
    api_client=client.api_client,
    ws_client=ws_client,
    message_handler=async_message_handler,
)
await manager.start()
await manager.subscribe_to_rooms()
```

### 4. `get_thenvoi_tools()` - Platform Tools
```python
tools = get_thenvoi_tools(client=api_client, agent_id=agent_id)
# Returns: send_message, add_participant, remove_participant,
#          get_participants, list_available_participants
```

### 5. `graph_as_tool()` - Wrap Graphs as Tools
```python
calculator_tool = graph_as_tool(
    calculator_graph,
    name="calculator",
    description="Evaluates math expressions"
)
```

### 6. `connect_graph_to_platform()` - Custom Graph Integration
```python
await connect_graph_to_platform(
    graph=my_custom_graph,
    platform_client=platform_client,
)
```

### 7. `load_agent_config()` - Configuration Loading
```python
agent_id, api_key = load_agent_config("my_agent")
```

---

## Examples Available

| File | Purpose |
|------|---------|
| `01_simple_agent.py` | Simplest agent - just LLM + platform tools |
| `02_custom_tools.py` | Add calculator and weather tools |
| `03_custom_personality.py` | Custom personality (pirate theme) |
| `10_calculator_as_tool.py` | Sub-graph as tool (math delegation) |
| `11_rag_as_tool.py` | RAG sub-graph (document retrieval) |
| `12_delegate_to_sql_agent.py` | SQL expert delegation |
| `20_custom_agent_with_instructions.py` | Custom system prompt |
| `21_custom_graph.py` | Full manual graph construction |

---

## Configuration

**Environment Variables (.env):**
```
THENVOI_WS_URL=wss://platform.thenvoi.com/ws
THENVOI_REST_API_URL=https://api.thenvoi.com
OPENAI_API_KEY=sk-...
```

**Agent Config (agent_config.yaml):**
```yaml
my_agent:
  agent_id: "agent-uuid"
  api_key: "agent-api-key"
```

---

## Integration Approaches

| Approach | Use Case | Complexity |
|----------|----------|------------|
| `create_langgraph_agent()` | Quick prototyping, simple agents | Low |
| `ThenvoiLangGraphAgent` class | More control over lifecycle | Medium |
| `connect_graph_to_platform()` | Full custom graph architecture | High |
