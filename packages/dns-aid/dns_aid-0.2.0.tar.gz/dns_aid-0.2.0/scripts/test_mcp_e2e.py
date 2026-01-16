#!/usr/bin/env python3
"""
DNS-AID MCP Server E2E Test Script.

Tests all MCP tools against a real agent endpoint.

IMPORTANT: The MCP server defaults to stdio transport.
For HTTP testing, you MUST start it with: dns-aid-mcp --transport http --port 8080

Usage:
    # Start MCP server first (in another terminal):
    dns-aid-mcp --transport http --port 8080

    # Then run this test:
    python scripts/test_mcp_e2e.py --endpoint YOUR_NGROK_URL

    # Or with defaults:
    python scripts/test_mcp_e2e.py
"""

import argparse
import json
import subprocess
import sys
import time

import httpx


def check_mcp_server(mcp_url: str) -> bool:
    """Check if MCP server is running."""
    try:
        resp = httpx.get(f"{mcp_url.replace('/mcp', '')}/health", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def start_mcp_server(port: int = 8080) -> subprocess.Popen | None:
    """Start MCP server in background."""
    print(f"Starting MCP server on port {port}...")
    try:
        proc = subprocess.Popen(
            ["dns-aid-mcp", "--transport", "http", "--port", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # Wait for startup
        for _ in range(10):
            time.sleep(0.5)
            if check_mcp_server(f"http://localhost:{port}/mcp"):
                print(f"  ✓ MCP server started on port {port}")
                return proc
        print("  ✗ MCP server failed to start")
        proc.kill()
        return None
    except FileNotFoundError:
        print("  ✗ dns-aid-mcp command not found. Install with: pip install -e '.[all]'")
        return None


def call_mcp_tool(mcp_url: str, tool_name: str, args: dict) -> dict:
    """Call an MCP tool via HTTP."""
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    with httpx.Client(timeout=60) as client:
        # Initialize session
        init_resp = client.post(
            mcp_url,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0"},
                },
            },
            headers=headers,
        )

        session_id = init_resp.headers.get("mcp-session-id", "")

        # Call the tool
        tool_headers = headers.copy()
        if session_id:
            tool_headers["mcp-session-id"] = session_id

        resp = client.post(
            mcp_url,
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": tool_name, "arguments": args},
            },
            headers=tool_headers,
        )

        result = resp.json()
        if "result" in result:
            content = result["result"].get("content", [])
            if content:
                return json.loads(content[0].get("text", "{}"))
        return result


