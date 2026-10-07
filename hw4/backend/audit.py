"""Append-only audit trail of agent-loop activity.

Each event is one JSON object written on its own line (JSON Lines) to
`output/audit_trail.json`. The file is only ever appended to — existing lines are never
read back or rewritten — so prior runs are never wiped, even if a later write fails.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE.parent / "output" / "audit_trail.json"

# Keep logged args/results short and free of chain-of-thought.
_MAX = 160


def _short(value: Any) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, default=str)
    return text if len(text) <= _MAX else text[: _MAX - 1] + "…"


def _append(record: dict[str, Any]) -> None:
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(
        {"time": datetime.now(timezone.utc).isoformat(), **record}, ensure_ascii=False
    )
    with AUDIT_PATH.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def record_tool(name: str, args: dict[str, Any], result: Any) -> None:
    """Log one tool call in the agent loop (name, short args, short result)."""
    _append(
        {
            "event": "tool_call",
            "tool_name": name,
            "args": _short(args),
            "result": _short(result),
        }
    )


def record_run_end(stop_reason: str, **extra: Any) -> None:
    """Log the end of one agent run and why the loop stopped."""
    _append({"event": "run_end", "stop_reason": stop_reason, **extra})
