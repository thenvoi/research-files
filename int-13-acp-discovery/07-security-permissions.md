# Security & Permissions Analysis

**Status:** Complete
**Last Updated:** 2026-01-06

## Summary

ACP employs process-level isolation as its primary security boundary, running agents as separate subprocesses with communication over stdio. The permission model is user-consent based, with agents requesting permission via `session/request_permission` before sensitive operations. Authentication is currently handled out-of-band (API keys in environment variables), with a draft RFD proposing standardized auth declaration. For Thenvoi, the key considerations are credential management, permission mapping, and enterprise security requirements.

## Key Findings

### 1. Process Isolation Model

ACP's security architecture relies on OS process isolation:

```
┌─────────────────────────────────────┐
│         Editor Process              │
│  (ACP Client - full trust)          │
└─────────────────┬───────────────────┘
                  │ stdio (controlled channel)
┌─────────────────▼───────────────────┐
│        Agent Process                │
│  (ACP Server - sandboxed)           │
│  - No direct filesystem access      │
│  - No network except via MCP        │
│  - Must request permissions         │
└─────────────────────────────────────┘
```

**Security Properties:**
| Property | Status | Notes |
|----------|--------|-------|
| Process isolation | ✅ | Separate process per agent |
| Memory isolation | ✅ | OS-level isolation |
| Filesystem isolation | ⚠️ | Agent can request access |
| Network isolation | ⚠️ | Can call MCP servers |
| Credential isolation | ⚠️ | Env vars visible to agent |