def run_e2e_test(
    mcp_url: str,
    endpoint: str,
    domain: str = "highvelocitynetworking.com",
    agent_name: str = "mcp-test-agent",
    protocol: str = "a2a",
) -> bool:
    """Run full E2E test."""
    print("=" * 60)
    print("DNS-AID MCP E2E TEST")
    print("=" * 60)
    print(f"\nMCP Server: {mcp_url}")
    print(f"Agent Endpoint: {endpoint}")
    print(f"Domain: {domain}")
    print(f"Agent Name: {agent_name}")
    print(f"Protocol: {protocol}")

    all_passed = True

    # Test 1: Publish
    print("\n" + "-" * 40)
    print("TEST 1: Publish Agent")
    print("-" * 40)
    try:
        result = call_mcp_tool(
            mcp_url,
            "publish_agent_to_dns",
            {
                "name": agent_name,
                "domain": domain,
                "protocol": protocol,
                "endpoint": endpoint,
                "port": 443,
                "capabilities": ["test", "demo"],
                "ttl": 300,
            },
        )
        if result.get("success"):
            print(f"  ✓ Published: {result.get('fqdn')}")
        else:
            print(f"  ✗ Failed: {result}")
            all_passed = False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        all_passed = False

    # Wait for DNS propagation
    print("\nWaiting 3s for DNS propagation...")
    time.sleep(3)

    # Test 2: Discover
    print("\n" + "-" * 40)
    print("TEST 2: Discover Agent")
    print("-" * 40)
    try:
        result = call_mcp_tool(
            mcp_url,
            "discover_agents_via_dns",
            {"domain": domain, "protocol": protocol, "name": agent_name},
        )
        count = result.get("count", 0)
        if count > 0:
            print(f"  ✓ Found {count} agent(s)")
            for agent in result.get("agents", []):
                print(f"    - {agent.get('name')}: {agent.get('endpoint')}")
        else:
            print(f"  ○ No agents found (DNS may still be propagating)")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 3: Verify
    print("\n" + "-" * 40)
    print("TEST 3: Verify Agent")
    print("-" * 40)
    fqdn = f"_{agent_name}._{protocol}._agents.{domain}"
    try:
        result = call_mcp_tool(mcp_url, "verify_agent_dns", {"fqdn": fqdn})
        score = result.get("security_score", 0)
        rating = result.get("security_rating", "Unknown")
        print(f"  Record exists: {'✓' if result.get('record_exists') else '✗'}")
        print(f"  SVCB valid: {'✓' if result.get('svcb_valid') else '✗'}")
        print(f"  DNSSEC: {'✓' if result.get('dnssec_valid') else '✗'}")
        print(f"  Endpoint reachable: {'✓' if result.get('endpoint_reachable') else '✗'}")
        print(f"  Score: {score}/100 ({rating})")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 4: List
    print("\n" + "-" * 40)
    print("TEST 4: List Agents")
    print("-" * 40)
    try:
        result = call_mcp_tool(mcp_url, "list_published_agents", {"domain": domain})
        count = result.get("count", 0)
        print(f"  ✓ Found {count} record(s)")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    # Test 5: Delete (cleanup)
    print("\n" + "-" * 40)
    print("TEST 5: Delete Agent (cleanup)")
    print("-" * 40)
    try:
        result = call_mcp_tool(
            mcp_url,
            "delete_agent_from_dns",
            {"name": agent_name, "domain": domain, "protocol": protocol},
        )
        if result.get("success"):
            print(f"  ✓ Deleted: {result.get('fqdn')}")
        else:
            print(f"  ✗ Failed: {result}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)

    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="DNS-AID MCP Server E2E Test",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
IMPORTANT: MCP server transport modes
=====================================
The DNS-AID MCP server supports two transport modes:

1. STDIO (default): For Claude Desktop integration
   $ dns-aid-mcp

2. HTTP: For programmatic testing
   $ dns-aid-mcp --transport http --port 8080

This script requires HTTP transport. If you see connection errors,
make sure the server is running with --transport http.

Examples:
  # Start server in one terminal:
  dns-aid-mcp --transport http --port 8080

  # Run tests in another terminal:
  python scripts/test_mcp_e2e.py --endpoint myagent.ngrok-free.app
  python scripts/test_mcp_e2e.py --auto-start --endpoint myagent.ngrok-free.app
""",
    )
    parser.add_argument(
        "--mcp-url",
        default="http://localhost:8080/mcp",
        help="MCP server URL (default: http://localhost:8080/mcp)",
    )
    parser.add_argument(
        "--endpoint",
        default="example.com",
        help="Agent endpoint hostname (default: example.com)",
    )
    parser.add_argument(
        "--domain",
        default="highvelocitynetworking.com",
        help="DNS domain (default: highvelocitynetworking.com)",
    )
    parser.add_argument(
        "--agent-name",
        default="mcp-test-agent",
        help="Agent name (default: mcp-test-agent)",
    )
    parser.add_argument(
        "--protocol",
        default="a2a",
        choices=["a2a", "mcp"],
        help="Protocol (default: a2a)",
    )
    parser.add_argument(
        "--auto-start",
        action="store_true",
        help="Automatically start MCP server if not running",
    )

    args = parser.parse_args()

    # Check/start MCP server
    mcp_proc = None
    if not check_mcp_server(args.mcp_url):
        if args.auto_start:
            port = int(args.mcp_url.split(":")[-1].split("/")[0])
            mcp_proc = start_mcp_server(port)
            if not mcp_proc:
                sys.exit(1)
        else:
            print("❌ MCP server not running!")
            print("")
            print("Start it with:")
            print("  dns-aid-mcp --transport http --port 8080")
            print("")
            print("Or use --auto-start to start automatically:")
            print(f"  python {sys.argv[0]} --auto-start --endpoint {args.endpoint}")
            sys.exit(1)

    try:
        success = run_e2e_test(
            mcp_url=args.mcp_url,
            endpoint=args.endpoint,
            domain=args.domain,
            agent_name=args.agent_name,
            protocol=args.protocol,
        )
        sys.exit(0 if success else 1)
    finally:
        if mcp_proc:
            print("\nStopping MCP server...")
            mcp_proc.terminate()
            mcp_proc.wait()


if __name__ == "__main__":
    main()
