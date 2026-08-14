# Juno's 7 Journal v2.8.0

## Release summary

v2.8.0 adds Drink the Voyage, a new browsing feature that turns the route into practical wine and beer suggestions, alongside the latest Aeolian route and journal refinements.

## Included changes

- Adds a new Drink the Voyage page.
- Adds homepage navigation and a journal teaser for the drink guide.
- Adds route-specific wine cards for Greece, Croatia, Malta, Sicily, Etna and the Aeolian Islands.
- Adds distinct Same style cards so users can filter practical alternatives separately from drinks genuinely from the route.
- Adds a simple beer option for the route.
- Adds a practical shopping-list section.
- Adds UK-friendly example links for several same-style wine choices.
- Adds recent Aeolian route, journal and media updates for Stromboli, Panarea and Lipari.
- Adds Sicilian and Aeolian flavour-card images.
- Updates version and build metadata to `2.8.0`.

## Validation performed

- Ran the site build successfully from the live local repository.
- Checked generated version metadata for `2.8.0`.
- Checked the Drink the Voyage card counts and filter metadata.
- Ran the character trap for common replacement-character, smart quote and currency mojibake issues.

## Apply and release commands

These commands are only needed if applying from a changed-files package. If Codex has already updated the live repository directly, review the working tree and commit the files in place.

```bash
git status
git add .
python tools/build_site.py
git status
git diff --cached

git commit -m "Release v2.8.0 drink the voyage"
git switch main
git pull --ff-only origin main
git merge --no-ff release/v2.8.0 -m "Merge release v2.8.0"
git tag -a v2.8.0 -m "Juno's 7 Journal v2.8.0"
git push origin main
git push origin v2.8.0
git branch -d release/v2.8.0
```