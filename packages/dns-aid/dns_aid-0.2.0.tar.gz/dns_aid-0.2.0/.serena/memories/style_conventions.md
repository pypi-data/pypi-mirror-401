# DNS-AID Code Style & Conventions

## General Principles
- **Type hints**: Required for all public functions
- **Docstrings**: All public functions must be documented
- **Async**: Use async/await for all I/O operations
- **Logging**: Use structlog for structured logging

## Code Style
- **Line length**: 100 characters (ruff config)
- **Python version**: 3.11+
- **Formatter**: ruff format
- **Linter**: ruff (rules: E, F, I, N, W, UP, B, C4, SIM)

## Naming Conventions
- **Classes**: PascalCase (e.g., `AgentRecord`, `DDNSBackend`)
- **Functions/methods**: snake_case (e.g., `publish_agent`, `create_svcb_record`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_TTL`)
- **Private**: Leading underscore (e.g., `_validate_domain`)

## File Organization
```
src/dns_aid/
├── core/           # Domain models and core logic
│   ├── models.py   # Pydantic models (AgentRecord, Protocol, etc.)
│   ├── publisher.py
│   ├── discoverer.py
│   └── validator.py
├── backends/       # DNS provider implementations
│   ├── base.py     # Abstract base class (DNSBackend)
│   ├── route53.py
│   ├── ddns.py
│   └── mock.py     # For testing
├── cli/            # Typer CLI commands
├── mcp/            # MCP server
└── utils/          # Helpers (logging, validation)
```

## Backend Pattern
All DNS backends inherit from `DNSBackend` (ABC) and implement:
- `create_svcb_record()`
- `create_txt_record()`
- `delete_record()`
- `list_records()`
- `zone_exists()`
- `publish_agent()` (default implementation in base)

## Model Pattern
Use Pydantic for all data models:
```python
from pydantic import BaseModel, Field

class AgentRecord(BaseModel):
    name: str = Field(..., description="Agent name")
    domain: str
    protocol: Protocol
    # ...
```

## Async Pattern
All I/O operations are async:
```python
async def publish(
    name: str,
    domain: str,
    protocol: str,
    endpoint: str,
    **kwargs
) -> PublishResult:
    ...
```

## Error Handling
- Use specific exceptions where appropriate
- Log errors with structlog before raising
- Return result objects with success/failure status for CLI operations

## Testing
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- Use pytest-asyncio for async tests
- Use `MockBackend` for unit testing DNS operations
