#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from shutil import copytree, rmtree
import hashlib
import json
import os
import re
import stat
import time

from voyage_routing import enrich_route_file
from contextual_discovery import build as build_contextual_discovery

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
SITE = ROOT / "site"
VERSION_FILE = ROOT / "VERSION"
RELEASE_TITLE_FILE = ROOT / "RELEASE_TITLE"
GEOMETRY_FILE = ROOT / "content" / "routes" / "voyage-geometry.json"

def current_version() -> str:
    return VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else "2.3.0"


def current_release_title() -> str:
    return RELEASE_TITLE_FILE.read_text(encoding="utf-8").strip() if RELEASE_TITLE_FILE.exists() else "Unreleased"

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



def sync_embedded_journal_media() -> int:
    """Keep journal.json's embedded media list aligned with the canonical media index."""
    journal_path = DOCS / "data" / "journal.json"
    media_path = DOCS / "data" / "media.json"
    journal = load_json(journal_path, {})
    media = load_json(media_path, [])

    if not isinstance(journal, dict):
        raise SystemExit(f"{journal_path} must contain a JSON object")
    if isinstance(media, dict):
        media = media.get("items") or media.get("media") or []
    if not isinstance(media, list):
        raise SystemExit(f"{media_path} must contain a media list")

    journal["release"] = current_version()
    journal["media"] = media
    journal_path.write_text(json.dumps(journal, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(media)


def sync_embedded_journal_route() -> int:
    """Keep journal.json's legacy embedded route copy aligned with route.json."""
    journal_path = DOCS / "data" / "journal.json"
    route_path = DOCS / "data" / "route.json"
    journal = load_json(journal_path, {})
    route = load_json(route_path, [])

    if not isinstance(journal, dict):
        raise SystemExit(f"{journal_path} must contain a JSON object")
    if not isinstance(route, list):
        raise SystemExit(f"{route_path} must contain a route list")

    journal["route"] = route
    journal_path.write_text(json.dumps(journal, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(route)



def validate_media_catalogue() -> dict:
    media_path = DOCS / "data" / "media.json"
    items = load_json(media_path, [])
    if not isinstance(items, list):
        raise SystemExit(f"{media_path} must contain a JSON list")
    allowed_types = {"photo", "video"}
    allowed_categories = {"scenic", "crew", "junos7", "ports-anchorages", "wildlife", "weather", "behind-scenes", "tenders-toys"}
    seen = set()
    errors = []
    for index, item in enumerate(items):
        media_id = item.get("id")
        if not media_id:
            errors.append(f"Media item {index + 1} has no id")
        elif media_id in seen:
            errors.append(f"Duplicate media id: {media_id}")
        seen.add(media_id)
        media_type = str(item.get("type", "")).lower()
        if media_type not in allowed_types:
            errors.append(f"{media_id}: invalid type {media_type!r}")
        categories = item.get("categories")
        if not isinstance(categories, list) or not categories:
            errors.append(f"{media_id}: at least one category is required")
        else:
            unknown = sorted(set(categories) - allowed_categories)
            if unknown:
                errors.append(f"{media_id}: unknown categories {unknown}")
        url = item.get("url")
        if not url or not (DOCS / url).is_file():
            errors.append(f"{media_id}: missing media file {url!r}")
        enhanced = item.get("enhancedUrl")
        if enhanced and not (DOCS / enhanced).is_file():
            errors.append(f"{media_id}: missing enhanced file {enhanced!r}")
    journal = load_json(DOCS / "data" / "journal.json", {})
    for entry in journal.get("entries", []) if isinstance(journal, dict) else []:
        for media_id in entry.get("media", []):
            if media_id not in seen:
                errors.append(f"Journal entry {entry.get('id')}: unknown media id {media_id}")
    if errors:
        raise SystemExit("Media validation failed:\n- " + "\n- ".join(errors))
    return {"mediaItems": len(items), "categories": sorted({c for item in items for c in item.get("categories", [])})}


def validate_text_encoding() -> None:
    """Catch mojibake replacement markers before they reach the public site."""
    paths = [
        DOCS / "data" / "journal.json",
        DOCS / "data" / "discoveries.json",
        DOCS / "data" / "media.json",
        DOCS / "data" / "route.json",
    ]
    suspicious = re.compile(r"(?<=[A-Za-z])\?(?=[A-Za-z])|(?<![?!.])\?(?=[A-Za-zÀ-ž])")
    allowed_keys = {"url", "enhancedUrl"}
    errors = []

    def walk(value, trail):
        if isinstance(value, dict):
            for key, child in value.items():
                walk(child, trail + [str(key)])
        elif isinstance(value, list):
            for index, child in enumerate(value):
                walk(child, trail + [str(index)])
        elif isinstance(value, str) and (not trail or trail[-1] not in allowed_keys):
            if suspicious.search(value):
                errors.append(f"{'.'.join(trail)}: {value}")

    for path in paths:
        data = load_json(path, None)
        if data is not None:
            walk(data, [path.relative_to(ROOT).as_posix()])

    if errors:
        raise SystemExit("Text encoding validation failed:\n- " + "\n- ".join(errors[:30]))

def count_journal_entries() -> int | None:
    data = load_json(DOCS / "data" / "journal.json", None)
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("entries", "journal", "items"):
            if isinstance(data.get(key), list):
                return len(data[key])
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


def update_dashboard_stats(route_stats: dict, discovery_stats: dict | None = None) -> None:
    path = DOCS / "data" / "dashboard.json"
    data = load_json(path, {})
    stats = data.setdefault("stats", {})
    stats.update(route_stats)

    journal_entries = count_journal_entries()
    if journal_entries is not None:
        stats["journalEntries"] = journal_entries
    stats.update(media_stats())
    if discovery_stats is not None:
        stats["contextualDiscoveries"] = int(discovery_stats.get("count", 0))
    data["version"] = current_version()
    data["release"] = current_release_title()

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_build_metadata(version: str, build_utc: str) -> None:
    info = {
        "version": version,
        "release": current_release_title(),
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
                "release": current_release_title(),
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

    version = current_version()
    build_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    media_validation = validate_media_catalogue()
    embedded_media_count = sync_embedded_journal_media()
    route_stats = enrich_route_file(DOCS / "data" / "route.json", GEOMETRY_FILE)
    embedded_route_count = sync_embedded_journal_route()
    discovery_stats = build_contextual_discovery()
    validate_text_encoding()
    update_dashboard_stats(route_stats, discovery_stats)
    write_build_metadata(version, build_utc)

    remove_tree(SITE)
    copytree(DOCS, SITE, ignore=lambda _dir, names: [name for name in names if ".bak" in name])

    file_count = sum(1 for p in SITE.rglob("*") if p.is_file())
    print(f"Built site/ from docs/ for version {version}")
    print(f"Files: {file_count}")
    print(f"Embedded journal media: {embedded_media_count}")
    print(f"Embedded journal route points: {embedded_route_count}")
    print(f"Gallery categories: {len(media_validation['categories'])}")
    if route_stats:
        print(f"Estimated voyage distance: {route_stats.get('distanceEstimatedNm')} NM")
        print(f"Manual sea-route legs: {route_stats.get('manualSeaRouteLegs')}")


if __name__ == "__main__":
    main()
