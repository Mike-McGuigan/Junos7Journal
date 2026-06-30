#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.0.1"
RELEASE = "Cam Towing Toys Fix"

MEDIA_ID = "cam-towing-toys"
MEDIA_ITEM = {
    "id": MEDIA_ID,
    "type": "video",
    "date": "2026-06-30",
    "url": "media/videos/2026-06-30-cam-towing-toys.mp4",
    "title": "Cam on a mission",
    "caption": "Cameron towing the yacht's inflatable water toys from the tender during livelier conditions. No-one was on the toys at the time."
}

BODY_ADDITION = (
    "Sophie also captured Cameron towing the yacht's inflatable water toys from the tender. "
    "It was one of those practical deck-crew moments that sits behind the guest experience: "
    "getting equipment safely into position and managing it in livelier conditions. "
    "It has since been confirmed that no-one was on the toys at the time."
)

def backup(path: Path):
    if path.exists():
        path.with_suffix(path.suffix + ".bak-1-0-1").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")

def dedupe_by_id(items):
    seen = set()
    out = []
    for item in items:
        item_id = item.get("id")
        if item_id in seen:
            continue
        seen.add(item_id)
        out.append(item)
    return out

def update_journal_json(path: Path):
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))

    media = data.setdefault("media", [])
    existing = next((m for m in media if m.get("id") == MEDIA_ID), None)
    if existing:
        existing.update(MEDIA_ITEM)
    else:
        media.append(MEDIA_ITEM)
    data["media"] = dedupe_by_id(media)

    entries = data.setdefault("entries", [])
    target = next((e for e in entries if e.get("date") == "2026-06-30"), None)
    if target is None:
        target = {
            "date": "2026-06-30",
            "title": "Underway — Changing Conditions",
            "location": "At Sea",
            "type": "at-sea",
            "person": "Cameron & Sophie",
            "quote": "Underway for another 2.5 hours. / A little stormy today. / Cam on a mission.",
            "media": [MEDIA_ID],
            "body": BODY_ADDITION
        }
        entries.append(target)
    else:
        media_ids = target.setdefault("media", [])
        if MEDIA_ID not in media_ids:
            media_ids.append(MEDIA_ID)
        quote = target.get("quote", "")
        if "Cam on a mission" not in quote:
            target["quote"] = (quote + " / Cam on a mission.").strip(" /")
        body = target.get("body", "")
        if "no-one was on the toys" not in body.lower():
            target["body"] = body.rstrip() + "\n\n" + BODY_ADDITION

    backup(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

def update_media_json(path: Path):
    if not path.exists():
        return False
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.setdefault("media", [])
    existing = next((m for m in items if m.get("id") == MEDIA_ID), None)
    if existing:
        existing.update(MEDIA_ITEM)
    else:
        items.append(MEDIA_ITEM)

    if isinstance(data, list):
        data = dedupe_by_id(items)
    else:
        data["media"] = dedupe_by_id(items)

    backup(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True

def update_markdown():
    md_path = ROOT / "content" / "journal" / "2026" / "2026-06-30-underway-changing-conditions.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)

    if md_path.exists():
        text = md_path.read_text(encoding="utf-8")
    else:
        text = """---
date: 2026-06-30
title: Underway — Changing Conditions
location: At Sea
type: at-sea
media:
  - underway-aft-deck
  - sophie-stormy
---

# 30 June 2026 — Underway
"""

    if "cam-towing-toys" not in text:
        text = text.replace("  - sophie-stormy", "  - sophie-stormy\n  - cam-towing-toys")
    if "Cam on a mission" not in text:
        text += """

## Sophie

> "Cam on a mission."

Sophie captured Cameron towing the yacht's inflatable water toys from the tender during livelier conditions. It has since been confirmed that no-one was on the toys at the time.

**Video caption**

> Cameron towing the yacht's inflatable water toys from the tender during livelier conditions. No-one was on the toys at the time.
"""
    backup(md_path)
    md_path.write_text(text, encoding="utf-8")

def update_version_files():
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    path = ROOT / "site" / "data" / "version.json"
    if path.exists():
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
    for rel in ["site/data/journal.json", "docs/data/journal.json"]:
        if update_journal_json(ROOT / rel):
            changed.append(rel)

    for rel in ["site/data/media.json", "content/media-index/media-index.json", "docs/data/media.json"]:
        if update_media_json(ROOT / rel):
            changed.append(rel)

    update_markdown()
    update_version_files()

    print("Added/updated Cam on a mission video content.")
    print("Updated JSON files where present:")
    for item in changed:
        print(f"- {item}")
    print("Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
