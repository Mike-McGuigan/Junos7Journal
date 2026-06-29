#!/usr/bin/env python3
from pathlib import Path
from shutil import copytree, rmtree
from datetime import datetime, timezone
import json
import hashlib
import os
import stat
import time

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"
VERSION_FILE = ROOT / "VERSION"

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def read_version():
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "0.0.0"

def force_remove_readonly(func, path, exc_info):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        raise

def remove_docs_safely():
    if not DOCS.exists():
        return

    for attempt in range(5):
        try:
            # Python 3.12+
            rmtree(DOCS, onexc=force_remove_readonly)
            return
        except TypeError:
            # Python <3.12
            try:
                rmtree(DOCS, onerror=force_remove_readonly)
                return
            except PermissionError:
                pass
        except PermissionError:
            pass

        time.sleep(1)

    raise SystemExit(
        "Could not remove docs/. Close any Explorer windows, editors, browser previews, "
        "or local web servers using docs/, pause OneDrive sync if needed, then try again."
    )

def main():
    if not SITE.exists():
        raise SystemExit("site/ folder not found. Nothing to build.")

    version = read_version()
    build_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    remove_docs_safely()
    copytree(SITE, DOCS)

    data_dir = DOCS / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    version_info = {
        "version": version,
        "release": "Release Management",
        "buildUtc": build_utc,
        "status": "development",
        "project": "Juno's 7 Mediterranean Journal",
        "pagesSource": "docs"
    }

    (data_dir / "version.json").write_text(json.dumps(version_info, indent=2), encoding="utf-8")
    (DOCS / "build-info.json").write_text(json.dumps(version_info, indent=2), encoding="utf-8")

    build_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Build Info - Juno's 7 Mediterranean Journal</title>
  <link rel="stylesheet" href="assets/css/style.css">
  <link rel="stylesheet" href="assets/css/version.css">
</head>
<body class="build-info-page">
  <h1>Build Info</h1>
  <div class="build-info-card">
    <p><strong>Project:</strong> Juno's 7 Mediterranean Journal</p>
    <p><strong>Version:</strong> {version}</p>
    <p><strong>Release:</strong> Release Management</p>
    <p><strong>Built:</strong> {build_utc}</p>
    <p><strong>GitHub Pages source:</strong> /docs</p>
  </div>
  <p><a href="index.html">Back to journal</a></p>
</body>
</html>
"""
    (DOCS / "build-info.html").write_text(build_html, encoding="utf-8")

    manifest = []
    for path in DOCS.rglob("*"):
        if path.is_file():
            manifest.append({
                "path": path.relative_to(DOCS).as_posix(),
                "sizeBytes": path.stat().st_size,
                "sha256": sha256(path)
            })

    (DOCS / "build-manifest.json").write_text(json.dumps({
        "version": version,
        "release": "Release Management",
        "buildUtc": build_utc,
        "fileCount": len(manifest),
        "files": manifest
    }, indent=2), encoding="utf-8")

    print(f"Built docs/ for version {version}")
    print(f"Files: {len(manifest)}")
    print("Open docs/build-info.html or publish docs/ via GitHub Pages.")

if __name__ == "__main__":
    main()
