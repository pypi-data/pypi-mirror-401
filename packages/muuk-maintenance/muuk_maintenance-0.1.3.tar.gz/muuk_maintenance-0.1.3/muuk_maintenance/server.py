#!/usr/bin/env python3
"""
MuukTest Maintenance MCP Server
Analyzes E2E test failures and provides repair suggestions.
"""
import asyncio
import json
import os
from pathlib import Path
from typing import Any, Dict, List

import requests
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from muuk_maintenance.utils import (
    ensure_dir,
    create_temp_zip,
    request_signed_url,
    upload_zip_to_s3,
    build_s3_path,
)

app = Server("muuk-maintenance")

# API Configuration
API_URL = os.getenv(
    "MUUK_API_URL",
    "https://bm5s428g6e.execute-api.us-east-2.amazonaws.com/staging",
)

MUUK_KEY = os.getenv("MUUK_KEY", "")
MUUK_AUTH_URL = "https://portal.muuktest.com:8081/generate_token_executer?="
SIGNED_URL_ENDPOINT = os.getenv(
    "MUUK_SIGNED_URL_ENDPOINT",
    "https://bm5s428g6e.execute-api.us-east-2.amazonaws.com/v1/mcp/getSignedUrl",
)


REQUEST_TIMEOUT_SECS = int(os.getenv("MUUK_TIMEOUT_SECS", "300"))


def _norm_path(p: str, workspace: Path = None) -> Path:
    """Normalize path to absolute, using workspace as base for relative paths."""
    path = Path(p).expanduser()
    if not path.is_absolute():
        base = workspace if workspace else Path.cwd()
        path = base / path
    return path.resolve()


def _validate_inputs(
    test_files_path: str,
    failure_data_path: str,
    workspace: Path = None,
) -> List[Path]:
    """Validate and normalize input paths."""
    test_path = _norm_path(test_files_path, workspace)
    failure_path = _norm_path(failure_data_path, workspace)

    missing = [str(p) for p in [test_path, failure_path] if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Missing file(s): {', '.join(missing)}")

    ensure_dir(test_path, "test-files path")
    ensure_dir(failure_path, "failure-data path")

    return [test_path, failure_path]


def _authenticate_muuk_key() -> bool:
    """Authenticate using Muuk Key. Success if status_code != 500."""

    try:
        r = requests.post(
            MUUK_AUTH_URL,
            json={"key": MUUK_KEY},
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
        return r.status_code != 500
    except requests.exceptions.RequestException:
        return False


def _analyze_impl(
    test_files_path: str,
    failure_data_path: str,
    workspace_path: str = None
) -> str:
    """Execute test failure analysis."""
    if not MUUK_KEY:
        return json.dumps({
            "error": "Muuk Key not configured",
            "hint": "Set MUUK_KEY environment variable"
        }, indent=2)


    if not _authenticate_muuk_key():
        return json.dumps({
            "error": "Invalid Muuk Key or authentication failed",
            "hint": "Verify your MUUK_KEY environment variable"
        }, indent=2)
    
    # Use workspace_path if provided, otherwise use cwd
    workspace = Path(workspace_path).resolve() if workspace_path else None
    
    try:
        test_path, failure_path = _validate_inputs(
            test_files_path, failure_data_path, workspace
        )
    except Exception as e:
        return json.dumps({"error": "Invalid input paths", "details": str(e)}, indent=2)

    zip_path = None
    try:
        source_path, signed_url = request_signed_url(MUUK_KEY, SIGNED_URL_ENDPOINT)
        zip_path = create_temp_zip(test_path, failure_path)
        upload_zip_to_s3(zip_path, signed_url)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "S3 upload failed", "details": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": "Upload preparation failed", "details": str(e)}, indent=2)
    finally:
        if zip_path and os.path.exists(zip_path):
            try:
                os.remove(zip_path)
            except OSError:
                pass

    payload = {
        "config": {
            "muuk_key": MUUK_KEY,
        },
        "s3_path": build_s3_path(source_path, signed_url),
    }

    headers = {
        "Content-Type": "application/json"
    }
    

    try:
        r = requests.post(API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECS)
    except requests.exceptions.Timeout:
        return json.dumps({"error": "Request timed out"}, indent=2)
    except requests.exceptions.RequestException as e:
        return json.dumps({"error": "Connection error", "details": str(e)}, indent=2)

    if r.status_code == 200:
        try:
            data = r.json()
            report = data.get("report", data)
            return report if isinstance(report, str) else json.dumps(report, indent=2)
        except Exception:
            return json.dumps({"error": "Invalid API response", "raw": r.text[:1000]}, indent=2)

    return json.dumps({
        "error": f"API error ({r.status_code})",
        "details": r.text[:2000],
        "payload_sent": payload,
    }, indent=2)


@app.list_tools()
async def list_tools() -> List[Tool]:
    """List available tools."""
    return [
        Tool(
            name="analyze_test_failure",
            description=(
                "Analyze an E2E test failure and get repair suggestions. "
                "You MUST always include workspace_path with the absolute path to the current project/workspace root. "
                "Get this from the current working directory or workspace folder. "
                "All other paths should be relative to the workspace (e.g., ./failure-data/)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "workspace_path": {
                        "type": "string",
                        "description": "REQUIRED: The absolute path to the current workspace/project root. You must always provide this - get it from the current working directory.",
                    },
                    "test_files_path": {
                        "type": "string",
                        "description": "Path to test files directory, relative to workspace (e.g., ./test-files/)",
                    },
                    "failure_data_path": {
                        "type": "string",
                        "description": "Path to failure data directory, relative to workspace (e.g., ./failure-data/)",
                    }
                },
                "required": ["workspace_path", "test_files_path", "failure_data_path"],
            },
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls."""
    if name != "analyze_test_failure":
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]

    required = ["workspace_path", "test_files_path", "failure_data_path"]
    missing = [k for k in required if not arguments.get(k)]
    if missing:
        return [TextContent(type="text", text=json.dumps({
            "error": "Missing required arguments",
            "missing": missing,
            "hint": "workspace_path must be the absolute path to your project root"
        }, indent=2))]

    try:
        result = await asyncio.to_thread(
            _analyze_impl,
            test_files_path=arguments["test_files_path"],
            failure_data_path=arguments["failure_data_path"],
            workspace_path=arguments["workspace_path"],
        )
    except Exception as e:
        result = json.dumps({"error": "Execution failed", "details": str(e)}, indent=2)

    return [TextContent(type="text", text=result)]


async def _main():
    """Async main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    """Main entry point."""
    asyncio.run(_main())


if __name__ == "__main__":
    main()
