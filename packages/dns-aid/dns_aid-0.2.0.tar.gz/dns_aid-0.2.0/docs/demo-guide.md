# DNS-AID Demo Guide

This guide walks through demonstrating DNS-AID's end-to-end agent discovery capabilities. Perfect for conference calls, IETF presentations, and Linux Foundation demos.

## Prerequisites

- DNS-AID installed: `pip install -e ".[all]"`
- AWS credentials configured (for Route 53)
- A running agent with A2A or MCP endpoint
- ngrok installed: `brew install ngrok` (for local agents)

## Quick Checklist Before Demo

Run these checks before starting your demo:

```bash
# 1. DNS-AID installed?
dns-aid --version
# Expected: dns-aid, version 0.2.0

# 2. AWS credentials configured?
aws sts get-caller-identity
# Expected: Account ID and ARN

# 3. Agent running?
curl http://localhost:8000/health
# Expected: {"status":"healthy",...}

# 4. ngrok configured?
ngrok config check
# Expected: Valid configuration at...
```

If any check fails, fix it before proceeding.

---

## Demo 1: Publish and Discover Your Agent

This demo shows the complete flow: publish an agent to DNS, discover it, verify it, and connect.

### Step 1: Start Your Agent

```bash
# Start your agent (example: multiagent platform on port 8000)
cd /path/to/your/agent
./start_http_servers.sh

# Verify it's running
curl http://localhost:8000/health
# Expected: {"status":"healthy",...}
```

### Step 2: Expose with ngrok (for local agents)

```bash
# Configure ngrok (first time only)
ngrok config add-authtoken YOUR_AUTHTOKEN

# Start tunnel
ngrok http 8000

# Note the public URL, e.g.:
# https://abc123.ngrok-free.app
```

### Step 3: Publish to DNS

DNS-AID supports two protocols: **A2A** (Google's Agent-to-Agent) and **MCP** (Anthropic's Model Context Protocol). This guide uses A2A for the full demo flow.

```bash
# Publish your agent to DNS via Route 53 (A2A protocol)
dns-aid publish \
  --name multiagent \
  --domain highvelocitynetworking.com \
  --protocol a2a \
  --endpoint abc123.ngrok-free.app \
  --port 443 \
  --capability ipam \
  --capability dns \
  --capability dhcp \
  --capability aws \
  --ttl 300

# Expected output:
# ✓ Agent published successfully!
#   FQDN: _multiagent._a2a._agents.highvelocitynetworking.com
#   Records created:
#     • SVCB _multiagent._a2a._agents.highvelocitynetworking.com  (alpn="a2a")
#     • TXT _multiagent._a2a._agents.highvelocitynetworking.com
```

> **Option B: MCP Protocol** — To publish an MCP agent instead, use `--protocol mcp`. The SVCB record will have `alpn="mcp"`. MCP agents use different connection patterns (see Demo 2, Option D for MCP server integration).

### Step 4: Verify DNS Records

```bash
# Using dig
dig _multiagent._a2a._agents.highvelocitynetworking.com SVCB +short
dig _multiagent._a2a._agents.highvelocitynetworking.com TXT +short

# Using DNS-AID verify (shows security score)
dns-aid verify _multiagent._a2a._agents.highvelocitynetworking.com

# Expected:
#   ✓ DNS record exists
#   ✓ SVCB record valid
#   ✗ DNSSEC validated (unless enabled)
#   ○ DANE/TLSA configured
#   ✓ Endpoint reachable
#   Security Score: 55/100 (Fair)
```

### Step 5: Discover via DNS

```bash
# Discover the agent
dns-aid discover highvelocitynetworking.com --protocol a2a --name multiagent

# Expected:
# ┌────────────┬──────────┬─────────────────────────┬──────────────────┐
# │ Name       │ Protocol │ Endpoint                │ Capabilities     │
# ├────────────┼──────────┼─────────────────────────┼──────────────────┤
# │ multiagent │ a2a      │ https://abc123.ngrok... │ ipam, dns, dhcp  │
# └────────────┴──────────┴─────────────────────────┴──────────────────┘
```

### Step 6: Connect to Discovered Agent

```bash
# Fetch the A2A agent card from discovered endpoint
# Note: ngrok free tier requires the skip-browser-warning header
curl -H "ngrok-skip-browser-warning: true" \
  https://abc123.ngrok-free.app/.well-known/agent.json | jq .

# Chat with the agent
curl -X POST https://abc123.ngrok-free.app/api/chat \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{"message": "List available tools", "agent": "main"}'
```

### Step 7: Cleanup

