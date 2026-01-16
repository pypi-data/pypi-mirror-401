#!/usr/bin/env python3
"""
Stealerlo.gs MCP Server - Python Implementation
Model Context Protocol server for Stealerlo.gs API

All endpoints use API key authentication (X-API-Key header).
Get your API key from https://search.stealerlo.gs
"""

import asyncio
import json
import os
import signal
import sys
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import httpx


API_BASE_URL = os.getenv("STEALERLO_API_URL", "https://api.stealerlo.gs")

# Create server instance
server = Server("stealerlogs-mcp-server")


def format_results(data: Any, max_items: int = 10) -> str:
    """Format API results for readable output"""
    if isinstance(data, dict):
        return json.dumps(data, indent=2, default=str)
    return str(data)


def get_headers(api_key: str) -> Dict[str, str]:
    """Get standard headers with API key"""
    return {
        "X-API-Key": api_key,
        "Content-Type": "application/json",
    }


# =============================================================================
# TOOL DEFINITIONS
# =============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        # --- Core Search ---
        Tool(
            name="search",
            description="""Search Stealerlo.gs stealerlog records.

Supports searching by: email, username, password, site, email_domain, url, phone, name, ip, uuid, app.
Returns credential and machine records.

Examples:
- Email: query="user@example.com", type="email"
- Email domain: query="example.com", type="email_domain"
- URL path: query="/wp-login.php", type="url"
- Wildcard: query="*@company.com", type="email", wildcard=true""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (email, username, password, domain, IP, phone, name, uuid)",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["email", "username", "password", "site", "email_domain", "url", "phone", "name", "ip", "uuid", "app"],
                        "description": "Type of search",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key (format: slgs_...)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results (default: 100, max: 1000)",
                        "default": 100,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Result offset for pagination",
                        "default": 0,
                    },
                    "useRegex": {
                        "type": "boolean",
                        "description": "Enable regex pattern matching",
                        "default": False,
                    },
                    "wildcard": {
                        "type": "boolean",
                        "description": "Enable wildcard pattern matching",
                        "default": False,
                    },
                    "dateFrom": {
                        "type": "string",
                        "description": "Filter from date (YYYY-MM-DD)",
                    },
                    "dateTo": {
                        "type": "string",
                        "description": "Filter to date (YYYY-MM-DD)",
                    },
                },
                "required": ["query", "type", "apiKey"],
            },
        ),
        
        # --- OSINT Proxy ---
        Tool(
            name="osint_search",
            description="""Search external OSINT providers through Stealerlo.gs proxy.

Providers:
- snusbase: Leak data and credential intelligence
- osintdog: Multiple OSINT services (HackCheck, BreachBase, etc.)
- shodan: Internet-wide scanning & host intelligence
- intelx: Intelligence X (restricted - accessPassword required)
- premierosint: Premier OSINT Provider (email/phone/username search)
- enformion: EnformionGO (restricted - accessPassword required)
- osintindustries: OSINT Industries (restricted - accessPassword required)

Examples:
- Snusbase email: provider="snusbase", action="search", query={"email": "user@example.com"}
- Snusbase domain: provider="snusbase", action="search", query={"domain": "example.com"}
- Shodan host: provider="shodan", action="host", query={"ip": "8.8.8.8"}
- OSINTDog: provider="osintdog", action="database", query={"query": "user@example.com", "search_type": "email"}
- Premier OSINT Provider: provider="premierosint", action="search", query={"email": "user@example.com"}""",
            inputSchema={
                "type": "object",
                "properties": {
                    "provider": {
                        "type": "string",
                        "enum": [
                            "snusbase",
                            "osintdog",
                            "shodan",
                            "intelx",
                            "premierosint",
                            "enformion",
                            "osintindustries",
                        ],
                        "description": "OSINT provider to query",
                    },
                    "action": {
                        "type": "string",
                        "description": "Provider-specific action (e.g., 'search', 'host', 'database')",
                    },
                    "query": {
                        "type": "object",
                        "description": "Provider-specific query payload",
                    },
                    "accessPassword": {
                        "type": "string",
                        "description": "Access password for restricted providers",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["provider", "action", "query", "apiKey"],
            },
        ),
        
        # --- IP Lookup ---
        Tool(
            name="ip_lookup",
            description="""Get geolocation and network information for IP addresses.
Batch lookup up to 100 IPs. Returns: city, country, ISP, AS, coordinates, timezone.

Example: terms=["8.8.8.8", "1.1.1.1"]""",
            inputSchema={
                "type": "object",
                "properties": {
                    "terms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of IP addresses (max 100)",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["terms", "apiKey"],
            },
        ),
        
        # --- Phone Lookup ---
        Tool(
            name="phone_lookup",
            description="""Reverse phone number lookup. Get caller name, carrier, location, phone type.
Batch lookup up to 10 numbers. Supports international numbers.

Example: terms=["+19739833179"]""",
            inputSchema={
                "type": "object",
                "properties": {
                    "terms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of phone numbers (max 10)",
                    },
                    "countryCode": {
                        "type": "string",
                        "description": "Optional country code for disambiguation (e.g., '1' for US)",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["terms", "apiKey"],
            },
        ),
        
        # --- Machine Info ---
        Tool(
            name="machine_info",
            description="""Get comprehensive system information for a machine by UUID.
Returns: hardware specs, OS, network info, installed software, processes.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "uuid": {
                        "type": "string",
                        "description": "Machine UUID from search results",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["uuid", "apiKey"],
            },
        ),
        
        # --- Machine Files ---
        Tool(
            name="machine_files",
            description="""Get files from a machine by UUID.

File types:
- all_passwords: All password/credential files
- all_txt_files: All txt files from the machine
- passwords: Single password file (if only one exists)
- common_files: Download compressed Common Files archive""",
            inputSchema={
                "type": "object",
                "properties": {
                    "machine_id": {
                        "type": "string",
                        "description": "Machine UUID",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["all_passwords", "all_txt_files", "passwords", "common_files"],
                        "description": "Type of files to retrieve",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["machine_id", "type", "apiKey"],
            },
        ),
        
        # --- Count ---
        Tool(
            name="count",
            description="""Get count of results for a search query without fetching full results.
Useful for estimating result size before running full search.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "type": {
                        "type": "string",
                        "enum": ["email", "username", "password", "site", "email_domain", "url", "phone", "name", "ip", "uuid", "app"],
                        "description": "Type of search",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["query", "type", "apiKey"],
            },
        ),
        
        # --- TruffleHog Secret Scan ---
        Tool(
            name="scan_secrets",
            description="""Scan for exposed secrets with TruffleHog.
Supports machine UUID scans, raw text, or base64 content.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "machineId": {
                        "type": "string",
                        "description": "Machine UUID to scan all TXT files",
                    },
                    "content": {
                        "type": "string",
                        "description": "Text content to scan for secrets",
                    },
                    "base64Content": {
                        "type": "string",
                        "description": "Base64-encoded content to scan",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["apiKey"],
            },
        ),
        
        # --- Health Check ---
        Tool(
            name="health",
            description="Check API health status. No authentication required.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        
        # --- Database Stats ---
        Tool(
            name="stats",
            description="Get total record count in the database.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        
        # --- Ingestion Logs ---
        Tool(
            name="ingestlog",
            description="Retrieve ingestion pipeline logs with filtering and pagination.",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of logs to return (max 100)",
                        "default": 50,
                    },
                    "offset": {
                        "type": "integer",
                        "description": "Result offset",
                        "default": 0,
                    },
                    "dateFrom": {
                        "type": "string",
                        "description": "Start date filter (YYYY-MM-DD)",
                    },
                    "dateTo": {
                        "type": "string",
                        "description": "End date filter (YYYY-MM-DD)",
                    },
                    "apiKey": {
                        "type": "string",
                        "description": "Your Stealerlo.gs API key",
                    },
                },
                "required": ["apiKey"],
            },
        ),
    ]


