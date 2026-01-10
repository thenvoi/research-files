# AgentCore Deep Dive

## What is Amazon Bedrock AgentCore?

Amazon Bedrock AgentCore is AWS's fully managed platform for building, deploying, and operating AI agents at scale. It eliminates infrastructure complexity, letting organizations focus on building agent capabilities rather than managing infrastructure.

**Timeline:**
- Preview: April 2025
- General Availability: October 2025
- Latest Updates: December 2025 (Policy, Evaluations previews)

**Adoption:**
- 2M+ SDK downloads in 5 months
- Enterprise customers: Amazon Devices, Cox Automotive, PGA TOUR, Thomson Reuters, Workday, S&P Global
- 80% of agents in AWS AI hackathon built on AgentCore

---

## The 9 AgentCore Services

### 1. Runtime

The core execution environment for AI agents.

**Capabilities:**
- Serverless execution (no infrastructure management)
- Complete session isolation (data security)
- Support for workloads up to 8 hours
- Low-latency conversational to async workloads
- Bidirectional streaming for voice agents
- A2A and MCP protocol support

**Technical Details:**
- Container-based deployment
- ARM64 architecture required
- Port requirements vary by protocol (8080/8000/9000)
- Automatic scaling

### 2. Gateway

Transforms APIs and services into agent-compatible tools.

**Capabilities:**
- Convert REST APIs to MCP-compatible tools
- Connect Lambda functions as tools
- Integrate existing MCP servers
- Semantic search for tool discovery
- Centralized tool catalog

**Key Features:**
- Translation: Agent requests → API/Lambda calls
- Composition: Multiple tools → single MCP endpoint
- Credential management: Secure injection

**MCP Server Support:**
- Protocol versions: 2025-06-18, 2025-03-26
- Automatic tool discovery via `tools/list`
- Session management via `Mcp-Session-Id` header

### 3. Memory

Persistent context and learning from interactions.

**Capabilities:**
- Maintain context across sessions
- Learn from user interactions
- Improve agent performance over time
- Centralized state checkpointing
- Episodic memory (new)

**Use Cases:**
- Personalized user experiences
- Context-aware responses
- Multi-turn conversation tracking
- Knowledge accumulation

### 4. Identity

Secure access management for agents.

**Capabilities:**
- AWS resource access via IAM
- Third-party service authentication
- OAuth 2.0 / SigV4 support
- Integration with existing identity providers

### 5. Browser

Cloud-based browser for web interactions.

**Capabilities:**
- Fast, secure browser runtime
- Web page interaction
- Data extraction from websites
- Form filling and navigation

**Use Cases:**
- Web scraping agents
- Automated testing
- Information gathering
- Web-based workflows

### 6. Code Interpreter

Secure sandbox for code execution.

**Capabilities:**
- Write and execute code securely
- Isolated sandbox environments
- Data visualization generation
- Computational tasks

### 7. Policy (Preview)

Real-time guardrails for agent actions.

**Capabilities:**
- Intercept tool calls in real-time
- Deterministic controls (not LLM-based)
- Block unauthorized actions
- Operates outside agent code
- Integration with Gateway

**Key Benefit:** Addresses enterprise concerns about agent autonomy and unexpected actions.

### 8. Evaluations (Preview)

Quality assessment and monitoring.

**Capabilities:**
- Sample live interactions
- Built-in evaluators (correctness, helpfulness, safety, goal success)
- Custom evaluators
- Continuous quality monitoring

**Availability:** US East, US West, Asia Pacific (Sydney), Europe (Frankfurt)

### 9. Observability

Monitoring and debugging capabilities.

**Capabilities:**
- CloudWatch dashboards
- OpenTelemetry integration
- Key metrics: token usage, latency, session duration, error rates
- Trace and debug issues
- Audit agent decisions

---

## Protocol Support

### A2A (Agent-to-Agent) Protocol

AgentCore Runtime supports the A2A protocol for multi-agent communication.

**Benefits:**
- Seamless interoperability across frameworks
- Standardized communication format
- Agent discovery via Agent Cards
- No complex translation layers needed

**Technical Implementation:**
- Port 9000 for A2A servers
- JSON-RPC communication
- `/.well-known/agent-card.json` discovery
- SigV4/OAuth 2.0 authentication

