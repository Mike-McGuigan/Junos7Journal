#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.5"
RELEASE = "Corfu Marker and Map Labels"

CORFU_POINT = {
    "date": "1 Jul",
    "name": "East Coast Corfu",
    "phase": "current",
    "lat": 39.6243,
    "lng": 19.9217,
    "note": "User-confirmed current area on the east coast of Corfu. Marker is approximate until a fresh precise AIS coordinate is available."
}

AIS_RECORD = {
    "timestampUtc": "2026-07-01T07:53:00Z",
    "vesselKey": "junos7",
    "displayName": "JUNOS 7",
    "mmsi": "319303300",
    "imo": "1109712",
    "status": "At/near east coast of Corfu",
    "area": "East coast of Corfu, Ionian Sea, Greece",
    "position": {
        "lat": 39.6243,
        "lng": 19.9217,
        "precision": "approximate area marker",
        "source": "user-confirmed current location"
    },
    "source": "user-confirmed observation; public free AIS coordinates may be stale",
    "confidence": "area high; exact coordinate approximate pending fresh precise AIS"
}

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-0-5").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def update_route(path):
    if not path.exists():
        return False
    route = json.loads(path.read_text(encoding="utf-8"))
    for point in route:
        if point.get("phase") == "current":
            point["phase"] = "onboard"
    route = [p for p in route if p.get("name") != CORFU_POINT["name"]]
    route.append(CORFU_POINT)
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
    tracker["latestStatus"] = "User-confirmed current area: east coast of Corfu"
    tracker["latestSource"] = "User-confirmed location; approximate map marker"
    tracker["latestPrecisePosition"] = None
    tracker["latestApproximatePosition"] = AIS_RECORD["position"]
    tracker["note"] = "Public free AIS coordinates may lag. This marker uses the user-confirmed current area and is intentionally labelled approximate."
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

def patch_dashboard_js(path):
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8")
    original = text
    backup(path)

    # Default to OSM labelled map, keep satellite available.
    text = text.replace(
        "sat.addTo(map);L.control.layers({'Satellite':sat,'Map':street}).addTo(map);",
        "street.addTo(map);L.control.layers({'Map with place names':street,'Satellite':sat}).addTo(map);"
    )
    text = text.replace(
        "satellite.addTo(map); L.control.layers({'Satellite': satellite, 'Map': street}).addTo(map);",
        "street.addTo(map); L.control.layers({'Map with place names': street, 'Satellite': satellite}).addTo(map);"
    )
    text = text.replace(
        "satellite.addTo(map);\n  L.control.layers({'Satellite': satellite, 'Map': street}).addTo(map);",
        "street.addTo(map);\n  L.control.layers({'Map with place names': street, 'Satellite': satellite}).addTo(map);"
    )
    text = text.replace("'Map':street", "'Map with place names':street")
    text = text.replace("'Map': street", "'Map with place names': street")

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False

def main():
    changed = []
    for rel in ["site/data/route.json", "content/routes/route-so-far.json", "docs/data/route.json"]:
        if update_route(ROOT / rel):
            changed.append(rel)
    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel):
            changed.append(rel)
    for rel in ["site/assets/js/dashboard.js", "docs/assets/js/dashboard.js"]:
        if patch_dashboard_js(ROOT / rel):
            changed.append(rel)
    update_version_json(ROOT / "site/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")

    out = ROOT / "data/ais/manual/2026-07-01-0753-junos7-east-corfu.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(AIS_RECORD, indent=2), encoding="utf-8")

    print("Added East Coast Corfu approximate current marker.")
    print("Changed the voyage map default layer to 'Map with place names'.")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
