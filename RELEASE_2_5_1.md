# Juno's 7 Journal v2.5.1 — Media Recovery & Route Update

This changed-files release is intended to be extracted over the repository root.

## Included

- Latest `route.json` and manual voyage geometry supplied on 19 July 2026.
- `content/routes/route-so-far.json` synchronised with the updated route.
- 7 July photograph of Cameron driving the small garage tender.
- 10 July photograph of Cameron and Sophie together on a quay.
- Journal and gallery links for both recovered photographs.
- Cautious wording where the 10 July marina and occasion are not confirmed.
- The working Esri satellite tile endpoint correction.
- Version updated to 2.5.1.

## Apply and build

From the repository root:

```bash
git switch main
git pull

git switch -c release/v2.5.1
```

Extract this ZIP over the repository root, allowing files to be replaced, then run:

```bash
python tools/build_site.py
```

Review the journal, gallery, route and satellite map locally. Then commit and push:

```bash
git add VERSION content docs tools/build_site.py RELEASE_2_5_1.md PATCH_MANIFEST_2_5_1.txt
git commit -m "Release v2.5.1 media recovery and route update"
git push -u origin release/v2.5.1
```

After review, merge using GitHub or locally:

```bash
git switch main
git merge --no-ff release/v2.5.1
git push origin main
```

The generated `site/` directory is deliberately excluded from this package. Regenerate it locally with `python tools/build_site.py`.
