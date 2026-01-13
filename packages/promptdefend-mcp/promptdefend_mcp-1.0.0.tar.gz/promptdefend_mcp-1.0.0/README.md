# Prompt Defend MCP Server (Python)

A Model Context Protocol (MCP) server that exposes Prompt Defend's 16-layer guardrail system as tools for AI agents.

## Installation

```bash
pip install promptdefend-mcp
```

Or install from source:

```bash
cd framework/promptdefend-mcp/python
pip install -e .
```

## Quick Start

### As a Standalone Server

```bash
promptdefend-mcp --api-key your-api-key
```

### With Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "promptdefend": {
      "command": "promptdefend-mcp",
      "args": ["--api-key", "your-api-key"]
    }
  }
}
```

## Available Tools

### `scan_prompt`
Scan a prompt for security threats using 16-layer guardrails.

**Input:**
```json
{
  "prompt": "string - The prompt to scan"
}
```

**Output:**
```json
{
  "safe": true,
  "reason": "No threats detected",
  "details": {...}
}
```

### `check_blocklist`
Check if a prompt contains known attack keywords.

**Input:**
```json
{
  "prompt": "string - The prompt to check"
}
```

### `check_allowlist`
Check if a prompt matches safe/educational phrases.

**Input:**
```json
{
  "prompt": "string - The prompt to check"
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PROMPTDEFEND_API_KEY` | Your Prompt Defend API key |
| `PROMPTDEFEND_BASE_URL` | Custom API endpoint (optional) |

## License

Proprietary - See LICENSE for details.

---

© 2026 Prompt Defend. All Rights Reserved.
