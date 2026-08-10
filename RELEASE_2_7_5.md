# Juno's 7 Journal v2.7.5

## Release summary

v2.7.5 adds the latest Sicily route, journal and media refinements, including Capo Passero, Syracuse, Riposto and Mount Etna.

## Included changes

- Adds the Capo Passero anchor-drag incident as a Crew Life journal entry.
- Adds Syracuse ashore and food updates from Cameron.
- Adds Porto dell'Etna Marina, Riposto as the current Sicily stop.
- Adds Mount Etna photos and videos captured from Riposto.
- Adds Mount Etna contextual detail, including its active status and visible volcanic glow.
- Adds the Cycladic Gem event-rental note to Sophie's "My Future House" entry.
- Removes an over-editorial note from the same entry.
- Preserves the v2.7.4 dashboard safeguards and route-editor fixes.
- Updates version and build metadata to `2.7.5`.

## Validation performed

- Ran the site build successfully from the live local repository.
- Checked generated version metadata for `2.7.5`.
- Ran the character trap for common replacement-character and mojibake issues.
- Ran Git whitespace validation.

## Apply and release commands

These commands are only needed if applying from a changed-files package. If Codex has already updated the live repository directly, review the working tree and commit the files in place.

```bash
git status
git add .
python tools/build_site.py
git status
git diff --cached

git commit -m "Release v2.7.5 Sicily and editorial refinements"
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.7.5 -m "Merge release v2.7.5"
git tag -a v2.7.5 -m "Juno's 7 Journal v2.7.5"
git push origin main
git push origin v2.7.5
git branch -d release/v2.7.5
```
