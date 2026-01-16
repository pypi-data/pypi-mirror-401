# Changelog

All notable changes to DNS-AID will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **DDNS Backend (RFC 2136)**
  - New `DDNSBackend` for universal DNS server support
  - Works with BIND9, Windows DNS, PowerDNS, Knot DNS, and any RFC 2136 compliant server
  - TSIG authentication support with multiple algorithms (hmac-sha256, sha384, sha512, sha224, md5)
  - Key file loading support (BIND key file format)
  - Full BANDAID compliance with ServiceMode SVCB records
  - Docker-based BIND9 integration tests
  - Documentation and examples for on-premise DNS deployments

## [0.2.0] - 2026-01-13

### Added
- **BANDAID Compliance**
  - Added `mandatory="alpn,port"` parameter to SVCB records per IETF draft
  - Ensures proper agent discovery signaling

- **Top-Level API Improvements**
  - Exported `unpublish()` and `delete()` (alias) to top-level API
  - Simpler imports: `from dns_aid import publish, unpublish, delete`

- **MCP E2E Test Script** (`scripts/test_mcp_e2e.py`)
  - Automated testing of all MCP tools via HTTP transport
  - Auto-start capability for MCP server
  - Full publish/discover/verify/list/delete cycle

- **Demo Guide** (`docs/demo-guide.md`)
  - Step-by-step demonstration guide for conferences
  - Quick Checklist for pre-demo verification
  - ngrok integration with `ngrok-skip-browser-warning` header
  - Python library E2E script example

- **Infoblox BloxOne Backend**
  - Full support for BloxOne Cloud API
  - DNS view configuration support
  - SVCB and TXT record creation/deletion
  - Zone listing and verification
  - Integration tests with real API

- **E2E Integration Tests** (`tests/integration/test_e2e.py`)
  - Full publish → discover → verify → delete workflow test
  - Multi-protocol discovery test (MCP + A2A)
  - Security scoring verification
  - Capabilities roundtrip test

- **Documentation**
  - CODE_OF_CONDUCT.md (Contributor Covenant 2.1)
  - Comprehensive Infoblox setup guide
  - Troubleshooting guide for both backends

### Changed
- Test suite expanded to 126 unit tests + 19 integration tests (from 108 in v0.1.0)

### Planned
- Cloudflare DNS backend
- Infoblox NIOS backend (on-prem)
- Agent capability negotiation
- Multi-region discovery

## [0.1.0] - 2026-01-13

### Added
- **Core Protocol Implementation**
  - SVCB record support per RFC 9460
  - TXT record metadata for capabilities and versioning
  - DNS-AID naming convention: `_{agent}._{protocol}._agents.{domain}`
  - Support for MCP (Model Context Protocol) and A2A (Agent-to-Agent) protocols

- **Python Library**
  - `publish()` - Publish agents to DNS
  - `discover()` - Discover agents at a domain
  - `verify()` - Verify DNS-AID records with security scoring
  - Pydantic models with full validation
  - Async/await throughout

- **CLI Interface** (`dns-aid`)
  - `dns-aid publish` - Publish agent records
  - `dns-aid discover` - Find agents at a domain
  - `dns-aid verify` - Check DNS record validity
  - `dns-aid list` - List all agents in a zone
  - `dns-aid delete` - Remove agent records
  - `dns-aid zones` - List available DNS zones
  - Rich terminal output with tables and colors

- **MCP Server** (`dns-aid-mcp`)
  - 5 MCP tools for AI agent integration
  - Stdio transport for Claude Desktop
  - HTTP transport with health endpoints
  - `/health`, `/ready`, `/` endpoints for orchestration

- **DNS Backends**
  - AWS Route 53 backend (production-ready)
  - Mock backend for testing

- **Security Features**
  - Comprehensive input validation (RFC 1035 compliant)
  - DNSSEC validation support
  - DANE/TLSA advisory checking
  - Security scoring (0-100) for agents
  - Default localhost binding for HTTP transport

- **Developer Experience**
  - Type hints throughout
  - Structured logging with structlog
  - Comprehensive test suite (108 tests)
  - GitHub Actions CI/CD pipeline
  - Docker support with multi-stage builds

### Security
- All inputs validated against DNS naming standards
- No hardcoded credentials
- Bandit security scanning in CI
- Dependency vulnerability checking with pip-audit

### Documentation
- Comprehensive README with examples
- Getting Started guide with AWS setup
- Security policy and vulnerability reporting
- Contributing guidelines

## References

- [IETF draft-mozleywilliams-dnsop-bandaid-02](https://datatracker.ietf.org/doc/draft-mozleywilliams-dnsop-bandaid/)
- [RFC 9460 - SVCB and HTTPS Resource Records](https://www.rfc-editor.org/rfc/rfc9460.html)
- [RFC 4033-4035 - DNSSEC](https://www.rfc-editor.org/rfc/rfc4033.html)

[Unreleased]: https://github.com/iracic82/dns-aid/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/iracic82/dns-aid/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/iracic82/dns-aid/releases/tag/v0.1.0
