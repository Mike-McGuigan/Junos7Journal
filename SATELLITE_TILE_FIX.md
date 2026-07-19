# Voyage satellite map tile fix

## Problem

The voyage dashboard requested Esri World Imagery tiles using the wrong coordinate order and an unnecessary `.png` suffix:

```text
.../tile/{z}/{x}/{y}.png
```

Leaflet uses `{x}/{y}`, while the ArcGIS REST tile endpoint expects `{y}/{x}`. This caused valid satellite tiles from unrelated locations to appear beneath the correctly positioned voyage route, producing the blocky farmland view seen around Cavtat.

## Fix

The voyage map now uses the correct Esri endpoint:

```text
.../tile/{z}/{y}/{x}
```

The labelled OpenStreetMap layer and all route, marker and timeline behaviour are unchanged.

## Apply and publish

Extract this changed-files ZIP into the repository root, replacing the existing file, then run:

```bash
python tools/build_site.py

git status
git add docs/assets/js/dashboard.js SATELLITE_TILE_FIX.md PATCH_MANIFEST_SATELLITE_TILE_FIX.txt site
git commit -m "Fix voyage satellite tile coordinates"
git push origin main
```

The package deliberately excludes the generated `site/` directory. `python tools/build_site.py` recreates it locally.
