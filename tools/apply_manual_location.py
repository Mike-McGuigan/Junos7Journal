#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.1"
RELEASE = "Current Marker Fix"

def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-2-1").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def load_update(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if "routePoint" not in data or "tracker" not in data:
        raise SystemExit("Invalid manual location update: expected routePoint and tracker.")
    data["routePoint"]["phase"] = "current"
    return data

def normalise_route(route, new_point):
    cleaned = []
    for item in route:
        same_named_point = item.get("name") == new_point.get("name") and item.get("date") == new_point.get("date")
        if same_named_point:
            continue
        if item.get("phase") == "current":
            item["phase"] = "onboard"
        cleaned.append(item)
    new_point["phase"] = "current"
    cleaned.append(new_point)
    return cleaned

def update_route(path, point):
    if not path.exists():
        return False
    route = json.loads(path.read_text(encoding="utf-8"))
    route = normalise_route(route, point)
    backup(path)
    path.write_text(json.dumps(route, indent=2), encoding="utf-8")
    return True

def update_dashboard(path, update):
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["release"] = RELEASE
    manual = update["tracker"]
    pos = manual["position"]
    tracker = data.setdefault("tracker", {})
    tracker["workflow"] = tracker.get("workflow", "running")
    tracker["provider"] = "manual / provider not configured"
    tracker["liveAis"] = False
    tracker["lastManualLookupUtc"] = manual["timestampUtc"]
    tracker["latestStatus"] = f"Manual location: {manual.get('area', update['routePoint']['name'])}"
    tracker["latestSource"] = manual.get("source", "captains dashboard")
    tracker["latestPrecisePosition"] = pos if "precise" in pos.get("precision", "") else None
    tracker["latestApproximatePosition"] = pos
    tracker["note"] = update["routePoint"].get("note", "")
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

def write_record(update):
    ts = update["tracker"]["timestampUtc"].replace(":", "").replace("-", "")
    name = update["routePoint"]["name"].lower().replace(" ", "-").replace("/", "-")
    out = ROOT / "data" / "ais" / "manual" / f"{ts[:8]}-{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(update, indent=2), encoding="utf-8")
    return out

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/apply_manual_location.py admin-input/latest-location.json")
    update = load_update(Path(sys.argv[1]))
    changed = []
    for rel in ["site/data/route.json", "content/routes/route-so-far.json", "docs/data/route.json"]:
        if update_route(ROOT / rel, update["routePoint"]):
            changed.append(rel)
    for rel in ["site/data/dashboard.json", "docs/data/dashboard.json"]:
        if update_dashboard(ROOT / rel, update):
            changed.append(rel)
    update_version(ROOT / "site/data/version.json")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    record = write_record(update)
    route_path = ROOT / "site/data/route.json"
    if route_path.exists():
        route = json.loads(route_path.read_text(encoding="utf-8"))
        current_count = sum(1 for p in route if p.get("phase") == "current")
        print(f"Current markers in site/data/route.json: {current_count}")
        if current_count != 1:
            raise SystemExit("Expected exactly one current marker.")
    print("Manual location applied.")
    print(f"Location: {update['routePoint']['name']}")
    print(f"Coordinates: {update['routePoint']['lat']}, {update['routePoint']['lng']}")
    print(f"Tracker record: {record.relative_to(ROOT)}")
    print("Updated files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
