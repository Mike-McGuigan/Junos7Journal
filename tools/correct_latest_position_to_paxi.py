#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.3"
RELEASE = "Paxi Position Correction"

PAXI_POINT = {
    "date": "30 Jun",
    "name": "Paxi / Paxos",
    "phase": "current",
    "lat": 39.2026,
    "lng": 20.1858,
    "note": "User-confirmed current location in Paxi/Paxos area. Plotted at an approximate Paxi/Gaios coordinate until a fresh precise AIS coordinate is available."
}

AIS_RECORD = {
    "timestampUtc": "2026-06-30T21:12:00Z",
    "vesselKey": "junos7",
    "displayName": "JUNOS 7",
    "mmsi": "319303300",
    "imo": "1109712",
    "status": "At/near Paxi",
    "area": "Paxi / Paxos, Ionian Sea, Greece",
    "position": {
        "lat": 39.2026,
        "lng": 20.1858,
        "precision": "approximate area marker",
        "source": "user-confirmed current location"
    },
    "replaces": {
        "lat": 39.01234,
        "lng": 20.32855,
        "reason": "Previous marker appears to have been a stale en-route AIS position."
    },
    "source": "user observation plus public AIS area context",
    "confidence": "area high; exact coordinate approximate pending fresh precise AIS"
}

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-0-3").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def update_route(path):
    if not path.exists():
        return False
    route = json.loads(path.read_text(encoding="utf-8"))
    filtered = []
    for point in route:
        name = point.get("name", "")
        if name in {"Latest AIS position - West Coast Greece", "Latest AIS position — West Coast Greece"}:
            continue
        if point.get("phase") == "current":
            point["phase"] = "onboard"
        filtered.append(point)
    existing = next((p for p in filtered if p.get("name") == PAXI_POINT["name"]), None)
    if existing:
        existing.update(PAXI_POINT)
    else:
        filtered.append(PAXI_POINT)
    backup(path)
    path.write_text(json.dumps(filtered, indent=2), encoding="utf-8")
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
    tracker["latestStatus"] = "User-confirmed current location: Paxi / Paxos"
    tracker["latestSource"] = "User-confirmed location; approximate map marker"
    tracker["latestPrecisePosition"] = None
    tracker["latestApproximatePosition"] = AIS_RECORD["position"]
    tracker["note"] = "Previous en-route AIS marker has been replaced because it appears stale. Current marker is plotted approximately in Paxi/Paxos pending a fresh precise AIS coordinate."
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
    out = ROOT / "data/ais/manual/2026-06-30-2112-junos7-paxi-correction.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(AIS_RECORD, indent=2), encoding="utf-8")
    print("Corrected latest position to Paxi / Paxos area.")
    print("Approximate marker plotted at: 39.2026, 20.1858")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
