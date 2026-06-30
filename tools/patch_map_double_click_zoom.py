#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_JS = ROOT / "site" / "assets" / "js" / "dashboard.js"

DOUBLE_CLICK_BLOCK = """
  // Double-click anywhere on the map to zoom in around that exact location.
  // This is deliberately stronger than Leaflet's default double-click zoom,
  // so it feels useful when browsing satellite tiles on desktop.
  map.doubleClickZoom.disable();
  map.on('dblclick', function (event) {
    const targetZoom = Math.min(map.getZoom() + 3, map.getMaxZoom() || 19);
    map.flyTo(event.latlng, targetZoom, { duration: 0.45 });
  });
"""

def main():
    if not DASHBOARD_JS.exists():
        raise SystemExit("site/assets/js/dashboard.js not found")

    text = DASHBOARD_JS.read_text(encoding="utf-8")
    backup = DASHBOARD_JS.with_suffix(".js.bak-0-7-3")
    backup.write_text(text, encoding="utf-8")

    if "map.on('dblclick'" in text or 'map.on("dblclick"' in text:
        print("Double-click zoom already appears to be installed.")
        return

    needles = [
        "const map = L.map('voyageMap', {scrollWheelZoom: false});",
        "const map = L.map('voyageMap', { scrollWheelZoom: false });",
        'const map = L.map("voyageMap", {scrollWheelZoom: false});',
        'const map = L.map("voyageMap", { scrollWheelZoom: false });'
    ]

    for needle in needles:
        if needle in text:
            text = text.replace(needle, needle + "\n" + DOUBLE_CLICK_BLOCK, 1)
            DASHBOARD_JS.write_text(text, encoding="utf-8")
            print("Patched map double-click zoom into site/assets/js/dashboard.js")
            print(f"Backup written to {backup}")
            return

    raise SystemExit("Could not find the map creation line in dashboard.js. Send me dashboard.js and I will adapt the patch.")

if __name__ == "__main__":
    main()
