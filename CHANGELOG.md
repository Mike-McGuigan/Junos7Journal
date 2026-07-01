# Changelog

## 1.2.1 - Current Marker Fix

### Fixed
- New admin-selected location is forced to `phase=current`.
- Previous current markers are demoted to `onboard`.
- Same-day/same-name manual locations are replaced instead of duplicated.

### Added
- `tools/fix_existing_current_marker.py`