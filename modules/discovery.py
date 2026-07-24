"""Host discovery helpers."""

from __future__ import annotations

import socket


def is_host_up(host: str, timeout: float = 0.8) -> bool:
    """Best-effort TCP reachability check against common ports."""
    for port in (80, 443, 22, 53):
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return True
        except OSError:
            continue
    # DNS resolve success is a weak signal the host name is valid
    try:
        socket.getaddrinfo(host, None)
        return False
    except OSError:
        return False
