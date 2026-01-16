# DNS-AID v2.0 Plan: The Agent Directory

> "Building the Google of Agents/MCPs"

**Status:** PLANNING
**Author:** DNS-AID Team
**Date:** 2026-01-13
**Version:** Draft 0.1

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Vision & Goals](#2-vision--goals)
3. [Architecture Overview](#3-architecture-overview)
4. [Component Deep Dives](#4-component-deep-dives)
5. [Data Models](#5-data-models)
6. [API Specifications](#6-api-specifications)
7. [Implementation Phases](#7-implementation-phases)
8. [Open Questions for Stakeholders](#8-open-questions-for-stakeholders)
9. [Risk Assessment](#9-risk-assessment)
10. [Success Metrics](#10-success-metrics)

---

## 1. Executive Summary

### The Problem

DNS-AID v1.x solves **publishing** and **single-domain discovery**:
- ✅ Organizations can publish their agents to DNS
- ✅ Clients can discover agents at a known domain
- ❌ No way to search "find me a CRM agent" across ALL domains
- ❌ No incentive for organizations to adopt (no visibility benefit)

### The Solution

DNS-AID v2.0 adds an **Agent Directory** - a decentralized-friendly search engine that:
1. **Crawls** DNS-AID compliant domains using multiple discovery methods
2. **Indexes** agent metadata, capabilities, and security posture
3. **Ranks** agents by relevance, trust, and quality
4. **Provides** a searchable API and web interface

### Value Proposition

| Stakeholder | Current State | With Agent Directory |
|-------------|---------------|----------------------|
| **Agent Publishers** | "We published, but who finds us?" | Listed in searchable directory, discoverable globally |
| **Agent Consumers** | "I need a CRM agent... where?" | Search by capability, protocol, trust level |
| **Enterprises** | "Why adopt DNS-AID?" | Visibility, discoverability, competitive advantage |
| **Ecosystem** | Fragmented, no discovery | Unified, searchable agent web |

---

## 2. Vision & Goals

### Vision Statement

> Make every AI agent on the internet discoverable through a single search, while preserving the decentralized, sovereign nature of DNS-AID.

### Goals

#### G1: Discoverability
- Any DNS-AID published agent should be findable via search
- Support natural language queries ("agents that can analyze financial data")
- Support structured queries (protocol=mcp, capability=crm)

#### G2: Trust & Ranking
- Agents ranked by security posture (DNSSEC, DANE, TLS)
- Agents ranked by reliability (uptime, response time)
- Agents ranked by community signals (usage, ratings)

#### G3: Decentralization Preservation
- Source of truth remains DNS (not our database)
- Multiple directory operators can exist (like search engines)
- Organizations retain full control over their agents

#### G4: Adoption Incentive
- "Easy Button" tools reduce publishing friction
- Directory listing provides visibility incentive
- Security badges reward best practices

### Non-Goals (v2.0)

- ❌ Agent marketplace / payments
- ❌ Agent execution / proxy
- ❌ Identity federation beyond DNS
- ❌ Real-time agent communication

---

## 3. Architecture Overview

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           DNS-AID v2.0 ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                              THE INTERNET                                        │
│    ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│    │ Org A   │  │ Org B   │  │ Org C   │  │ Org D   │  │ Org ... │             │
│    │ DNS     │  │ DNS     │  │ DNS     │  │ DNS     │  │ DNS     │             │
│    │ Zone    │  │ Zone    │  │ Zone    │  │ Zone    │  │ Zone    │             │
│    └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘             │
│         │            │            │            │            │                    │
│         └────────────┴─────┬──────┴────────────┴────────────┘                    │
│                            │                                                     │
│  ┌─────────────────────────┼─────────────────────────────────────────────────┐  │
│  │                         ▼           DISCOVERY ENGINE                       │  │
│  │  ┌──────────────────────────────────────────────────────────────────────┐ │  │
│  │  │                        CRAWLER FLEET                                  │ │  │
│  │  │                                                                       │ │  │
│  │  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐    │ │  │
│  │  │  │   Domain    │ │    NSEC     │ │     CT      │ │   Index     │    │ │  │
│  │  │  │ Submission  │ │   Zone      │ │    Log      │ │   Entry     │    │ │  │
│  │  │  │   Queue     │ │   Walker    │ │  Monitor    │ │   Reader    │    │ │  │
│  │  │  │             │ │             │ │             │ │             │    │ │  │
│  │  │  │ Manual +    │ │ DNSSEC      │ │ Real-time   │ │ _index.*    │    │ │  │
│  │  │  │ API submit  │ │ NSEC chain  │ │ cert stream │ │ convention  │    │ │  │
│  │  │  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘    │ │  │
│  │  │         │               │               │               │           │ │  │
│  │  │         └───────────────┴───────┬───────┴───────────────┘           │ │  │
│  │  │                                 │                                    │ │  │
│  │  │                                 ▼                                    │ │  │
│  │  │                    ┌─────────────────────────┐                       │ │  │
│  │  │                    │    AGENT DISCOVERER     │                       │ │  │
│  │  │                    │                         │                       │ │  │
│  │  │                    │  Uses dns-aid.discover()│                       │ │  │
│  │  │                    │  + dns-aid.verify()     │                       │ │  │
│  │  │                    │  for each candidate     │                       │ │  │
│  │  │                    └────────────┬────────────┘                       │ │  │
│  │  │                                 │                                    │ │  │
│  │  └─────────────────────────────────┼────────────────────────────────────┘ │  │
│  │                                    │                                      │  │
│  │  ┌─────────────────────────────────▼────────────────────────────────────┐ │  │
│  │  │                         AGENT INDEX                                   │ │  │
│  │  │                                                                       │ │  │
│  │  │  ┌─────────────────────────────────────────────────────────────────┐ │ │  │
│  │  │  │                      PostgreSQL Database                        │ │ │  │
│  │  │  │                                                                 │ │ │  │
│  │  │  │  agents              domains             crawl_history          │ │ │  │
│  │  │  │  ├─ fqdn (PK)        ├─ domain (PK)      ├─ id                  │ │ │  │
│  │  │  │  ├─ domain           ├─ verified         ├─ domain              │ │ │  │
│  │  │  │  ├─ name             ├─ last_crawled     ├─ timestamp           │ │ │  │
│  │  │  │  ├─ protocol         ├─ agent_count      ├─ agents_found        │ │ │  │
│  │  │  │  ├─ endpoint         ├─ discovery_method ├─ status              │ │ │  │
│  │  │  │  ├─ capabilities[]   ├─ nsec_enabled     └─────────────────     │ │ │  │
│  │  │  │  ├─ security_score   ├─ index_entry                             │ │ │  │
│  │  │  │  ├─ trust_score      └─────────────────                         │ │ │  │
│  │  │  │  ├─ last_seen                                                   │ │ │  │
│  │  │  │  ├─ first_seen                                                  │ │ │  │
│  │  │  │  └─ metadata (JSON)                                             │ │ │  │
│  │  │  │                                                                 │ │ │  │
│  │  │  │  + Full-text search index (capabilities, description)           │ │ │  │
│  │  │  │  + Vector embeddings for semantic search (future)               │ │ │  │
│  │  │  └─────────────────────────────────────────────────────────────────┘ │ │  │
│  │  │                                                                       │ │  │
│  │  └───────────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                            │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐ │  │
│  │  │                           PUBLIC API                                   │ │  │
│  │  │                                                                        │ │  │
│  │  │  REST API (FastAPI)                   GraphQL (future)                 │ │  │
│  │  │  ┌────────────────────────────────┐   ┌────────────────────────────┐  │ │  │
│  │  │  │ GET  /api/v1/search            │   │ query {                    │  │ │  │
│  │  │  │ GET  /api/v1/agents/{fqdn}     │   │   searchAgents(q: "crm")   │  │ │  │
│  │  │  │ GET  /api/v1/domains/{domain}  │   │   { fqdn, endpoint, ... }  │  │ │  │
│  │  │  │ POST /api/v1/domains/submit    │   │ }                          │  │ │  │
│  │  │  │ GET  /api/v1/stats             │   │                            │  │ │  │
│  │  │  └────────────────────────────────┘   └────────────────────────────┘  │ │  │
│  │  │                                                                        │ │  │
│  │  └────────────────────────────────────────────────────────────────────────┘ │  │
│  │                                                                             │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                              WEB INTERFACE                                   │ │
│  │                                                                              │ │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │ │
│  │  │                                                                     │   │ │
│  │  │   🔍 Search Agents                                    [Search]     │   │ │
│  │  │   ┌─────────────────────────────────────────────────────────────┐  │   │ │
│  │  │   │  "CRM agents with MCP protocol"                             │  │   │ │
│  │  │   └─────────────────────────────────────────────────────────────┘  │   │ │
│  │  │                                                                     │   │ │
│  │  │   Filters: [Protocol ▼] [Capabilities ▼] [Security ▼] [Sort ▼]    │   │ │
│  │  │                                                                     │   │ │
│  │  │   Results (42 agents found):                                        │   │ │
│  │  │   ┌─────────────────────────────────────────────────────────────┐  │   │ │
│  │  │   │ 🤖 sales-assistant                    ⭐ 95/100 Security    │  │   │ │
│  │  │   │    salesforce.com | MCP | crm, sales, pipeline              │  │   │ │
│  │  │   │    https://mcp.salesforce.com:443                           │  │   │ │
│  │  │   │    [DNSSEC ✓] [DANE ✓] [Verified ✓]                        │  │   │ │
│  │  │   ├─────────────────────────────────────────────────────────────┤  │   │ │
│  │  │   │ 🤖 hubspot-connector                  ⭐ 78/100 Security    │  │   │ │
│  │  │   │    hubspot.com | MCP | crm, marketing, contacts             │  │   │ │
│  │  │   │    https://agent.hubspot.com:443                            │  │   │ │
│  │  │   │    [DNSSEC ✓] [DANE ✗] [Verified ✓]                        │  │   │ │
│  │  │   └─────────────────────────────────────────────────────────────┘  │   │ │
│  │  │                                                                     │   │ │
│  │  └─────────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                              │ │
│  └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐ │
│  │                         EASY BUTTON TOOLS (Phase 3)                          │ │
│  │                                                                              │ │
│  │  ┌─────────────────────────────┐    ┌─────────────────────────────┐        │ │
│  │  │     CoreDNS Plugin (Go)     │    │    DNS-AID Wallet (Python)  │        │ │
│  │  │                             │    │                             │        │ │
│  │  │  Kubernetes-native agent    │    │  Standalone identity        │        │ │
│  │  │  identity provisioning      │    │  management daemon          │        │ │
│  │  │                             │    │                             │        │ │
│  │  │  - Watch K8s services       │    │  - Key generation           │        │ │
│  │  │  - Auto SVCB/TXT records    │    │  - Certificate lifecycle    │        │ │
│  │  │  - DNSSEC zone signing      │    │  - TLSA record management   │        │ │
│  │  │  - TLSA generation          │    │  - Automated rotation       │        │ │
│  │  └─────────────────────────────┘    └─────────────────────────────┘        │ │
│  │                                                                              │ │
│  └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Project Structure (Proposed)

```
DNS-AID/
├── src/dns_aid/
│   ├── core/                    # Existing: publisher, discoverer, validator
│   ├── backends/                # Existing: route53, infoblox, ddns
│   ├── cli/                     # Existing: CLI commands
│   ├── mcp/                     # Existing: MCP server
│   │
│   │   ═══════════════════════ NEW v2.0 COMPONENTS ═══════════════════════
│   │
│   ├── directory/               # NEW: Agent Directory core
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models for index
│   │   ├── database.py          # Database connection/session management
│   │   ├── search.py            # Search logic (full-text, filters)
│   │   └── ranking.py           # Agent ranking algorithms
│   │
│   ├── crawlers/                # NEW: Discovery crawlers
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract crawler interface
│   │   ├── submission.py        # Manual domain submission handler
│   │   ├── zone_walker.py       # NSEC zone enumeration
│   │   ├── ct_monitor.py        # Certificate Transparency monitor
│   │   ├── index_reader.py      # _index._agents.* reader
│   │   └── scheduler.py         # Crawl scheduling/orchestration
│   │
│   ├── api/                     # NEW: Public REST API
│   │   ├── __init__.py
│   │   ├── app.py               # FastAPI application
│   │   ├── routes/
│   │   │   ├── search.py        # /api/v1/search
│   │   │   ├── agents.py        # /api/v1/agents/{fqdn}
│   │   │   ├── domains.py       # /api/v1/domains/{domain}
│   │   │   └── submit.py        # /api/v1/domains/submit
│   │   └── schemas.py           # Pydantic request/response models
│   │
│   └── web/                     # NEW: Web interface (optional)
│       ├── __init__.py
│       ├── templates/           # Jinja2 templates
│       └── static/              # CSS, JS assets
│
├── tests/
│   ├── unit/
│   │   ├── directory/           # NEW: Directory tests
│   │   ├── crawlers/            # NEW: Crawler tests
│   │   └── api/                 # NEW: API tests
│   └── integration/
│       └── test_directory.py    # NEW: Full crawl-to-search tests
│
├── docs/
│   ├── PLAN-v2-agent-directory.md  # This document
│   └── api-reference-v2.md         # NEW: API documentation
│
├── docker/
│   ├── Dockerfile               # Existing
│   ├── docker-compose.yml       # Existing
│   └── docker-compose.directory.yml  # NEW: Directory stack
│
└── wallet/                      # NEW: Separate package (Phase 3)
    └── (future)

coredns-dns-aid/                 # NEW: Separate Go repository (Phase 3)
    └── (future)
```

---

## 4. Component Deep Dives

### 4.1 Domain Submission Queue

**Purpose:** Allow organizations to manually register their domain for crawling.

**Why needed:** Not all domains use NSEC or have CT-logged certs. Manual submission is the simplest discovery method.

```
┌─────────────────────────────────────────────────────────────────┐
│                    DOMAIN SUBMISSION FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Organization                    Directory Service              │
│        │                                │                        │
│        │  POST /api/v1/domains/submit   │                        │
│        │  { "domain": "acme.com" }      │                        │
│        ├───────────────────────────────►│                        │
│        │                                │                        │
│        │                                │  1. Verify ownership   │
│        │                                │     (DNS TXT challenge │
│        │◄───────────────────────────────┤      or email)         │
│        │  "Add TXT record:              │                        │
│        │   _dnsaid-verify.acme.com      │                        │
│        │   = abc123xyz"                 │                        │
│        │                                │                        │
│        │  (org adds TXT record)         │                        │
│        │                                │                        │
│        │  POST /api/v1/domains/verify   │                        │
│        │  { "domain": "acme.com" }      │                        │
│        ├───────────────────────────────►│                        │
│        │                                │  2. Check TXT record   │
│        │                                │  3. Queue for crawling │
│        │◄───────────────────────────────┤  4. Return status      │
│        │  { "status": "verified",       │                        │
│        │    "next_crawl": "2026-01-14"} │                        │
│        │                                │                        │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
# src/dns_aid/crawlers/submission.py

class DomainSubmission:
    """Handle manual domain submissions with verification."""

    async def submit(self, domain: str) -> SubmissionResult:
        """
        Submit a domain for indexing.

        Returns a verification challenge (TXT record to add).
        """
        challenge = self._generate_challenge(domain)
        await self.db.create_pending_submission(domain, challenge)
        return SubmissionResult(
            domain=domain,
            challenge_type="dns-txt",
            challenge_name=f"_dnsaid-verify.{domain}",
            challenge_value=challenge,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )

    async def verify(self, domain: str) -> VerificationResult:
        """
        Verify domain ownership via DNS TXT challenge.
        """
        pending = await self.db.get_pending_submission(domain)
        if not pending:
            raise SubmissionNotFound(domain)

        # Check DNS for challenge
        txt_records = await self._query_txt(f"_dnsaid-verify.{domain}")
        if pending.challenge in txt_records:
            await self.db.mark_verified(domain)
            await self.crawler_queue.enqueue(domain, priority="high")
            return VerificationResult(status="verified")

        return VerificationResult(status="pending", message="TXT record not found")
```

### 4.2 NSEC Zone Walker

**Purpose:** Enumerate all agents in a DNSSEC-signed zone using NSEC chain walking.

**How it works:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    NSEC ZONE WALKING                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NSEC records form a linked list of all names in a zone:        │
│                                                                  │
│  Query: example.com NSEC                                         │
│  Answer: example.com NSEC _agents.example.com                    │
│                      ▲              │                            │
│                      │              ▼                            │
│  Query: _agents.example.com NSEC                                 │
│  Answer: _agents.example.com NSEC _chat._mcp._agents.example.com │
│                                          │                       │
│                                          ▼                       │
│  Query: _chat._mcp._agents.example.com NSEC                      │
│  Answer: ... NSEC _sales._a2a._agents.example.com                │
│                          │                                       │
│                          ▼                                       │
│  Query: _sales._a2a._agents.example.com NSEC                     │
│  Answer: ... NSEC www.example.com   (wrapped around)             │
│                                                                  │
│  Result: Found 2 agents:                                         │
│    - _chat._mcp._agents.example.com                              │
│    - _sales._a2a._agents.example.com                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Important considerations:**

1. **NSEC vs NSEC3**: NSEC3 hashes names, preventing enumeration. Only NSEC allows walking.
2. **Opt-in model**: Organizations must choose to use NSEC for their `_agents` zone.
3. **Rate limiting**: Don't hammer DNS servers; respect TTLs.

**Implementation:**

```python
# src/dns_aid/crawlers/zone_walker.py

class NSECZoneWalker:
    """
    Crawl DNS zones using NSEC chain walking.

    Only works on zones with NSEC (not NSEC3) records.
    Organizations opt-in by using NSEC for their _agents subdomain.
    """

    async def walk_zone(self, domain: str) -> list[str]:
        """
        Walk the NSEC chain to enumerate all names in _agents.{domain}.

        Returns list of discovered agent FQDNs.
        """
        agents = []
        start = f"_agents.{domain}"
        current = start

        while True:
            try:
                nsec = await self._query_nsec(current)
                next_name = nsec.next_name

                # Check if this is an agent record
                if "_agents." in str(next_name) and next_name != start:
                    agents.append(str(next_name))

                # Check for wrap-around (completed the chain)
                if self._is_before(next_name, start):
                    break

                current = str(next_name)

            except NSECNotFound:
                # Zone doesn't use NSEC or doesn't exist
                break
            except Exception as e:
                logger.warning(f"Zone walk error for {domain}: {e}")
                break

        return agents

    async def check_nsec_enabled(self, domain: str) -> bool:
        """Check if domain has NSEC (not NSEC3) for _agents subdomain."""
        try:
            await self._query_nsec(f"_agents.{domain}")
            return True
        except NSEC3Found:
            return False  # Uses NSEC3, can't walk
        except NSECNotFound:
            return False
```

### 4.3 Certificate Transparency Monitor

**Purpose:** Discover new agents by monitoring CT logs for new certificates.

**How it works:**

```
┌─────────────────────────────────────────────────────────────────┐
│              CERTIFICATE TRANSPARENCY MONITORING                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  CT Logs (Google Argon, Let's Encrypt Oak, etc.)                │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Real-time stream of newly issued certificates:             ││
│  │                                                              ││
│  │  → CN=mcp.acme.com, SAN=[mcp.acme.com], Issuer=Let's Encrypt││
│  │  → CN=agent.bigcorp.com, SAN=[...], Issuer=DigiCert         ││
│  │  → CN=www.random.com, SAN=[...], Issuer=Sectigo             ││
│  │  → CN=chat.startup.io, SAN=[chat.startup.io], Issuer=ZeroSSL││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  CT Monitor filters for potentially interesting domains:    ││
│  │                                                              ││
│  │  Heuristics:                                                 ││
│  │  - Subdomain starts with: mcp, agent, a2a, ai, assistant    ││
│  │  - Domain is in our "known DNS-AID domains" list            ││
│  │  - Certificate has specific extensions (future)             ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  For each candidate, query DNS for agent records:           ││
│  │                                                              ││
│  │  Certificate: mcp.acme.com                                   ││
│  │  → Try: _mcp._mcp._agents.acme.com SVCB    (not found)      ││
│  │  → Try: _default._mcp._agents.acme.com SVCB (found!)        ││
│  │  → Index this agent                                          ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Implementation:**

```python
# src/dns_aid/crawlers/ct_monitor.py

class CTLogMonitor:
    """
    Monitor Certificate Transparency logs for new agent-related certificates.

    Uses certstream or direct CT log API to watch for new certs.
    """

    # Patterns that suggest an agent endpoint
    INTERESTING_PREFIXES = [
        "mcp", "agent", "a2a", "ai", "assistant", "bot",
        "chat", "llm", "api-agent", "aiagent"
    ]

    async def start_monitoring(self):
        """Start streaming CT log entries."""
        async for cert in self._stream_certificates():
            if self._is_interesting(cert):
                await self._check_for_agents(cert)

    def _is_interesting(self, cert: Certificate) -> bool:
        """Check if certificate might be for an agent."""
        domains = cert.san_domains + [cert.common_name]

        for domain in domains:
            parts = domain.split(".")
            if parts[0].lower() in self.INTERESTING_PREFIXES:
                return True

            # Also check if domain is in our known DNS-AID domains
            base_domain = ".".join(parts[-2:])
            if base_domain in self.known_dnsaid_domains:
                return True

        return False

    async def _check_for_agents(self, cert: Certificate):
        """Query DNS to check if this domain has DNS-AID agents."""
        for domain in cert.san_domains:
            base_domain = self._extract_base_domain(domain)

            try:
                # Use existing dns-aid discover
                result = await discover(base_domain)
                for agent in result.agents:
                    await self.index_agent(agent)

            except Exception as e:
                logger.debug(f"No agents at {base_domain}: {e}")
```

### 4.4 Passive DNS Discovery

**Purpose:** Discover agents by observing DNS queries that have already happened across the internet.

**Credit:** Suggested by Steve Salo - instead of actively crawling, observe what's already being queried.

**How it works:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    PASSIVE DNS DISCOVERY                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  How Passive DNS Data Gets Collected (by providers):            │
│                                                                  │
│      Internet DNS Traffic                                        │
│              │                                                   │
│    ┌─────────┼─────────┬─────────────┐                          │
│    │         │         │             │                          │
│    ▼         ▼         ▼             ▼                          │
│  ┌────┐   ┌────┐   ┌────┐       ┌────────┐                      │
│  │ISP │   │Corp│   │Cloud│      │Security│                      │
│  │DNS │   │DNS │   │DNS  │      │Vendors │                      │
│  └──┬─┘   └──┬─┘   └──┬─┘       └───┬────┘                      │
│     │        │        │             │                            │
│     │   Sensors collect query/response pairs                     │
│     │        │        │             │                            │
│     └────────┴────────┴─────────────┘                           │
│                       │                                          │
│                       ▼                                          │
│        ┌──────────────────────────────┐                         │
│        │   PASSIVE DNS DATABASE       │                         │
│        │   (Farsight, Cisco, etc.)    │                         │
│        │                              │                         │
│        │   Billions of DNS records    │                         │
│        │   with query counts          │                         │
│        └──────────────┬───────────────┘                         │
│                       │                                          │
│                       │ We query for "_agents." patterns         │
│                       ▼                                          │
│        ┌──────────────────────────────┐                         │
│        │  Results:                    │                         │
│        │  _chat._mcp._agents.acme.com │                         │
│        │    → seen 10,482 times       │                         │
│        │  _api._a2a._agents.google.com│                         │
│        │    → seen 5,291 times        │                         │
│        └──────────────────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key Advantage:** Shows agents that are actually being USED, plus popularity/usage data.

#### Passive DNS Providers (Worldwide)

| Provider | Coverage | Best For | Pricing | API |
|----------|----------|----------|---------|-----|
| **Farsight DNSDB** | Largest global coverage, 100B+ records | Best overall data quality | $500-5000+/month | REST API |
| **Cisco Umbrella** | Strong enterprise coverage | Orgs already using Cisco security | Part of Umbrella license | REST API |
| **DomainTools** | Good historical data | Brand protection, investigations | $300-2000/month | REST API |
| **SecurityTrails** | Good coverage, developer-friendly | Startups, smaller budgets | $50-500/month | REST API |
| **VirusTotal** | Included in threat intel | Already have VT subscription | Part of VT Enterprise | REST API |
| **Spamhaus** | Focus on abuse/spam | Filtering bad actors | Contact for pricing | REST API |

**Recommendation for worldwide coverage:** Farsight DNSDB is the gold standard but expensive. SecurityTrails is more affordable for starting out.

#### Build vs Partner Decision

**Option A: Partner with pDNS Provider**

| Pros | Cons |
|------|------|
| Immediate access to billions of records | Ongoing cost ($500-5000/month) |
| No infrastructure to maintain | Dependent on third party |
| Global coverage from day one | Data access terms may be restrictive |
| Historical data available | |

**Option B: Build Our Own Sensors**

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUILD OUR OWN pDNS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Requirements:                                                   │
│  1. Run DNS resolvers that people actually use                   │
│  2. Deploy sensors to capture query/response pairs               │
│  3. Store and index the data                                     │
│  4. Build query API                                              │
│                                                                  │
│  Options to get DNS traffic:                                     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ A) Partner with ISPs/Cloud Providers                        ││
│  │    - They run resolvers with millions of users              ││
│  │    - We provide sensor software, they share anonymized data ││
│  │    - Hard to negotiate, legal complexity                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ B) Run Public Resolver (like 1.1.1.1 or 8.8.8.8)           ││
│  │    - Offer free, fast, privacy-focused DNS                  ││
│  │    - Users opt-in by using our resolver                     ││
│  │    - Requires significant infrastructure                    ││
│  │    - Cloudflare/Google already dominate this space          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ C) Sensor Software for Enterprise Partners                  ││
│  │    - Enterprises run our sensor on their internal DNS       ││
│  │    - They get analytics, we get (anonymized) agent data     ││
│  │    - Easier sell than ISPs, more targeted data              ││
│  │    - Limited to participating enterprises                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ D) Contribute to Existing Open Projects                     ││
│  │    - CIRCL Passive DNS (Luxembourg CERT - open source)      ││
│  │    - Join their sensor network, access shared data          ││
│  │    - Less control, but lower barrier                        ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

| Option | Effort | Coverage | Cost | Recommendation |
|--------|--------|----------|------|----------------|
| Partner (Farsight) | Low | Global | High ($$$) | Best if budget exists |
| Partner (SecurityTrails) | Low | Good | Medium ($$) | Good starting point |
| Build + ISP partners | Very High | Depends on partners | Low ongoing | Hard to execute |
| Build public resolver | Extreme | Could be large | Very High infra | Not realistic |
| Enterprise sensors | Medium | Limited to partners | Low | Good complement |
| CIRCL/Open projects | Low | Variable | Free | Worth exploring |

#### Implementation (Partner Approach)

```python
# src/dns_aid/crawlers/passive_dns.py

class PassiveDNSCrawler:
    """
    Discover agents via passive DNS databases.

    Queries pDNS providers for records matching DNS-AID patterns.
    Returns agents that have been queried (i.e., actually used).
    """

    def __init__(self, provider: str = "securitytrails"):
        self.provider = provider
        self.api_key = os.environ.get(f"{provider.upper()}_API_KEY")

    async def discover_agents(self) -> list[AgentRecord]:
        """Query pDNS for DNS-AID records."""

        # Search patterns for DNS-AID records
        patterns = [
            "*._mcp._agents.*",
            "*._a2a._agents.*",
            "*._agents.*"
        ]

        agents = []
        for pattern in patterns:
            results = await self._query_pdns(pattern)
            for record in results:
                if self._is_valid_dnsaid_record(record):
                    agent = await self._enrich_agent(record)
                    agent.popularity = record.query_count  # Bonus: usage data!
                    agents.append(agent)

        return agents

    async def _query_pdns(self, pattern: str) -> list[PDNSRecord]:
        """Query the passive DNS provider."""
        if self.provider == "farsight":
            return await self._query_farsight(pattern)
        elif self.provider == "securitytrails":
            return await self._query_securitytrails(pattern)
        # ... other providers
```

#### Comparison: All Discovery Methods

| Method | Active/Passive | Cost | Coverage | Shows Usage | Phase |
|--------|----------------|------|----------|-------------|-------|
| Domain submission | Active (manual) | Free | Opt-in only | No | 1 |
| NSEC zone walking | Active (crawl) | Free | NSEC zones only | No | 2 |
| CT log monitoring | Passive (certs) | Free | Public TLS only | No | 2 |
| _index._agents.* | Active (read) | Free | Opt-in only | No | 2 |
| **Passive DNS** | Passive (observe) | $$-$$$ | Queried records | **Yes** | 2-3 |

#### Questions for Stakeholders (Passive DNS)

| Question | Options | Impact |
|----------|---------|--------|
| Do we have budget for pDNS API? | $50-500/month (SecurityTrails) or $500-5000 (Farsight) | Determines if we can use this method |
| Any existing pDNS relationships? | Check with security team - may have Umbrella, VT, etc. | Could be free if already licensed |
| Build our own sensors? | Enterprise sensor program vs partner with CIRCL | Long-term play, lower cost |
| Privacy implications? | pDNS shows who queries what | May need policy/legal review |

### 4.5 Index Entry Point Reader

**Purpose:** Read the standardized `_index._agents.*` entry point.

**Convention:**

```
# Organization publishes at this well-known location:
_index._agents.example.com  TXT  "agents=15" "updated=2026-01-13"
_index._agents.example.com  PTR  _public-agents.example.com.

# Or with SVCB pointing to an API:
_index._agents.example.com  SVCB 1 api.example.com. path="/agents.json"
```

**Implementation:**

```python
# src/dns_aid/crawlers/index_reader.py

class IndexEntryReader:
    """
    Read _index._agents.{domain} entry points.

    Organizations can publish metadata about their agents at this
    well-known location, similar to robots.txt or .well-known/*.
    """

    async def read_index(self, domain: str) -> IndexEntry | None:
        """Read index entry point for a domain."""
        fqdn = f"_index._agents.{domain}"

        # Try TXT record first
        txt_data = await self._query_txt(fqdn)
        if txt_data:
            return self._parse_txt_index(txt_data)

        # Try PTR record (points to agent zone)
        ptr_data = await self._query_ptr(fqdn)
        if ptr_data:
            return IndexEntry(
                domain=domain,
                agent_zone=ptr_data,
                discovery_hint="ptr"
            )

        # Try SVCB (points to API)
        svcb_data = await self._query_svcb(fqdn)
        if svcb_data:
            return IndexEntry(
                domain=domain,
                api_endpoint=svcb_data.target,
                discovery_hint="api"
            )

        return None
```

### 4.5 Agent Index Database

**Purpose:** Store discovered agents with metadata for searching.

**Schema:**

```sql
-- Core tables for agent directory

CREATE TABLE domains (
    domain VARCHAR(255) PRIMARY KEY,
    verified BOOLEAN DEFAULT FALSE,
    verification_method VARCHAR(50),  -- 'dns-txt', 'email', 'manual'
    first_seen TIMESTAMP DEFAULT NOW(),
    last_crawled TIMESTAMP,
    next_crawl TIMESTAMP,
    crawl_frequency_hours INT DEFAULT 24,
    agent_count INT DEFAULT 0,

    -- Discovery metadata
    nsec_enabled BOOLEAN DEFAULT FALSE,
    has_index_entry BOOLEAN DEFAULT FALSE,
    index_entry_data JSONB,

    -- Trust signals
    dnssec_enabled BOOLEAN DEFAULT FALSE,
    dane_enabled BOOLEAN DEFAULT FALSE,

    -- Crawl status
    crawl_status VARCHAR(20) DEFAULT 'pending',  -- pending, active, paused, failed
    last_error TEXT,
    consecutive_failures INT DEFAULT 0
);

CREATE TABLE agents (
    fqdn VARCHAR(255) PRIMARY KEY,
    domain VARCHAR(255) REFERENCES domains(domain),

    -- Core identity
    name VARCHAR(63) NOT NULL,
    protocol VARCHAR(20) NOT NULL,  -- mcp, a2a
    endpoint_url VARCHAR(500) NOT NULL,
    port INT DEFAULT 443,

    -- Capabilities
    capabilities TEXT[],
    version VARCHAR(50),

    -- Metadata (from TXT records)
    description TEXT,
    metadata JSONB,

    -- Timestamps
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    last_verified TIMESTAMP,

    -- Security scoring
    security_score INT,  -- 0-100
    dnssec_valid BOOLEAN,
    dane_valid BOOLEAN,
    tls_valid BOOLEAN,
    endpoint_reachable BOOLEAN,

    -- Trust/ranking
    trust_score INT DEFAULT 50,  -- 0-100
    popularity_score INT DEFAULT 0,

    -- Full-text search
    search_vector TSVECTOR
);

-- Index for full-text search
CREATE INDEX idx_agents_search ON agents USING GIN(search_vector);

-- Index for capability filtering
CREATE INDEX idx_agents_capabilities ON agents USING GIN(capabilities);

-- Index for protocol filtering
CREATE INDEX idx_agents_protocol ON agents(protocol);

-- Index for security score sorting
CREATE INDEX idx_agents_security ON agents(security_score DESC);

CREATE TABLE crawl_history (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) REFERENCES domains(domain),
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(20),  -- success, partial, failed
    agents_found INT DEFAULT 0,
    agents_added INT DEFAULT 0,
    agents_updated INT DEFAULT 0,
    agents_removed INT DEFAULT 0,
    discovery_method VARCHAR(50),  -- submission, nsec, ct, index
    error_message TEXT
);

-- Trigger to update search vector
CREATE OR REPLACE FUNCTION update_agent_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', COALESCE(NEW.name, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.description, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(array_to_string(NEW.capabilities, ' '), '')), 'C') ||
        setweight(to_tsvector('english', COALESCE(NEW.domain, '')), 'D');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER agent_search_vector_update
    BEFORE INSERT OR UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_agent_search_vector();
```

### 4.6 Search API

**Purpose:** Provide REST API for searching the agent directory.

**Endpoints:**

```yaml
openapi: 3.0.0
info:
  title: DNS-AID Agent Directory API
  version: 2.0.0

paths:
  /api/v1/search:
    get:
      summary: Search for agents
      parameters:
        - name: q
          in: query
          description: Search query (full-text)
          schema:
            type: string
          example: "CRM sales automation"
        - name: protocol
          in: query
          description: Filter by protocol
          schema:
            type: string
            enum: [mcp, a2a]
        - name: capability
          in: query
          description: Filter by capability (can repeat)
          schema:
            type: array
            items:
              type: string
          example: ["crm", "sales"]
        - name: min_security
          in: query
          description: Minimum security score (0-100)
          schema:
            type: integer
        - name: sort
          in: query
          description: Sort order
          schema:
            type: string
            enum: [relevance, security, popularity, newest]
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: offset
          in: query
          schema:
            type: integer
            default: 0
      responses:
        200:
          description: Search results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResults'

  /api/v1/agents/{fqdn}:
    get:
      summary: Get agent details
      parameters:
        - name: fqdn
          in: path
          required: true
          schema:
            type: string
          example: "_sales._mcp._agents.salesforce.com"
      responses:
        200:
          description: Agent details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AgentDetail'
        404:
          description: Agent not found

  /api/v1/domains/{domain}:
    get:
      summary: List all agents for a domain
      parameters:
        - name: domain
          in: path
          required: true
          schema:
            type: string
          example: "salesforce.com"
      responses:
        200:
          description: Domain agents
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DomainAgents'

  /api/v1/domains/submit:
    post:
      summary: Submit domain for indexing
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                domain:
                  type: string
                  example: "acme.com"
      responses:
        200:
          description: Verification challenge
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/VerificationChallenge'

  /api/v1/stats:
    get:
      summary: Directory statistics
      responses:
        200:
          description: Stats
          content:
            application/json:
              schema:
                type: object
                properties:
                  total_agents:
                    type: integer
                  total_domains:
                    type: integer
                  protocols:
                    type: object
                  last_updated:
                    type: string
                    format: date-time

components:
  schemas:
    SearchResults:
      type: object
      properties:
        total:
          type: integer
        offset:
          type: integer
        limit:
          type: integer
        agents:
          type: array
          items:
            $ref: '#/components/schemas/AgentSummary'

    AgentSummary:
      type: object
      properties:
        fqdn:
          type: string
        name:
          type: string
        domain:
          type: string
        protocol:
          type: string
        endpoint_url:
          type: string
        capabilities:
          type: array
          items:
            type: string
        security_score:
          type: integer
        badges:
          type: array
          items:
            type: string
            enum: [dnssec, dane, verified]

    AgentDetail:
      allOf:
        - $ref: '#/components/schemas/AgentSummary'
        - type: object
          properties:
            version:
              type: string
            description:
              type: string
            first_seen:
              type: string
              format: date-time
            last_verified:
              type: string
              format: date-time
            security:
              type: object
              properties:
                dnssec_valid:
                  type: boolean
                dane_valid:
                  type: boolean
                tls_valid:
                  type: boolean
            metadata:
              type: object
```

---

## 5. Data Models

### 5.1 Python Models (Pydantic)

```python
# src/dns_aid/directory/models.py

from datetime import datetime
from pydantic import BaseModel, Field

class DomainRecord(BaseModel):
    """Domain in the directory."""
    domain: str
    verified: bool = False
    verification_method: str | None = None
    first_seen: datetime
    last_crawled: datetime | None = None
    agent_count: int = 0
    nsec_enabled: bool = False
    dnssec_enabled: bool = False
    dane_enabled: bool = False
    crawl_status: str = "pending"

class AgentRecord(BaseModel):
    """Agent in the directory index."""
    fqdn: str
    domain: str
    name: str
    protocol: str
    endpoint_url: str
    port: int = 443
    capabilities: list[str] = []
    version: str | None = None
    description: str | None = None

    # Timestamps
    first_seen: datetime
    last_seen: datetime
    last_verified: datetime | None = None

    # Scores
    security_score: int | None = None
    trust_score: int = 50

    # Security details
    dnssec_valid: bool | None = None
    dane_valid: bool | None = None
    tls_valid: bool | None = None
    endpoint_reachable: bool | None = None

    # Computed
    @property
    def badges(self) -> list[str]:
        badges = []
        if self.dnssec_valid:
            badges.append("dnssec")
        if self.dane_valid:
            badges.append("dane")
        if self.endpoint_reachable:
            badges.append("verified")
        return badges

class SearchQuery(BaseModel):
    """Search query parameters."""
    q: str | None = None
    protocol: str | None = None
    capabilities: list[str] = []
    min_security: int | None = None
    sort: str = "relevance"
    limit: int = Field(default=20, le=100)
    offset: int = 0

class SearchResults(BaseModel):
    """Search results."""
    total: int
    offset: int
    limit: int
    agents: list[AgentRecord]
    query_time_ms: float
```

---

## 6. API Specifications

See Section 4.6 for OpenAPI specification.

**Base URL options:**
- `https://directory.dns-aid.org/api/v1/` (hosted service)
- `http://localhost:8080/api/v1/` (self-hosted)

---

## 7. Implementation Phases

### Phase 1: Foundation (4-6 weeks)

**Goal:** Basic searchable directory with manual submission.

```
┌─────────────────────────────────────────────────────────────────┐
│                         PHASE 1 SCOPE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ Domain submission API                                        │
│  ✅ DNS TXT verification                                         │
│  ✅ Basic crawler (uses existing discover())                     │
│  ✅ PostgreSQL agent index                                       │
│  ✅ Full-text search                                             │
│  ✅ REST API (search, agents, domains)                           │
│  ✅ Basic web UI                                                 │
│  ✅ Docker Compose deployment                                    │
│                                                                  │
│  ❌ NSEC zone walking                                            │
│  ❌ CT log monitoring                                            │
│  ❌ _index._agents.* convention                                  │
│  ❌ Advanced ranking                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Deliverables:**
1. `src/dns_aid/directory/` module
2. `src/dns_aid/crawlers/submission.py`
3. `src/dns_aid/api/` module
4. Database migrations
5. Docker Compose for directory stack
6. Documentation

### Phase 2: Advanced Discovery (4-6 weeks)

**Goal:** Automated discovery without manual submission.

```
┌─────────────────────────────────────────────────────────────────┐
│                         PHASE 2 SCOPE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ NSEC zone walker                                             │
│  ✅ CT log monitor (certstream integration)                      │
│  ✅ _index._agents.* convention (spec + implementation)          │
│  ✅ Crawl scheduler (periodic re-crawling)                       │
│  ✅ Improved ranking algorithm                                   │
│  ✅ API rate limiting                                            │
│  ✅ Webhook notifications (new agents)                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Deliverables:**
1. `src/dns_aid/crawlers/zone_walker.py`
2. `src/dns_aid/crawlers/ct_monitor.py`
3. `src/dns_aid/crawlers/index_reader.py`
4. `_index._agents.*` RFC-style specification document
5. Webhook notification system

### Phase 3: Easy Button Tools (8-12 weeks)

**Goal:** Zero-config agent publishing.

```
┌─────────────────────────────────────────────────────────────────┐
│                         PHASE 3 SCOPE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✅ DNS-AID Wallet (Python daemon)                               │
│     - Key generation (Ed25519)                                   │
│     - Certificate management (ACME/Let's Encrypt)               │
│     - TLSA record generation                                     │
│     - Automated rotation                                         │
│                                                                  │
│  ✅ CoreDNS Plugin (Go, separate repo)                           │
│     - Kubernetes service watcher                                 │
│     - Auto SVCB/TXT record generation                           │
│     - DNSSEC zone signing (stretch goal)                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Deliverables:**
1. `dns-aid-wallet/` Python package
2. `coredns-dns-aid/` Go repository
3. Kubernetes deployment examples
4. Helm chart

### Phase 4: Scale & Polish (ongoing)

**Goal:** Production-ready service.

- Semantic search (vector embeddings)
- GraphQL API
- Agent analytics dashboard
- Community ratings/reviews
- Federation protocol (multiple directory operators)

---

## 8. Open Questions for Stakeholders

### Q1: Governance & Operation

**Question:** Who operates the "Google of Agents" directory service?

| Option | Pros | Cons |
|--------|------|------|
| **A: DNS-AID project operates it** | Single source of truth, consistent quality | Centralization concerns, operational burden |
| **B: Multiple operators (federation)** | Decentralized, resilient | Fragmentation, inconsistent data |
| **C: Open source only (self-host)** | Maximum decentralization | No default directory, adoption barrier |
| **D: Foundation-operated** | Neutral governance, sustainable funding | Requires foundation setup |

**Recommendation:** Start with A (project-operated), design for B (federation) from day one.

---

### Q2: Verification Requirements

**Question:** How strict should domain verification be?

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: DNS TXT challenge** | Add `_dnsaid-verify.domain.com TXT "challenge"` | Proves DNS control, automatable | Requires DNS access |
| **B: Email to domain contacts** | Email to admin@, webmaster@, etc. | No DNS changes needed | Slower, less automatable |
| **C: No verification** | Trust DNS ownership implicitly | Fastest adoption | Spam/abuse risk |
| **D: Tiered** | Unverified (listed) vs Verified (badge) | Balances speed and trust | UX complexity |

**Recommendation:** D (Tiered) - list unverified domains but mark them, encourage verification for trust badge.

---

### Q3: NSEC Adoption

**Question:** Will organizations actually enable NSEC (vs NSEC3) for discoverability?

**Context:**
- NSEC3 is the default for most DNSSEC deployments (prevents zone enumeration)
- Enabling NSEC requires explicit configuration and exposes all zone names
- We're asking orgs to intentionally "leak" their agent names

**Options:**
1. **Rely on NSEC** - Some orgs will opt-in, enough for bootstrap
2. **Don't rely on NSEC** - Focus on submission + CT monitoring
3. **Create new convention** - `_public-agents.domain` subdomain with NSEC

**Recommendation:** Option 3 - define a convention where orgs create a dedicated subdomain for public agents with NSEC enabled, keeping their main zone private.

---

### Q4: Trust Scoring

**Question:** How should agents be ranked/scored?

**Proposed factors:**

| Factor | Weight | Source |
|--------|--------|--------|
| DNSSEC validation | 25% | DNS query |
| DANE/TLSA present | 20% | DNS query |
| TLS certificate valid | 15% | HTTPS check |
| Endpoint reachable | 15% | HTTPS check |
| Domain age | 10% | WHOIS |
| Community rating | 15% | User feedback (future) |

**Questions:**
- Should we include subjective factors (ratings)?
- Should verified domains rank higher?
- Should we penalize "new" agents?

---

### Q5: Scope of CoreDNS Plugin

**Question:** How much automation should the CoreDNS plugin provide?

| Feature | Complexity | Value |
|---------|------------|-------|
| Auto SVCB/TXT creation | Low | High |
| Auto DNSSEC signing | Very High | High |
| Auto TLSA/DANE | High | Medium |
| Auto certificate provisioning | High | High |

**Recommendation:** Start with SVCB/TXT only. DNSSEC signing is extremely complex (key ceremonies, rollovers) - may be better left to existing tools.

---

### Q6: Business Model

**Question:** How is this sustained long-term?

| Model | Description | Viability |
|-------|-------------|-----------|
| **Open source + donations** | Community funded | Low sustainability |
| **Foundation grants** | Linux Foundation, etc. | Requires acceptance |
| **Freemium API** | Free tier + paid for higher limits | Sustainable but adds friction |
| **Enterprise features** | Private directories, SLA, support | Good for adoption |
| **Sponsorships** | Companies sponsor for visibility | Works at scale |

**Recommendation:** Start open source, pursue Foundation membership, add enterprise features later.

---

### Q7: Privacy Considerations

**Question:** What data do we collect and expose?

**Concerns:**
- Crawling exposes which organizations use DNS-AID
- Agent capabilities reveal business functions
- Endpoint URLs could be sensitive

**Options:**
1. **Opt-in only** - Only index submitted domains
2. **Opt-out available** - Index everything, allow removal
3. **Robots.txt equivalent** - `_noindex._agents.domain.com` to block

**Recommendation:** Combination - opt-in by default, respect `_noindex` convention.

---

### Q8: Rate Limiting & Abuse

**Question:** How do we prevent abuse of the directory?

**Threats:**
- Spam submissions (fake agents)
- Scraping (competitor harvesting)
- DoS (overwhelming the API)

**Mitigations:**
- Domain verification (prevents spam)
- API keys with rate limits
- Proof-of-work for anonymous access (aggressive)
- IP-based rate limiting

---

## 9. Risk Assessment

### Technical Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| NSEC adoption is low | Can't do zone walking | High | Focus on other discovery methods |
| CT log volume overwhelming | Can't keep up | Medium | Filter aggressively, scale horizontally |
| Database scaling issues | Slow searches | Low | Use proper indexing, consider read replicas |
| DNS providers block crawling | Can't verify agents | Low | Respect rate limits, use distributed crawlers |

### Adoption Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| No one submits domains | Empty directory | Medium | Seed with known DNS-AID users, outreach |
| Privacy concerns | Orgs opt out | Medium | Strong opt-out, clear privacy policy |
| Competing directories | Fragmentation | Low | Open federation protocol |

### Operational Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Operational costs unsustainable | Service shutdown | Medium | Plan funding early, efficiency focus |
| Single point of failure | Outage | Medium | Multi-region, federation design |

---

## 10. Success Metrics

### Phase 1 Success (Month 3)

- [ ] 100+ domains submitted
- [ ] 500+ agents indexed
- [ ] API response time < 200ms p95
- [ ] Search relevance "good" (manual testing)

### Phase 2 Success (Month 6)

- [ ] 1,000+ domains indexed
- [ ] 5,000+ agents indexed
- [ ] 3+ discovery methods working
- [ ] 10+ orgs using _index._agents.* convention

### Phase 3 Success (Month 12)

- [ ] DNS-AID Wallet released
- [ ] CoreDNS plugin released
- [ ] 10+ Kubernetes deployments using plugin
- [ ] 50+ orgs using Wallet

### Long-term Success (Year 2+)

- [ ] 10,000+ agents indexed
- [ ] Industry recognition as "the" agent directory
- [ ] Federation with 2+ other directory operators
- [ ] Sustainable funding model

---

## Appendix A: Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| API Framework | FastAPI | Async, OpenAPI docs, Pydantic integration |
| Database | PostgreSQL | Full-text search, JSON support, reliability |
| Task Queue | Celery + Redis | Mature, scalable |
| CT Monitoring | certstream / pyctl | Real-time CT log streaming |
| DNS Library | dnspython | Already using in DNS-AID |
| Web UI | HTMX + Jinja2 | Simple, no JS framework needed |
| Deployment | Docker Compose / K8s | Flexible |

---

## Appendix B: Competitive Landscape

### Discovery & Registry Competitors

| Competitor | Model | Strengths | Weaknesses |
|------------|-------|-----------|------------|
| **GoDaddy ANS** | Centralized registry - they own the database | Brand recognition, commercial backing, simple onboarding | Vendor lock-in, single point of control, not sovereign, pay-to-play |
| **ai.txt** | Simple text file at /.well-known/ai.txt | Dead simple, backed by Cloudflare/OpenAI | No cryptographic verification, HTTP-only, can be spoofed, no search |
| **AgentDNS (China Telecom)** | DNS-based, Chinese research | Similar technical goals | Governance unclear, nation-state concerns, limited adoption |
| **Agent marketplaces** | Centralized platforms (e.g., OpenAI GPT Store) | Search exists, user trust | Platform lock-in, fees, approval gates, not interoperable |

### Google's Full-Stack Play (Strategic Threat)

Google is building a complete agent ecosystem that could marginalize independent discovery:

| Layer | Google Solution | What It Does | DNS-AID Alternative |
|-------|-----------------|--------------|---------------------|
| **Discovery** | Google Search / Gemini | Find agents via Google AI surfaces | DNS-AID Directory (decentralized) |
| **Communication** | A2A (Agent-to-Agent) | Agent interoperability protocol | Protocol-agnostic (supports A2A, MCP) |
| **Commerce** | **UCP (Universal Commerce Protocol)** | Payments/checkout in AI interfaces | N/A (out of scope) |
| **Runtime** | Vertex AI Agent Builder | Host and run agents | N/A (out of scope) |

**Google UCP Details (announced 2025):**
- Open standard for AI commerce: https://developers.google.com/merchant/ucp
- Enables purchases directly in Gemini/Search AI surfaces
- MCP-compatible, works with A2A
- Native checkout or iframe-based embedded checkout
- **Strategic intent**: Own the transaction layer, take fees, control visibility

**The Risk:**
Google wants discovery to happen through **their** AI surfaces, not DNS. If agents are only found via Gemini/Search:
1. Google controls visibility (pay-to-rank)
2. Google takes transaction fees via UCP
3. Independent agents become invisible

**DNS-AID's Counter-Position:**
- **Sovereign discovery** - Not dependent on Google's algorithm
- **No gatekeepers** - DNS is neutral infrastructure
- **No rent extraction** - No fees for visibility
- **Interoperable** - Works WITH Google protocols (A2A, MCP), not against them

### Our Differentiation Summary

| Dimension | Centralized (Google/GoDaddy) | DNS-AID |
|-----------|------------------------------|---------|
| Control | Platform owns registry | Organizations own their DNS |
| Visibility | Platform decides ranking | DNS is neutral |
| Fees | Transaction/listing fees likely | Free (DNS infrastructure) |
| Lock-in | High | None |
| Security | Trust the platform | DNSSEC cryptographic proof |
| Interop | Platform-specific | Protocol-agnostic |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | 2026-01-13 | DNS-AID Team | Initial draft |

---

*This document is a living plan. Updates will be made as stakeholder feedback is incorporated and implementation progresses.*
