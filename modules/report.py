"""Report writer."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_report(
    path: Path,
    *,
    target: str,
    host_up: bool,
    results: list[dict[str, Any]],
) -> Path:
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": "network-recon-toolkit",
        "target": target,
        "host_up": host_up,
        "open_ports": [r for r in results if r["state"] == "open"],
        "all_results": results,
        "disclaimer": "Authorized use only.",
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
