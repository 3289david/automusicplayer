"""PyInstaller 런타임 훅 — exe 빌드 후 HTTPS·yt-dlp·멀티프로세싱 안정화."""
from __future__ import annotations

import os
import sys


def _apply_certifi() -> None:
    try:
        import certifi

        ca = certifi.where()
        os.environ.setdefault("SSL_CERT_FILE", ca)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", ca)
    except Exception:
        pass


def _apply_freeze_support() -> None:
    if not getattr(sys, "frozen", False):
        return
    try:
        import multiprocessing

        multiprocessing.freeze_support()
    except Exception:
        pass


_apply_certifi()
_apply_freeze_support()