**Example Agent Card:**
```json
{
  "name": "Calculator Agent",
  "description": "Performs arithmetic operations",
  "url": "https://...",
  "version": "1.0.0",
  "protocolVersion": "0.3",
  "capabilities": {
    "streaming": true
  },
  "skills": [
    {
      "id": "calculate",
      "name": "Calculate",
      "description": "Perform arithmetic"
    }
  ]
}
```

### MCP (Model Context Protocol)

AgentCore Gateway supports MCP for tool integration.

**Technical Implementation:**
- Port 8000 for MCP servers
- Stateless streamable-HTTP transport
- JSON-RPC for `tools/list` and `tools/call`
- Session management via headers

---

## Framework Compatibility

AgentCore is framework-agnostic, supporting:

- **Strands Agents** (AWS native)
- **LangGraph** / LangChain
- **CrewAI**
- **LlamaIndex**
- **Google ADK**
- **OpenAI Agents SDK**
- **Anthropic Claude Agents SDK**
- **PydanticAI**

Any framework can deploy to AgentCore Runtime if it meets the container requirements.

---

## Multi-Agent Patterns

AgentCore supports several multi-agent patterns:

### 1. Supervisor Agent Pattern

Central orchestrator coordinates specialized agents.

```
           ┌─────────────┐
           │ Supervisor  │
           │   Agent     │
           └──────┬──────┘
       ┌──────────┼──────────┐
       ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Agent A  │ │ Agent B  │ │ Agent C  │
│ (Task 1) │ │ (Task 2) │ │ (Task 3) │
└──────────┘ └──────────┘ └──────────┘
```

**Use Cases:**
- Incident response
- Data analysis
- Customer support routing

### 2. Agent Discovery

Agents discover peers via Agent Cards.

- Fetch `/.well-known/agent-card.json`
- Parse capabilities and skills
- Route requests to appropriate agents

### 3. Multi-Agent Voice

Bidirectional streaming enables:
- Simultaneous listen and respond
- Interrupt handling
- Context changes mid-conversation

---

## Security Features

### Enterprise-Grade Security

- **Session Isolation:** Complete isolation between sessions
- **VPC Connectivity:** Amazon VPC support
- **PrivateLink:** AWS PrivateLink support
- **CloudFormation:** Infrastructure as code
- **Resource Tagging:** Organizational controls

### Authentication

- IAM for AWS resources
- SigV4 for AgentCore APIs
- OAuth 2.0 for third-party services
- API keys for external access

### Policy Controls

- Real-time interception of tool calls
- Deterministic blocking (not LLM-based)
- Operates outside agent code
- Configurable rules

---

## Pricing Model

AgentCore is pay-as-you-go:

- **Runtime:** Per-second execution time
- **Memory:** Per-GB storage
- **Gateway:** Per-request
- **Other services:** Varies

No upfront costs, scale to zero when idle.

---

## Related AWS Services

### Agent Squad (formerly Multi-Agent Orchestrator)

Open-source framework for multi-agent routing:
- Intelligent intent classification
- Dynamic query routing
- Python and TypeScript support
- Context management

### Amazon Bedrock Agents

Higher-level agent building blocks:
- Knowledge bases integration
- Action groups
- More structured than AgentCore

### Strands Agents

AWS's agent framework:
- Native AgentCore integration
- Tool and A2A support
- Python SDK

---

## Limitations and Considerations

### From Developer Feedback

1. **Overkill for Simple Cases:** Simple Bedrock invocations handle most use cases; AgentCore makes sense for complex scenarios.

2. **Regional Availability:** Some features (Evaluations, Policy) limited to specific regions.

3. **Production Scale:** Still forming opinions on how well it handles production workloads at scale.

4. **M×N Integration Problem:** Connecting each agent to multiple tools creates complexity, though Gateway helps.

### What AgentCore Doesn't Do

1. **Human-in-the-Loop:** No native human participant support
2. **Cross-Enterprise Orchestration:** Single AWS account focus
3. **Visual Workflow Builder:** Code/config based only
4. **Framework-Specific Features:** Generic to support all frameworks

---

## Key Sources

- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/)
- [AgentCore FAQs](https://aws.amazon.com/bedrock/agentcore/faqs/)
- [AgentCore Developer Guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [AgentCore Python SDK](https://github.com/aws/bedrock-agentcore-sdk-python)
- [AgentCore Samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples)
- [A2A Protocol in AgentCore](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/introducing-amazon-bedrock-agentcore-gateway-transforming-enterprise-ai-agent-tool-development/)
