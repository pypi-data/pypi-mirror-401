# Getting Started with DNS-AID

This guide will walk you through installing, configuring, and testing DNS-AID.

## Prerequisites

- Python 3.11 or higher
- One of the following DNS backends:
  - AWS account with Route 53 access
  - Infoblox UDDI account with API key
  - Any RFC 2136 compliant DNS server (BIND, Windows DNS, PowerDNS, etc.)
- A domain with a hosted zone in your DNS provider

## Installation

### Option 1: Install from source (recommended for testing)

```bash
# Clone the repository
git clone https://github.com/iracic82/dns-aid.git
cd dns-aid

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install with all dependencies
pip install -e ".[all]"
```

### Option 2: Install specific components

```bash
pip install -e "."           # Core library only
pip install -e ".[cli]"      # Core + CLI
pip install -e ".[mcp]"      # Core + MCP server
pip install -e ".[route53]"  # Core + Route 53 backend
```

## Quick Test (No AWS needed)

Test with the mock backend:

```bash
# Run unit tests
pytest tests/unit/ -v

# Test CLI help
dns-aid --help

# Test MCP server help
dns-aid-mcp --help
```

## AWS Route 53 Setup

### 1. Configure AWS Credentials

```bash
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

Or use AWS CLI:
```bash
aws configure
```

### 2. Verify Zone Access

```bash
dns-aid zones
```

Expected output:
```
Available DNS zones (route53):

┌─────────────────────────────┬────────────────┬─────────┬────────┐
│ Domain                      │ Zone ID        │ Records │ Type   │
├─────────────────────────────┼────────────────┼─────────┼────────┤
│ yourdomain.com              │ Z1234567890ABC │ 5       │ Public │
└─────────────────────────────┴────────────────┴─────────┴────────┘
```

### 3. Set Test Zone

```bash
export DNS_AID_TEST_ZONE="yourdomain.com"
```

## Infoblox UDDI Setup

Infoblox UDDI is Infoblox's cloud-native DDI platform. Follow these steps to configure DNS-AID with Infoblox UDDI.

### 1. Get Your API Key

1. Log in to [Infoblox Cloud Portal](https://csp.infoblox.com)
2. Navigate to **Administration** → **API Keys**
3. Click **Create API Key**
4. Select appropriate permissions (DNS read/write)
5. Copy the API key (it's only shown once!)

### 2. Configure Environment Variables

```bash
# Required: Your Infoblox UDDI API key
export INFOBLOX_API_KEY="your-api-key-here"

# Optional: DNS view name (default: "default")
export INFOBLOX_DNS_VIEW="default"

# Optional: Custom API URL (rarely needed)
# export INFOBLOX_BASE_URL="https://csp.infoblox.com"
```

### 3. Identify Your Zone and View

In the Infoblox Portal:
1. Go to **DNS** → **Authoritative Zones**
2. Find your zone (e.g., `example.com`)
3. Note which **DNS View** it belongs to (visible in the zone details)

> **Important**: Zones exist within DNS Views. If your zone is in a view other than
> "default", you must set `INFOBLOX_DNS_VIEW` to match.

### 4. Set Test Zone

```bash
export INFOBLOX_TEST_ZONE="your-zone.com"
```

### 5. Verify Connection (Python)

```python
import asyncio
from dns_aid.backends.infoblox import InfobloxBloxOneBackend

async def verify_connection():
    backend = InfobloxBloxOneBackend()

    # List zones to verify API access
    zones = await backend.list_zones()
    print(f"Found {len(zones)} zones:")
    for zone in zones[:5]:  # Show first 5
        print(f"  - {zone['name']}")

    # Check if your test zone exists
    exists = await backend.zone_exists("your-zone.com")
    print(f"\nTest zone exists: {exists}")

    await backend.close()

