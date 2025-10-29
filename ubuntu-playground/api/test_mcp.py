#!/usr/bin/env python3
"""
TEST 3: MCP Endpoint Compatibility (Windows-safe, no emojis)
Tests the Model Context Protocol SSE endpoint and tool availability
"""
import requests
import json
import time
import re

PASS = "[PASS]"
FAIL = "[FAIL]"
INFO = "[INFO]"

BASE_URL = "http://localhost:8003"

def test_mcp_sse_stream():
    """TEST 3.1: Test MCP SSE endpoint returns proper stream"""
    print("\n" + "="*80)
    print("TEST 3.1: MCP SSE Stream - Endpoint Discovery")
    print("="*80)

    try:
        # Test SSE stream endpoint
        response = requests.get(f"{BASE_URL}/mcp", stream=True, timeout=5)

        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'N/A')}")

        # Read first few SSE events
        lines = []
        for line in response.iter_lines(decode_unicode=True):
            if line:
                lines.append(line)
            if len(lines) >= 5:
                break

        print(f"\nFirst {len(lines)} SSE events:")
        for line in lines:
            print(f"  {line}")

        # Check for session endpoint in response
        session_endpoint = None
        for line in lines:
            if "data:" in line and "/mcp/messages/" in line:
                # Extract session endpoint
                match = re.search(r'data:\s*(/mcp/messages/\?session_id=[\w]+)', line)
                if match:
                    session_endpoint = match.group(1)
                    break

        if response.status_code == 200 and "text/event-stream" in response.headers.get('content-type', ''):
            print(f"\n{PASS} TEST 3.1: MCP SSE stream working correctly")
            if session_endpoint:
                print(f"{INFO} Session endpoint: {session_endpoint}")
            return True, session_endpoint
        else:
            print(f"\n{FAIL} TEST 3.1: Invalid SSE response")
            return False, None

    except Exception as e:
        print(f"\n{FAIL} TEST 3.1 ERROR: {e}")
        return False, None


def test_mcp_list_tools(session_endpoint):
    """TEST 3.2: List available MCP tools"""
    print("\n" + "="*80)
    print("TEST 3.2: MCP Tools - List Available Tools")
    print("="*80)

    if not session_endpoint:
        print(f"{FAIL} No session endpoint available")
        return False

    try:
        # Send tools/list request via MCP protocol
        request_payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/list"
        }

        response = requests.post(
            f"{BASE_URL}{session_endpoint}",
            headers={"Content-Type": "application/json"},
            json=request_payload,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)[:500]}...")

            # Check if tools are listed
            if "result" in result and "tools" in result["result"]:
                tools = result["result"]["tools"]
                print(f"\n{INFO} Found {len(tools)} MCP tools:")
                for i, tool in enumerate(tools[:10], 1):  # Show first 10
                    print(f"  {i}. {tool.get('name', 'N/A')}: {tool.get('description', 'N/A')[:60]}")

                print(f"\n{PASS} TEST 3.2: Successfully listed {len(tools)} MCP tools")
                return True, tools
            else:
                print(f"\n{FAIL} TEST 3.2: No tools found in response")
                return False, []
        else:
            print(f"\n{FAIL} TEST 3.2: Failed to list tools (status={response.status_code})")
            return False, []

    except Exception as e:
        print(f"\n{FAIL} TEST 3.2 ERROR: {e}")
        return False, []


def test_mcp_tool_call(session_endpoint, tools):
    """TEST 3.3: Test calling an MCP tool"""
    print("\n" + "="*80)
    print("TEST 3.3: MCP Tool Call - Execute workspace/list")
    print("="*80)

    if not session_endpoint or not tools:
        print(f"{FAIL} No session endpoint or tools available")
        return False

    try:
        # Find workspace/list tool
        list_tool = None
        for tool in tools:
            if tool.get("name") == "workspace_list":
                list_tool = tool
                break

        if not list_tool:
            print(f"{INFO} workspace_list tool not found, trying first available tool")
            list_tool = tools[0] if tools else None

        if not list_tool:
            print(f"{FAIL} No tools available to test")
            return False

        tool_name = list_tool.get("name")
        print(f"{INFO} Testing tool: {tool_name}")

        # Call the tool
        request_payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": {"path": ""}  # Empty path to list root
            }
        }

        response = requests.post(
            f"{BASE_URL}{session_endpoint}",
            headers={"Content-Type": "application/json"},
            json=request_payload,
            timeout=10
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)[:400]}...")

            if "result" in result:
                print(f"\n{PASS} TEST 3.3: Successfully called MCP tool '{tool_name}'")
                return True
            else:
                print(f"\n{FAIL} TEST 3.3: Tool call returned no result")
                return False
        else:
            print(f"\n{FAIL} TEST 3.3: Tool call failed (status={response.status_code})")
            return False

    except Exception as e:
        print(f"\n{FAIL} TEST 3.3 ERROR: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "#"*80)
    print("#  TEST 3: MCP ENDPOINT COMPATIBILITY")
    print("#  Testing Model Context Protocol SSE and tool calls")
    print("#"*80)

    results = []

    # TEST 3.1: SSE Stream
    passed, session_endpoint = test_mcp_sse_stream()
    results.append(("TEST 3.1: MCP SSE Stream", passed))

    # TEST 3.2: List Tools
    if session_endpoint:
        passed, tools = test_mcp_list_tools(session_endpoint)
        results.append(("TEST 3.2: MCP List Tools", passed))

        # TEST 3.3: Tool Call
        if tools:
            passed = test_mcp_tool_call(session_endpoint, tools)
            results.append(("TEST 3.3: MCP Tool Call", passed))
        else:
            print(f"\n{INFO} Skipping TEST 3.3 (no tools available)")
            results.append(("TEST 3.3: MCP Tool Call", False))
    else:
        print(f"\n{INFO} Skipping TEST 3.2 and 3.3 (no session endpoint)")
        results.append(("TEST 3.2: MCP List Tools", False))
        results.append(("TEST 3.3: MCP Tool Call", False))

    # Summary
    print("\n" + "="*80)
    print("TEST 3 SUMMARY")
    print("="*80)

    for test_name, passed in results:
        status = f"{PASS}" if passed else f"{FAIL}"
        print(f"{status}: {test_name}")

    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")

    if total_passed == total_tests:
        print(f"\n{INFO} ALL TESTS PASSED! MCP endpoint working correctly.")
    else:
        print(f"\n{INFO} {total_tests - total_passed} test(s) failed. Review output above.")
