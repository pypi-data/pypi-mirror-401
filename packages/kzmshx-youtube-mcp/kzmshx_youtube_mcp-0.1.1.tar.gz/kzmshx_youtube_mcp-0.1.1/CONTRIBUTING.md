# Contributing

## Development Setup

```bash
# Clone and install
git clone https://github.com/kzmshx/kzmshx-youtube-mcp.git
cd kzmshx-youtube-mcp
uv sync
```

## Commands

```bash
make help       # Show all commands
make lint       # Run linter
make fix        # Auto-fix lint issues
make test       # Run tests
make typecheck  # Run type checker
make dev        # Launch MCP Inspector
```

## MCP Inspector

`make dev` launches [MCP Inspector](https://github.com/modelcontextprotocol/inspector) at http://localhost:6274 for interactive testing.

Features:

- Browse and test tools interactively
- View request/response payloads
- Test different input parameters

## Testing

Tests use pytest with pytest-asyncio. Run with:

```bash
make test
```

For FastMCP Client-based integration tests, use the async fixture pattern:

```python
import pytest
from fastmcp import Client

@pytest.fixture
async def client():
    from youtube_mcp.server import mcp
    async with Client(transport=mcp) as c:
        yield c

async def test_get_transcript(client):
    result = await client.call_tool("get_transcript", {"url": "VIDEO_ID"})
    assert result is not None
```

## Code Style

- Formatter/Linter: Ruff
- Type checker: mypy (strict mode)
- Line length: 120

Run `make fix` before committing.

## Commit Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `refactor:` Code refactoring
- `test:` Tests
- `chore:` Maintenance
