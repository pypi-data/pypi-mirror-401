# DNS-AID

**DNS-based Agent Identification and Discovery**

Reference implementation for [IETF draft-mozleywilliams-dnsop-bandaid-02](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-bandaid/).

DNS-AID enables AI agents to discover each other via DNS, using the internet's existing naming infrastructure instead of centralized registries or hardcoded URLs.

> **New to DNS-AID?** Check out the [Getting Started Guide](docs/getting-started.md) for step-by-step setup and testing instructions.

## Quick Start

```bash
# Basic installation
pip install dns-aid

# With CLI support
pip install dns-aid[cli]

# With MCP server for AI agents
pip install dns-aid[mcp]

# With Route 53 backend
pip install dns-aid[route53]

# Everything
pip install dns-aid[all]
```

### Python Library

```python
import dns_aid

# Publish your agent to DNS
await dns_aid.publish(
    name="my-agent",
    domain="example.com",
    protocol="mcp",
    endpoint="agent.example.com",
    capabilities=["chat", "code-review"]
)

# Discover agents at a domain
agents = await dns_aid.discover("example.com")
for agent in agents:
    print(f"{agent.name}: {agent.endpoint_url}")

# Verify an agent's DNS records
result = await dns_aid.verify("_my-agent._mcp._agents.example.com")
print(f"Security Score: {result.security_score}/100")
```

## CLI Usage

```bash
# Publish an agent to DNS
dns-aid publish \
    --name my-agent \
    --domain example.com \
    --protocol mcp \
    --endpoint agent.example.com \
    --capability chat \
    --capability code-review

# Discover agents at a domain
dns-aid discover example.com

# Discover with filters
dns-aid discover example.com --protocol mcp --name chat

# Output as JSON
dns-aid discover example.com --json

# Verify DNS records
dns-aid verify _my-agent._mcp._agents.example.com

# List DNS-AID records in a zone
dns-aid list example.com

# List available zones (Route 53)
dns-aid zones

# Delete an agent
dns-aid delete --name my-agent --domain example.com --protocol mcp
```

## MCP Server

DNS-AID includes an MCP (Model Context Protocol) server that allows AI agents like Claude to publish and discover other agents.

### Running the MCP Server

```bash
# Run with stdio transport (default - for Claude Desktop, etc.)
dns-aid-mcp

# Run with HTTP transport
dns-aid-mcp --transport http --port 8000
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `publish_agent_to_dns` | Publish an AI agent to DNS using DNS-AID protocol |
| `discover_agents_via_dns` | Discover AI agents at a domain |
| `verify_agent_dns` | Verify DNS-AID records and security |
| `list_published_agents` | List all agents in a domain |
| `delete_agent_from_dns` | Remove an agent from DNS |

### Claude Desktop Integration

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dns-aid": {
      "command": "dns-aid-mcp"
    }
  }
}
```

Then Claude can discover and connect to AI agents:

> "Find available agents at example.com"
>
> "Publish my chat agent to DNS at mycompany.com"

## How It Works

DNS-AID uses SVCB records (RFC 9460) to advertise AI agents:

```
_chat._a2a._agents.example.com. 3600 IN SVCB 1 chat.example.com. alpn="a2a" port=443 mandatory="alpn,port"
_chat._a2a._agents.example.com. 3600 IN TXT "capabilities=chat,assistant" "version=1.0.0"
```

This allows any DNS client to discover agents without proprietary protocols or central registries.

### Discovery Flow

