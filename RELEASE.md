# Current Release

Version: 1.2.0

Name: Captain's Dashboard

## Highlights

- Adds a Leaflet-based Captain's Dashboard admin page.
- Click the map to select a new latest location.
- Existing route is visible on the admin map.
- Drag the selected marker to refine the position.
- Download update JSON and apply it locally.
- Labelled map tiles are the default; satellite remains available.

## Apply

```bash
python tools/patch_captains_dashboard_nav.py
python tools/build_site.py
```

## Use

1. Open `admin.html`.
2. Click the map at the latest location.
3. Download the generated JSON.
4. Save it as `admin-input/latest-location.json`.
5. Run:

```bash
python tools/apply_manual_location.py admin-input/latest-location.json
python tools/build_site.py
```