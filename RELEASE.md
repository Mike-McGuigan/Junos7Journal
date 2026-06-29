# Current Release

Version: 0.5.0

Name: Release Management

Build date: 2026-06-29 16:18:56 UTC

Status: Development

## Highlights

- Adds root `VERSION`
- Adds root `RELEASE.md`
- Adds `site/data/version.json`
- Adds visible version badge/footer support
- Adds `tools/build_site.py`
- Adds GitHub Pages diagnostic page generation

## Publish Workflow

```bash
python tools/patch_version_display.py
python tools/build_site.py
git add .
git commit -m "Release 0.5.0"
git push
```

Then check:

```text
https://YOUR-GITHUB-USERNAME.github.io/Junos7Journal/build-info.html
```
