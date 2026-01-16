#!/usr/bin/env python3
"""MCP server that proxies to the search API."""

import json
import sys
import httpx

API_URL = "http://68.183.102.39:8000/mcp"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}


def call_api(method: str, params: dict = None, req_id: int = 1) -> dict:
    """Call the remote MCP API."""
    payload = {"jsonrpc": "2.0", "method": method, "id": req_id}
    if params:
        payload["params"] = params

    response = httpx.post(API_URL, json=payload, headers=HEADERS, timeout=60.0)
    text = response.text

    if text.startswith("event:"):
        for line in text.split("\n"):
            if line.startswith("data:"):
                return json.loads(line[5:].strip())
    return json.loads(text)


def handle_request(request: dict) -> dict | None:
    """Handle incoming JSON-RPC request."""
    method = request.get("method", "")
    params = request.get("params", {})
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "mcp-taxcode", "version": "0.1.0"}
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        api_response = call_api("tools/list", req_id=req_id)
        tools = api_response.get("result", {}).get("tools", [])
        tools = [t for t in tools if t.get("name") == "search_tax_code"]
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}
    elif method == "tools/call":
        api_response = call_api("tools/call", params, req_id=req_id)
        if "error" in api_response:
            return {"jsonrpc": "2.0", "id": req_id, "error": api_response["error"]}
        return {"jsonrpc": "2.0", "id": req_id, "result": api_response.get("result", {})}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method not found: {method}"}}


def main():
    """Main loop - read JSON-RPC from stdin, write to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            if response:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except Exception as e:
            error_response = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(error_response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
