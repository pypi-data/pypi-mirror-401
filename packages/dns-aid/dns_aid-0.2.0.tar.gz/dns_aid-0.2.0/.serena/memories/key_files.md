# DNS-AID Key Files Reference

## Core Logic
| File | Purpose |
|------|---------|
| `src/dns_aid/core/models.py` | Pydantic models (AgentRecord, Protocol, PublishResult, etc.) |
| `src/dns_aid/core/publisher.py` | `publish()` function - publishes agents to DNS |
| `src/dns_aid/core/discoverer.py` | `discover()` function - discovers agents via DNS |
| `src/dns_aid/core/validator.py` | `verify()` function - DNSSEC/DANE validation, security scoring |

## DNS Backends
| File | Purpose |
|------|---------|
| `src/dns_aid/backends/base.py` | Abstract base class `DNSBackend` |
| `src/dns_aid/backends/route53.py` | AWS Route 53 backend |
| `src/dns_aid/backends/ddns.py` | RFC 2136 Dynamic DNS backend (BIND, PowerDNS, etc.) |
| `src/dns_aid/backends/infoblox/bloxone.py` | Infoblox BloxOne backend |
| `src/dns_aid/backends/infoblox/nios.py` | Infoblox NIOS backend |
| `src/dns_aid/backends/mock.py` | Mock backend for testing |

## User Interfaces
| File | Purpose |
|------|---------|
| `src/dns_aid/cli/main.py` | Typer CLI (publish, discover, verify, delete, list, zones) |
| `src/dns_aid/mcp/server.py` | MCP server for AI assistant integration |

## Utilities
| File | Purpose |
|------|---------|
| `src/dns_aid/utils/logging.py` | Structlog configuration |
| `src/dns_aid/utils/validation.py` | Input validation helpers |

## Public API
| File | Exports |
|------|---------|
| `src/dns_aid/__init__.py` | `publish`, `discover`, `verify`, `AgentRecord`, `Protocol` |

## Configuration
| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, dependencies, tool configs |
| `CLAUDE.md` | AI assistant instructions for this project |

## Tests
| Directory | Contents |
|-----------|----------|
| `tests/unit/` | Unit tests for models, backends, etc. |
| `tests/integration/` | Integration tests (DDNS with Docker BIND9) |
| `tests/integration/bind/` | Docker Compose setup for BIND9 testing |

## Documentation
| File | Purpose |
|------|---------|
| `docs/PLAN-v2-agent-directory.md` | v2 Agent Directory technical plan |
| `docs/v2-call-prep-agent-directory.md` | Stakeholder call prep document |
