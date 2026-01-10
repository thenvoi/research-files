# AWS Bedrock Marketplace Listing Guide

## Overview

AWS Marketplace allows ISVs to list AI agents, tools, and services that run on Amazon Bedrock AgentCore. This guide covers how to list Thenvoi as a marketplace offering.

---

## Listing Types for Thenvoi

### Option 1: A2A Server Listing

**Container Type:** A2A Server
**Port:** 9000
**Value Proposition:** Multi-agent orchestration with human-in-the-loop

**Listing Title:** Thenvoi Multi-Agent Orchestration
**Category:** AI Agents & Tools

### Option 2: MCP Server Listing

**Container Type:** MCP Server
**Port:** 8000
**Value Proposition:** Orchestration tools for any AI agent

**Listing Title:** Thenvoi Orchestration Tools
**Category:** AI Tools

### Option 3: Both (Recommended)

List both A2A server and MCP server as separate products for maximum reach.

---

## Technical Requirements

### Container Requirements (All Types)

| Requirement | Specification |
|-------------|---------------|
| Architecture | ARM64 |
| Base Image | Amazon Linux 2023 or similar |
| Container Registry | Amazon ECR |
| Health Check | `/ping` endpoint returning 200 |
| Startup Time | < 60 seconds |
| Memory | Configurable, recommend 512MB - 4GB |
| Security | No hardcoded credentials |

### A2A Server Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ping` | GET | Health check |
| `/.well-known/agent-card.json` | GET | Agent discovery |
| `/` | POST | JSON-RPC message handling |

**Port:** 9000

**JSON-RPC Methods:**
- `message/send` - Send message to agent
- `tasks/get` - Get task status

### MCP Server Requirements

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ping` | GET | Health check |
| `/mcp` | POST | JSON-RPC tool calls |

**Port:** 8000

**JSON-RPC Methods:**
- `tools/list` - List available tools
- `tools/call` - Execute a tool

---

## Registration Process

### Step 1: Register as AWS Marketplace Seller

1. **Prerequisites:**
   - AWS account
   - Valid business information
   - Tax documentation
   - Bank account for disbursements

2. **Registration:**
   - Go to [AWS Marketplace Management Portal](https://aws.amazon.com/marketplace/management/)
   - Complete seller registration
   - Wait for approval (typically 1-2 weeks)

### Step 2: Complete Foundational Technical Review (FTR)

**Purpose:** Validate solution meets AWS standards

**Key Areas:**
- Security (no vulnerabilities)
- Reliability (proper error handling)
- Operational excellence (logging, monitoring)
- Architecture (follows best practices)

**Process:**
- Self-assessment questionnaire
- AWS review
- Remediation if needed
- Approval

**Timeline:** 2-4 weeks

### Step 3: Prepare Container Image

**Dockerfile Example (A2A Server):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ .

# Expose port
EXPOSE 9000

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:9000/ping || exit 1

# Run server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]
```

**Build for ARM64:**
```bash
docker buildx build --platform linux/arm64 -t thenvoi-a2a-server .
```

### Step 4: Push to Amazon ECR

```bash
# Create repository
aws ecr create-repository --repository-name thenvoi-a2a-server

# Login to ECR
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com

# Tag and push
docker tag thenvoi-a2a-server:latest <account>.dkr.ecr.<region>.amazonaws.com/thenvoi-a2a-server:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/thenvoi-a2a-server:latest
```

### Step 5: Create Marketplace Listing

**Required Information:**

1. **Product Details:**
   - Product name
   - Short description (< 200 chars)
   - Long description
   - Product logo (120x120, 180x180)
   - Screenshots (optional)

2. **Pricing:**
   - Free tier (recommended for adoption)
   - Usage-based pricing
   - Subscription pricing

3. **Support:**
   - Support email
   - Documentation URL
   - Terms of service

4. **Technical:**
   - Container image ARN
   - Port configuration
   - Environment variables
   - IAM permissions needed

### Step 6: Submit for Review

- AWS reviews listing (1-2 weeks)
- May request changes
- Once approved, listing goes live

---

## Pricing Strategy

### Option A: Usage-Based

**Model:** Pay per request/minute

**Example:**
- First 1,000 requests/month: Free
- $0.001 per request after free tier
- $0.01 per minute of active session

**Pros:**
- Low barrier to entry
- Scales with usage
- Attractive to enterprises

**Cons:**
- Revenue depends on adoption
- Harder to predict revenue

### Option B: Subscription

**Model:** Monthly flat fee

**Example:**
- Starter: $99/month (10K requests)
- Pro: $499/month (100K requests)
- Enterprise: Custom

**Pros:**
- Predictable revenue
- Simpler billing

**Cons:**
- Higher barrier to entry
- May limit experimentation

