#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.1"
RELEASE = "Current Marker Fix"

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-2-1-current-fix").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def fix_route(path):
    if not path.exists():
        return False
    route = json.loads(path.read_text(encoding="utf-8"))
    target_index = None
    for i, point in enumerate(route):
        if point.get("name") == "East Coast Corfu":
            target_index = i
    if target_index is None:
        target_index = len(route) - 1
    for i, point in enumerate(route):
        if i == target_index:
            point["phase"] = "current"
        elif point.get("phase") == "current":
            point["phase"] = "onboard"
    backup(path)
    path.write_text(json.dumps(route, indent=2), encoding="utf-8")
    return True

def update_dashboard(path):
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["release"] = RELEASE
    tracker = data.setdefault("tracker", {})
    tracker["latestStatus"] = "Manual location: East Coast Corfu"
    tracker["note"] = "Current marker corrected so the admin-added East Coast Corfu point is the only current marker."
    backup(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

def update_version(path):
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        data = {}
    data["version"] = VERSION
    data["release"] = RELEASE
    backup(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def main():
    changed = []
    for rel in ["site/data/route.json", "content/routes/route-so-far.json", "docs/data/route.json"]:
        if fix_route(ROOT / rel):
            changed.append(rel)
    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel):
            changed.append(rel)
    update_version(ROOT / "site/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    print("Corrected current marker. East Coast Corfu is now current.")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
