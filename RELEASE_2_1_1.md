# Release 2.1.1 - Geographic Intelligence polish

Small follow-up patch for v2.1.0.

## Fixes

- Captain's Dashboard admin map now displays enriched friendly location information in route marker popups when available.
- Publish health check no longer shows the Git credential helper as a blocking error when it is not globally configured.
- Version metadata updated to 2.1.1.

## Install

Extract this zip over the repository root and allow files to be replaced, then run:

```bash
python tools/build_site.py
```
