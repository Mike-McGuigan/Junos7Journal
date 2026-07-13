# Juno's 7 Journal v2.2.1 — Journal Experience Patch

This patch is built from the merged v2.2.0 `main` snapshot supplied on 13 July.

> **Corrected archive:** this build supersedes the earlier v2.2.1 ZIP that used an interim logo.

## Fixes and enhancements

- Replaces the incorrect identity mark with the approved **J7 yacht logo** supplied by Mike: ivory J7 lettering, gold bow accent and wake on a deep-navy rounded square.
- Keeps the newest journal chapter fully featured at the top.
- Adds a **Oldest → Newest / Newest → Oldest** toggle for the complete journal.
- Defaults to chronological reading and remembers the reader's choice in the browser.
- Keeps the newest entry in the complete journal in either order and marks it **Latest**.
- Fixes the “Much Nicer” sequence so the rainy, choppy video appears before the improved-weather photograph.

## 13 July — towards Biševo and back to Komiža

- Preserves the supplied roundabout sea route towards Biševo before returning to anchor off Komiža.
- Adds Cameron's video with the comment: “Another dolphin — on the bow under way.”
- Adds Sophie's second video, including the delighted shriek from one of the owner's children.
- Updates the latest route status to **At anchor off Komiža**.

## Recommended installation — patch branch

1. From the root of the current repository:

   ```bash
   git switch main
   git pull
   git status
   git switch -c release/v2.2.1
   ```

2. Extract the ZIP to a temporary folder. Copy everything **inside** its
   `Junos7Journal-main` folder over the repository root. Allow Windows to merge
   folders and replace files.

3. Rebuild and review:

   ```bash
   python tools/build_site.py
   git status
   git add .
   git commit -m "Release v2.2.1 Journal Experience Patch"
   git push -u origin release/v2.2.1
   ```

4. Explore locally:

   ```bash
   python -m http.server 8000 --directory docs
   ```

   Open `http://localhost:8000`.

5. Once satisfied:

   ```bash
   git switch main
   git pull
   git merge --no-ff release/v2.2.1
   git push
   git tag -a v2.2.1 -m "Juno's 7 Journal v2.2.1"
   git push origin v2.2.1
   ```
