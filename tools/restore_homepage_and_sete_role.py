#!/usr/bin/env python3
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

SAFE_CAPTION = "Juno's 7 in the marina shortly after Cameron and Sophie joined."
SETE_ROLE = "Chase boat / support vessel accompanying Juno's 7."

def restore_homepage_from_backup():
    if not INDEX.exists():
        raise SystemExit("site/index.html not found")

    candidates = [
        INDEX.with_suffix(".html.bak-0-7-5"),
        INDEX.with_suffix(".html.bak-0-7-2"),
        INDEX.with_suffix(".html.bak-0-7-1"),
    ]

    backup = next((p for p in candidates if p.exists()), None)

    if backup:
        text = backup.read_text(encoding="utf-8")
        INDEX.with_suffix(".html.bak-before-0-7-6-restore").write_text(
            INDEX.read_text(encoding="utf-8"), encoding="utf-8"
        )
        print(f"Restored homepage from {backup.name}")
    else:
        text = INDEX.read_text(encoding="utf-8")
        print("No homepage backup found; cleaning current homepage only.")

    # Remove duplicate dashboard CTA blocks from previous patches, without touching surrounding sections.
    text = re.sub(
        r'<div\s+class=["\']voyage-dashboard-cta["\'][\s\S]*?</div>',
        '',
        text,
        flags=re.I
    )

    # Make navigation/buttons open the new real dashboard page where obvious.
    text = text.replace('href="#voyage"', 'href="voyage.html"')
    text = text.replace("href='#voyage'", "href='voyage.html'")

    # Add one small link only if there is no direct voyage.html link.
    if "voyage.html" not in text:
        cta = """
<div class="voyage-dashboard-cta">
  <p class="kicker">Voyage Dashboard</p>
  <h3>Open the live Voyage Dashboard</h3>
  <p>The interactive map, latest known position and route timeline now live on their own page.</p>
  <a href="voyage.html">Open Voyage Dashboard</a>
</div>
"""
        text = text.replace("</body>", cta + "\n</body>")

    INDEX.write_text(text, encoding="utf-8")

def fix_sete_role():
    changed = []
    for rel in [
        "content/vessels/sete.json",
        "site/data/vessels/sete.json",
        "docs/data/vessels/sete.json",
        "site/data/sete.json",
        "docs/data/sete.json",
    ]:
        path = ROOT / rel
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        if isinstance(data, dict):
            data["name"] = data.get("name", "SETE")
            data["mmsi"] = data.get("mmsi", "319314700")
            data["type"] = data.get("type", "Chase boat")
            data["role_in_journal"] = SETE_ROLE
            data["caption_note"] = "Do not state SETE is visible in a photograph unless it can be clearly identified."
            path.with_suffix(path.suffix + ".bak-0-7-6").write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            changed.append(rel)

    if changed:
        print("Restored SETE vessel role in:")
        for item in changed:
            print(f"- {item}")
    else:
        print("No SETE vessel JSON file found to update.")

def fix_known_photo_captions_only():
    changed = []
    target_files = [
        ROOT / "site" / "data" / "journal.json",
        ROOT / "content" / "media-index" / "media-index.json",
        ROOT / "docs" / "data" / "journal.json",
    ]

    for path in target_files:
        if not path.exists():
            continue

        text = path.read_text(encoding="utf-8")
        original = text

        for field in ["caption", "title", "alt"]:
            pattern = rf'("{field}"\s*:\s*")([^"]*Juno[^"]*SETE[^"]*)(")'
            text = re.sub(
                pattern,
                lambda m: m.group(1) + SAFE_CAPTION.replace('"', '\\"') + m.group(3),
                text,
                flags=re.I
            )

        for phrase in [
            "Juno’s 7 with her chase boat SETE nearby.",
            "Juno's 7 with her chase boat SETE nearby.",
            "Juno’s 7 with SETE nearby.",
            "Juno's 7 with SETE nearby.",
            "Juno’s 7 and her chase boat SETE.",
            "Juno's 7 and her chase boat SETE.",
        ]:
            text = text.replace(phrase, SAFE_CAPTION)

        if text != original:
            path.with_suffix(path.suffix + ".bak-0-7-6").write_text(original, encoding="utf-8")
            path.write_text(text, encoding="utf-8")
            changed.append(path.relative_to(ROOT).as_posix())

    if changed:
        print("Corrected photo captions in:")
        for item in changed:
            print(f"- {item}")
    else:
        print("No matching photo captions found in known journal/media data files.")

def main():
    restore_homepage_from_backup()
    fix_sete_role()
    fix_known_photo_captions_only()
    print("Done. Now run: python tools/build_site.py")

if __name__ == "__main__":
    main()
