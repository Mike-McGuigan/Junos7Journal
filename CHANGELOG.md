# Changelog

## 0.7.3 - Map Double Click Zoom

### Added
- `tools/patch_map_double_click_zoom.py`

### Changed
- Adds double-click-to-zoom behaviour to the Leaflet voyage map.

### Behaviour
- Single click behaviour is unchanged.
- Double-click zooms in around the clicked map tile.
- The map zoom increases by 3 levels, capped at the map provider's maximum zoom.