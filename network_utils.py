"""LAN(사설망) IP 주소 조회."""
from __future__ import annotations

import socket
from typing import Any


def get_lan_ips() -> list[str]:
    """같은 Wi-Fi에서 접속 가능한 IPv4 주소 목록."""
    found: list[str] = []

    # 활성 인터페이스(외부로 나가는 경로) IP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip and not ip.startswith("127."):
                found.append(ip)
    except OSError:
        pass

    # 호스트명에 묶인 주소
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = info[4][0]
            if ip and not ip.startswith("127.") and ip not in found:
                found.append(ip)
    except OSError:
        pass

    return found


def host_urls(port: int) -> dict[str, list[str] | str]:
    """지정 포트 HTTP 접속 URL (로컬 + LAN)."""
    local = f"http://127.0.0.1:{port}/"
    lan = [f"http://{ip}:{port}/" for ip in get_lan_ips()]
    primary_lan = lan[0] if lan else ""
    return {
        "local": local,
        "lan": lan,
        "primary_lan": primary_lan,
    }


def panel_urls(port: int) -> dict[str, list[str] | str]:
    """패널 접속 URL (로컬 + LAN)."""
    return host_urls(port)


def website_urls(port: int) -> dict[str, list[str] | str]:
    """관리자 웹 포털 접속 URL (로컬 + LAN)."""
    return host_urls(port)


def network_access_urls(panel_port: int, website_port: int) -> dict[str, Any]:
    """패널·웹 포털 LAN 주소를 한 번에 반환."""
    panel = panel_urls(panel_port)
    website = website_urls(website_port)
    return {
        "local": panel["local"],
        "lan": panel["lan"],
        "primary_lan": panel["primary_lan"],
        "panel_local": panel["local"],
        "panel_lan": panel["lan"],
        "panel_primary_lan": panel["primary_lan"],
        "website_port": website_port,
        "website_local": website["local"],
        "website_lan": website["lan"],
        "website_primary_lan": website["primary_lan"],
    }
