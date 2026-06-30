#!/usr/bin/env python3
from pathlib import Path
from shutil import copytree, rmtree
from datetime import datetime, timezone
import json, hashlib, os, stat, time

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"site"
DOCS=ROOT/"docs"
VERSION_FILE=ROOT/"VERSION"

def sha256(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_version():
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "0.0.0"

def force_remove(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_docs():
    if not DOCS.exists(): return
    for _ in range(5):
        try:
            rmtree(DOCS, onexc=force_remove); return
        except TypeError:
            try: rmtree(DOCS, onerror=force_remove); return
            except PermissionError: time.sleep(1)
        except PermissionError: time.sleep(1)
    raise SystemExit("Could not remove docs/. Close any process using docs/ and try again.")

def main():
    version=read_version()
    build_utc=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    remove_docs()
    copytree(SITE, DOCS)
    data_dir=DOCS/"data"; data_dir.mkdir(parents=True, exist_ok=True)
    version_info={"version":version,"release":"Dashboard and Mapping","buildUtc":build_utc,"project":"Juno's 7 Mediterranean Journal","pagesSource":"docs"}
    (data_dir/"version.json").write_text(json.dumps(version_info, indent=2), encoding="utf-8")
    (DOCS/"build-info.json").write_text(json.dumps(version_info, indent=2), encoding="utf-8")
    (DOCS/"build-info.html").write_text(f'''<!DOCTYPE html><html><head><meta charset="utf-8"><title>Build Info</title><link rel="stylesheet" href="assets/css/style.css"><link rel="stylesheet" href="assets/css/dashboard.css"></head><body><section class="section"><p class="kicker">Build Info</p><h2>Juno's 7 Mediterranean Journal</h2><p><strong>Version:</strong> {version}</p><p><strong>Release:</strong> Dashboard and Mapping</p><p><strong>Built:</strong> {build_utc}</p><p><a href="index.html">Home</a> · <a href="voyage.html">Voyage dashboard</a></p></section></body></html>''', encoding="utf-8")
    manifest=[]
    for path in DOCS.rglob("*"):
        if path.is_file():
            manifest.append({"path":path.relative_to(DOCS).as_posix(),"sizeBytes":path.stat().st_size,"sha256":sha256(path)})
    (DOCS/"build-manifest.json").write_text(json.dumps({"version":version,"release":"Dashboard and Mapping","buildUtc":build_utc,"fileCount":len(manifest),"files":manifest}, indent=2), encoding="utf-8")
    print(f"Built docs/ for version {version}")
    print(f"Files: {len(manifest)}")

if __name__=="__main__":
    main()