```
  Agent A                        DNS                           Agent B
     │                            │                               │
     │  "Find chat agent at       │                               │
     │   salesforce.com"          │                               │
     │                            │                               │
     ├───────────────────────────►│                               │
     │  Query: _chat._a2a._agents.salesforce.com SVCB             │
     │                            │                               │
     │◄───────────────────────────┤                               │
     │  Response: SVCB 1 chat.salesforce.com alpn="a2a" port=443 mandatory="alpn,port"
     │  (DNSSEC validated)        │                               │
     │                            │                               │
     ├────────────────────────────────────────────────────────────►│
     │  Connect to https://chat.salesforce.com:443                │
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        DNS-AID ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────────────┐
│   AI Agents     │     │   Developers    │     │   Infrastructure Ops    │
│  (Claude, etc.) │     │                 │     │                         │
└────────┬────────┘     └────────┬────────┘     └────────────┬────────────┘
         │                       │                           │
         │ MCP Protocol          │ CLI                       │ CLI / API
         ▼                       ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DNS-AID TOOLKIT                                 │
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────┐ │
│  │   MCP Server    │  │      CLI        │  │     Python Library      │ │
│  │                 │  │                 │  │                         │ │
│  │ • publish_agent │  │ • dns-aid       │  │ • dns_aid.publish()     │ │
│  │ • discover_     │  │   publish       │  │ • dns_aid.discover()    │ │
│  │   agents        │  │ • dns-aid       │  │ • dns_aid.verify()      │ │
│  │ • verify_agent  │  │   discover      │  │                         │ │
│  │ • list_agents   │  │ • dns-aid       │  │                         │ │
│  │                 │  │   verify        │  │                         │ │
│  └────────┬────────┘  └────────┬────────┘  └────────────┬────────────┘ │
│           │                    │                        │              │
│           └────────────────────┴────────────────────────┘              │
│                                │                                       │
│                                ▼                                       │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                        CORE ENGINE                              │  │
│  │                                                                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │  │
│  │  │  Publisher  │  │ Discoverer  │  │      Validator          │ │  │
│  │  │             │  │             │  │                         │ │  │
│  │  │ Create SVCB │  │ Query DNS   │  │ • DNSSEC validation     │ │  │
│  │  │ Create TXT  │  │ Parse SVCB  │  │ • DANE/TLSA check       │ │  │
│  │  │             │  │ Return      │  │ • Endpoint health       │ │  │
│  │  │             │  │ endpoints   │  │                         │ │  │
│  │  └──────┬──────┘  └──────┬──────┘  └────────────┬────────────┘ │  │
│  │         │                │                      │              │  │
│  └─────────┴────────────────┴──────────────────────┴──────────────┘  │
│                             │                                        │
└─────────────────────────────┼────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────────────────────────┐
│                          DNS BACKEND ABSTRACTION                                  │
│                                                                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐      │
│  │  Route53  │  │ Infoblox  │  │   DDNS    │  │Cloudflare │  │   Mock    │      │
│  │  (AWS)    │  │   UDDI    │  │ (RFC2136) │  │ (Planned) │  │ (Testing) │      │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘      │
│        │              │              │              │              │             │
└────────┴──────────────┴──────────────┴──────────────┴──────────────┴─────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       DNS INFRASTRUCTURE                                │
│                                                                         │
│   Authoritative DNS servers hosting _agents.{domain} zones              │
│   with SVCB, TXT, and TLSA records secured by DNSSEC                   │
└─────────────────────────────────────────────────────────────────────────┘
```

## Choosing the Right Interface

DNS-AID provides three interfaces. Choose based on your use case:

### Python Library

**Best for:** Application developers building agent discovery into their code.

```python
import dns_aid

# Integrate directly into your Python application
agents = await dns_aid.discover("example.com", protocol="mcp")
```

| Use Case | Example |
|----------|---------|
| Building an AI agent that discovers other agents | Agent mesh applications |
| Embedding discovery into existing Python apps | Adding DNS-AID to a Flask/FastAPI service |
| Automated pipelines and scripts | CI/CD, scheduled publishing |
| Unit testing with mock backend | Testing without real DNS |

### CLI Tool

**Best for:** Operators, DevOps, and quick manual operations.

```bash
dns-aid discover example.com --protocol mcp
```

| Use Case | Example |
|----------|---------|
| Manual publishing/discovery | Testing a new agent deployment |
| Shell scripts and automation | `cron` jobs, deployment scripts |
| Debugging and troubleshooting | Checking DNS records exist |
| Zone management | Listing agents, bulk operations |

### MCP Server

**Best for:** AI assistants (Claude, etc.) that need DNS-AID capabilities.

```bash
dns-aid-mcp  # Claude can now use DNS-AID tools
```

| Use Case | Example |
|----------|---------|
| Claude Desktop integration | "Find agents at salesforce.com" |
| AI-driven infrastructure | Agent self-registration and discovery |
| Natural language DNS management | "Publish my chat agent to DNS" |
| Building agentic workflows | Multi-agent orchestration |

### Decision Matrix

| You want to... | Use |
|----------------|-----|
| Build discovery into your Python app | **Python Library** |
| Run ad-hoc commands from terminal | **CLI** |
| Automate with shell scripts | **CLI** |
| Enable Claude/AI to manage DNS-AID | **MCP Server** |
| Test without real DNS | **Python Library** (with MockBackend) |
| Debug DNS record issues | **CLI** (`dns-aid verify`) |

## DNS Backends

DNS-AID supports multiple DNS backends:

| Backend | Description | Status |
|---------|-------------|--------|
| Route 53 | AWS Route 53 | ✅ Production |
| Infoblox UDDI | Infoblox Universal DDI (cloud) | ✅ Production |
| DDNS | RFC 2136 Dynamic DNS (BIND, etc.) | ✅ Production |
| Mock | In-memory (testing) | ✅ Production |
| NIOS | Infoblox NIOS (on-prem) | 🚧 Planned |
| Cloudflare | Cloudflare DNS | 🚧 Planned |

