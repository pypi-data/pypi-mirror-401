# Stealerlo.gs MCP Server (Python)

Model Context Protocol (MCP) server that exposes Stealerlo.gs search + utility tools to AI assistants (e.g. Claude Desktop, Cursor).

## Features

- **10 tools** covering core API endpoints
- **API key authentication only** - no JWT tokens required
- Works with Claude Desktop, Cursor, and any MCP-compatible client

## Available Tools

| Tool | Description |
|------|-------------|
| `search` | Search stealerlog records (email, username, password, site, email_domain, url, phone, name, ip, uuid, app) |
| `osint_search` | Query external OSINT providers (Snusbase, OSINTDog, Shodan, IntelX, Premier OSINT Provider, EnformionGO, OSINT Industries) |
| `ip_lookup` | IP geolocation and network info |
| `phone_lookup` | Reverse phone lookup with caller ID |
| `machine_info` | Get system info for a machine UUID |
| `machine_files` | Retrieve files from a machine (passwords, txt files) |
| `count` | Count results without fetching |
| `scan_secrets` | TruffleHog secret detection (750+ types) |
| `health` | API health check |
| `stats` | Database record count |
| `ingestlog` | Ingestion pipeline logs |

## Install

```bash
pip install stealerlogs-mcp-server
```

Or install from source:

```bash
cd tools/mcp-server-python
pip install -e .
```

## Get an API Key

1. Go to https://search.stealerlo.gs
2. Sign in and navigate to your dashboard
3. Generate an API key (format: `slgs_...`)

## Run

```bash
stealerlogs-mcp
```

The server uses stdio transport and waits for MCP protocol messages.

## Claude Desktop Config

Add to `~/.config/Claude/claude_desktop_config.json` (Linux) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "stealerlo": {
      "command": "stealerlogs-mcp"
    }
  }
}
```

## Cursor Config

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "stealerlo": {
      "command": "stealerlogs-mcp"
    }
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STEALERLO_API_URL` | `https://api.stealerlo.gs` | API base URL |

## Example Usage

Once configured, you can ask your AI assistant:

- "Search for credentials from user@example.com"
- "Look up the IP address 8.8.8.8"
- "Run an OSINT search for example.com"
- "Scan this config file for exposed secrets"

The AI will automatically use the appropriate tools with your API key.

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector stealerlogs-mcp
```

This opens a web UI to test tools interactively.