asyncio.run(verify_connection())
```

### Infoblox UDDI Limitations & BANDAID Compliance

> **⚠️ Important**: Infoblox UDDI is **not fully compliant** with the
> [BANDAID draft](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-bandaid/).
>
> Infoblox UDDI SVCB only supports "alias mode" (priority 0) and lacks support for required
> SVC parameters (`alpn`, `port`, `mandatory`). The BANDAID draft requires ServiceMode
> SVCB records (priority > 0) with these parameters.
>
> **For full compliance, use Route 53 or another RFC 9460-compliant provider.**
>
> DNS-AID stores `alpn` and `port` in TXT records as a fallback, but this is a
> workaround, not a standard-compliant solution.

### Verifying Records

Since Infoblox UDDI zones may be private (not publicly resolvable), verify records via API instead of `dig`:

```python
async with InfobloxBloxOneBackend() as backend:
    async for record in backend.list_records("your-zone.com"):
        if "_agents" in record["fqdn"]:
            print(f"{record['type']}: {record['fqdn']}")
```

## DDNS Setup (RFC 2136)

DDNS (Dynamic DNS) works with any DNS server supporting RFC 2136, including BIND9, Windows DNS, PowerDNS, and Knot DNS. This is ideal for on-premise infrastructure without vendor-specific APIs.

### 1. Create a TSIG Key

On your DNS server (BIND9 example):

```bash
# Generate a TSIG key
tsig-keygen -a hmac-sha256 dns-aid-key > /etc/bind/dns-aid-key.conf
```

This creates a key file like:
```
key "dns-aid-key" {
    algorithm hmac-sha256;
    secret "YourBase64SecretHere==";
};
```

### 2. Configure Your DNS Zone

Add the key to your zone configuration:

```
include "/etc/bind/dns-aid-key.conf";

zone "example.com" {
    type master;
    file "/var/lib/bind/example.com.zone";
    allow-update { key "dns-aid-key"; };
};
```

### 3. Configure Environment Variables

```bash
# Required
export DDNS_SERVER="ns1.example.com"
export DDNS_KEY_NAME="dns-aid-key"
export DDNS_KEY_SECRET="YourBase64SecretHere=="

# Optional
export DDNS_KEY_ALGORITHM="hmac-sha256"  # default
export DDNS_PORT="53"                     # default
```

### 4. Set Test Zone

```bash
export DNS_AID_TEST_ZONE="example.com"
```

### 5. Verify Connection (Python)

```python
import asyncio
from dns_aid.backends.ddns import DDNSBackend

async def verify_connection():
    backend = DDNSBackend()

    # Check if zone exists
    exists = await backend.zone_exists("example.com")
    print(f"Zone exists: {exists}")

asyncio.run(verify_connection())
```

### DDNS Advantages

- **Universal**: Works with BIND, Windows DNS, PowerDNS, Knot, and any RFC 2136 server
- **Full BANDAID compliance**: Supports ServiceMode SVCB with all parameters
- **No vendor lock-in**: Standard protocol, no proprietary APIs
- **On-premise friendly**: Perfect for enterprise internal DNS

### DDNS Troubleshooting

#### "TSIG key not configured" error
- Ensure `DDNS_KEY_NAME` and `DDNS_KEY_SECRET` are set
- Check the key secret is base64 encoded

#### "DDNS update failed: NOTAUTH"
- The zone doesn't permit updates with your key
- Check `allow-update` in your zone configuration

#### "DDNS update failed: REFUSED"
- DNS server refused the update
- Verify TSIG key name and secret match the server configuration

#### Connection timeout
- Check firewall rules allow TCP/UDP port 53 (or your configured port)
- Verify the DNS server is reachable: `dig @ns1.example.com example.com SOA`

## End-to-End Test

### Step 1: Publish an Agent

```bash
dns-aid publish \
  --name test-agent \
  --domain $DNS_AID_TEST_ZONE \
  --protocol mcp \
  --endpoint mcp.$DNS_AID_TEST_ZONE \
  --capability demo \
  --capability test \
  --ttl 300
```

Expected output:
```
Publishing agent to DNS...

✓ Agent published successfully!

  FQDN: _test-agent._mcp._agents.yourdomain.com
  Endpoint: https://mcp.yourdomain.com:443

  Records created:
    • SVCB _test-agent._mcp._agents.yourdomain.com
    • TXT _test-agent._mcp._agents.yourdomain.com

Verify with:
  dig _test-agent._mcp._agents.yourdomain.com SVCB
  dig _test-agent._mcp._agents.yourdomain.com TXT
