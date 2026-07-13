# Juno's 7 Journal v2.2.2 — Journal Experience Polish

This is a **changed-files patch** for an existing v2.2.1 repository. It is not a full repository export.

## Changes

- The opening chapter now identifies **Kos** immediately and displays **Kos, Greece** as its location.
- The supplied J7 artwork is rebuilt on the exact site navy (`#061928`) with clean transparent outer corners and no white rim.
- Gallery cards use a continuous navy surface, removing white gaps and corner slivers when captions differ in length.
- Gallery titles use high-contrast ivory with a stronger weight.
- Gallery descriptions use brighter, medium-weight text for easier reading.

## Apply the patch

1. Create a branch from your current v2.2.1 `main`:

   ```bash
   git switch main
   git pull
   git switch -c release/v2.2.2
   ```

2. Extract this ZIP directly over the repository root, allowing folders to merge and changed files to be replaced.

3. The ZIP already contains matching `docs/` and `site/` output. A rebuild is optional, but recommended as a verification step:

   ```bash
   python tools/build_site.py
   ```

4. Review and commit:

   ```bash
   git status
   git add .
   git commit -m "Release v2.2.2 Journal Experience Polish"
   git push -u origin release/v2.2.2
   ```

5. Explore locally:

   ```bash
   python -m http.server 8000 --directory docs
   ```

   Open `http://localhost:8000`.
