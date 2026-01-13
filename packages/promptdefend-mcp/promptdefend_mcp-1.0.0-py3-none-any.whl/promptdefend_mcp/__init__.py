#!/usr/bin/env python3
"""
Prompt Defend MCP Server

A Model Context Protocol server that exposes Prompt Defend's 16-layer
guardrail system as tools for AI agents like Claude.
"""

import asyncio
import json
import os
import sys
from typing import Any, Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("Error: mcp package not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)

try:
    import httpx
except ImportError:
    print("Error: httpx package not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(1)


class PromptDefendMCP:
    """Prompt Defend MCP Server implementation."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.promptdefend.dev"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(
            headers={"X-API-Key": api_key},
            timeout=30.0
        )
    
    async def scan_prompt(self, prompt: str) -> dict:
        """Scan a prompt using Prompt Defend's 16-layer guardrails."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/guardrails/check",
                json={"prompt": prompt}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "safe": data.get("status") == "SAFE",
                    "status": data.get("status"),
                    "details": data.get("details", {}),
                    "fast_path": data.get("details", {}).get("fast_path", False)
                }
            elif response.status_code == 403:
                data = response.json()
                detail = data.get("detail", {})
                return {
                    "safe": False,
                    "status": "BLOCKED",
                    "error_type": detail.get("error_type"),
                    "reason": detail.get("message"),
                    "details": detail.get("details", {})
                }
            else:
                return {
                    "safe": False,
                    "status": "ERROR",
                    "error": f"API returned status {response.status_code}"
                }
        except Exception as e:
            return {
                "safe": False,
                "status": "ERROR",
                "error": str(e)
            }
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


def create_server(api_key: str, base_url: str = "https://api.promptdefend.dev") -> Server:
    """Create and configure the MCP server."""
    
    server = Server("promptdefend")
    pd = PromptDefendMCP(api_key, base_url)
    
    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """List available Prompt Defend tools."""
        return [
            Tool(
                name="scan_prompt",
                description="Scan a prompt for security threats using Prompt Defend's 16-layer guardrail system. Detects prompt injection, jailbreaks, DAN attacks, encoded payloads, and more.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt text to scan for security threats"
                        }
                    },
                    "required": ["prompt"]
                }
            ),
            Tool(
                name="validate_user_input",
                description="Validate user input before passing to an LLM. Returns safe=true if input is clean, safe=false with reason if threats detected.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "The user input to validate"
                        }
                    },
                    "required": ["input"]
                }
            ),
            Tool(
                name="get_security_report",
                description="Get a detailed security analysis report for a prompt, including which of the 16 guardrail layers flagged issues.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "The prompt to analyze"
                        }
                    },
                    "required": ["prompt"]
                }
            )
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls."""
        
        if name == "scan_prompt":
            prompt = arguments.get("prompt", "")
            result = await pd.scan_prompt(prompt)
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2)
            )]
        
        elif name == "validate_user_input":
            input_text = arguments.get("input", "")
            result = await pd.scan_prompt(input_text)
            
            if result.get("safe"):
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "valid": True,
                        "message": "Input is safe to process"
                    }, indent=2)
                )]
            else:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "valid": False,
                        "message": result.get("reason", "Security threat detected"),
                        "error_type": result.get("error_type"),
                        "details": result.get("details")
                    }, indent=2)
                )]
        
        elif name == "get_security_report":
            prompt = arguments.get("prompt", "")
            result = await pd.scan_prompt(prompt)
            
            report = {
                "prompt_length": len(prompt),
                "status": result.get("status"),
                "safe": result.get("safe"),
                "fast_path_used": result.get("fast_path", False),
                "layers_checked": 16,
                "details": result.get("details", {})
            }
            
            if not result.get("safe"):
                report["threat_detected"] = {
                    "type": result.get("error_type"),
                    "reason": result.get("reason")
                }
            
            return [TextContent(
                type="text",
                text=json.dumps(report, indent=2)
            )]
        
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"})
            )]
    
    return server


async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prompt Defend MCP Server")
    parser.add_argument("--api-key", type=str, help="Prompt Defend API key")
    parser.add_argument("--base-url", type=str, default="https://api.promptdefend.dev", help="API base URL")
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("PROMPTDEFEND_API_KEY")
    
    if not api_key:
        print("Error: API key required. Use --api-key or set PROMPTDEFEND_API_KEY", file=sys.stderr)
        sys.exit(1)
    
    server = create_server(api_key, args.base_url)
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)


if __name__ == "__main__":
    asyncio.run(main())
