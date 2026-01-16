# DNS-AID Task Completion Checklist

## Before Marking a Task Complete

### 1. Code Quality
```bash
# Run linter
ruff check src/

# Run formatter
ruff format src/

# Run type checker
mypy src/
```

### 2. Testing
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run with coverage (target: >80%)
pytest --cov=dns_aid --cov-report=term-missing
```

### 3. Documentation
- Ensure docstrings are added for new public functions
- Update README.md if adding new features
- Update CHANGELOG.md for significant changes

### 4. Security
- Never store secrets in code or logs
- Validate all inputs with Pydantic
- Ensure DNSSEC validation is enforced for public DNS queries

## Common Verification Commands

```bash
# Quick validation (run all)
ruff check src/ && ruff format src/ --check && pytest tests/unit/ -q

# Full validation
ruff check src/ && mypy src/ && pytest --cov=dns_aid
```

## DNS Standards Compliance
When working with DNS records, ensure compliance with:
- RFC 9460: SVCB/HTTPS records
- RFC 4033-4035: DNSSEC
- RFC 6698: DANE TLSA
- RFC 8552: Underscored naming convention
- IETF draft-mozleywilliams-dnsop-bandaid-02

## Git Commit Guidelines
- Use conventional commits format
- Include tests with new features
- Don't commit secrets or credentials
