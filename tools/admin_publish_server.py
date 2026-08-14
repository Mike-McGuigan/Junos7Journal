#!/usr/bin/env python3
from __future__ import annotations

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import json
import os
import re
import socket
import subprocess
import sys
import webbrowser

ROOT = Path(__file__).resolve().parents[1]
PORT = 8765
VERSION_FILE = ROOT / "VERSION"
RELEASE_TITLE_FILE = ROOT / "RELEASE_TITLE"
GEOMETRY_FILE = ROOT / "content" / "routes" / "voyage-geometry.json"
ROUTE_FILE = ROOT / "docs" / "data" / "route.json"


def current_version():
    if VERSION_FILE.exists():
        value = VERSION_FILE.read_text(encoding="utf-8").strip()
        if value:
            return value
    return "2.7.5"


def current_release_title():
    if RELEASE_TITLE_FILE.exists():
        value = RELEASE_TITLE_FILE.read_text(encoding="utf-8").strip()
        if value:
            return value
    return "Unreleased"


def same_root(a, b):
    try:
        return Path(a).resolve() == Path(b).resolve()
    except Exception:
        return str(a).lower() == str(b).lower()


def check_existing_server():
    try:
        with urlopen(f"http://localhost:{PORT}/api/health", timeout=1.5) as response:
            if response.status != 200:
                return None
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def port_in_use():
    try:
        with socket.create_connection(("localhost", PORT), timeout=0.5):
            return True
    except OSError:
        return False


def run(cmd, check=True):
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    p = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=False,
        encoding="utf-8",
        errors="replace",
        env=env
    )

    if check and p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n\n{p.stdout}")

    return p.stdout.strip()


def git_health():
    info = {"ok": True, "version": current_version(), "release": current_release_title(), "repo": ROOT.name, "root": str(ROOT), "checks": []}

    def check(name, cmd, required=True, warning_ok=False):
        try:
            out = run(cmd, True)
            info["checks"].append({"name": name, "ok": True, "required": required, "warning": False, "output": out})
            return out
        except Exception as exc:
            output = str(exc)
            if warning_ok:
                info["checks"].append({"name": name, "ok": True, "required": False, "warning": True, "output": output})
            else:
                info["checks"].append({"name": name, "ok": False, "required": required, "warning": not required, "output": output})
                if required:
                    info["ok"] = False
            return ""

    check("Git installed", ["git", "--version"])
    info["branch"] = check("Current branch", ["git", "branch", "--show-current"], False) or "unknown"
    info["remote"] = check("Remote", ["git", "remote", "-v"], False)
    status = check("Working tree", ["git", "status", "--short"], False)
    info["workingTreeClean"] = not bool(status.strip())
    try:
        helper = run(["git", "config", "--global", "credential.helper"], True)
    except Exception:
        helper = ""
    info["credentialHelper"] = helper or "not configured globally"
    return info


def safe_name(value):
    value = str(value or "junos7").replace("->", " to ").replace(">", " to ")
    value = re.sub(r"[^A-Za-z0-9]+", "-", value.lower())
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "junos7"


def write_update(update):
    name = safe_name(update.get("routePoint", {}).get("name", "junos7"))
    directory = ROOT / "admin-input"
    directory.mkdir(parents=True, exist_ok=True)
    out = directory / "latest-location.json"
    archive = directory / f"manual-location-{name}.json"
    text = json.dumps(update, indent=2, ensure_ascii=False)
    out.write_text(text, encoding="utf-8")
    archive.write_text(text, encoding="utf-8")
    return out


def save_location_update(update):
    log = []
    loc = update.get("routePoint", {}).get("name", "Manual location")

    if not git_health()["ok"]:
        raise RuntimeError("Git health check failed. Check the dashboard/server output.")

    path = write_update(update)
    log.append(f"Wrote {path.relative_to(ROOT)}")
    log.append(run([sys.executable, "tools/apply_manual_location.py", str(path.relative_to(ROOT))]))
    log.append(run([sys.executable, "tools/build_site.py"]))
    log.append(f"Route update saved locally for {loc} in {ROOT}. Commit and push the repository to publish the public site.")
    return "\n".join(log)



def read_geometry():
    if not GEOMETRY_FILE.exists():
        return {
            "schemaVersion": 1,
            "description": "Optional manual sea-aware route waypoints for Juno's 7. Add legs here when a straight line between route stops would cross land.",
            "legs": [],
        }
    return json.loads(GEOMETRY_FILE.read_text(encoding="utf-8"))


