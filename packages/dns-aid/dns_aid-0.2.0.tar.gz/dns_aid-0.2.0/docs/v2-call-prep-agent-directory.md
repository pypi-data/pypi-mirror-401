# DNS-AID v2: Agent Directory - Call Prep Document

**Purpose:** Prep document for Wednesday Engineering call with Wei Chen, Scott H., and team.
**Date:** 2026-01-13

---

## SLACK REPLY MESSAGE (Copy-Paste)

```
Thanks Wei, glad the work resonated with everyone.

Yes, this is absolutely doable. I've already analyzed the Gemini write-up and drafted a technical plan. The core idea is solid - we'd essentially build a search engine that crawls DNS-AID records and makes them searchable, similar to how Google crawls websites.

The good news: DNS-AID v1 already has most of the building blocks. The publish/discover/verify infrastructure is in place. What we'd add is:

1. A crawler that discovers agents across domains (using the NSEC zone walking, CT log monitoring, and submission methods mentioned in the write-up)
2. A searchable index (database + API)
3. A search interface (web UI)

Before I commit to delivery timelines, there are a few questions we should discuss on Wednesday:

GOVERNANCE
- Who operates this service long-term? Us? A foundation? Federated model?
- This determines who pays, who's liable, and who makes policy decisions (e.g., removing malicious agents)

SUSTAINABILITY
- Infrastructure costs are minimal to start (can do serverless for under $50/month)
- Real cost is ongoing maintenance - someone needs to monitor, update, respond to issues
- Do we have commitment for this beyond initial build?

ADOPTION
- A directory with 10 companies is useless. We need critical mass.
- How do we get organizations to publish agents AND submit for indexing?
- Who owns outreach/partnerships?

COMPETITIVE POSITIONING
- GoDaddy ANS is centralized (they own the registry)
- We're decentralized (we index DNS, we don't own it)
- Need to be clear on this differentiation

I've put together a detailed technical plan at docs/PLAN-v2-agent-directory.md covering architecture, phasing, and all the stakeholder questions. Happy to walk through it Wednesday.

The short answer: Yes, we can build this. The longer answer: Let's align on governance and sustainability before I start coding.
```

---

## DETAILED RECAP FOR WEDNESDAY CALL

### What Was Proposed (From Gemini 3 Deep Research Write-up)

Wei shared a proposal to build a "Google of Agents/MCPs" - a searchable directory that indexes the decentralized DNS-AID ecosystem. Key points from the write-up:

