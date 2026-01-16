# DNS-AID Project Overview

## Purpose
DNS-AID (DNS-based Agent Identification and Discovery) is a reference implementation for the IETF draft-mozleywilliams-dnsop-bandaid-02 protocol. It enables AI agents to discover each other via DNS instead of hardcoded URLs or central registries.

## Mission
"Rapidly build a working prototype with automated tooling that integrates into existing AI workflow to demonstrate to the AI developers and IETF that DNS-AID is easy and it works now."

## What It Does
- **Publish** agent identities to DNS (SVCB + TXT records)
- **Discover** agents by querying DNS
- **Verify** agent security (DNSSEC, DANE, TLS)

## DNS Record Format
```
# SVCB Record (Service Binding)
_{agent-name}._{protocol}._agents.{domain}. SVCB 1 {target}. alpn="{protocol}" port={port}

# TXT Record (Capabilities)
_{agent-name}._{protocol}._agents.{domain}. TXT "capabilities={list}" "version={ver}"
```

## Supported Protocols
- `mcp` - Model Context Protocol (Anthropic)
- `a2a` - Agent-to-Agent (Google)
- `https` - Standard HTTPS

## Tech Stack
- **Language**: Python 3.11+
- **Build**: Hatchling
- **DNS**: dnspython
- **Validation**: Pydantic
- **HTTP**: httpx
- **Logging**: structlog
- **CLI**: Typer + Rich
- **MCP Server**: mcp library + uvicorn
- **Testing**: pytest + pytest-asyncio
- **Linting**: ruff
- **Type Checking**: mypy

## Project Structure
```
DNS-AID/
├── src/dns_aid/
│   ├── core/           # Core logic (publisher, discoverer, validator, models)
│   ├── backends/       # DNS providers (route53, infoblox, ddns, mock)
│   ├── cli/            # Command-line interface (Typer)
│   ├── mcp/            # MCP server for AI integration
│   └── utils/          # Logging, validation helpers
├── tests/              # Unit and integration tests
├── examples/           # Usage examples
├── docs/               # Documentation
└── scripts/            # Helper scripts
```

## Key Entry Points
- `dns-aid` - CLI tool
- `dns-aid-mcp` - MCP server
- `dns_aid.publish()` - Library function
- `dns_aid.discover()` - Library function
- `dns_aid.verify()` - Library function
