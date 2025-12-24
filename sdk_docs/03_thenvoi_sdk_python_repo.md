# Thenvoi SDK Python Repository Research

**Location:** `/Users/roishikler/codebase/thenvoi-sdk-python`

## Overview

This appears to be essentially the same SDK as python-sdk with nearly identical architecture and functionality. The key difference is the package naming and potentially minor implementation differences.

---

## Architecture

```
src/thenvoi/
├── agent/
│   ├── core/                          # Shared infrastructure
│   │   ├── platform_client.py        # ThenvoiPlatformClient
│   │   └── room_manager.py           # RoomManager
│   └── langgraph/                     # LangGraph adapter
│       ├── agent.py                  # ThenvoiLangGraphAgent, ConnectedGraphAgent
│       ├── tools.py                  # get_thenvoi_tools()
│       ├── graph_tools.py            # graph_as_tool()
│       ├── prompts.py                # System prompt generation
│       └── message_formatters.py     # Message formatting
├── client/
│   ├── rest/                         # AsyncRestClient, RestClient
│   └── streaming/                    # WebSocketClient
└── config/
    └── loader.py                     # load_agent_config()
```

---

## Key Classes (Same as python-sdk)

1. **ThenvoiPlatformClient** - Core infrastructure (validation, WebSocket, API client)
2. **RoomManager** - Room subscriptions and event routing
3. **create_langgraph_agent()** - Functional API for simple agents
4. **ThenvoiLangGraphAgent** - Class-based API for more control
5. **connect_graph_to_platform()** - Custom graph integration
6. **get_thenvoi_tools()** - Platform tools for LangGraph
7. **graph_as_tool()** - Wrap graphs as tools

---

## Platform Tools

```python
tools = get_thenvoi_tools(client=api_client, agent_id=agent_id)

# Returns LangChain tools:
# - retrieve_room_id: Get current room ID
# - create_message: Send message to room
# - list_available_participants: Show who can be added
# - get_participants: Show room participants
# - add_participant: Add someone to room
# - remove_participant: Remove from room
```

**Important:** Room ID comes from `thread_id` in `RunnableConfig`, not from LLM parameters.

---

## Usage Patterns

### Pattern 1: Simple Agent
```python
from thenvoi.agent.langgraph import create_langgraph_agent

await create_langgraph_agent(
    agent_id=agent_id,
    api_key=api_key,
    llm=ChatOpenAI(model="gpt-4o"),
    checkpointer=InMemorySaver(),
    ws_url=ws_url,
    thenvoi_restapi_url=thenvoi_restapi_url,
)
```

### Pattern 2: Custom Tools
```python
@tool
def calculate(operation: str, left: float, right: float) -> str:
    """Perform math calculation."""
    ...

await create_langgraph_agent(
    ...,
    additional_tools=[calculate],
    custom_instructions="Use calculator for math.",
)
```

### Pattern 3: Custom Graph
```python
from thenvoi.agent.langgraph import connect_graph_to_platform, get_thenvoi_tools

platform_client = ThenvoiPlatformClient(...)
tools = get_thenvoi_tools(platform_client.api_client, agent_id)

# Build custom graph with tools
graph = StateGraph(MessagesState)
# ... add nodes and edges ...
compiled_graph = graph.compile(checkpointer=InMemorySaver())

await connect_graph_to_platform(
    graph=compiled_graph,
    platform_client=platform_client,
)
```

---

## Message Flow

```
Incoming Chat Message
        ↓
WebSocket (Phoenix Channels)
        ↓
MessageCreatedPayload
        ↓
RoomManager.message_handler
        ↓
LangGraph Agent (invoke with thread_id=room_id)
        ↓
LLM decides: response or tools?
        ↓
If tools → Tool execution streamed to room
If response → create_message tool called
        ↓
Response sent via REST API
        ↓
Broadcast to Room Participants
```

---

## Examples Available

Same structure as python-sdk:
- `01_simple_agent.py` - Basic setup
- `02_custom_tools.py` - Adding custom tools
- `03_custom_personality.py` - Custom instructions
- `10_calculator_as_tool.py` - Graph as tool
- `11_rag_as_tool.py` - RAG system as tool
- `12_delegate_to_sql_agent.py` - SQL delegation
- `20_custom_agent_with_instructions.py` - Enhanced setup
- `21_custom_graph.py` - Full custom graph

---

## Dependencies

**Core:**
- websockets >= 10.0
- httpx >= 0.24.0
- pydantic >= 2.0.0
- phoenix-channels-python-client
- python-dotenv >= 1.1.1
- pyyaml >= 6.0

**LangGraph Optional:**
- langchain >= 1.0.0
- langgraph >= 1.0.0
- langchain-openai >= 0.3.0
- openai >= 1.0.0
