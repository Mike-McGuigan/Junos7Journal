# Release 2.0.0 — Production Dashboard

## Highlights

- Consolidated production release.
- Captain's Dashboard with click-to-place map updates.
- One-click local Publish.
- Windows launcher.
- Git health checks.
- Correct current-marker handling.
- About Juno's 7 and Meet the Crew pages.
- Labelled voyage map workflow.

## Apply

Copy this release over the repository root, then run:

```bash
python tools/patch_v2_navigation.py
python tools/build_site.py
git add .
git commit -m "Release 2.0.0 production dashboard"
git push
```

## Use

Double-click:

```text
Start Captains Dashboard.bat
```

Then click the map, enter the location name, and click **Publish**.
