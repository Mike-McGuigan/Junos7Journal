#!/usr/bin/env python3
from pathlib import Path
from shutil import copytree, rmtree, ignore_patterns
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import time

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"
VERSION_FILE = ROOT / "VERSION"

RELEASE = "Geographic Intelligence"
PROJECT = "Juno's 7 Mediterranean Journal"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def force_remove(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def remove_site() -> None:
    if not SITE.exists():
        return
    for _ in range(5):
        try:
            rmtree(SITE, onexc=force_remove)
            return
        except TypeError:
            try:
                rmtree(SITE, onerror=force_remove)
                return
            except PermissionError:
                time.sleep(1)
        except PermissionError:
            time.sleep(1)
    raise SystemExit("Could not remove site/. Close anything using site/ and try again.")


def read_version() -> str:
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text(encoding="utf-8").strip()
    return "2.1.1"


def read_release(default: str = RELEASE) -> str:
    version_json = DOCS / "data" / "version.json"
    if version_json.exists():
        try:
            data = json.loads(version_json.read_text(encoding="utf-8"))
            return data.get("release") or default
        except Exception:
            pass
    return default


def write_build_metadata(version: str, release: str, build_utc: str) -> None:
    info = {
        "version": version,
        "release": release,
        "buildUtc": build_utc,
        "project": PROJECT,
        "pagesSource": "site",
        "sourceFolder": "docs",
        "outputFolder": "site",
    }

    (SITE / "data").mkdir(parents=True, exist_ok=True)
    (SITE / "data" / "version.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    (SITE / "build-info.json").write_text(json.dumps(info, indent=2), encoding="utf-8")


def write_manifest(version: str, release: str, build_utc: str) -> int:
    manifest = []
    for path in SITE.rglob("*"):
        if path.is_file():
            manifest.append(
                {
                    "path": path.relative_to(SITE).as_posix(),
                    "sizeBytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )

    (SITE / "build-manifest.json").write_text(
        json.dumps(
            {
                "version": version,
                "release": release,
                "buildUtc": build_utc,
                "fileCount": len(manifest),
                "files": manifest,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return len(manifest)


def main() -> None:
    if not DOCS.exists():
        raise SystemExit("docs/ does not exist. docs/ is now the source folder for the generated site.")

    version = read_version()
    release = read_release()
    build_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    remove_site()
    copytree(
        DOCS,
        SITE,
        ignore=ignore_patterns("*.bak-*", "*.bak-geo-*"),
    )

    write_build_metadata(version, release, build_utc)
    file_count = write_manifest(version, release, build_utc)

    print(f"Built site/ from docs/ for version {version}")
    print(f"Release: {release}")
    print(f"Files: {file_count}")


if __name__ == "__main__":
    main()
