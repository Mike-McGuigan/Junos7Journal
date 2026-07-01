#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.2.0"
RELEASE = "Captain's Dashboard"
def backup(path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-2-0").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
def update_route(path, point):
    if not path.exists(): return False
    route=json.loads(path.read_text(encoding="utf-8"))
    if point.get("phase")=="current":
        for item in route:
            if item.get("phase")=="current": item["phase"]="onboard"
    route=[item for item in route if not (item.get("date")==point.get("date") and item.get("name")==point.get("name") and abs(float(item.get("lat",999))-float(point.get("lat",0)))<0.000001 and abs(float(item.get("lng",999))-float(point.get("lng",0)))<0.000001)]
    route.append(point); backup(path); path.write_text(json.dumps(route,indent=2),encoding="utf-8"); return True
def update_dashboard(path, update):
    if not path.exists(): return False
    data=json.loads(path.read_text(encoding="utf-8")); data["version"]=VERSION; data["release"]=RELEASE
    manual=update["tracker"]; pos=manual["position"]; tracker=data.setdefault("tracker",{})
    tracker["workflow"]=tracker.get("workflow","running"); tracker["provider"]="manual / provider not configured"; tracker["liveAis"]=False
    tracker["lastManualLookupUtc"]=manual["timestampUtc"]; tracker["latestStatus"]=f"Manual location: {manual.get('area', update['routePoint']['name'])}"
    tracker["latestSource"]=manual.get("source","captains dashboard"); tracker["latestPrecisePosition"]=pos if "precise" in pos.get("precision","") else None
    tracker["latestApproximatePosition"]=pos; tracker["note"]=update["routePoint"].get("note","")
    backup(path); path.write_text(json.dumps(data,indent=2),encoding="utf-8"); return True
def update_version(path):
    if not path.exists(): return
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception: data={}
    data["version"]=VERSION; data["release"]=RELEASE; backup(path); path.write_text(json.dumps(data,indent=2),encoding="utf-8")
def write_record(update):
    ts=update["tracker"]["timestampUtc"].replace(":","").replace("-","")
    name=update["routePoint"]["name"].lower().replace(" ","-").replace("/","-")
    out=ROOT/"data"/"ais"/"manual"/f"{ts[:8]}-{name}.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(update,indent=2),encoding="utf-8"); return out
def main():
    if len(sys.argv)!=2: raise SystemExit("Usage: python tools/apply_manual_location.py admin-input/latest-location.json")
    update=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if "routePoint" not in update or "tracker" not in update: raise SystemExit("Invalid manual location update.")
    changed=[]
    for rel in ["site/data/route.json","content/routes/route-so-far.json","docs/data/route.json"]:
        if update_route(ROOT/rel, update["routePoint"]): changed.append(rel)
    for rel in ["site/data/dashboard.json","docs/data/dashboard.json"]:
        if update_dashboard(ROOT/rel, update): changed.append(rel)
    update_version(ROOT/"site/data/version.json"); (ROOT/"VERSION").write_text(VERSION+"\\n",encoding="utf-8")
    record=write_record(update)
    print("Manual location applied.")
    print(f"Location: {update['routePoint']['name']}")
    print(f"Coordinates: {update['routePoint']['lat']}, {update['routePoint']['lng']}")
    print(f"Tracker record: {record.relative_to(ROOT)}")
    print("Updated files where present:")
    for item in changed: print(f"- {item}")
    print("Now run: python tools/build_site.py")
if __name__=="__main__": main()