# =============================================================================
# TOOL HANDLERS - Return list[TextContent] for MCP SDK
# =============================================================================

async def handle_search(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle search tool"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required. Get one at https://search.stealerlo.gs")]
    
    payload = {
        "query": args.get("query"),
        "type": args.get("type"),
    }
    
    # Optional parameters
    for key in ["limit", "offset", "useRegex", "wildcard", "dateFrom", "dateTo", "searchAfter"]:
        if key in args and args[key] is not None:
            payload[key] = args[key]
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/search",
            headers=get_headers(api_key),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        # Format results nicely
        total = data.get("total", 0)
        results = data.get("results", [])
        took = data.get("took", 0)
        
        output = f"## Search Results\n\n"
        output += f"**Query:** `{args.get('query')}` (type: {args.get('type')})\n"
        output += f"**Total:** {total} results | **Returned:** {len(results)} | **Time:** {took}ms\n\n"
        
        if results:
            output += "### Results\n\n"
            for i, result in enumerate(results[:20], 1):
                output += f"**{i}.** "
                result_type = result.get("type")
                if result_type == "credential":
                    if result.get("email"):
                        output += f"Email: `{result['email']}` "
                    if result.get("username"):
                        output += f"User: `{result['username']}` "
                    if result.get("password"):
                        output += f"Pass: `{result['password']}` "
                    if result.get("site"):
                        output += f"Site: `{result['site']}` "
                    if result.get("machine_id"):
                        output += f"Machine: `{result['machine_id']}`"
                elif result_type == "machine":
                    if result.get("uuid"):
                        output += f"UUID: `{result['uuid']}` "
                    if result.get("ip"):
                        output += f"IP: `{result['ip']}` "
                    if result.get("country"):
                        output += f"Country: `{result['country']}` "
                    if result.get("channel"):
                        output += f"Channel: `{result['channel']}`"
                else:
                    output += json.dumps(result, default=str)[:200]
                output += "\n"
            
            if len(results) > 20:
                output += f"\n... and {len(results) - 20} more results\n"
        else:
            output += "No results found.\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_osint_search(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle OSINT proxy search"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    payload = {
        "provider": args.get("provider"),
        "action": args.get("action"),
        "query": args.get("query"),
    }
    if args.get("accessPassword"):
        payload["accessPassword"] = args.get("accessPassword")
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/source",
            headers=get_headers(api_key),
            json=payload,
            timeout=60.0
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## OSINT Search Results\n\n"
        output += f"**Provider:** {args.get('provider')} | **Action:** {args.get('action')}\n\n"
        output += "```json\n"
        output += json.dumps(data, indent=2, default=str)[:5000]
        output += "\n```\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_ip_lookup(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle IP geolocation lookup"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/iplookup",
            headers=get_headers(api_key),
            json={"terms": args.get("terms", [])}
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## IP Lookup Results\n\n"
        
        results = data.get("results", {})
        for ip, info in results.items():
            output += f"### {ip}\n"
            output += f"- **Location:** {info.get('city', 'N/A')}, {info.get('country', 'N/A')}\n"
            output += f"- **ISP:** {info.get('isp', 'N/A')}\n"
            output += f"- **AS:** {info.get('as', 'N/A')}\n"
            output += f"- **Coords:** {info.get('lat', 'N/A')}, {info.get('lon', 'N/A')}\n"
            output += f"- **Timezone:** {info.get('timezone', 'N/A')}\n\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_phone_lookup(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle phone number lookup"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    payload = {"terms": args.get("terms", [])}
    if args.get("countryCode"):
        payload["countryCode"] = args["countryCode"]
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/phonelookup",
            headers=get_headers(api_key),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## Phone Lookup Results\n\n"
        
        results = data.get("results", {})
        for phone, info in results.items():
            output += f"### {info.get('formatted_number', phone)}\n"
            output += f"- **Name:** {info.get('name', 'Unknown')}\n"
            output += f"- **Location:** {info.get('location', 'N/A')}\n"
            output += f"- **Type:** {info.get('phone_type', 'N/A')}\n"
            carriers = info.get("carriers", [])
            if carriers:
                output += f"- **Carrier:** {carriers[0].get('company', 'N/A')}\n"
            output += "\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_machine_info(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle machine info lookup"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    try:
        response = await client.get(
            f"{API_BASE_URL}/machineinfo",
            headers=get_headers(api_key),
            params={"uuid": args.get("uuid")}
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## Machine Information\n\n"
        output += f"**UUID:** `{args.get('uuid')}`\n\n"
        system = data.get("system", {})
        hardware = data.get("hardware", {})
        network = data.get("network", {})
        output += f"- **Computer:** {system.get('computer_name', 'N/A')}\n"
        output += f"- **User:** {system.get('user_name', 'N/A')}\n"
        output += f"- **OS:** {system.get('os', 'N/A')} {system.get('os_version', '')}\n"
        output += f"- **IP:** {network.get('ip', 'N/A')}\n"
        output += f"- **CPU:** {hardware.get('cpu', 'N/A')}\n"
        output += f"- **RAM:** {hardware.get('ram_mb', 'N/A')}\n"
        output += f"- **GPU:** {hardware.get('gpu', 'N/A')}\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_machine_files(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle machine files retrieval"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    try:
        response = await client.get(
            f"{API_BASE_URL}/machine-files",
            headers=get_headers(api_key),
            params={
                "machine_id": args.get("machine_id"),
                "type": args.get("type") or args.get("file_type")
            }
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## Machine Files\n\n"
        output += f"**Machine:** `{args.get('machine_id')}`\n"
        output += f"**Type:** {args.get('type') or args.get('file_type')}\n\n"
        
        files = data.get("files", [])
        output += f"**Found:** {len(files)} files\n\n"
        
        for f in files[:10]:
            output += f"### {f.get('file_name', 'Unknown')}\n"
            output += f"Path: `{f.get('file_path', 'N/A')}`\n"
            content = f.get("content", "")
            if content:
                output += f"```\n{content[:1000]}\n```\n"
            output += "\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_count(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle count query"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/count",
            headers=get_headers(api_key),
            json={
                "query": args.get("query"),
                "type": args.get("type")
            }
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## Count Results\n\n"
        output += f"**Query:** `{args.get('query')}` (type: {args.get('type')})\n"
        output += f"**Count:** {data.get('count', 0):,} results\n"
        output += f"**Time:** {data.get('took', 0)}ms\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_scan_secrets(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle TruffleHog secret scanning"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    payload = {}
    if args.get("machineId"):
        payload["machineId"] = args.get("machineId")
    if args.get("content"):
        payload["content"] = args.get("content")
    if args.get("base64Content"):
        payload["base64Content"] = args.get("base64Content")
    if not payload:
        return [TextContent(type="text", text="Error: provide machineId, content, or base64Content")]
    
    try:
        response = await client.post(
            f"{API_BASE_URL}/trufflehog",
            headers=get_headers(api_key),
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        
        output = f"## Secret Scan Results\n\n"
        output += f"**Secrets Found:** {data.get('secretsFound', 0)}\n\n"
        
        results = data.get("results", [])
        for r in results:
            output += f"### {r.get('detectorName', 'Unknown')}\n"
            output += f"- **Verified:** {'✅' if r.get('verified') else '❌'}\n"
            output += f"- **Redacted:** `{r.get('redacted', 'N/A')}`\n"
            output += f"- **Line:** {r.get('line', 'N/A')}\n\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_health(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle health check"""
    try:
        response = await client.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        data = response.json()
        
        return [TextContent(
            type="text",
            text=f"## API Health\n\n**Status:** {data.get('status', 'unknown')}\n**Timestamp:** {data.get('timestamp', 'N/A')}"
        )]
        
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_stats(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle database stats"""
    try:
        response = await client.get(
            f"{API_BASE_URL}/count",
            headers=get_headers(args.get("apiKey")) if args.get("apiKey") else None
        )
        response.raise_for_status()
        data = response.json()
        
        count = data.get("count", 0)
        return [TextContent(
            type="text",
            text=f"## Database Statistics\n\n**Total Records:** {count:,}"
        )]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def handle_ingestlog(client: httpx.AsyncClient, args: Dict[str, Any]) -> list[TextContent]:
    """Handle ingestion log retrieval"""
    api_key = args.get("apiKey")
    if not api_key:
        return [TextContent(type="text", text="Error: apiKey is required")]
    
    params = {}
    for key in ["limit", "offset", "dateFrom", "dateTo"]:
        if args.get(key) is not None:
            params[key] = args[key]
    
    try:
        response = await client.get(
            f"{API_BASE_URL}/ingestlog",
            headers=get_headers(api_key),
            params=params
        )
        response.raise_for_status()
        data = response.json()
        
        output = "## Ingestion Logs\n\n"
        output += f"**Total:** {data.get('total', 0)} | **Size:** {data.get('size', 0)} | **Took:** {data.get('took', 0)}ms\n\n"
        logs = data.get("logs", [])
        for entry in logs[:10]:
            output += f"- **{entry.get('timestamp', 'N/A')}** {entry.get('source', 'N/A')} | {entry.get('status', 'N/A')}\n"
        if len(logs) > 10:
            output += f"\n... and {len(logs) - 10} more log entries\n"
        
        return [TextContent(type="text", text=output)]
        
    except httpx.HTTPStatusError as e:
        return [TextContent(type="text", text=f"Error: HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# =============================================================================
# TOOL ROUTER
# =============================================================================

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> list[TextContent]:
    """Route tool calls to handlers"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        handlers = {
            "search": handle_search,
            "osint_search": handle_osint_search,
            "ip_lookup": handle_ip_lookup,
            "phone_lookup": handle_phone_lookup,
            "machine_info": handle_machine_info,
            "machine_files": handle_machine_files,
            "count": handle_count,
            "scan_secrets": handle_scan_secrets,
            "health": handle_health,
            "stats": handle_stats,
            "ingestlog": handle_ingestlog,
        }
        
        handler = handlers.get(name)
        if handler:
            return await handler(client, arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]


# =============================================================================
# SERVER ENTRY POINT
# =============================================================================

async def _run_server():
    """Async server runner"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Main entry point for the MCP server (console script)"""
    def signal_handler(signum, frame):
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        asyncio.run(_run_server())
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