### Route 53 Setup

1. Configure AWS credentials:
   ```bash
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export AWS_DEFAULT_REGION="us-east-1"  # Optional
   ```

   Or use AWS CLI profiles:
   ```bash
   aws configure
   # Or use a named profile
   export AWS_PROFILE="my-profile"
   ```

2. Verify zone access:
   ```bash
   dns-aid zones
   ```

3. Publish your agent:
   ```bash
   dns-aid publish -n my-agent -d myzone.com -p mcp -e mcp.myzone.com
   ```

### Infoblox UDDI Setup

Infoblox UDDI (Universal DDI) is Infoblox's cloud-native DDI platform. DNS-AID supports creating SVCB and TXT records via the Infoblox API.

#### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `INFOBLOX_API_KEY` | Yes | - | Infoblox UDDI API key from Cloud Portal |
| `INFOBLOX_DNS_VIEW` | No | `default` | DNS view name (zones exist within views) |
| `INFOBLOX_BASE_URL` | No | `https://csp.infoblox.com` | API base URL |

#### Step-by-Step Setup

1. **Get your API key** from [Infoblox Cloud Portal](https://csp.infoblox.com):
   - Navigate to **Administration** → **API Keys**
   - Create a new API key with DNS permissions
   - Copy the key (shown only once)

2. **Configure environment variables**:
   ```bash
   export INFOBLOX_API_KEY="your-api-key"
   export INFOBLOX_DNS_VIEW="default"  # Or your specific view name
   ```

3. **Identify your zone and view**:
   - In Infoblox Portal, go to **DNS** → **Authoritative Zones**
   - Note the zone name (e.g., `example.com`) and which view it belongs to

4. **Use in Python**:
   ```python
   from dns_aid.backends.infoblox import InfobloxBloxOneBackend
   from dns_aid.core.publisher import set_default_backend
   from dns_aid import publish

   # Initialize backend (reads from environment variables)
   backend = InfobloxBloxOneBackend()

   # Or with explicit configuration
   backend = InfobloxBloxOneBackend(
       api_key="your-api-key",
       dns_view="default",  # Your DNS view name
   )

   set_default_backend(backend)

   await publish(
       name="my-agent",
       domain="example.com",
       protocol="mcp",
       endpoint="agent.example.com",
       capabilities=["chat", "code-review"]
   )
   ```

#### Infoblox UDDI Limitations & BANDAID Compliance

> **⚠️ Important**: Infoblox UDDI SVCB records only support "alias mode" (priority 0) and do not
> support SVC parameters (`alpn`, `port`, `mandatory`). This means **Infoblox UDDI is not fully
> compliant with the [BANDAID draft](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-bandaid/)**.
>
> The draft requires ServiceMode SVCB records (priority > 0) with mandatory `alpn` and `port`
> parameters. Infoblox UDDI's limitation is a platform constraint, not a DNS-AID limitation.

| BANDAID Requirement | Route 53 | Infoblox UDDI |
|---------------------|----------|---------------|
| ServiceMode (priority > 0) | ✅ | ❌ |
| `alpn` parameter | ✅ | ❌ |
| `port` parameter | ✅ | ❌ |
| `mandatory` key | ✅ | ❌ |

**For full BANDAID compliance, use Route 53 or another RFC 9460-compliant DNS provider.**

DNS-AID stores `alpn` and `port` in TXT records as a fallback for Infoblox UDDI, but this is
a workaround and not standard-compliant for agent discovery.

#### Verify Records via API

Since Infoblox UDDI zones may not be publicly resolvable, verify records via the API:

```python
async with InfobloxBloxOneBackend() as backend:
    async for record in backend.list_records("example.com", name_pattern="my-agent"):
        print(f"{record['type']}: {record['fqdn']}")
```

### DDNS Setup (RFC 2136)

DDNS (Dynamic DNS) is a universal backend that works with any DNS server supporting RFC 2136, including BIND9, Windows DNS, PowerDNS, and Knot DNS. This is ideal for on-premise DNS infrastructure without vendor-specific APIs.

#### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DDNS_SERVER` | Yes | - | DNS server hostname or IP |
| `DDNS_KEY_NAME` | Yes | - | TSIG key name |
| `DDNS_KEY_SECRET` | Yes | - | TSIG key secret (base64) |
| `DDNS_KEY_ALGORITHM` | No | `hmac-sha256` | TSIG algorithm |
| `DDNS_PORT` | No | `53` | DNS server port |

#### Step-by-Step Setup

1. **Create a TSIG key** on your DNS server (BIND example):
   ```bash
   tsig-keygen -a hmac-sha256 dns-aid-key > /etc/bind/dns-aid-key.conf
   ```

2. **Configure your zone** to allow updates with the key:
   ```
   zone "example.com" {
       type master;
       file "/var/lib/bind/example.com.zone";
       allow-update { key "dns-aid-key"; };
   };
   ```

3. **Configure DNS-AID**:
   ```bash
   export DDNS_SERVER="ns1.example.com"
   export DDNS_KEY_NAME="dns-aid-key"
   export DDNS_KEY_SECRET="your-base64-secret"
   ```

4. **Use in Python**:
   ```python
   from dns_aid.backends.ddns import DDNSBackend
   from dns_aid import publish

   backend = DDNSBackend()
   # Or with explicit configuration
   backend = DDNSBackend(
       server="ns1.example.com",
       key_name="dns-aid-key",
       key_secret="base64secret==",
       key_algorithm="hmac-sha256"
   )

   await publish(
       name="my-agent",
       domain="example.com",
       protocol="mcp",
       endpoint="agent.example.com",
       backend=backend
   )
   ```

#### DDNS Advantages

- **Universal**: Works with BIND, Windows DNS, PowerDNS, Knot, and any RFC 2136 server
- **No vendor lock-in**: Standard protocol, no proprietary APIs
- **On-premise friendly**: Perfect for enterprise internal DNS
- **Full BANDAID compliance**: Supports ServiceMode SVCB with all parameters

## Why DNS-AID?

### vs Competing Proposals

| Approach | Problem | DNS-AID Advantage |
|----------|---------|-------------------|
| **ANS (GoDaddy)** | Centralized registry, KYC required, single gatekeeper | Federated — you control your domain, publish instantly |
| **Google (A2A + UCP)** | Discovery via Gemini/Search, payments via UCP | Neutral discovery — no platform lock-in or transaction fees |
| **AgentDNS (China Telecom)** | Requires 6G infrastructure, carrier control | Works NOW on existing DNS infrastructure |
| **NANDA (MIT)** | New P2P overlay network, new ops paradigm | Uses infrastructure your DNS team already operates |
| **Web3 (ERC-8004)** | Gas fees, crypto wallets, enterprise-hostile | Free DNS queries, no blockchain complexity |
| **ai.txt / llms.txt** | No integrity verification, free-form JSON | DNSSEC cryptographic verification, structured SVCB |

### Feature Comparison

| Feature | DNS-AID | Central Registry | ai.txt |
|---------|---------|------------------|--------|
| **Decentralized** | ✅ | ❌ | ✅ |
| **Secure (DNSSEC)** | ✅ | Varies | ❌ |
| **Sovereign** | ✅ | ❌ | ✅ |
| **Standards-based** | ✅ (IETF) | ❌ | ❌ |
| **Works with existing infra** | ✅ | ❌ | ✅ |

### The Sovereignty Question

> **Who controls agent discovery?**
> - ANS: GoDaddy (US company as gatekeeper)
> - AgentDNS: China Telecom (state-owned carrier)
> - Web3: Ethereum Foundation
> - **DNS-AID: You control your own domain**
>
> DNS-AID preserves sovereignty. Organizations and nations maintain control over their own agent namespaces with no central authority that can block, censor, or surveil agent discovery.

### Google's Agent Ecosystem

Google is building a full-stack agent platform: **A2A** (communication), **UCP** (payments), and **Gemini/Search** (discovery). While A2A is an open protocol, discovery through Google surfaces means:
- Google controls visibility (pay-to-rank)
- Transaction fees via [UCP](https://developers.google.com/merchant/ucp)
- Platform dependency for reach

**DNS-AID complements A2A** by providing neutral, decentralized discovery — find agents anywhere, not just through Google.

## Examples

See the `examples/` directory:

- `demo_route53.py` - Basic Route 53 publish/discover
- `demo_full.py` - Complete end-to-end demonstration

```bash
# Run the full demo
export DNS_AID_TEST_ZONE="your-zone.com"
python examples/demo_full.py
```

## Development

```bash
# Clone the repo
git clone https://github.com/dns-aid/dns-aid
cd dns-aid

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[all]"

# Run tests
pytest

# Run with coverage
pytest --cov=dns_aid
```

## Related Standards

- [RFC 9460](https://www.rfc-editor.org/rfc/rfc9460.html) - SVCB and HTTPS Resource Records
- [RFC 4033-4035](https://www.rfc-editor.org/rfc/rfc4033.html) - DNSSEC
- [RFC 6698](https://www.rfc-editor.org/rfc/rfc6698.html) - DANE TLSA

## License

Apache 2.0

## Contributing

Contributions welcome! This project is intended for contribution to the Linux Foundation Agent AI Foundation.

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
