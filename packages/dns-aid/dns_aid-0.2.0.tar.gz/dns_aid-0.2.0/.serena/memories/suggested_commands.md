# DNS-AID Development Commands

## Installation
```bash
# Install in development mode with all dependencies
pip install -e ".[dev,cli,mcp]"

# Install specific backends
pip install -e ".[route53]"    # AWS Route 53
pip install -e ".[infoblox]"   # Infoblox BloxOne/NIOS
```

## Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=dns_aid --cov-report=html

# Run specific test file
pytest tests/unit/test_models.py -v

# Run integration tests (requires setup)
DDNS_TEST_ENABLED=1 pytest tests/integration/test_ddns.py -v
```

## Linting & Formatting
```bash
# Lint with ruff
ruff check src/

# Auto-fix lint issues
ruff check src/ --fix

# Format code
ruff format src/

# Type checking
mypy src/
```

## CLI Usage
```bash
# Publish an agent
dns-aid publish -n agent-name -d example.com -p mcp --endpoint mcp.example.com

# Discover agents
dns-aid discover -d example.com -p mcp

# Verify agent security
dns-aid verify -d example.com -n agent-name -p mcp

# Delete agent
dns-aid delete -n agent-name -d example.com -p mcp

# List agents in zone
dns-aid list -d example.com

# List available zones
dns-aid zones
```

## MCP Server
```bash
# Run MCP server
python -m dns_aid.mcp.server

# Or via entry point
dns-aid-mcp
```

## Environment Variables
```bash
# Route 53
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1

# DDNS (RFC 2136)
export DDNS_SERVER=ns1.example.com
export DDNS_KEY_NAME=dns-aid-key
export DDNS_KEY_SECRET=base64secret==
export DDNS_PORT=53  # optional
```

## Docker
```bash
# Build image
docker build -t dns-aid .

# Run BIND9 for integration testing
cd tests/integration/bind && docker-compose up -d
```

## System Commands (macOS/Darwin)
```bash
# File operations
ls -la
find . -name "*.py"
grep -r "pattern" src/

# Git
git status
git diff
git log --oneline -10

# DNS testing
dig @8.8.8.8 _agent._mcp._agents.example.com SVCB
dig @8.8.8.8 _agent._mcp._agents.example.com TXT
```