> "Process-level isolation provides strong security boundaries but limits some interaction patterns." - [ACP Documentation](https://agentclientprotocol.com/)

**Confidence:** High (protocol design)

### 2. Permission Model

ACP uses an explicit permission request model:

**Permission Request Flow:**
```
Agent                           Client (Editor)
  │                                  │
  │ session/request_permission       │
  │ ─────────────────────────────────▶ User sees prompt
  │                                  │
  │          User approves/denies    │
  │ ◀───────────────────────────────  │
  │                                  │
```

**Permission Request Example:**
```json
{
  "method": "session/request_permission",
  "params": {
    "type": "filesystem",
    "operation": "write",
    "path": "/path/to/file.py",
    "description": "Write updated code to file"
  }
}
```

**Permission Types:**
| Type | Operations | User Prompt |
|------|-----------|-------------|
| `filesystem` | read, write, delete | "Allow access to file?" |
| `terminal` | execute, kill | "Allow command execution?" |
| `network` | fetch, post | "Allow network request?" |
| `sensitive` | custom | "Allow sensitive operation?" |

**Confidence:** High (protocol specification)

### 3. Authentication Patterns

**Current State:** Authentication is handled out-of-band:

```json
{
  "agent_servers": {
    "My Agent": {
      "env": {
        "API_KEY": "sk-...",  // Exposed in config
        "OPENAI_API_KEY": "sk-..."
      }
    }
  }
}
```

**Issues:**
- API keys stored in plain text config
- No credential rotation
- No OAuth flow support
- No secure credential storage

**Authentication RFD (#330):**
> "Define a way for an agent to declare different ways to authenticate, this will allow clients to present better UX to users."

**Proposed Authentication Methods:**
- API key (header/query)
- OAuth 2.0 flows
- Token refresh
- Multi-factor (future)

**Confidence:** High (GitHub RFD #330)

### 4. Client-Side Security Controls

The editor (ACP client) maintains control through:

**1. Permission Gating:**
> "The client maintains control over actions the agent can perform by asking the user for permission before executing any tool calls."

**2. Capability Negotiation:**
```json
{
  "method": "initialize",
  "params": {
    "capabilities": {
      "filesystem": {
        "read": true,
        "write": false  // Disable writes
      },
      "terminal": false  // No terminal access
    }
  }
}
```

**3. Operation Auditing:**
- Editors can log all operations
- ACP logs viewable in Zed (`dev: open acp logs`)
- No standardized audit format

**Confidence:** High (protocol specification)

### 5. MCP Security Integration

When agents use MCP tools, additional security applies:

**MCP Credential Flow:**
```
Editor → (MCP credentials) → Agent → MCP Server → External Service
```

**Security Considerations:**
- Editor controls which MCP servers agent can access
- Agent receives credentials for MCP servers
- Tool calls may require user permission
- MCP servers can have their own auth

**Confidence:** High (MCP integration analysis)

### 6. Remote Agent Security (Draft)

Remote agents (HTTP/WebSocket) have different security model:

**Draft Considerations:**
- TLS for transport security
- Token-based authentication
- Rate limiting
- Tenant isolation

**Status:** Still in development, no final specification.

**Confidence:** Medium (RFD stage)

## Community Signals

### Security Concerns Raised

1. **Credential exposure** - API keys in config files
2. **Permission fatigue** - Too many prompts
3. **Trust model** - Who verifies agents?
4. **Audit gaps** - No standardized logging
5. **Enterprise needs** - SSO, compliance features missing

### Security RFDs in Progress

| RFD | Topic | Status |
|-----|-------|--------|
| #330 | Authentication | Draft |
| #340 | Agent-guided Selection | Draft |
| - | Proxy Chains | Draft |
| - | Telemetry Export | Draft |

## Gaps Identified

### Protocol Gaps

1. **No agent verification** - Cannot verify agent authenticity
2. **No credential encryption** - Plain text API keys
3. **No audit standard** - Each editor logs differently
4. **No revocation** - Cannot revoke agent access remotely
5. **No role-based access** - All or nothing permissions

### Enterprise Gaps

1. **No SSO support** - Enterprise auth not supported
2. **No compliance features** - No SOC2, GDPR tooling
3. **No admin controls** - Cannot manage org-wide
4. **No secret management** - No vault integration
5. **No network policies** - Cannot restrict agent network

### Implementation Gaps

1. **Permission UX** - Users click "allow" without reading
2. **Scope granularity** - Cannot limit to specific paths
3. **Time-based access** - No expiring permissions
4. **Audit trail** - No standardized format

## Implications for Thenvoi

### Security Advantages

Thenvoi can provide enhanced security through:

**1. Server-Side Authentication**
```
User → Editor → Thenvoi ACP → [Auth Layer] → Platform
                                    │
                                    └── API Key validation
                                        Rate limiting
                                        Tenant isolation
```

**2. Centralized Permission Management**
- Define permissions in Thenvoi dashboard
- Sync to ACP agent
- Audit trail in platform
- Admin controls for orgs

**3. Enterprise Features**
| Feature | ACP Native | Thenvoi Can Add |
|---------|-----------|-----------------|
| SSO | ❌ | ✅ |
| RBAC | ❌ | ✅ |
| Audit logs | ⚠️ | ✅ |
| Compliance | ❌ | ✅ |
| Secret management | ❌ | ✅ |

### Security Implementation

**1. Credential Management**
```python
class ThenvoiACPAgent:
    def __init__(self):
        # Don't store API key in config
        # Use secure credential flow
        self.auth = SecureAuthProvider()

    async def authenticate(self):
        # OAuth flow or token refresh
        token = await self.auth.get_token()
        self.client = EnvoiClient(token=token)
```

**2. Permission Mapping**
```python
# Map ACP permissions to Thenvoi permissions
PERMISSION_MAP = {
    'filesystem:read': 'tools.filesystem.read',
    'filesystem:write': 'tools.filesystem.write',
    'terminal:execute': 'tools.terminal.execute',
}

async def handle_permission_request(self, request):
    acp_permission = request.params.type
    thenvoi_permission = PERMISSION_MAP.get(acp_permission)

    # Check Thenvoi permission
    allowed = await self.client.permissions.check(thenvoi_permission)

    if allowed:
        return PermissionResponse(granted=True)
    else:
        # Escalate to user
        return PermissionResponse(granted=False, reason='Org policy')
```

**3. Audit Integration**
```python
async def handle_prompt(self, request):
    # Log all prompts for audit
    await self.client.audit.log({
        'action': 'prompt',
        'session_id': request.params.sessionId,
        'user': self.current_user,
        'timestamp': datetime.now(),
        'content_hash': hash(request.params.prompt)
    })

    # Process prompt
    response = await self.process_prompt(request)

    # Log response
    await self.client.audit.log({
        'action': 'response',
        'session_id': request.params.sessionId,
        'latency_ms': response.latency
    })

    return response
```

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| API key exposure | OAuth flow, token refresh |
| Permission bypass | Server-side validation |
| Audit gaps | Centralized logging |
| Compliance | Platform handles compliance |
| Credential rotation | Automatic token refresh |

### Recommended Security Investments

| Priority | Investment | Rationale |
|----------|-----------|-----------|
| P0 | OAuth/token flow | Replace API keys |
| P0 | Server-side permission checks | Defense in depth |
| P1 | Audit logging | Compliance requirement |
| P1 | Rate limiting | Abuse prevention |
| P2 | SSO integration | Enterprise requirement |
| P2 | RBAC | Multi-user orgs |

## Sources Consulted

- [x] [ACP Protocol Overview](https://agentclientprotocol.com/overview/introduction) - Security model
- [x] [ACP Authentication RFD #330](https://github.com/agentclientprotocol/agent-client-protocol/pull/330) - Auth proposals
- [x] [Zed External Agents](https://zed.dev/docs/ai/external-agents) - Client security
- [x] [AI SDK ACP Provider](https://ai-sdk.dev/providers/community-providers/acp) - Implementation patterns
- [x] ACP Schema - Permission types

## Related Research Files

- [01-acp-architecture.md](./01-acp-architecture.md) - Protocol foundation
- [02-acp-mcp-integration.md](./02-acp-mcp-integration.md) - MCP security
- [05-thenvoi-as-acp-agent.md](./05-thenvoi-as-acp-agent.md) - Implementation
