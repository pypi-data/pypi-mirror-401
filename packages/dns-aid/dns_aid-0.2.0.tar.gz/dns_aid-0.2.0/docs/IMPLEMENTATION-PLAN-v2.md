# DNS-AID v2.0: Agent Directory - Phased Implementation Plan

> **Status:** APPROVED FOR DEVELOPMENT
> **Date:** 2026-01-14
> **Stakeholder Approval:** Wei Chen, Padmini (funding confirmed)

---

## Executive Summary

Build the "Google of Agents" - a searchable directory that indexes DNS-AID published agents across the internet. Each phase is self-contained, fully tested, and deployable before proceeding.

### Stakeholder Requirements (from Wei Chen)
- Open-source for critical mass adoption
- Use Infoblox proprietary DNS traffic data for popularity ranking
- Use threat intel for indicator of compromise (IOC) detection
- Paid services: takedown, advanced analytics via Infoblox

---

## Pre-LF Contribution: Completed Tasks

### Priority 1: CI/Branch Protection Hardening ✅ COMPLETED

| Task | Status |
|------|--------|
| Add coverage threshold (`--cov-fail-under=70`) | ✅ Done |
| Remove continue-on-error from type-check | ✅ Done |
| Remove continue-on-error from security scan | ✅ Done |
| Create `.github/dependabot.yml` | ✅ Done |
| GitHub branch protection settings | ⏳ Manual step |

### Priority 2: Test Coverage ✅ COMPLETED (54% → 71.83%)

| Test File | Status |
|-----------|--------|
| `tests/unit/test_ddns_backend.py` | ✅ Created |
| `tests/unit/test_route53_backend.py` | ✅ Created |
| `tests/unit/test_logging.py` | ✅ Created |

### Priority 3: RFC Documentation ✅ COMPLETED

| Document | Path |
|----------|------|
| IANA Considerations | `docs/rfc/iana-considerations.md` |
| Security Considerations | `docs/rfc/security-considerations.md` |
| Privacy Considerations | `docs/rfc/privacy-considerations.md` |
| Wire Format (ABNF) | `docs/rfc/wire-format.abnf` |

### Priority 4: GitHub Templates ✅ COMPLETED

| File | Status |
|------|--------|
| `.github/ISSUE_TEMPLATE/config.yml` | ✅ Created |
| `.github/FUNDING.yml` | ✅ Created |

---

## Discovery Methods Comparison

| Method | Type | Cost | Coverage | Popularity Data | Phase | Status |
|--------|------|------|----------|-----------------|-------|--------|
| Domain submission | Active (manual) | Free | Opt-in only | No | 1 | **Primary** |
| `_index._agents.*` | Active (read) | Free | Opt-in only | No | 2 | **Primary** |
| CT log monitoring | Passive (certs) | Free | Public TLS only | No | 2 | **Primary** |
| **Passive DNS** | **Passive (observe)** | **Internal (Infoblox)** | **Queried records** | **Yes ✓** | **2** | **Primary** |
| Pattern Probing | Active (targeted) | Free | Common names | No | 2 | **Fallback** |
| NSEC zone walking | Active (crawl) | Free | DNSSEC zones | No | 2 | **Optional** ⚠️ |

> **⚠️ NSEC Zone Walking:** Implemented as **optional feature flag** (`ENABLE_NSEC_WALKER`). IETF/DNSOP have historically opposed zone enumeration mechanisms (privacy concern). This feature can be disabled without breaking discovery - pattern probing serves as fallback.

### Discovery Strategy (Priority Order)

```
For each domain:
1. _index._agents.{domain} TXT     ← Primary (1 query, gets all agents)
   │
   ├── Found? → Parse and query each listed agent
   │
   └── Not found? ↓

2. If ENABLE_NSEC_WALKER && domain has DNSSEC:
   │
   ├── NSEC walk → enumerate _agents.* records
   │
   └── Disabled or failed? ↓

3. Pattern Probing (fallback)
   └── Try common names: assistant, chat, api, agent, help
       × protocols: mcp, a2a

4. pDNS enrichment (background, always running)
   └── Adds popularity scores, catches stragglers
```

**Key Insight:** Passive DNS is the only method that shows agents that are **actually being used** (not just published) and provides real popularity data from DNS query volumes.

---

## Operational Model Decision

### Recommended Architecture: **Hybrid Serverless + Managed Services**

| Component | Technology | Why |
|-----------|------------|-----|
| **API** | AWS Lambda + API Gateway | Auto-scaling, pay-per-request, zero ops |
| **Database** | Amazon RDS PostgreSQL (Serverless v2) | Auto-scaling, managed, full SQL |
| **Search** | PostgreSQL Full-Text (Phase 1) → OpenSearch (Phase 4) | Start simple, scale later |
| **Crawler Workers** | AWS Lambda (scheduled) | Event-driven, cost-effective |
| **Long-running Crawls** | AWS Fargate | For CT monitoring, NSEC walking (optional) |
| **Queue** | Amazon SQS | Reliable, serverless |
| **Cache** | Amazon ElastiCache Redis | API response caching |
| **CDN/Web** | CloudFront + S3 | Static assets, global edge |
| **Monitoring** | CloudWatch + X-Ray | Integrated observability |

### Cost Estimate (at scale)

| Phase | Monthly Cost | Notes |
|-------|--------------|-------|
| Phase 1 (MVP) | $50-150 | Serverless minimums |
| Phase 2 (Crawlers) | $150-400 | Fargate for long-running |
| Phase 3 (Scale) | $500-1500 | Higher traffic, OpenSearch |
| Phase 4 (Enterprise) | $2000-5000 | Full feature set |

---

## Phase 1: Foundation & MVP
**Duration:** 3-4 weeks
**Goal:** Working API + Database + Domain Submission

### 1.1 Deliverables

| Component | Description |
|-----------|-------------|
| Database Schema | PostgreSQL with agents, domains, crawl_history tables |
| Domain Submission API | POST /submit, GET /verify endpoints |
| Basic Search API | GET /search?q=, GET /agents/{fqdn} |
| Health & Metrics | /health, /metrics endpoints |
| Infrastructure | Terraform/CDK for AWS deployment |

### 1.2 Technical Specifications

