#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.0.1"
RELEASE = "Restore Historical Route"

CANONICAL_ROUTE = [
    {"date": "11 Jun", "name": "Lindos, Rhodes", "phase": "onboard", "lat": 36.091, "lng": 28.086},
    {"date": "11-12 Jun", "name": "Chalki", "phase": "onboard", "lat": 36.222, "lng": 27.611},
    {"date": "12-13 Jun", "name": "Symi", "phase": "onboard", "lat": 36.617, "lng": 27.838},
    {"date": "15-16 Jun", "name": "Nisyros", "phase": "onboard", "lat": 36.611, "lng": 27.133},
    {"date": "16-18 Jun", "name": "Kos", "phase": "onboard", "lat": 36.893, "lng": 27.289},
    {"date": "17 Jun", "name": "Cameron & Sophie join", "phase": "milestone", "lat": 36.893, "lng": 27.289},
    {"date": "18-19 Jun", "name": "Lipsi", "phase": "onboard", "lat": 37.295, "lng": 26.766},
    {"date": "19-21 Jun", "name": "Patmos", "phase": "onboard", "lat": 37.324, "lng": 26.545},
    {"date": "22 Jun", "name": "Katapola, Amorgos", "phase": "onboard", "lat": 36.827, "lng": 25.863},
    {"date": "22-23 Jun", "name": "Ios", "phase": "onboard", "lat": 36.722, "lng": 25.272},
    {"date": "23 Jun", "name": "Ios departure AIS", "phase": "ais", "lat": 36.71285, "lng": 25.28499},
    {"date": "24 Jun", "name": "Sea of Crete AIS marker", "phase": "ais", "lat": 36.6513, "lng": 24.3377},
    {"date": "25 Jun", "name": "Sea of Crete / Cyclades area", "phase": "ais", "lat": 36.6473, "lng": 24.3392},
    {"date": "26-27 Jun", "name": "Zakynthos", "phase": "onboard", "lat": 37.788, "lng": 20.899},
    {"date": "28 Jun", "name": "Sami, Kefalonia", "phase": "onboard", "lat": 38.253, "lng": 20.647},
    {"date": "29-30 Jun", "name": "East Coast Ithaca / Underway", "phase": "onboard", "lat": 38.43164, "lng": 20.58843},
    {"date": "30 Jun", "name": "Paxi / Paxos", "phase": "onboard", "lat": 39.2026, "lng": 20.1858},
    {"date": "1 Jul", "name": "East Coast Corfu", "phase": "current", "lat": 39.6243, "lng": 19.9217}
]

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-2-0-1").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def load_current_point():
    route_path = ROOT / "site" / "data" / "route.json"
    if not route_path.exists():
        return None
    try:
        route = json.loads(route_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    currents = [p for p in route if p.get("phase") == "current"]
    return currents[-1] if currents else None

def restore_route(path):
    current = load_current_point()
    route = [dict(p) for p in CANONICAL_ROUTE]

    # Preserve a newer manually-added current point if it is not already in the canonical route.
    if current and current.get("name") not in {p["name"] for p in route}:
        for p in route:
            if p.get("phase") == "current":
                p["phase"] = "onboard"
        current["phase"] = "current"
        route.append(current)

    if path.exists():
        backup(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(route, indent=2), encoding="utf-8")
    return True

def update_dashboard(path):
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["release"] = RELEASE
    stats = data.setdefault("stats", {})
    stats["routeStops"] = len(CANONICAL_ROUTE)
    tracker = data.setdefault("tracker", {})
    tracker["latestStatus"] = "Historical route restored"
    tracker["note"] = "v2.0.1 restored the full route history after v2.0.0 accidentally shipped a shortened placeholder route."
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
        if restore_route(ROOT / rel):
            changed.append(rel)
    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel):
            changed.append(rel)
    update_version(ROOT / "site/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    print("Historical route restored.")
    print("Updated files:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
