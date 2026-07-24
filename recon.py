#!/usr/bin/env python3
"""Network Recon Toolkit — authorized lab use only."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from modules.discovery import is_host_up
from modules.ports import scan_ports
from modules.report import write_report

BANNER = """
╔══════════════════════════════════════════════════════╗
║  NETWORK RECON TOOLKIT — AUTHORIZED LABS ONLY        ║
║  Unauthorized scanning is illegal.                   ║
╚══════════════════════════════════════════════════════╝
"""


def parse_ports(raw: str) -> list[int]:
    ports: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            ports.extend(range(int(start), int(end) + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))


def main() -> int:
    print(BANNER)
    parser = argparse.ArgumentParser(
        description="Educational network recon for authorized targets only."
    )
    parser.add_argument("--target", required=True, help="IP or hostname")
    parser.add_argument(
        "--ports",
        default="22,80,443,3389,8080",
        help="Comma-separated ports or ranges (e.g. 20-25,80,443)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.8,
        help="Socket timeout in seconds",
    )
    parser.add_argument(
        "--out",
        default="report.json",
        help="Output report path",
    )
    parser.add_argument(
        "--i-own-this-target",
        action="store_true",
        help="Required confirmation that you are authorized",
    )
    args = parser.parse_args()

    if not args.i_own_this_target:
        print(
            "[!] Refusing to scan. Re-run with --i-own-this-target only if authorized.",
            file=sys.stderr,
        )
        return 2

    ports = parse_ports(args.ports)
    print(f"[*] Target: {args.target}")
    print(f"[*] Checking reachability…")
    alive = is_host_up(args.target, timeout=args.timeout)
    print(f"[*] Host up: {alive}")

    print(f"[*] Scanning {len(ports)} port(s)…")
    results = scan_ports(args.target, ports, timeout=args.timeout)
    open_ports = [r for r in results if r["state"] == "open"]
    print(f"[+] Open ports: {len(open_ports)}")
    for item in open_ports:
        banner = item.get("banner") or "-"
        print(f"    {item['port']:>5}/tcp  open  {item.get('service', '?')}  | {banner[:60]}")

    path = write_report(
        Path(args.out),
        target=args.target,
        host_up=alive,
        results=results,
    )
    print(f"[*] Report written → {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