```bash
# Delete the DNS records when done
dns-aid delete \
  --name multiagent \
  --domain highvelocitynetworking.com \
  --protocol a2a \
  --force

# Stop ngrok
pkill ngrok
```

---

## Demo 2: Another Agent Discovers Your Agent

This demonstrates the real power of DNS-AID: **any agent anywhere can discover yours using only DNS**.

### Option A: Using Python

Create a file `discover_agent.py`:

```python
#!/usr/bin/env python3
"""
Example: Another agent discovers and connects to a DNS-AID published agent.
"""
import asyncio
import dns.resolver
import httpx


async def discover_and_connect():
    # === STEP 1: DNS Discovery ===
    print("🔍 Step 1: Querying DNS for agent...")

    fqdn = "_multiagent._a2a._agents.highvelocitynetworking.com"

    # Query SVCB record
    answers = dns.resolver.resolve(fqdn, "SVCB")

    for rdata in answers:
        target = str(rdata.target).rstrip(".")
        port_param = rdata.params.get(3)
        port = port_param.port if port_param else 443

        print(f"   Found: {target}:{port}")
        endpoint = f"https://{target}:{port}"

    # Query TXT for capabilities
    txt_answers = dns.resolver.resolve(fqdn, "TXT")
    capabilities = []
    for rdata in txt_answers:
        for txt in rdata.strings:
            txt_str = txt.decode()
            if txt_str.startswith("capabilities="):
                capabilities = txt_str.split("=")[1].split(",")

    print(f"   Capabilities: {capabilities}")

    # === STEP 2: Connect to Agent ===
    print(f"\n🔗 Step 2: Connecting to {endpoint}...")

    async with httpx.AsyncClient(timeout=30) as client:
        # Fetch A2A agent card
        resp = await client.get(f"{endpoint}/.well-known/agent.json")
        agent_card = resp.json()

        print(f"   Agent: {agent_card['name']}")
        print(f"   Version: {agent_card['version']}")
        print(f"   Skills: {[s['name'] for s in agent_card['skills']]}")

        # === STEP 3: Interact with Agent ===
        print(f"\n💬 Step 3: Sending request to agent...")

        resp = await client.post(
            f"{endpoint}/api/chat",
            json={
                "message": "What tools do you have for DNS management?",
                "agent": "network_specialist"
            }
        )

        result = resp.json()
        print(f"   Response: {result.get('response', result)[:200]}...")

    print("\n✅ Discovery and communication complete!")


if __name__ == "__main__":
    asyncio.run(discover_and_connect())
```

Run it:
```bash
python discover_agent.py
```

### Option B: Using DNS-AID Library

```python
#!/usr/bin/env python3
"""
Simpler version using dns_aid library directly.
"""
import asyncio
import httpx
import dns_aid


async def main():
    # Discover agent via DNS-AID
    print("🔍 Discovering agents at highvelocitynetworking.com...")
    result = await dns_aid.discover(
        "highvelocitynetworking.com",
        protocol="a2a",
        name="multiagent"
    )

    if not result.agents:
        print("No agents found!")
        return

    agent = result.agents[0]
    print(f"   Found: {agent.name} at {agent.endpoint_url}")
    print(f"   Capabilities: {agent.capabilities}")

    # Connect and interact
    print(f"\n🔗 Connecting to {agent.endpoint_url}...")
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{agent.endpoint_url}/.well-known/agent.json")
        card = resp.json()
        print(f"   Agent: {card['name']} v{card['version']}")
        print(f"   Tools: {sum(s['tools_count'] for s in card['skills'])} total")

    print("\n✅ Done!")


asyncio.run(main())
```

### Option C: Using curl (Shell Script)

```bash
#!/bin/bash
# discover_agent.sh - Discover and connect to a DNS-AID agent

DOMAIN="highvelocitynetworking.com"
AGENT_NAME="multiagent"
PROTOCOL="a2a"

echo "🔍 Step 1: DNS Discovery"
echo "========================"

# Query SVCB record
FQDN="_${AGENT_NAME}._${PROTOCOL}._agents.${DOMAIN}"
echo "Querying: $FQDN"

# Get the target from SVCB (using dig + parsing)
SVCB=$(dig $FQDN SVCB +short)
echo "SVCB Record: $SVCB"

# Extract target (second field after priority)
TARGET=$(echo $SVCB | awk '{print $2}' | sed 's/\.$//')
echo "Target: $TARGET"

# Get capabilities from TXT
echo ""
echo "Capabilities:"
dig $FQDN TXT +short

echo ""
echo "🔗 Step 2: Connect to Agent"
echo "==========================="

ENDPOINT="https://${TARGET}"
echo "Endpoint: $ENDPOINT"

# Fetch agent card (ngrok free tier needs this header)
echo ""
echo "Agent Card:"
curl -s -H "ngrok-skip-browser-warning: true" "$ENDPOINT/.well-known/agent.json" | jq '{name, version, skills: [.skills[].name]}'

# Check health
echo ""
echo "Health Status:"
curl -s -H "ngrok-skip-browser-warning: true" "$ENDPOINT/health" | jq .

echo ""
echo "✅ Discovery complete!"
```