#### Database Schema
```sql
-- Core tables
CREATE TABLE domains (
    domain VARCHAR(255) PRIMARY KEY,
    verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(64),
    submitted_at TIMESTAMP DEFAULT NOW(),
    verified_at TIMESTAMP,
    last_crawled TIMESTAMP,
    crawl_status VARCHAR(20) DEFAULT 'pending',
    agent_count INTEGER DEFAULT 0,
    metadata JSONB
);

CREATE TABLE agents (
    fqdn VARCHAR(512) PRIMARY KEY,
    domain VARCHAR(255) REFERENCES domains(domain),
    name VARCHAR(63) NOT NULL,
    protocol VARCHAR(20) NOT NULL,
    endpoint_url VARCHAR(512),
    port INTEGER DEFAULT 443,
    capabilities TEXT[],
    version VARCHAR(32),
    security_score INTEGER DEFAULT 0,
    trust_score INTEGER DEFAULT 0,
    popularity_score INTEGER DEFAULT 0,  -- From Infoblox DNS data
    threat_flags JSONB DEFAULT '{}',     -- IOC indicators
    first_seen TIMESTAMP DEFAULT NOW(),
    last_seen TIMESTAMP DEFAULT NOW(),
    last_verified TIMESTAMP,
    metadata JSONB,
    -- Full-text search
    search_vector TSVECTOR GENERATED ALWAYS AS (
        setweight(to_tsvector('english', name), 'A') ||
        setweight(to_tsvector('english', coalesce(array_to_string(capabilities, ' '), '')), 'B')
    ) STORED
);

CREATE INDEX idx_agents_search ON agents USING GIN(search_vector);
CREATE INDEX idx_agents_domain ON agents(domain);
CREATE INDEX idx_agents_protocol ON agents(protocol);
CREATE INDEX idx_agents_security ON agents(security_score DESC);

CREATE TABLE crawl_history (
    id SERIAL PRIMARY KEY,
    domain VARCHAR(255) REFERENCES domains(domain),
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    status VARCHAR(20),
    agents_found INTEGER DEFAULT 0,
    agents_added INTEGER DEFAULT 0,
    agents_updated INTEGER DEFAULT 0,
    error_message TEXT
);
```

#### API Endpoints (FastAPI)
```python
# Phase 1 endpoints
POST /api/v1/domains/submit     # Submit domain for indexing
POST /api/v1/domains/verify     # Verify domain ownership
GET  /api/v1/search             # Search agents
GET  /api/v1/agents/{fqdn}      # Get agent details
GET  /api/v1/domains/{domain}   # Get domain info
GET  /api/v1/health             # Health check
GET  /api/v1/stats              # Directory statistics
```

#### Project Structure (Phase 1)
```
src/dns_aid/
├── directory/
│   ├── __init__.py
│   ├── models.py          # SQLAlchemy models
│   ├── database.py        # Async DB connection (asyncpg)
│   ├── repository.py      # Data access layer
│   └── search.py          # Search logic
├── api/
│   ├── __init__.py
│   ├── app.py             # FastAPI app
│   ├── dependencies.py    # DI for DB sessions
│   ├── schemas.py         # Pydantic request/response
│   └── routes/
│       ├── search.py
│       ├── agents.py
│       ├── domains.py
│       └── health.py
└── crawlers/
    ├── __init__.py
    ├── base.py            # Abstract crawler
    └── submission.py      # Domain submission handler
```

### 1.3 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Input Validation | Pydantic models with strict validation |
| SQL Injection | SQLAlchemy ORM, parameterized queries |
| Rate Limiting | API Gateway throttling (100 req/s default) |
| Authentication | API keys for submission (optional in Phase 1) |
| HTTPS Only | CloudFront with ACM certificate |
| Domain Verification | DNS TXT challenge (prevents spam) |

### 1.4 Performance Requirements

| Metric | Target | How |
|--------|--------|-----|
| API Latency (p95) | < 200ms | Lambda + RDS Proxy connection pooling |
| Search Latency | < 500ms | PostgreSQL GIN index |
| Concurrent Users | 100 | Lambda auto-scaling |
| Database Connections | 50 | RDS Proxy |

### 1.5 Testing Requirements

| Test Type | Coverage Target | Tools |
|-----------|-----------------|-------|
| Unit Tests | > 80% | pytest, pytest-asyncio |
| Integration Tests | Key flows | pytest + testcontainers (PostgreSQL) |
| API Tests | All endpoints | pytest + httpx |
| Load Tests | 100 concurrent | locust |

### 1.6 Definition of Done (Phase 1)

- [ ] Database deployed to RDS Serverless v2
- [ ] API deployed to Lambda + API Gateway
- [ ] Domain submission flow working end-to-end
- [ ] Search returns results from database
- [ ] All unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Load test: 100 req/s sustained
- [ ] Security scan passing (bandit, safety)
- [ ] Documentation: API reference
- [ ] Monitoring: CloudWatch dashboards

---

## Phase 2: Crawler Infrastructure
**Duration:** 3-4 weeks
**Goal:** Automated agent discovery via multiple methods

### 2.1 Deliverables

| Component | Description | Status |
|-----------|-------------|--------|
| Crawler Base | Abstract crawler interface | Required |
| Submission Crawler | Process verified domains | Required |
| Index Reader | Read _index._agents.* convention (primary active discovery) | Required |
| CT Log Monitor | Watch Certificate Transparency | Required |
| **Passive DNS Crawler** | **Discover agents via pDNS databases (shows ACTUAL usage)** | Required |
| Pattern Prober | Try common agent names as fallback | Required |
| NSEC Zone Walker | Enumerate DNSSEC zones (feature flag) | **Optional** ⚠️ |
| Scheduler | Crawl queue management | Required |

### 2.2 Crawler Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CRAWLER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   SQS Queues                    Lambda/Fargate Workers       │
│   ─────────                     ────────────────────         │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ submission- │──────────────│ Submission Crawler  │      │
│   │ queue       │              │ (Lambda - quick)    │      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ index-      │──────────────│ Index Reader        │      │
│   │ queue       │              │ (Lambda - quick)    │      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ ct-         │──────────────│ CT Log Monitor      │      │
│   │ queue       │              │ (Fargate - stream)  │      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ probe-      │──────────────│ Pattern Prober      │      │
│   │ queue       │              │ (Lambda - fallback) │      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ nsec-       │──────────────│ NSEC Walker ⚠️      │      │
│   │ queue       │              │ (Fargate - optional)│      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   ┌─────────────┐              ┌─────────────────────┐      │
│   │ pdns-       │──────────────│ Passive DNS Crawler │      │
│   │ queue       │              │ (Lambda - API calls)│      │
│   └─────────────┘              └─────────────────────┘      │
│                                                              │
│   EventBridge (cron)           ┌─────────────────────┐      │
│   ──────────────────           │ Re-crawl Scheduler  │      │
│   Every 6 hours ───────────────│ (Lambda)            │      │
│                                └─────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Crawler Implementations

