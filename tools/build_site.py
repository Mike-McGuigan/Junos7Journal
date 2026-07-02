#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from shutil import copytree, rmtree
import hashlib
import json
import os
import stat
import time

from voyage_routing import enrich_route_file

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = ROOT / "site"
VERSION_FILE = ROOT / "VERSION"
GEOMETRY_FILE = ROOT / "content" / "routes" / "voyage-geometry.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def force_remove(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_tree(path: Path) -> None:
    if not path.exists():
        return
    for _ in range(5):
        try:
            rmtree(path, onexc=force_remove)
            return
        except TypeError:
            try:
                rmtree(path, onerror=force_remove)
                return
            except PermissionError:
                time.sleep(1)
        except PermissionError:
            time.sleep(1)
    raise SystemExit(f"Could not remove {path}. Close anything using it and try again.")


def load_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return fallback


def count_journal_entries() -> int | None:
    data = load_json(DOCS / "data" / "journal.json", None)
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("entries", "journal", "items"):
            if isinstance(data.get(key), list):
                return len(data[key])
    journal_dir = ROOT / "content" / "journal"
    if journal_dir.exists():
        return len([p for p in journal_dir.rglob("*.md") if not p.name.startswith(".")])
    return None


def media_stats() -> dict:
    data = load_json(DOCS / "data" / "media.json", None)
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        for key in ("items", "media"):
            if isinstance(data.get(key), list):
                items = data[key]
                break

    if items:
        photos = sum(1 for item in items if str(item.get("type", "")).lower() in {"photo", "image"})
        videos = sum(1 for item in items if str(item.get("type", "")).lower() == "video")
        return {"mediaItems": len(items), "photos": photos, "videos": videos}

    media_root = DOCS / "media"
    photo_count = len(list((media_root / "photos").glob("*"))) if (media_root / "photos").exists() else None
    video_count = len(list((media_root / "videos").glob("*"))) if (media_root / "videos").exists() else None
    out = {}
    if photo_count is not None:
        out["photos"] = photo_count
    if video_count is not None:
        out["videos"] = video_count
    if out:
        out["mediaItems"] = out.get("photos", 0) + out.get("videos", 0)
    return out


def update_dashboard_stats(route_stats: dict) -> None:
    path = DOCS / "data" / "dashboard.json"
    data = load_json(path, {})
    stats = data.setdefault("stats", {})
    stats.update(route_stats)

    journal_entries = count_journal_entries()
    if journal_entries is not None:
        stats["journalEntries"] = journal_entries
    stats.update(media_stats())

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_build_metadata(version: str, build_utc: str) -> None:
    info = {
        "version": version,
        "release": "Geographic Intelligence",
        "buildUtc": build_utc,
        "project": "Juno's 7 Mediterranean Journal",
        "pagesSource": "docs",
        "siteOutput": "site",
    }
    (DOCS / "data").mkdir(parents=True, exist_ok=True)
    (DOCS / "data" / "version.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    (DOCS / "build-info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")

    manifest = []
    for path in DOCS.rglob("*"):
        if path.is_file():
            manifest.append(
                {
                    "path": path.relative_to(DOCS).as_posix(),
                    "sizeBytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    (DOCS / "build-manifest.json").write_text(
        json.dumps(
            {
                "version": version,
                "release": "Geographic Intelligence",
                "buildUtc": build_utc,
                "fileCount": len(manifest),
                "files": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("docs/ does not exist. Nothing to build.")

    version = VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "2.1.1"
    build_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    route_stats = enrich_route_file(DOCS / "data" / "route.json", GEOMETRY_FILE)
    update_dashboard_stats(route_stats)
    write_build_metadata(version, build_utc)

    remove_tree(SITE)
    copytree(DOCS, SITE, ignore=lambda _dir, names: [name for name in names if ".bak" in name])

    file_count = sum(1 for p in SITE.rglob("*") if p.is_file())
    print(f"Built site/ from docs/ for version {version}")
    print(f"Files: {file_count}")
    if route_stats:
        print(f"Estimated voyage distance: {route_stats.get('distanceEstimatedNm')} NM")
        print(f"Manual sea-route legs: {route_stats.get('manualSeaRouteLegs')}")


if __name__ == "__main__":
    main()