### Option D: Using Claude Desktop (MCP)

If you have DNS-AID MCP server configured in Claude Desktop:

1. Start the MCP server:
   ```bash
   dns-aid-mcp
   ```

2. In Claude Desktop, ask:
   > "Discover agents at highvelocitynetworking.com using the a2a protocol"

3. Claude will use the `discover_agents_via_dns` tool and return the results.

4. Then ask:
   > "What capabilities does the multiagent have?"

### Option E: Programmatic MCP Testing

**IMPORTANT**: The MCP server supports two transport modes:

| Mode | Command | Use Case |
|------|---------|----------|
| **stdio** (default) | `dns-aid-mcp` | Claude Desktop integration |
| **http** | `dns-aid-mcp --transport http --port 8080` | Programmatic testing |

For automated testing, you MUST use HTTP transport:

```bash
# Terminal 1: Start MCP server with HTTP transport
dns-aid-mcp --transport http --port 8080

# Terminal 2: Run E2E test script
python scripts/test_mcp_e2e.py --endpoint YOUR_NGROK_URL --auto-start
```

The test script will:
1. Publish your agent to DNS via MCP
2. Discover it via DNS query
3. Verify the DNS records
4. List all published agents
5. Clean up (delete records)

Example with your agent:
```bash
# Start ngrok
ngrok http 8000

# Run MCP E2E test (with auto-start)
python scripts/test_mcp_e2e.py \
  --endpoint abc123.ngrok-free.app \
  --domain highvelocitynetworking.com \
  --agent-name multiagent \
  --protocol a2a \
  --auto-start
```

**Common MCP Issues:**

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server not running | Start with `--transport http` |
| 406 Not Acceptable | Missing Accept header | Use `Accept: application/json, text/event-stream` |
| Session errors | Missing session ID | Include `mcp-session-id` header from init response |

---

## Demo 3: Full E2E Test Script

Save this as `e2e_demo.py` for a complete automated demo:

