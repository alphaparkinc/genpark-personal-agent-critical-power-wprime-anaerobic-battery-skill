# -*- coding: utf-8 -*-
"""MCP Server for Critical Power & W-Prime Anaerobic Work Capacity Battery Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import CriticalPowerWPrimeAnaerobicBatteryModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "compute_critical_power_and_wprime",
        "description": "Calculate Critical Power (watts) and anaerobic work capacity W' (kilojoules) from 3-minute and 12-minute maximal mean power efforts.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "p1_watts": {
                    "type": "number",
                    "description": "Short maximal power (e.g. 3-min power)"
                },
                "t1_seconds": {
                    "type": "integer",
                    "description": "e.g. 180"
                },
                "p2_watts": {
                    "type": "number",
                    "description": "Long maximal power (e.g. 12-min power)"
                },
                "t2_seconds": {
                    "type": "integer",
                    "description": "e.g. 720"
                }
            },
            "required": [
                "p1_watts",
                "t1_seconds",
                "p2_watts",
                "t2_seconds"
            ]
        }
    },
    {
        "name": "simulate_wprime_depletion_and_recovery",
        "description": "Simulate real-time anaerobic battery W' depletion during above-CP surges and exponential reconstitution during sub-CP recovery intervals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "critical_power_watts": {
                    "type": "number"
                },
                "wprime_joules": {
                    "type": "number"
                },
                "surge_power_watts": {
                    "type": "number"
                },
                "surge_duration_seconds": {
                    "type": "integer"
                },
                "recovery_power_watts": {
                    "type": "number"
                },
                "recovery_duration_seconds": {
                    "type": "integer"
                }
            },
            "required": [
                "critical_power_watts",
                "wprime_joules",
                "surge_power_watts",
                "surge_duration_seconds"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-critical-power-wprime-anaerobic-battery-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(CriticalPowerWPrimeAnaerobicBatteryModel, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-critical-power-wprime-anaerobic-battery-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-critical-power-wprime-anaerobic-battery-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