```

### Step 2: Verify DNS Records

```bash
# Using DNS-AID
dns-aid verify _test-agent._mcp._agents.$DNS_AID_TEST_ZONE

# Using dig (external verification)
dig _test-agent._mcp._agents.$DNS_AID_TEST_ZONE SVCB +short
dig _test-agent._mcp._agents.$DNS_AID_TEST_ZONE TXT +short
```

### Step 3: Discover Agents

```bash
dns-aid discover $DNS_AID_TEST_ZONE
```

Expected output:
```
Discovering agents at yourdomain.com...

Found 1 agent(s) at yourdomain.com:

┌────────────┬──────────┬────────────────────────────────┬─────────────┐
│ Name       │ Protocol │ Endpoint                       │ Capabilities│
├────────────┼──────────┼────────────────────────────────┼─────────────┤
│ test-agent │ mcp      │ https://mcp.yourdomain.com:443 │ demo, test  │
└────────────┴──────────┴────────────────────────────────┴─────────────┘
```

### Step 4: List All Records

```bash
dns-aid list $DNS_AID_TEST_ZONE
```

### Step 5: Clean Up

```bash
dns-aid delete --name test-agent --domain $DNS_AID_TEST_ZONE --protocol mcp --force
```

## Using the Python Library

```python
import asyncio
from dns_aid import publish, discover, verify

async def main():
    # Publish an agent
    result = await publish(
        name="my-agent",
        domain="yourdomain.com",
        protocol="mcp",
        endpoint="mcp.yourdomain.com",
        capabilities=["chat", "code-review"],
    )
    print(f"Published: {result.agent.fqdn}")

    # Discover agents
    discovery = await discover("yourdomain.com")
    for agent in discovery.agents:
        print(f"Found: {agent.name} at {agent.endpoint_url}")

    # Verify an agent
    verification = await verify("_my-agent._mcp._agents.yourdomain.com")
    print(f"Security Score: {verification.security_score}/100")

asyncio.run(main())
```

## Using the MCP Server

### Start the Server

```bash
# Stdio transport (for Claude Desktop)
dns-aid-mcp

# HTTP transport (for remote access)
dns-aid-mcp --transport http --port 8000
```

### Test Health Endpoints (HTTP mode)

```bash
# Start server in background
dns-aid-mcp --transport http --port 8000 &

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl http://localhost:8000/
```

### Claude Desktop Integration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dns-aid": {
      "command": "dns-aid-mcp"
    }
  }
}
```

Restart Claude Desktop, then ask:
- "Discover agents at example.com"
- "Publish my agent to DNS"

## Running the Full Demo

```bash
# Set your zone
export DNS_AID_TEST_ZONE="yourdomain.com"

# Run interactive demo
python examples/demo_full.py
```

## Troubleshooting

### Route 53 Issues

#### "Zone not found" error
- Verify AWS credentials: `aws sts get-caller-identity`
- Check zone exists: `dns-aid zones`
- Ensure correct region: `export AWS_DEFAULT_REGION=us-east-1`

#### DNS records not appearing
- Wait for propagation (up to 60 seconds for Route 53)
- Check TTL settings
- Verify with `dig` directly

### Infoblox UDDI Issues

#### "No zone found for domain" error
- Verify `INFOBLOX_DNS_VIEW` matches your zone's view
- Check zone name spelling (with or without trailing dot)
- Ensure API key has DNS permissions

#### "401 Unauthorized" error
- Regenerate your API key in the Cloud Portal
- Ensure the key hasn't expired
- Check `INFOBLOX_API_KEY` is set correctly

#### "400 Bad Request" on zone lookup
- The DNS view name may be incorrect
- Check available views in the Infoblox Portal under DNS → Views

#### Records created but can't dig them
- Infoblox UDDI zones may be private (not publicly resolvable)
- Verify records via API instead:
  ```python
  async for rec in backend.list_records("zone.com"):
      print(rec)
  ```

### MCP Server Issues

#### MCP server not connecting
- Check if server is running: `ps aux | grep dns-aid-mcp`
- Test health endpoint: `curl http://localhost:8000/health`
- Check Claude Desktop logs

## Next Steps

- Read the [API Reference](api-reference.md)
- Explore [examples/](../examples/)
- Review the [IETF draft specification](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-bandaid/)