```python
#!/usr/bin/env python3
"""
DNS-AID End-to-End Demo Script

Demonstrates the complete flow:
1. Publish agent to DNS
2. Verify DNS records
3. Discover agent via DNS
4. Connect to discovered endpoint
5. Cleanup
"""
import asyncio
import os
import sys

import dns.resolver
import httpx

import dns_aid
from dns_aid.backends import Route53Backend


async def run_demo():
    # Configuration
    DOMAIN = os.environ.get("DNS_AID_TEST_ZONE", "highvelocitynetworking.com")
    AGENT_NAME = "demo-agent"
    PROTOCOL = "a2a"
    ENDPOINT = os.environ.get("AGENT_ENDPOINT")  # e.g., abc123.ngrok-free.app

    if not ENDPOINT:
        print("❌ Set AGENT_ENDPOINT environment variable to your ngrok URL")
        print("   Example: export AGENT_ENDPOINT=abc123.ngrok-free.app")
        sys.exit(1)

    print("=" * 60)
    print("DNS-AID END-TO-END DEMO")
    print("=" * 60)

    # === STEP 1: PUBLISH ===
    print("\n📤 STEP 1: Publishing agent to DNS...")

    backend = Route53Backend()

    result = await dns_aid.publish(
        name=AGENT_NAME,
        domain=DOMAIN,
        protocol=PROTOCOL,
        endpoint=ENDPOINT,
        port=443,
        capabilities=["demo", "test"],
        ttl=300,
        backend=backend,
    )

    print(f"   ✓ Published: {result.agent.fqdn}")
    print(f"   ✓ Records: {result.records_created}")

    # === STEP 2: VERIFY DNS ===
    print("\n🔍 STEP 2: Verifying DNS records...")

    fqdn = f"_{AGENT_NAME}._{PROTOCOL}._agents.{DOMAIN}"

    # Direct DNS query
    try:
        svcb = dns.resolver.resolve(fqdn, "SVCB")
        print(f"   ✓ SVCB: {list(svcb)[0]}")
    except Exception as e:
        print(f"   ✗ SVCB query failed: {e}")

    try:
        txt = dns.resolver.resolve(fqdn, "TXT")
        for r in txt:
            print(f"   ✓ TXT: {r}")
    except Exception as e:
        print(f"   ✗ TXT query failed: {e}")

    # === STEP 3: VERIFY SECURITY ===
    print("\n🔒 STEP 3: Security verification...")

    verification = await dns_aid.verify(fqdn)
    print(f"   DNS exists: {'✓' if verification.record_exists else '✗'}")
    print(f"   SVCB valid: {'✓' if verification.svcb_valid else '✗'}")
    print(f"   DNSSEC: {'✓' if verification.dnssec_valid else '✗'}")
    print(f"   Endpoint: {'✓' if verification.endpoint_reachable else '✗'}")
    print(f"   Score: {verification.security_score}/100 ({verification.security_rating})")

    # === STEP 4: DISCOVER ===
    print("\n🌐 STEP 4: Discovering agent via DNS...")

    discovery = await dns_aid.discover(DOMAIN, protocol=PROTOCOL, name=AGENT_NAME)

    if discovery.agents:
        agent = discovery.agents[0]
        print(f"   ✓ Found: {agent.name}")
        print(f"   ✓ Endpoint: {agent.endpoint_url}")
        print(f"   ✓ Capabilities: {agent.capabilities}")
    else:
        print("   ✗ No agents found!")
        return

    # === STEP 5: CONNECT ===
    print("\n🔗 STEP 5: Connecting to discovered agent...")

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.get(f"{agent.endpoint_url}/health")
            health = resp.json()
            print(f"   ✓ Health: {health.get('status', 'unknown')}")

            resp = await client.get(f"{agent.endpoint_url}/.well-known/agent.json")
            card = resp.json()
            print(f"   ✓ Agent: {card['name']} v{card['version']}")
        except Exception as e:
            print(f"   ✗ Connection failed: {e}")

    # === STEP 6: CLEANUP ===
    print("\n🧹 STEP 6: Cleanup...")

    deleted = await dns_aid.delete(
        name=AGENT_NAME,
        domain=DOMAIN,
        protocol=PROTOCOL,
        backend=backend,
    )
    print(f"   {'✓' if deleted else '✗'} Records deleted")

    print("\n" + "=" * 60)
    print("✅ DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_demo())
```

Run the demo:
```bash
export AGENT_ENDPOINT=abc123.ngrok-free.app
python e2e_demo.py
```

---

## Conference Call Talking Points

### The Problem (30 seconds)
> "Today, AI agents have no standard way to discover each other. You either hardcode URLs, use central registries, or proprietary protocols. This limits interoperability and creates vendor lock-in."

### The Solution (30 seconds)
> "DNS-AID uses the internet's existing DNS infrastructure for agent discovery. Just like you find websites via DNS, agents find each other via DNS. No new protocols, no central registries, fully decentralized and secure with DNSSEC."

### Live Demo (2-3 minutes)
1. Show agent running locally
2. Publish to DNS with one command
3. Verify DNS records exist
4. Discover from "another location" (different terminal)
5. Connect to discovered agent
6. Show it's real HTTP traffic to real agent

### The Magic Moment
> "Notice we never hardcoded the URL. We asked DNS 'where is the multiagent at highvelocitynetworking.com?' and DNS told us. Any agent, anywhere in the world, can now discover this agent using standard DNS queries."

### Security (30 seconds)
> "DNS-AID supports DNSSEC for tamper-proof records and DANE for certificate binding. The verification shows a security score. Production deployments should enable DNSSEC for full security."

---

## Troubleshooting

### DNS records not appearing
- Wait 30-60 seconds for propagation
- Check Route 53 console directly
- Verify zone exists: `dns-aid zones`

### ngrok connection refused
- Ensure local agent is running on the correct port
- Check ngrok dashboard for tunnel status
- Try `curl http://localhost:8000/health` locally first

### DNSSEC shows as invalid
- Most domains don't have DNSSEC enabled by default
- Enable in Route 53: Domain → DNSSEC signing → Enable
- This is optional but recommended for production

### Endpoint unreachable during verify
- ngrok free tier may require browser confirmation
- Check if ngrok tunnel is still active
- Verify the agent is responding locally

### curl returns HTML instead of JSON (ngrok)
- ngrok free tier shows a browser warning page by default
- Add `-H "ngrok-skip-browser-warning: true"` to all curl commands
- Example: `curl -H "ngrok-skip-browser-warning: true" https://abc123.ngrok-free.app/health`
