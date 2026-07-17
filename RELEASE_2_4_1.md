# Juno's 7 Mediterranean Journal v2.4.1

## Gallery Classification Fix

This patch makes gallery classification durable and corrects the agreed terminology issue.

### Changes

- Stores every gallery category in the canonical `content/media-index/media-index.json` source, preventing later publish/build activity from losing or reverting classifications.
- Corrects the Cavtat passage photograph to `Juno's 7` and `Scenic`; it is no longer treated as a port or anchorage image.
- Corrects the Black Pearl photograph to `Ports & Anchorages` and `Scenic`; it is no longer classified as crew or Juno's 7.
- Removes `Tenders & Toys` from the Smokvica storm photograph because no tender or toy is visible.
- Removes the photograph caption's unsupported suggestion that SETE can be seen during the Cavtat passage.
- Standardises current source and generated wording from `under way` to `underway`.
- Rebuilds `site/` from `docs/` and validates all 42 media records across all eight gallery categories.

## Applying the changed-files ZIP

Extract the ZIP into the root of the local `Junos7Journal` repository and allow it to replace existing files. Then run the following commands from the repository root.

## Complete Git commands

```bash
git switch main
git pull --ff-only origin main
git switch -c release/v2.4.1

git status
git add --all
git commit -m "Release v2.4.1 gallery classification fix"

git switch main
git merge --no-ff release/v2.4.1 -m "Merge release v2.4.1"
git tag -a v2.4.1 -m "Juno's 7 Journal v2.4.1"

git push origin main
git push origin v2.4.1

git branch -d release/v2.4.1
git status
```

`git push origin v2.4.1` pushes the annotated release tag. The release branch remains local and is deleted after the merge.

The final `git status` should report that the working tree is clean.
