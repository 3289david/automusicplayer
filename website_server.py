"""LAN 관리자 웹 포털 — 번들 website/ 폴더를 고정 포트로 제공."""
from __future__ import annotations

import threading

from flask import Flask, send_from_directory
from config_store import BUNDLE_DIR, WEBSITE_PORT

_website_dir = BUNDLE_DIR / "website"


def create_website_app() -> Flask:
    root = str(_website_dir)
    wapp = Flask(__name__, static_folder=root, static_url_path="")

    @wapp.route("/")
    @wapp.route("/index.html")
    def index():
        return send_from_directory(root, "index.html")

    @wapp.route("/login.html")
    def login_page():
        return send_from_directory(root, "login.html")

    return wapp


def run_website_server(port: int = WEBSITE_PORT) -> None:
    wapp = create_website_app()
    wapp.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
        threaded=True,
    )


def start_website_server_thread(port: int = WEBSITE_PORT) -> threading.Thread:
    t = threading.Thread(target=run_website_server, args=(port,), daemon=True)
    t.start()
    return t