### Option C: Hybrid (Recommended)

**Model:** Free tier + usage-based + subscription discounts

**Example:**
- Free: 1,000 requests/month
- Pay-as-you-go: $0.001/request
- Pro subscription: $299/month (50K requests included, $0.0005/request after)
- Enterprise: Custom pricing

---

## ISV Accelerate Program

### What Is It?

AWS program providing co-sell support and benefits for ISVs with marketplace listings.

### Benefits

- Dedicated co-sell support
- AWS sales team collaboration
- MDF (Market Development Funds) - 50% more for Agentic AI
- Featured placement in marketplace
- Joint marketing opportunities

### Requirements

- SaaS solution running on or integrated with AWS
- Active marketplace listing
- Minimum revenue thresholds (varies)

### How to Apply

1. Complete marketplace listing
2. Apply via AWS Partner Central
3. AWS reviews and approves

---

## Listing Content Examples

### Product Name

**A2A Server:** Thenvoi Multi-Agent Orchestration
**MCP Server:** Thenvoi Orchestration Tools for AI Agents

### Short Description

**A2A Server:**
> Multi-agent orchestration platform with human-in-the-loop capabilities. Coordinate AI agents across frameworks with built-in supervisor patterns and approval workflows.

**MCP Server:**
> Add multi-agent orchestration to any AI agent. Tools for creating sessions, coordinating agents, and requesting human input.

### Long Description

> **Thenvoi Multi-Agent Orchestration** enables AI agents on Amazon Bedrock AgentCore to collaborate effectively. Whether you're building with LangGraph, CrewAI, Strands, or custom frameworks, Thenvoi provides the orchestration layer to coordinate complex multi-agent workflows.
>
> **Key Features:**
> - **Orchestration Patterns:** Built-in supervisor, collaborative, and hierarchical patterns
> - **Human-in-the-Loop:** Request human approval or input during agent workflows
> - **Cross-Framework:** Works with any AI framework deployed on AgentCore
> - **Real-Time Visibility:** Monitor agent conversations as they happen
> - **Session Management:** Persistent context across agent interactions
>
> **Use Cases:**
> - Complex analysis requiring multiple specialized agents
> - Workflows requiring human approval before execution
> - Cross-team agent collaboration
> - Customer support with escalation to human agents
>
> **Getting Started:**
> Deploy the Thenvoi A2A server to your AgentCore Runtime and start orchestrating agents immediately. Any agent can discover Thenvoi via the standard A2A Agent Card mechanism.

### Support Information

- **Documentation:** https://docs.thenvoi.com/agentcore
- **Support Email:** support@thenvoi.com
- **Community:** https://community.thenvoi.com

---

## Documentation Requirements

### User Guide

1. **Quick Start**
   - Deploy Thenvoi to AgentCore
   - Create first session
   - Connect agents

2. **Configuration**
   - Environment variables
   - Authentication setup
   - Customization options

3. **API Reference**
   - A2A endpoints
   - MCP tools
   - Response formats

4. **Examples**
   - Multi-agent analysis
   - Human approval workflow
   - Cross-framework coordination

### Architecture Guide

- How Thenvoi integrates with AgentCore
- Data flow diagrams
- Security architecture

---

## Post-Launch Activities

### Monitoring

- Track usage metrics
- Monitor error rates
- Gather customer feedback

### Updates

- Regular security patches
- Feature updates
- Version management

### Marketing

- Blog posts about integration
- Case studies
- Webinars with AWS

---

## Timeline Estimate

| Phase | Duration | Activities |
|-------|----------|------------|
| Seller Registration | 1-2 weeks | Register, complete tax docs |
| FTR | 2-4 weeks | Self-assessment, review, remediation |
| Container Prep | 1-2 weeks | Build, test, push to ECR |
| Listing Creation | 1 week | Content, pricing, configuration |
| AWS Review | 1-2 weeks | Review, feedback, approval |
| **Total** | **6-11 weeks** | End-to-end |

---

## Checklist

### Pre-Submission

- [ ] AWS account with Marketplace access
- [ ] Business registration complete
- [ ] Tax documentation submitted
- [ ] Bank account configured
- [ ] FTR completed

### Container

- [ ] ARM64 architecture
- [ ] Health check endpoint working
- [ ] Port configured correctly (8000/9000)
- [ ] No hardcoded secrets
- [ ] Tested locally
- [ ] Pushed to ECR

### Listing

- [ ] Product name finalized
- [ ] Descriptions written
- [ ] Logo uploaded (120x120, 180x180)
- [ ] Pricing configured
- [ ] Support information provided
- [ ] Documentation URL valid

### Post-Launch

- [ ] Monitoring configured
- [ ] Support process ready
- [ ] Marketing plan in place
- [ ] Feedback collection mechanism