def save_geometry(data):
    if not isinstance(data, dict) or not isinstance(data.get("legs"), list):
        raise ValueError("Invalid geometry payload. Expected an object with a legs array.")
    data.setdefault("schemaVersion", 1)
    data.setdefault("description", "Optional manual sea-aware route waypoints for Juno's 7. Add legs here when a straight line between route stops would cross land.")
    GEOMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    GEOMETRY_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    log = [f"Saved {GEOMETRY_FILE.relative_to(ROOT)}"]
    log.append(run([sys.executable, "tools/build_site.py"]))
    log.append(f"Route geometry saved locally in {ROOT}. Review, commit and push when ready.")
    return "\n".join(log)


def read_route():
    if not ROUTE_FILE.exists():
        return []
    return json.loads(ROUTE_FILE.read_text(encoding="utf-8"))


def save_route_payload(payload):
    route = payload.get("route") if isinstance(payload, dict) else None
    if not isinstance(route, list):
        raise ValueError("Invalid route payload. Expected an object with a route array.")
    for item in route:
        if not isinstance(item, dict):
            raise ValueError("Invalid route item. Each route point must be an object.")
        if "lat" not in item or "lng" not in item:
            raise ValueError("Invalid route item. Each route point needs lat and lng.")
        # Validate numeric coordinates before writing anything.
        float(item["lat"])
        float(item["lng"])

    ROUTE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ROUTE_FILE.write_text(json.dumps(route, indent=2, ensure_ascii=False), encoding="utf-8")
    log = [f"Saved {ROUTE_FILE.relative_to(ROOT)}"]

    geometry = payload.get("geometry") if isinstance(payload, dict) else None
    if geometry is not None:
        if not isinstance(geometry, dict) or not isinstance(geometry.get("legs"), list):
            raise ValueError("Invalid geometry payload. Expected an object with a legs array.")
        geometry.setdefault("schemaVersion", 1)
        geometry.setdefault("description", "Optional manual sea-aware route waypoints for Juno's 7. Add legs here when a straight line between route stops would cross land.")
        GEOMETRY_FILE.parent.mkdir(parents=True, exist_ok=True)
        GEOMETRY_FILE.write_text(json.dumps(geometry, indent=2, ensure_ascii=False), encoding="utf-8")
        log.append(f"Saved {GEOMETRY_FILE.relative_to(ROOT)}")

    log.append(run([sys.executable, "tools/build_site.py"]))
    log.append(f"Route stop saved locally in {ROOT}. Review, commit and push when ready.")
    return "\n".join(log)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "site"), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def _json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path in {"/api/status", "/api/health"}:
            self._json(200, git_health())
            return
        if path == "/api/geometry":
            self._json(200, read_geometry())
            return
        if path == "/api/route":
            self._json(200, read_route())
            return
        super().do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size).decode("utf-8"))
            if path == "/api/publish":
                if "routePoint" not in payload or "tracker" not in payload:
                    raise ValueError("Invalid update payload")
                self._json(200, {"ok": True, "log": save_location_update(payload)})
                return
            if path == "/api/geometry":
                self._json(200, {"ok": True, "log": save_geometry(payload)})
                return
            if path == "/api/route":
                self._json(200, {"ok": True, "log": save_route_payload(payload)})
                return
            self._json(404, {"ok": False, "error": "Not found"})
        except Exception as exc:
            self._json(500, {"ok": False, "error": str(exc)})


def main():
    os.chdir(ROOT)
    url = f"http://localhost:{PORT}/admin.html"
    print("=" * 72)
    print("Captain's Dashboard")
    print("=" * 72)
    print(f"Repository: {ROOT}")
    print(f"URL:        {url}\n")
    existing = check_existing_server()
    if existing:
        existing_root = existing.get("root", "unknown")
        if same_root(existing_root, ROOT):
            print("A Captain's Dashboard server is already running for this repository.")
            print(f"Existing server: {existing_root}")
            print(f"Opening:         {url}")
            webbrowser.open(url)
            return
        print("ERROR: port 8765 is already being served by a different repository.")
        print(f"Existing server: {existing_root}")
        print(f"This repository: {ROOT}")
        print("\nStop the other dashboard server, then start this one again.")
        raise SystemExit(1)
    if port_in_use():
        print("ERROR: port 8765 is already in use, but it is not answering as a Captain's Dashboard server.")
        print("Stop the process using port 8765, then start this dashboard again.")
        raise SystemExit(1)
    print("Health check:")
    health = git_health()
    for item in health["checks"]:
        symbol = "OK " if item["ok"] and not item.get("warning") else ("WARN" if item.get("warning") else "ERR")
        first = (item["output"] or "").splitlines()[0] if item["output"] else ""
        print(f"  [{symbol}] {item['name']}: {first}")
    print("\nLeave this window open while using Save Route Update. Press Ctrl+C to stop.")
    print("=" * 72)
    webbrowser.open(url)
    try:
        ThreadingHTTPServer(("localhost", PORT), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nCaptain's Dashboard stopped.")


if __name__ == "__main__":
    main()
