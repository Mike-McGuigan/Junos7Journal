#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.2"
RELEASE = "Latest Position Update"

LATEST_POINT = {
    "date": "30 Jun",
    "name": "Latest AIS position - West Coast Greece",
    "phase": "current",
    "lat": 39.01234,
    "lng": 20.32855,
    "note": "Latest precise public coordinate found from MyShipTracking: 39.01234, 20.32855, reported 2026-06-30 06:16 UTC. Other public AIS sources report recent reception in the East Mediterranean / West Coast Greece area, but did not expose a newer precise coordinate."
}

AIS_RECORD = {
    "timestampUtc": "2026-06-30T20:10:00Z",
    "vesselKey": "junos7",
    "displayName": "JUNOS 7",
    "mmsi": "319303300",
    "imo": "1109712",
    "status": "Under way / recent AIS reception",
    "area": "West Coast Greece / Ionian Sea",
    "latestPrecisePosition": {
        "lat": 39.01234,
        "lng": 20.32855,
        "reportedUtc": "2026-06-30T06:16:00Z",
        "source": "MyShipTracking public page"
    },
    "source": "manual public AIS lookup",
    "confidence": "latest precise coordinate from public source; current area corroborated by other public AIS snippets"
}

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-0-2").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def update_route(path):
    if not path.exists():
        return False
    route = json.loads(path.read_text(encoding="utf-8"))
    for point in route:
        if point.get("phase") == "current":
            point["phase"] = "onboard"
    existing = next((p for p in route if p.get("name") == LATEST_POINT["name"]), None)
    if existing:
        existing.update(LATEST_POINT)
    else:
        route.append(LATEST_POINT)
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
    tracker["workflow"] = tracker.get("workflow", "running")
    tracker["provider"] = "manual / provider not configured"
    tracker["liveAis"] = False
    tracker["lastManualLookupUtc"] = AIS_RECORD["timestampUtc"]
    tracker["latestStatus"] = "Latest precise public coordinate plotted - West Coast Greece / Ionian Sea"
    tracker["latestSource"] = "Manual public AIS lookup"
    tracker["latestPrecisePosition"] = AIS_RECORD["latestPrecisePosition"]
    tracker["note"] = "Latest precise coordinate from MyShipTracking; recent area corroborated by VesselFinder/Maritime Optima public snippets."
    backup(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

def update_version_json(path):
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
        if update_route(ROOT / rel):
            changed.append(rel)
    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel):
            changed.append(rel)
    update_version_json(ROOT / "site/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    out = ROOT / "data/ais/manual/2026-06-30-2010-junos7-latest-position.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(AIS_RECORD, indent=2), encoding="utf-8")
    print("Latest position plotted: 39.01234, 20.32855")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