#### Submission Crawler (Lambda)
```python
# Triggered when domain verified
async def crawl_domain(domain: str) -> CrawlResult:
    """
    Crawl a single domain for DNS-AID agents.
    Uses existing dns-aid.discover() and dns-aid.verify()
    """
    agents_found = []

    for protocol in ["mcp", "a2a", "https"]:
        try:
            discovery = await dns_aid.discover(domain, protocol=protocol)
            for agent in discovery.agents:
                # Verify each agent
                verification = await dns_aid.verify(agent.fqdn)
                agent.security_score = verification.security_score
                agents_found.append(agent)
        except Exception as e:
            logger.warning(f"Failed to discover {protocol} agents: {e}")

    return CrawlResult(domain=domain, agents=agents_found)
```

#### Index Reader (Lambda - Primary Active Discovery)
```python
async def read_index(domain: str) -> list[AgentRef] | None:
    """
    Read _index._agents.{domain} TXT record.
    Most efficient active discovery - 1 query returns all agents.
    """
    try:
        txt = await query_txt(f"_index._agents.{domain}")
        # Format: "agents=network:mcp,chat:a2a,billing:https"
        if txt and txt.startswith("agents="):
            agents_str = txt.split("=", 1)[1]
            return [
                AgentRef(name=p.split(":")[0], protocol=p.split(":")[1])
                for p in agents_str.split(",")
            ]
    except Exception as e:
        logger.warning(f"Index read failed for {domain}: {e}")
    return None
```

#### NSEC Zone Walker (Fargate - Optional ⚠️)
```python
# Feature flag - can be disabled if IETF objects
from config import ENABLE_NSEC_WALKER

async def walk_zone(domain: str) -> list[str]:
    """
    Walk NSEC chain to enumerate all _agents.* records.

    ⚠️ OPTIONAL: Controlled by ENABLE_NSEC_WALKER feature flag.
    IETF/DNSOP may object to zone enumeration.
    Falls back to pattern probing if disabled.
    """
    if not ENABLE_NSEC_WALKER:
        logger.info("NSEC walking disabled, using pattern probing")
        return await probe_patterns(domain)

    if not await domain_has_dnssec(domain):
        return await probe_patterns(domain)

    found_names = []
    current = f"_agents.{domain}"

    while True:
        try:
            nsec = await query_nsec(current)
            if nsec.next_name.endswith(f".{domain}"):
                if "_agents" in nsec.next_name:
                    found_names.append(nsec.next_name)
                current = nsec.next_name
            else:
                break  # Wrapped around
        except NXDomain:
            break

    return found_names
```

#### Pattern Prober (Lambda - Fallback)
```python
# Fallback when index not available
COMMON_NAMES = ["assistant", "chat", "api", "agent", "help", "support"]
PROTOCOLS = ["mcp", "a2a"]

async def probe_patterns(domain: str) -> list[Agent]:
    """
    Try common agent names as fallback discovery.
    Used when _index._agents.* not published.
    """
    found = []
    for name in COMMON_NAMES:
        for proto in PROTOCOLS:
            fqdn = f"_{name}._{proto}._agents.{domain}"
            try:
                if await svcb_exists(fqdn):
                    agent = await dns_aid.discover(domain, name=name, protocol=proto)
                    found.extend(agent)
            except Exception:
                pass  # Name doesn't exist, continue
    return found
```

#### CT Log Monitor (Fargate - Streaming)
```python
# Continuous stream processing
async def monitor_ct_logs():
    """
    Watch CT logs for new certificates matching agent patterns.
    """
    patterns = ["mcp.*", "agent.*", "a2a.*", "*._agents.*"]

    async for entry in ct_log_stream():
        for domain in entry.domains:
            if matches_any(domain, patterns):
                # Queue for crawling
                await sqs.send_message(
                    QueueUrl=SUBMISSION_QUEUE,
                    MessageBody=json.dumps({"domain": extract_base_domain(domain)})
                )
```

#### Passive DNS Crawler (Lambda - API Calls)
```python
# Discovers agents that are ACTUALLY BEING USED
# Credit: Steve Salo suggested observing what's already being queried

class PassiveDNSCrawler:
    """
    Discover agents via passive DNS databases.

    Key Advantage: Shows agents that are actually being QUERIED,
    not just published. Also provides popularity/usage data.
    """

    def __init__(self, provider: str = "infoblox"):
        # Infoblox is preferred (internal data, no external cost)
        # Fallback options: SecurityTrails, Farsight DNSDB
        self.provider = provider

    async def discover_agents(self) -> list[AgentRecord]:
        """Query pDNS for DNS-AID record patterns."""

        # Search patterns for DNS-AID records
        patterns = [
            "*._mcp._agents.*",
            "*._a2a._agents.*",
            "*._https._agents.*",
        ]

        agents = []
        for pattern in patterns:
            records = await self._query_pdns(pattern)
            for record in records:
                if record.rdatatype in ["SVCB", "TXT"]:
                    agent = parse_dns_aid_record(record)
                    # BONUS: Get popularity from query count!
                    agent.popularity_score = self._calculate_popularity(record.query_count)
                    agents.append(agent)

        return agents

    def _calculate_popularity(self, query_count: int) -> int:
        """Logarithmic scale: 1M queries = 100, 1K = 50, 1 = 0"""
        if query_count <= 0:
            return 0
        return min(100, int(math.log10(query_count) * 16.67))
```

**pDNS Provider Options:**

| Provider | Coverage | Cost | Notes |
|----------|----------|------|-------|
| **Infoblox (internal)** | Infoblox DNS traffic | Free (internal) | **Preferred - stakeholder requirement** |
| SecurityTrails | Good global coverage | $50-500/mo | Affordable starter option |
| Farsight DNSDB | Largest coverage (100B+ records) | $500-5000/mo | Gold standard but expensive |
| VirusTotal | Security-focused | Part of VT license | If org already has VT |

