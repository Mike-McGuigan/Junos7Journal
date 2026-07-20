# Juno’s 7 Journal v2.5.4

## Release name

**Authentic Yacht Wordmark**

## Summary

This branding refinement introduces a scalable SVG wordmark inspired by the
lettering carried on Juno’s 7. The letters are stored as vector paths rather
than live text, so the result remains crisp at any size and does not depend on
a commercial font being installed on the reader’s device.

## Included changes

- Added `docs/assets/icons/junos7-wordmark.svg`.
- Replaced the homepage hero’s text-only yacht name with the SVG wordmark.
- Preserved accessible alternative text for screen readers.
- Added responsive desktop and mobile sizing.
- Retained the existing J7 emblem above the new wordmark.
- Updated `VERSION`, `CHANGELOG.md`, `ROADMAP.md` and build metadata.

## Validation

- [x] SVG contains vector paths and no embedded font.
- [x] SVG uses the site’s ivory hero colour and remains independent of installed fonts.
- [x] Homepage references the new asset.
- [x] Alternative text remains available.
- [x] Site build completes successfully.
- [x] Generated `site/` contains the SVG and updated homepage.
- [x] Version panel reports v2.5.4.
- [x] Changed-files ZIP and SHA256 checksum generated.

## Local release workflow

Run these commands from the repository root.

### 1. Create the release branch

```bash
git checkout main
git pull
git checkout -b release/v2.5.4
```

Extract the changed-files ZIP into the repository, preserving its folder
structure.

### 2. Build

```bash
python tools/build_site.py
```

### 3. Test and review

Start a local web server:

```bash
python -m http.server 8000 --directory site
```

Open `http://localhost:8000` and verify:

- the Juno’s 7 wordmark displays correctly on the homepage;
- the wordmark remains clear at desktop and mobile widths;
- journal, gallery and voyage pages load;
- the interactive map and satellite layer work;
- Captain’s Dashboard opens;
- the version panel reports v2.5.4.

Stop the server with `Ctrl+C`.

Review the changed files:

```bash
git status
git diff --check
git diff
```

### 4. Commit the release branch

```bash
git add .
git commit -m "Release v2.5.4 - Authentic yacht wordmark"
git push -u origin release/v2.5.4
```

### 5. Merge into main

```bash
git checkout main
git pull
git merge --no-ff release/v2.5.4
```

### 6. Tag and push the release

```bash
git tag -a v2.5.4 -m "Juno's 7 Journal v2.5.4"
git push origin main
git push origin v2.5.4
```

### 7. Delete the release branch

After confirming the main branch and tag are correct:

```bash
git branch -d release/v2.5.4
git push origin --delete release/v2.5.4
```

## Rollback

Before the merge, simply switch back to `main` and delete the branch.

After the merge, inspect the merge commit and revert it without rewriting
history:

```bash
git log --oneline --decorate -10
git revert -m 1 <merge-commit-hash>
git push origin main
```
