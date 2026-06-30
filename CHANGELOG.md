# Changelog

## 0.7.2 - Route Gap and Homepage Map Replacement

### Added
- `data/ais/manual/2026-06-30-1010-junos7-gap-reconstruction.json`
- Additional route points for 23 Jun, 24 Jun and 25 Jun.
- Homepage replacement tool: `tools/replace_homepage_voyage_section.py`

### Changed
- `site/data/route.json` now includes partial public-history points between Ios and Zakynthos.
- `site/data/dashboard.json` version updated to 0.7.2.
- Homepage old embedded voyage SVG section can now be replaced entirely rather than just linked around.

### Notes
The Ios to Zakynthos gap is a partial reconstruction from public AIS snippets, not complete historical AIS.
