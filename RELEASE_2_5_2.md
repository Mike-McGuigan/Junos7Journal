# Juno's 7 Journal v2.5.2 — Anchorage Journal Update

This changed-files release is intended to be extracted over the repository root.

## Included

- A concise journal entry for the 17 July anchorage off Levrnaka.
- A concise journal entry for the 18 July anchorage off Žut.
- No journal entry for the 19 July "En route to Zadar" map point because it is an underway position rather than a stop.
- Version updated to 2.5.2.

## Apply and build

From the repository root:

```bash
git switch main
git pull
git switch -c release/v2.5.2
```

Extract this ZIP over the repository root, allowing files to be replaced, then run:

```bash
python tools/build_site.py
```

Review the two new journal entries locally, then commit and push:

```bash
git add VERSION content/journal/2026/2026-07-17-levrnaka.md content/journal/2026/2026-07-18-zut.md docs tools/build_site.py RELEASE_2_5_2.md PATCH_MANIFEST_2_5_2.txt
git commit -m "Release v2.5.2 anchorage journal update"
git push -u origin release/v2.5.2
```

After review, merge using GitHub or locally:

```bash
git switch main
git merge --no-ff release/v2.5.2
git push origin main
```

The generated `site/` directory is deliberately excluded from this package. Regenerate it locally with `python tools/build_site.py`.
