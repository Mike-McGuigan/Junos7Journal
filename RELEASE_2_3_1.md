# Juno's 7 Journal v2.3.1

## Hero branding polish

- The public-page hero now uses a transparent J7 mark, allowing the page's live navy/sea gradient to show through exactly.
- The approved rounded-square logo remains the favicon and installed-app icon.
- The hero mark is larger and the artwork occupies more of its canvas.

## Apply

Extract the changed-files patch over a v2.3.0 repository root, rebuild, preview and commit on a release branch.

```bash
python tools/build_site.py
python -m http.server 8000 --directory docs
```
