# Current Release

Version: 1.0.0

Name: Juno's 7 Companion Pages

Build date: 2026-06-30 16:30:56 UTC

## Highlights

- Adds `site/about.html` — About Juno's 7.
- Adds `site/crew.html` — Meet the Crew.
- Adds companion page styling.
- Adds a navigation patch script.
- Adds `PROJECT_NOTES.md`.
- Adds structured yacht data at `site/data/about-junos7.json`.

## Apply

```bash
python tools/patch_companion_nav.py
python tools/build_site.py
```

Commit:

```text
Release 1.0.0 companion pages
```