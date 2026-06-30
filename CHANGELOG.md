# Changelog

## 0.7.1 - Current Location and Homepage Voyage Link

### Added
- `data/ais/manual/2026-06-30-0918-junos7.json`
- Latest AIS summary data in `site/data/dashboard.json`
- Current marker in `site/data/route.json`
- Homepage patch tool: `tools/patch_homepage_voyage_link.py`

### Changed
- Dashboard now displays latest precise stored coordinates and current public AIS summary.
- Map highlights the latest/current marker in orange.
- Homepage navigation can be patched to link to `voyage.html`.

### Note
The 30 Jun lookup confirms recent AIS reporting in the East Mediterranean / West Coast Greece area. The fresh public text result did not expose a new coordinate, so the map retains the latest precise coordinate already stored from 29 Jun.