**Recommendation:** Use Infoblox internal pDNS data as primary source (per Wei Chen's stakeholder requirements). This provides:
1. Popularity data from real DNS query volumes
2. No external API cost
3. Proprietary competitive advantage

### 2.4 Performance & Scaling

| Component | Scaling Strategy |
|-----------|------------------|
| Submission Crawler | Lambda concurrency (1000 default) |
| Index Reader | Lambda concurrency (1000 default) |
| Pattern Prober | Lambda concurrency (500, rate-limited) |
| CT Monitor | Single Fargate task (streaming) |
| NSEC Walker ⚠️ | Fargate tasks (max 10 concurrent) - optional |
| **Passive DNS Crawler** | Lambda (scheduled daily), rate-limited to pDNS API limits |
| Database Writes | Batch inserts (100 agents/batch) |

### 2.5 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| DNS Query Safety | Timeout (10s), retry limit (3) |
| Rate Limiting | 10 queries/second per domain |
| Abuse Prevention | Blocklist for misbehaving domains |
| Data Validation | Verify SVCB/TXT format before storing |

### 2.6 Definition of Done (Phase 2)

- [ ] Submission crawler processing verified domains
- [ ] Index reader parsing _index._agents.* records (primary active discovery)
- [ ] Pattern prober as fallback for domains without index
- [ ] CT monitor detecting new agent certificates
- [ ] NSEC walker with feature flag (optional, can be disabled) ⚠️
- [ ] **Passive DNS crawler discovering agents from Infoblox pDNS data**
- [ ] **Popularity scores populated from pDNS query volumes**
- [ ] Scheduler re-crawling domains every 6 hours
- [ ] All crawlers have >80% test coverage
- [ ] Integration test: submit → crawl → search flow
- [ ] Monitoring: Crawler success/failure metrics
- [ ] Alerting: Failed crawl threshold
- [ ] Feature flag documentation for NSEC walker

---

## Phase 3: Ranking & Intelligence
**Duration:** 2-3 weeks
**Goal:** Trust scoring with Infoblox data integration + BANDAID custom params

### 3.1 Deliverables

| Component | Description |
|-----------|-------------|
| Security Scoring | DNSSEC, DANE, TLS verification |
| Popularity Scoring | DNS query volume (Infoblox data) |
| Threat Detection | IOC matching (Infoblox threat intel) |
| Ranking Algorithm | Combined score for search results |
| **BANDAID Custom SVCB Params** | `cap`, `cap-sha256`, `bap`, `policy` support |

### 3.1.1 BANDAID Custom SVCB Parameters (IETF Draft Alignment)

Per draft-mozleywilliams-dnsop-bandaid-02 Section 4.4.3, implement support for:

| Parameter | Key | Purpose | Implementation |
|-----------|-----|---------|----------------|
| `cap` | key65001 | Capability descriptor URN | Parse/publish capability schema reference |
| `cap-sha256` | key65002 | Integrity digest | Verify capability descriptor hasn't changed |
| `bap` | key65010 | BANDAID App Protocols | Advertise supported protocols (a2a/1, mcp/1) |
| `policy` | key65003 | Policy bundle URI | Jurisdiction/compliance signaling |
| `realm` | key65004 | Multi-tenant scope | Auth realm for federated agents |

**Example SVCB with custom params:**
```
_billing._mcp._agents.example.com. 600 IN SVCB 1 svc.example.com. (
    alpn="mcp"
    port=443
    mandatory=alpn,port,key65001
    key65001="cap=urn:cap:example:mcp:billing.v1"
    key65002="cap-sha256=yvZ0n7q8bE2gYkz..."
    key65010="bap=mcp/1,a2a/1"
)
```

**Files to create:**
- `src/dns_aid/core/svcb_params.py` — Custom parameter parsing/generation
- `src/dns_aid/core/capability_schema.py` — Capability descriptor handling
- `tests/unit/test_svcb_params.py` — Parameter validation tests

### 3.2 Scoring System

```python
class AgentRanking:
    """
    Multi-factor ranking algorithm.
    """

    def calculate_score(self, agent: Agent) -> RankingScore:
        return RankingScore(
            # Security (0-100) - from dns-aid.verify()
            security=self._security_score(agent),

            # Popularity (0-100) - from Infoblox DNS traffic
            popularity=self._popularity_score(agent),

            # Trust (0-100) - combined factors
            trust=self._trust_score(agent),

            # Threat flags - IOC indicators
            threats=self._threat_check(agent),

            # Final ranking score
            overall=self._weighted_score(agent)
        )

    def _security_score(self, agent: Agent) -> int:
        """
        Based on dns-aid.verify() results.
        """
        score = 0
        if agent.dnssec_valid:
            score += 40
        if agent.dane_valid:
            score += 30
        if agent.endpoint_reachable:
            score += 20
        if agent.tls_valid:
            score += 10
        return score

    def _popularity_score(self, agent: Agent) -> int:
        """
        Based on Infoblox DNS traffic data.
        Higher query volume = more popular = higher score.
        """
        # Logarithmic scale: 1M queries = 100, 1K = 50, 1 = 0
        if agent.query_count <= 0:
            return 0
        return min(100, int(math.log10(agent.query_count) * 16.67))

    def _threat_check(self, agent: Agent) -> list[ThreatFlag]:
        """
        Check against Infoblox threat intel.
        """
        flags = []

        # Check domain reputation
        reputation = self.infoblox.get_domain_reputation(agent.domain)
        if reputation.risk_score > 70:
            flags.append(ThreatFlag(
                type="domain_reputation",
                severity="high",
                details=reputation.details
            ))

        # Check IOC database
        iocs = self.infoblox.check_ioc(agent.endpoint_url)
        for ioc in iocs:
            flags.append(ThreatFlag(
                type="ioc_match",
                severity=ioc.severity,
                details=ioc.indicator
            ))

        return flags
```

### 3.3 Infoblox Integration

```python
class InfobloxDataClient:
    """
    Client for Infoblox proprietary data APIs.
    """

    async def get_query_volume(self, fqdn: str) -> QueryVolumeData:
        """
        Get DNS query volume for an FQDN.
        Uses Infoblox passive DNS data.
        """
        # API call to Infoblox data platform
        response = await self.client.get(
            f"{self.base_url}/dns/query-volume",
            params={"fqdn": fqdn, "period": "30d"}
        )
        return QueryVolumeData(**response.json())

    async def get_domain_reputation(self, domain: str) -> ReputationData:
        """
        Get domain reputation score.
        """
        response = await self.client.get(
            f"{self.base_url}/threat/domain-reputation",
            params={"domain": domain}
        )
        return ReputationData(**response.json())

    async def check_ioc(self, indicator: str) -> list[IOCMatch]:
        """
        Check indicator against IOC database.
        """
        response = await self.client.post(
            f"{self.base_url}/threat/ioc-lookup",
            json={"indicators": [indicator]}
        )
        return [IOCMatch(**m) for m in response.json()["matches"]]
```

### 3.4 Definition of Done (Phase 3)

- [ ] Security scoring integrated with dns-aid.verify()
- [ ] Infoblox data client implemented
- [ ] Popularity scoring from DNS traffic
- [ ] Threat detection from IOC database
- [ ] Search results ranked by combined score
- [ ] API returns threat flags for flagged agents
- [ ] Unit tests for all scoring functions
- [ ] Integration test with mock Infoblox data

---

## Phase 4: Scale & Production Hardening
**Duration:** 2-3 weeks
**Goal:** Production-ready at scale

### 4.1 Deliverables

| Component | Description |
|-----------|-------------|
| Caching Layer | Redis for API response caching |
| Search Upgrade | PostgreSQL → OpenSearch (if needed) |
| CDN | CloudFront for API edge caching |
| Multi-region | Active-passive failover |
| Monitoring | Full observability stack |

### 4.2 Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    CACHING ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Client                                                     │
│     │                                                        │
│     ▼                                                        │
│   CloudFront (Edge Cache)                                    │
│   TTL: 60s for /search, 300s for /agents/{fqdn}             │
│     │                                                        │
│     ▼                                                        │
│   API Gateway                                                │
│     │                                                        │
│     ▼                                                        │
│   Lambda                                                     │
│     │                                                        │
│     ├──► Redis (Application Cache)                          │
│     │    TTL: 300s for search results                       │
│     │    TTL: 600s for agent details                        │
│     │                                                        │
│     └──► RDS PostgreSQL (Source of Truth)                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Performance Targets (Production)

| Metric | Target |
|--------|--------|
| API Latency (p50) | < 50ms |
| API Latency (p95) | < 200ms |
| API Latency (p99) | < 500ms |
| Availability | 99.9% |
| Concurrent Users | 10,000 |
| Requests/Second | 1,000 |
| Database Connections | 500 (via RDS Proxy) |
| Index Size | 1M+ agents |

### 4.4 Monitoring & Alerting

| Metric | Alert Threshold |
|--------|-----------------|
| API Error Rate | > 1% for 5 min |
| API Latency p95 | > 1s for 5 min |
| Crawler Failures | > 10% for 1 hour |
| Database CPU | > 80% for 10 min |
| Lambda Errors | > 5% for 5 min |

### 4.5 Definition of Done (Phase 4)

- [ ] Redis caching reducing DB load by 80%
- [ ] CloudFront edge caching enabled
- [ ] Load test: 1000 req/s sustained
- [ ] Multi-AZ deployment for RDS
- [ ] Disaster recovery runbook documented
- [ ] CloudWatch dashboards for all components
- [ ] PagerDuty alerts configured
- [ ] Runbook for common incidents

---

## Phase 5: Web Interface & Enterprise Features
**Duration:** 3-4 weeks
**Goal:** User-facing search UI + enterprise features

### 5.1 Deliverables

| Component | Description |
|-----------|-------------|
| Web UI | Search interface (React/HTMX) |
| Domain Dashboard | For domain owners |
| API Keys | For programmatic access |
| Takedown API | Enterprise feature (paid) |
| Analytics | Usage reporting |

### 5.2 Web Interface

```
Technology Stack:
- Frontend: HTMX + Alpine.js (simple, fast)
- Styling: Tailwind CSS
- Hosting: S3 + CloudFront (static)
- API: Same Lambda backend
```

### 5.3 Enterprise Features (Paid via Infoblox)

| Feature | Description |
|---------|-------------|
| Takedown Requests | Report malicious agents |
| Private Agents | Enterprise-only visibility |
| Analytics Dashboard | Search/discovery metrics |
| SLA Support | Guaranteed response times |

### 5.4 Definition of Done (Phase 5)

- [ ] Web UI deployed and functional
- [ ] Domain owner dashboard
- [ ] API key management
- [ ] Takedown workflow (manual → Infoblox)
- [ ] Analytics tracking implemented
- [ ] Documentation: User guide

---

## Testing Strategy (All Phases)

### Test Pyramid

```
                    ┌─────────┐
                    │   E2E   │  10%
                    │  Tests  │
                   ─┴─────────┴─
                  ┌─────────────┐
                  │ Integration │  30%
                  │   Tests     │
                 ─┴─────────────┴─
                ┌─────────────────┐
                │   Unit Tests    │  60%
                │                 │
               ─┴─────────────────┴─
```

### Test Requirements per Phase

| Phase | Unit | Integration | E2E | Load |
|-------|------|-------------|-----|------|
| 1 | >80% | Key flows | Submit→Search | 100 req/s |
| 2 | >80% | Crawler→DB | Full crawl | 50 domains |
| 3 | >80% | Scoring | Ranking | - |
| 4 | >80% | Cache | Full flow | 1000 req/s |
| 5 | >70% | UI flows | User journey | 500 users |

---

## Security Checklist (All Phases)

| Category | Requirement | Phase |
|----------|-------------|-------|
| Input Validation | Pydantic strict mode | 1 |
| SQL Injection | ORM only, no raw SQL | 1 |
| Rate Limiting | API Gateway throttle | 1 |
| Authentication | API keys for write ops | 1 |
| HTTPS | TLS 1.2+ only | 1 |
| Secrets | AWS Secrets Manager | 1 |
| Logging | No PII in logs | 1 |
| Domain Verification | DNS TXT challenge | 1 |
| Crawler Safety | Timeout, retries, blocklist | 2 |
| Data Integrity | Verify DNS responses | 2 |
| Threat Detection | IOC flagging | 3 |
| DDoS Protection | CloudFront + WAF | 4 |
| Audit Logging | CloudTrail | 4 |

---

## Infrastructure as Code

```
infrastructure/
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── modules/
│   │   ├── api/           # Lambda + API Gateway
│   │   ├── database/      # RDS + RDS Proxy
│   │   ├── cache/         # ElastiCache Redis
│   │   ├── queues/        # SQS
│   │   ├── crawlers/      # Fargate + EventBridge
│   │   └── cdn/           # CloudFront
│   └── environments/
│       ├── dev.tfvars
│       ├── staging.tfvars
│       └── prod.tfvars
└── scripts/
    ├── deploy.sh
    ├── migrate.sh
    └── rollback.sh
```

---

## Timeline Summary (Updated for 10/10 Quality)

| Phase | Duration | Cumulative | Focus |
|-------|----------|------------|-------|
| **Phase 0: RFC Foundation** | 2-3 weeks | 3 weeks | IANA, Security, Privacy, Wire Format |
| Phase 1: Foundation | 3-4 weeks | 7 weeks | API + DB + Circuit Breakers |
| Phase 2: Crawlers | 3-4 weeks | 11 weeks | Discovery + Event Sourcing |
| Phase 3: Ranking | 2-3 weeks | 14 weeks | Infoblox + SOC2 Mapping |
| Phase 4: Scale | 3-4 weeks | 18 weeks | Active-Active + Zero-Trust |
| Phase 5: UI/Enterprise | 3-4 weeks | 22 weeks | WCAG + Compliance Docs |

**Total: ~5-6 months to RFC-quality production**

### Quality Score Breakdown

| Category | Current | With Enhancements | Gap |
|----------|---------|-------------------|-----|
| **RFC Compliance** | 4/10 | 10/10 | IANA, Security, Privacy, Wire Format |
| **Architecture** | 6/10 | 10/10 | Circuit breakers, Active-Active, Zero-Trust |
| **Code Quality** | 7/10 | 10/10 | OpenAPI, Property-based tests, SBOM |
| **Compliance** | 3/10 | 10/10 | SOC2, ISO27001, GDPR Article 30 |
| **Overall** | 5/10 | **10/10** | +20-30 weeks of work |

---

## Success Metrics

| Metric | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 |
|--------|---------|---------|---------|---------|---------|
| Indexed Agents | 100 | 1,000 | 5,000 | 20,000 | 50,000 |
| Domains | 20 | 200 | 1,000 | 5,000 | 10,000 |
| API Requests/day | 1K | 10K | 50K | 200K | 500K |
| Unique Users/month | 50 | 500 | 2,000 | 10,000 | 25,000 |

---

## Files to Create (Phase 1)

| Path | Purpose |
|------|---------|
| `src/dns_aid/directory/__init__.py` | Package init |
| `src/dns_aid/directory/models.py` | SQLAlchemy models |
| `src/dns_aid/directory/database.py` | Async DB connection |
| `src/dns_aid/directory/repository.py` | Data access layer |
| `src/dns_aid/directory/search.py` | Search logic |
| `src/dns_aid/api/__init__.py` | Package init |
| `src/dns_aid/api/app.py` | FastAPI application |
| `src/dns_aid/api/schemas.py` | Request/response models |
| `src/dns_aid/api/routes/search.py` | Search endpoints |
| `src/dns_aid/api/routes/agents.py` | Agent endpoints |
| `src/dns_aid/api/routes/domains.py` | Domain endpoints |
| `src/dns_aid/api/routes/health.py` | Health check |
| `src/dns_aid/crawlers/__init__.py` | Package init |
| `src/dns_aid/crawlers/base.py` | Abstract crawler |
| `src/dns_aid/crawlers/submission.py` | Submission handler |
| `tests/unit/directory/` | Directory tests |
| `tests/unit/api/` | API tests |
| `tests/integration/test_api.py` | API integration tests |
| `infrastructure/terraform/` | IaC |
| `docs/API-REFERENCE.md` | API documentation |

---

## Files to Create (Phase 2)

| Path | Purpose | Status |
|------|---------|--------|
| `src/dns_aid/crawlers/index_reader.py` | _index._agents.* convention reader (primary) | Required |
| `src/dns_aid/crawlers/pattern_prober.py` | Common name probing (fallback) | Required |
| `src/dns_aid/crawlers/ct_monitor.py` | Certificate Transparency monitor | Required |
| `src/dns_aid/crawlers/zone_walker.py` | NSEC zone enumeration | **Optional** ⚠️ |
| `src/dns_aid/crawlers/passive_dns.py` | **Passive DNS discovery (Infoblox pDNS data)** | Required |
| `src/dns_aid/crawlers/scheduler.py` | Crawl scheduling/orchestration | Required |
| `src/dns_aid/crawlers/config.py` | Feature flags (ENABLE_NSEC_WALKER, etc.) | Required |
| `src/dns_aid/clients/__init__.py` | External client package | Required |
| `src/dns_aid/clients/infoblox_pdns.py` | Infoblox passive DNS API client | Required |
| `tests/unit/crawlers/test_index_reader.py` | Index reader tests | Required |
| `tests/unit/crawlers/test_pattern_prober.py` | Pattern prober tests | Required |
| `tests/unit/crawlers/test_passive_dns.py` | pDNS crawler tests | Required |
| `tests/unit/crawlers/test_ct_monitor.py` | CT monitor tests | Required |
| `tests/unit/crawlers/test_zone_walker.py` | NSEC walker tests | **Optional** ⚠️ |
| `tests/integration/test_crawlers.py` | End-to-end crawler tests | Required |

---

## Verification (Phase 1)

```bash
# Run all tests
pytest tests/ -v --cov=dns_aid

# Run API locally
uvicorn dns_aid.api.app:app --reload

# Test endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/search?q=crm
curl -X POST http://localhost:8000/api/v1/domains/submit \
  -H "Content-Type: application/json" \
  -d '{"domain": "example.com"}'

# Load test
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

---

## RFC/Enterprise Grade Enhancements (10/10 Quality)

This section documents improvements required for IETF RFC submission and enterprise audit readiness.

### Phase 0: Foundation Documents (Pre-Implementation)
**Duration:** 2-3 weeks
**Goal:** RFC-compliant documentation foundation

#### 0.1 IANA Considerations (RFC Mandatory)

| Registration | Registry | Status |
|--------------|----------|--------|
| `_agents` underscore name | RFC 8552 Underscored Names | Required |
| `mcp` ALPN identifier | TLS ALPN Protocol IDs | Required |
| `a2a` ALPN identifier | TLS ALPN Protocol IDs | Required |
| DNS-AID error codes | New registry | Proposed |

#### 0.2 Security Considerations (RFC Mandatory)

```
THREAT MODEL (STRIDE Analysis)
─────────────────────────────────────────────────────────────
Threat              Attack Vector                   Mitigation
─────────────────────────────────────────────────────────────
Spoofing           DNS cache poisoning             DNSSEC validation (MUST)
Tampering          Record modification             DNSSEC signing (MUST)
Repudiation        False agent claims              Domain verification (MUST)
Info Disclosure    Zone enumeration                NSEC3 recommendation (SHOULD)
Denial of Service  DNS amplification               Rate limiting (MUST)
Elevation          Unauthorized updates            TSIG authentication (MUST)
─────────────────────────────────────────────────────────────
```

#### 0.3 Privacy Considerations (GDPR Alignment)

| Requirement | Implementation |
|-------------|----------------|
| Data Minimization | Only index public DNS records |
| Right to Erasure | DELETE /api/v1/agents/{fqdn} with domain verification |
| Lawful Basis | Legitimate interest (public DNS data) |
| Data Retention | 90-day retention, then anonymization |
| Cross-border | DNS is global; document standard contractual clauses |
| pDNS Privacy | Infoblox DPA required; no individual query logging |

#### 0.4 Wire Protocol Format (ABNF Grammar)

```abnf
; DNS-AID SVCB Record Format (RFC 9460 compliant)
dns-aid-svcb = svc-priority SP target-name SP svc-params

svc-priority = 1*5DIGIT  ; 0-65535
target-name  = dns-name / "."
svc-params   = *(SP svc-param)

svc-param    = alpn-param / port-param / mandatory-param / unknown-param
alpn-param   = "alpn=" DQUOTE alpn-id *("," alpn-id) DQUOTE
port-param   = "port=" 1*5DIGIT
alpn-id      = "mcp" / "a2a" / "https" / 1*ALPHA

; DNS-AID TXT Record Format
dns-aid-txt  = capabilities-kv *(SP txt-kv)
capabilities-kv = "capabilities=" capability-list
capability-list = capability *("," capability)
capability   = 1*ALPHA
txt-kv       = key "=" value
```

#### 0.5 Error Code Registry

| Code | Name | Description | HTTP |
|------|------|-------------|------|
| DNS_AID_001 | DOMAIN_NOT_VERIFIED | Domain ownership not verified | 403 |
| DNS_AID_002 | AGENT_NOT_FOUND | Agent FQDN not in index | 404 |
| DNS_AID_003 | RATE_LIMITED | Too many requests | 429 |
| DNS_AID_004 | DNSSEC_INVALID | DNSSEC validation failed | 422 |
| DNS_AID_005 | SVCB_MALFORMED | Invalid SVCB record format | 422 |
| DNS_AID_006 | CRAWL_FAILED | Crawler could not reach domain | 502 |
| DNS_AID_007 | THREAT_DETECTED | IOC match found | 451 |

#### 0.6 Versioning & Extension Mechanism

```
API Versioning:
- URL path versioning: /api/v1/, /api/v2/
- Sunset header for deprecation: Sunset: Sat, 01 Jan 2028 00:00:00 GMT
- 12-month deprecation notice minimum

Protocol Extensions:
- New SVCB parameters: Register via IANA "DNS SVCB" registry
- New TXT keys: Prefix with "x-" for experimental, then standardize
- Capability discovery: GET /api/v1/capabilities
```

#### 0.7 Architecture Decision Records (ADRs)

| ADR | Decision | Rationale |
|-----|----------|-----------|
| ADR-001 | PostgreSQL over DynamoDB | Full-text search, ACID, GIN indexes |
| ADR-002 | Lambda + Fargate hybrid | Cost optimization for mixed workloads |
| ADR-003 | Infoblox pDNS over Farsight | Internal data, zero external cost |
| ADR-004 | SVCB over custom records | RFC 9460 compliance, broad support |
| ADR-005 | Active-Active over Active-Passive | Zero RPO, global availability |

---

### Architecture Enhancements (Enterprise Grade)

#### Resilience Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                  RESILIENCE ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  External APIs (Infoblox, CT Logs, DNS)                     │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────┐                    │
│  │       CIRCUIT BREAKER (per service) │                    │
│  │  ┌─────────┐ ┌─────────┐ ┌────────┐ │                    │
│  │  │ Closed  │→│  Open   │→│ Half-  │ │                    │
│  │  │(normal) │ │(failing)│ │ Open   │ │                    │
│  │  └─────────┘ └─────────┘ └────────┘ │                    │
│  │                                      │                    │
│  │  Failure threshold: 5 failures/30s   │                    │
│  │  Recovery timeout: 60s               │                    │
│  │  Half-open max requests: 3           │                    │
│  └─────────────────────────────────────┘                    │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────┐                    │
│  │       BULKHEAD ISOLATION            │                    │
│  │                                      │                    │
│  │  Crawler Pool: 10 concurrent max     │                    │
│  │  API Pool: 100 concurrent max        │                    │
│  │  Infoblox Pool: 5 concurrent max     │                    │
│  └─────────────────────────────────────┘                    │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────────────────────────┐                    │
│  │       RETRY WITH EXPONENTIAL BACKOFF │                   │
│  │                                      │                    │
│  │  Initial: 100ms                      │                    │
│  │  Max: 30s                            │                    │
│  │  Multiplier: 2x                      │                    │
│  │  Jitter: ±20%                        │                    │
│  └─────────────────────────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Active-Active Multi-Region (Phase 4 Upgrade)

```
┌─────────────────────────────────────────────────────────────┐
│                ACTIVE-ACTIVE ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   Route 53 (Latency-Based Routing)                          │
│              │                                               │
│    ┌─────────┴─────────┐                                    │
│    ▼                   ▼                                     │
│                                                              │
│  ┌───────────────┐   ┌───────────────┐                      │
│  │   US-EAST-1   │   │   EU-WEST-1   │                      │
│  │               │   │               │                      │
│  │  CloudFront   │   │  CloudFront   │                      │
│  │      │        │   │      │        │                      │
│  │  API Gateway  │   │  API Gateway  │                      │
│  │      │        │   │      │        │                      │
│  │    Lambda     │   │    Lambda     │                      │
│  │      │        │   │      │        │                      │
│  │  RDS Primary ◄┼───┼► RDS Replica  │                      │
│  │               │   │               │                      │
│  │  ElastiCache  │   │  ElastiCache  │                      │
│  │   (Global)    │   │   (Global)    │                      │
│  └───────────────┘   └───────────────┘                      │
│                                                              │
│  Conflict Resolution: Last-Write-Wins with vector clocks    │
│  Data Residency: EU data stays in EU (GDPR)                 │
│  RPO: 0 (synchronous for critical data)                     │
│  RTO: < 30 seconds (automatic failover)                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### Zero-Trust Security Model

| Layer | Implementation |
|-------|----------------|
| Network | VPC with no public subnets; all traffic via VPC endpoints |
| Identity | IAM roles per function; no shared credentials |
| Service-to-Service | mTLS via AWS App Mesh |
| Secrets | AWS Secrets Manager with automatic rotation (30-day) |
| Data | Encryption at rest (KMS CMK); in transit (TLS 1.3) |
| Audit | CloudTrail + GuardDuty + Security Hub |

#### Event Sourcing for Audit Trail

```
┌─────────────────────────────────────────────────────────────┐
│                  EVENT SOURCING ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Commands                     Events                         │
│  ────────                     ──────                         │
│                                                              │
│  SubmitDomain ───────────────► DomainSubmitted              │
│  VerifyDomain ───────────────► DomainVerified               │
│  CrawlDomain  ───────────────► AgentDiscovered              │
│                               AgentUpdated                   │
│                               AgentRemoved                   │
│  DeleteAgent  ───────────────► AgentDeleted                 │
│                                                              │
│  Event Store (DynamoDB Streams → Kinesis → S3)              │
│  ─────────────────────────────────────────────              │
│  │ event_id │ timestamp │ type │ aggregate │ payload │      │
│  │ uuid     │ ISO8601   │ str  │ fqdn      │ json    │      │
│                                                              │
│  Benefits:                                                   │
│  - Complete audit trail (SOC2/ISO27001)                     │
│  - Event replay for debugging                               │
│  - CQRS: Separate read models for search                    │
│  - 7-year retention for compliance                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Code Quality Enhancements

#### OpenAPI 3.1 Specification (Required)

```yaml
# docs/openapi.yaml (Phase 1 deliverable)
openapi: "3.1.0"
info:
  title: DNS-AID Agent Directory API
  version: "1.0.0"
  license:
    name: Apache 2.0
    identifier: Apache-2.0
servers:
  - url: https://api.dns-aid.io/v1
security:
  - ApiKeyAuth: []
paths:
  /search:
    get:
      operationId: searchAgents
      parameters:
        - name: q
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Search results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'
```

#### Testing Pyramid Enhancement

| Test Type | Current | Target | Tools |
|-----------|---------|--------|-------|
| Unit Tests | >80% | >90% | pytest |
| Property-Based | None | Key parsers | Hypothesis |
| Mutation Testing | None | >70% score | mutmut |
| Contract Testing | None | All APIs | Pact |
| Performance | Load tests | Benchmarks | pytest-benchmark |
| Security | bandit | Full SAST/DAST | Snyk, OWASP ZAP |

#### SBOM & Supply Chain Security

```yaml
# .github/workflows/sbom.yml
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    format: spdx-json
    output-file: sbom.spdx.json

- name: Sign SBOM
  uses: sigstore/cosign-installer@v3
  run: cosign attest --predicate sbom.spdx.json

- name: Verify Dependencies
  uses: snyk/actions/python@master
  with:
    command: test --severity-threshold=high
```

---

### Compliance Documentation

#### SOC2 Type II Control Mapping

| SOC2 Control | Implementation | Evidence |
|--------------|----------------|----------|
| CC6.1 Logical Access | IAM roles, API keys | CloudTrail logs |
| CC6.6 System Boundaries | VPC, Security Groups | AWS Config |
| CC7.2 System Monitoring | CloudWatch, GuardDuty | Dashboards, Alerts |
| CC7.3 Change Management | GitOps, PR reviews | GitHub audit log |
| CC8.1 Data Integrity | DNSSEC validation | Verification reports |
| A1.1 Availability | Multi-AZ, Auto-scaling | SLA metrics |

#### ISO 27001 Annex A Alignment

| Control | Status | Documentation |
|---------|--------|---------------|
| A.9 Access Control | Implemented | IAM policy docs |
| A.10 Cryptography | Implemented | KMS key policy |
| A.12 Operations | Planned | Runbooks |
| A.14 System Acquisition | Planned | SDLC policy |
| A.18 Compliance | Planned | Compliance matrix |

#### GDPR Article 30 Records

| Processing Activity | Data Categories | Lawful Basis | Retention |
|---------------------|-----------------|--------------|-----------|
| Agent Indexing | Public DNS records | Legitimate interest | 90 days |
| Domain Verification | Email, DNS TXT | Contract | Until unverified |
| pDNS Popularity | Aggregated query counts | Legitimate interest | 30 days |
| Threat Detection | IOC matches | Legitimate interest | 7 years |

---

### Files to Create (Phase 0)

| Path | Purpose |
|------|---------|
| `docs/rfc/security-considerations.md` | RFC Security section |
| `docs/rfc/privacy-considerations.md` | RFC Privacy section |
| `docs/rfc/iana-considerations.md` | RFC IANA registrations |
| `docs/rfc/wire-format.abnf` | Protocol grammar |
| `docs/openapi.yaml` | OpenAPI 3.1 specification |
| `docs/asyncapi.yaml` | Event schemas |
| `docs/adr/` | Architecture Decision Records |
| `docs/compliance/soc2-mapping.md` | SOC2 control matrix |
| `docs/compliance/gdpr-article30.md` | GDPR records |
| `.github/workflows/sbom.yml` | SBOM generation |
| `.github/workflows/security.yml` | Security scanning |

---

## Competitive Landscape

### Why This Matters for v2

The Agent Directory competes directly with platforms that want to own agent discovery. Understanding the competitive landscape helps position DNS-AID correctly.

| Competitor | Model | DNS-AID Differentiation |
|------------|-------|------------------------|
| **GoDaddy ANS** | Centralized registry (they own the database) | We index DNS, we don't own it - decentralized |
| **Google (A2A + UCP)** | Full-stack: discovery via Gemini/Search, payments via UCP | Neutral discovery; no platform lock-in or transaction fees |
| **ai.txt (Cloudflare/OpenAI)** | Simple HTTP file at /.well-known/ | Cryptographic verification (DNSSEC), not spoofable |
| **AgentDNS (China Telecom)** | DNS-based, state-controlled | Independent governance, not nation-state controlled |

### Google's Full-Stack Play (Key Risk)

Google is building end-to-end agent infrastructure:
- **A2A** - Agent communication protocol (open standard)
- **UCP** - Universal Commerce Protocol for payments in AI interfaces
  - https://developers.google.com/merchant/ucp
- **Discovery via Gemini/Search** - Find agents through Google AI surfaces

**The Risk:** Google wants agents discovered through THEIR surfaces, not DNS:
1. Google controls visibility (pay-to-rank)
2. Google takes transaction fees via UCP
3. Independent agents become invisible

**DNS-AID's Counter-Position:**
- We're protocol-agnostic (supports A2A, MCP, HTTPS)
- We provide neutral, decentralized discovery
- No transaction fees, no platform lock-in
- Complements Google's protocols without competing on commerce
