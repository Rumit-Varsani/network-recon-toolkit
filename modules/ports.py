"""Port scanning and light banner grabbing."""

from __future__ import annotations

import socket
from typing import Any

COMMON_SERVICES = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    143: "imap",
    443: "https",
    445: "smb",
    3306: "mysql",
    3389: "rdp",
    5432: "postgres",
    8080: "http-proxy",
}


def grab_banner(host: str, port: int, timeout: float) -> str | None:
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            if port in (80, 8080):
                sock.sendall(b"HEAD / HTTP/1.0\r\nHost: lab\r\n\r\n")
            data = sock.recv(256)
            if not data:
                return None
            return data.decode("utf-8", errors="replace").strip().splitlines()[0][:120]
    except OSError:
        return None


def scan_ports(host: str, ports: list[int], timeout: float = 0.8) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for port in ports:
        entry: dict[str, Any] = {
            "port": port,
            "state": "closed",
            "service": COMMON_SERVICES.get(port, "unknown"),
            "banner": None,
        }
        try:
            with socket.create_connection((host, port), timeout=timeout):
                entry["state"] = "open"
                entry["banner"] = grab_banner(host, port, timeout)
        except OSError:
            pass
        results.append(entry)
    return results
