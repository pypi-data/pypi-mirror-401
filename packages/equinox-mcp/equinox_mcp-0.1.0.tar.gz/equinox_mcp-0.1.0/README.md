# equinox-mcp

MCP (Model Context Protocol) server for [Equinox](https://github.com/patrick-kidger/equinox) documentation.

Enables LLMs to access up-to-date Equinox documentation and validate generated code.

## Installation

```bash
pip install equinox-mcp
```

Or run without installing:

```bash
uvx equinox-mcp
```

## Usage with Claude Code

```bash
# Add as MCP server
claude mcp add -t stdio -s user equinox -- python -m equinox_mcp

# Or with uvx
claude mcp add -t stdio -s user equinox -- uvx equinox-mcp
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `EQUINOX_DOCS_PATH` | (none) | Path to local Equinox docs directory (offline mode) |
| `EQUINOX_MCP_CACHE_DIR` | `~/.cache/equinox-mcp` | Cache directory for online mode |
| `EQUINOX_MCP_CACHE_TTL` | `24` | Cache TTL in hours |
| `EQUINOX_MCP_NO_CACHE` | `0` | Set to `1` to disable caching |

### Offline Mode

Point to a local Equinox clone for offline access:

```bash
export EQUINOX_DOCS_PATH=/path/to/equinox/docs
python -m equinox_mcp
```

### Online Mode (Default)

Fetches docs from GitHub with local caching:

```bash
python -m equinox_mcp
# Fetches from: raw.githubusercontent.com/patrick-kidger/equinox/main/docs/
```

## Available Tools

| Tool | Description |
|------|-------------|
| `list-sections` | List all available documentation sections |
| `get-documentation` | Fetch specific documentation content |
| `equinox-checker` | Validate Equinox module code |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