**1. The Problem Statement**
- DNS-AID enables decentralized agent publishing (unlike GoDaddy's centralized ANS)
- But decentralization is useless without discovery - how do you find agents across all domains?
- Proposal: Build an aggregated, searchable index by "crawling" DNS-AID compliant domains

**2. Three Discovery Methods Proposed**

| Method | How It Works | Technical Detail |
|--------|--------------|------------------|
| **NSEC Zone Walking** | Follow the NSEC chain in DNSSEC zones to enumerate all records | Requires zones use NSEC (not NSEC3). Orgs opt-in by creating "_public-agents" subdomain with NSEC enabled |
| **CT Log Monitoring** | Watch Certificate Transparency logs for new certs, then probe DNS | Real-time stream of new certificates. Filter for agent-like subdomains (mcp.*, agent.*, etc.) |
| **_index._agents.* Entry Point** | Standardized location where orgs advertise their agent catalog | Like robots.txt for agents. Gives orgs control over indexing |

**3. "Easy Button" Tools Proposed**

| Tool | Purpose | Complexity |
|------|---------|------------|
| **CoreDNS Plugin** | Auto-provision agent identities in Kubernetes. Watch K8s API, generate SVCB/TXT/TLSA records automatically | High - requires Go developer, DNSSEC signing is complex |
| **DNS-AID Wallet** | Standalone identity management daemon. Key generation, cert lifecycle, TLSA publishing, auto-rotation | High - cryptographic complexity |

---

### What DNS-AID v1 Already Has

| Component | Status | Notes |
|-----------|--------|-------|
| SVCB record creation | Done | Full BANDAID compliance |
| TXT record for capabilities | Done | Capabilities, version metadata |
| Multiple backends | Done | Route53, Infoblox, DDNS (RFC 2136) |
| Single-domain discovery | Done | discover() function works |
| DNSSEC validation | Done | Read-only validation |
| Security scoring | Done | 0-100 score based on DNSSEC, DANE, TLS |
| CLI | Done | publish, discover, verify, delete, list, zones |
| MCP Server | Done | 5 tools for AI assistant integration |

---

### What We Would Build (v2)

```
DNS-AID v1 (Current)              DNS-AID v2 (Proposed Addition)
────────────────────              ─────────────────────────────────

publish()  ──────────►  DNS       ┌─────────────────────────────┐
discover() ◄──────────  Records   │  CRAWLER                    │
verify()                          │  - Domain submission queue  │
                                  │  - NSEC zone walker         │
                                  │  - CT log monitor           │
                                  │  - _index.* reader          │
                                  └─────────────┬───────────────┘
                                                │
                                                ▼
                                  ┌─────────────────────────────┐
                                  │  AGENT INDEX                │
                                  │  - PostgreSQL database      │
                                  │  - Full-text search         │
                                  │  - Security/trust scoring   │
                                  └─────────────┬───────────────┘
                                                │
                                                ▼
                                  ┌─────────────────────────────┐
                                  │  PUBLIC API + WEB UI        │
                                  │  - GET /search?q=crm        │
                                  │  - GET /agents/{fqdn}       │
                                  │  - Search interface         │
                                  └─────────────────────────────┘
```

---

### Proposed Project Structure

```
DNS-AID/
├── src/dns_aid/
│   ├── core/              # Existing
│   ├── backends/          # Existing
│   ├── cli/               # Existing
│   ├── mcp/               # Existing
│   │
│   ├── directory/         # NEW - Agent index
│   │   ├── models.py      # SQLAlchemy models
│   │   ├── database.py    # DB connection
│   │   ├── search.py      # Search logic
│   │   └── ranking.py     # Trust/security ranking
│   │
│   ├── crawlers/          # NEW - Discovery
│   │   ├── submission.py  # Domain submission + verification
│   │   ├── zone_walker.py # NSEC enumeration
│   │   ├── ct_monitor.py  # Certificate Transparency
│   │   └── index_reader.py# _index._agents.* convention
│   │
│   └── api/               # NEW - Public API
│       ├── app.py         # FastAPI application
│       └── routes/        # Endpoints
```

---

### Estimated Effort

| Phase | Scope | Duration | Dependencies |
|-------|-------|----------|--------------|
| **Phase 1** | Domain submission, basic crawler, PostgreSQL index, REST API, simple web UI | 4-6 weeks | None |
| **Phase 2** | NSEC walker, CT monitor, _index.* convention, improved ranking | 4-6 weeks | Phase 1 |
| **Phase 3** | CoreDNS plugin (Go), DNS-AID Wallet | 8-12 weeks | Go developer, Phase 2 |

---

### Infrastructure Options

| Approach | Monthly Cost | Pros | Cons |
|----------|--------------|------|------|
| **Serverless (recommended start)** | $0-50 | Cheap, scales automatically | Cold starts, vendor lock-in |
| **Traditional VMs** | $200-500 | Full control | Ops burden |
| **At scale** | $1,000-3,000 | Handles traffic | Cost |

Serverless breakdown:
- Cloudflare Workers or AWS Lambda: $0-30/month
- Supabase/PlanetScale (managed DB): $0-25/month
- GitHub Actions (scheduled crawler): $0

---

### Competitive Landscape

| Competitor | Model | Strengths | Weaknesses |
|------------|-------|-----------|------------|
| **GoDaddy ANS** | Centralized registry - they own the database | Brand recognition, commercial backing | Vendor lock-in, single point of control, not sovereign |
| **ai.txt** | Simple text file at /.well-known/ai.txt | Dead simple, backed by Cloudflare/OpenAI | No cryptographic verification, HTTP-only, can be spoofed |
| **AgentDNS (China Telecom)** | DNS-based, Chinese research | Similar goals | Governance unclear, nation-state concerns |
| **Agent marketplaces** | Centralized platforms | Search exists | Platform lock-in, fees, not open |

**NEW: Google's Full-Stack Play (UCP)**

Google is building end-to-end agent infrastructure:
- **A2A** - Agent communication protocol
- **UCP** - Universal Commerce Protocol (payments in Gemini/Search) - https://developers.google.com/merchant/ucp
- **Discovery via Gemini/Search** - Find agents through Google AI surfaces

**The risk:** Google wants agents discovered through THEIR surfaces, not DNS. They control visibility + take transaction fees.

**Our differentiation:**
- Decentralized: We INDEX DNS, we don't OWN it
- Sovereign: Organizations control their own agents
- Secure: DNSSEC verification, trust scoring
- Open: Open source, no vendor lock-in
- **Not competing with Google** - We complement their protocols (A2A/MCP), just provide neutral discovery

---

### Questions to Resolve on Wednesday Call

**BLOCKER QUESTIONS (Must answer before committing)**

| # | Question | Options | Why It Matters |
|---|----------|---------|----------------|
| 1 | Who operates the directory service? | A) Us, B) Foundation, C) Federated, D) Commercial | Determines costs, liability, governance, neutrality |
| 2 | Do we have budget/commitment for ongoing operations? | Serverless: $0-50/month, Real cost is maintenance time | Service dies if no sustained commitment |
| 3 | How do we get organizations to adopt? | Manual outreach, DNS provider partnerships, AI assistant integration | Empty directory is useless |

**IMPORTANT QUESTIONS (Can answer during Phase 1)**

| # | Question | Options | Why It Matters |
|---|----------|---------|----------------|
| 4 | Is this meant to become a standard? | A) Just our impl, B) IETF informational, C) Full standardization | Affects timeline, resources, partnerships |
| 5 | How do we position vs GoDaddy ANS? | Compete? Complement? | Clear messaging needed |
| 6 | What are success metrics? | 100 orgs in 3 months? 1000 in 12 months? | Need go/no-go criteria |
| 7 | Legal/privacy considerations? | ToS, GDPR, liability | Need review before launch |

**CAN DEFER (Phase 3)**

| # | Question | Notes |
|---|----------|-------|
| 8 | Build CoreDNS plugin? | Requires Go developer, 8-12 weeks |
| 9 | Build DNS-AID Wallet? | Complex crypto, 6-8 weeks |

---

### Recommendation

**Short answer:** Yes, this is absolutely doable and aligns well with DNS-AID's mission.

**Before committing:**
1. Get clear answer on governance (who operates?)
2. Confirm ongoing commitment (not just build, but maintain)
3. Identify adoption strategy owner

**If green light:**
- Start with Phase 1 (4-6 weeks to MVP)
- Use serverless to minimize costs
- Validate with early adopters before scaling

---

### Related Documents

| File | Purpose |
|------|---------|
| `docs/PLAN-v2-agent-directory.md` | Full technical plan (25KB, detailed architecture, API specs, database schema) |
| `docs/v2-call-prep-agent-directory.md` | This document - call prep and Slack message |
