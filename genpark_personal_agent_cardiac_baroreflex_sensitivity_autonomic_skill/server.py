# -*- coding: utf-8 -*-
"""MCP Server for Cardiac Baroreflex Sensitivity (BRS) & Vagal Tone Sentinel Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import CardiacBaroreflexSensitivitySentinel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "compute_baroreflex_sensitivity_index",
        "description": "Calculate BRS slope (ms/mmHg) from continuous beat-to-beat systolic pressure and ECG RR-intervals.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "rr_interval_delta_ms": {
                    "type": "number"
                },
                "systolic_pressure_delta_mmhg": {
                    "type": "number"
                },
                "baseline_hrv_rmssd": {
                    "type": "number"
                }
            },
            "required": [
                "rr_interval_delta_ms",
                "systolic_pressure_delta_mmhg"
            ]
        }
    },
    {
        "name": "synthesize_vagal_nerve_stimulation_protocol",
        "description": "Formulate resonant frequency slow-paced breathing (0.1 Hz / 6 breaths/min) to restore baroreflex buffering.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "brs_score": {
                    "type": "number"
                }
            },
            "required": [
                "brs_score"
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
                "serverInfo": {"name": "genpark-personal-agent-cardiac-baroreflex-sensitivity-autonomic-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(CardiacBaroreflexSensitivitySentinel, tool_name, None)
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
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-cardiac-baroreflex-sensitivity-autonomic-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
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
