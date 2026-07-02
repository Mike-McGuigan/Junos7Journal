# Stop Position Editor

Adds a Stop Editor to Captain's Dashboard.

## What it does
- Select an existing stop from the new Stop Editor panel.
- Click **Move Stop**.
- Drag the cyan marker or click a new map position.
- Click **Save Stop**.
- The local server updates `docs/data/route.json`, optionally clears manual sea-route geometry for adjacent legs, runs `tools/build_site.py`, and refreshes the local site output.

## Files changed
- `docs/admin.html`
- `docs/assets/js/admin-map.js`
- `docs/assets/css/admin-map.css`
- `tools/admin_publish_server.py`

## Notes
Moving a stop can invalidate manual sea-route waypoints on the previous and next legs. The editor defaults to clearing those affected manual routes so they can be redrawn cleanly.
