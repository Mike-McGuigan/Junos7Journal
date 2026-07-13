# Juno's 7 Journal v2.2.0 — Journal Experience

This release changes the public site from a collection of journal cards into a
story-led, magazine-style experience while preserving the route and local
Captain's Dashboard workflow.

This package supersedes the withdrawn initial v2.2.0 archive.

## Journal Experience

- Magazine-style chapter layout with stronger typography and spacing.
- Structured optional sections for Crew Moments, Did You Know?, Flavour of the
  Place and Notable Encounters.
- Photo captions integrated into each chapter.
- Story media is shown uncropped; gallery thumbnails remain cropped for quick
  browsing.
- Full-screen photo and video viewer.
- Chapter index and responsive mobile layouts.
- Expanded journal through Vis with 22 chapters.

## Complete recent media set

The corrected release includes all 17 items from the re-provided media bundle,
plus the separately supplied working-aloft portrait:

- Black Pearl at Polače.
- Two Pakleni Islands approach photographs.
- Cameron's peaceful night-shift video.
- Four Milna anchorage photographs, Cameron's dolphin footage and the captain's
  drone footage.
- Teak dent repair using an iron and damp towel.
- Two Vis sunset photographs from the evening ash arrived from the Korčula
  wildfire.
- The 6am rain/choppy-sea video and the later “Much nicer hahahaa” photograph.
- Two Cameron-working-aloft photographs.
- Cameron and Sophie's feet in the Adriatic during the 12 July afternoon off.

The Triumph encounter remains a text-led chapter because no matching Triumph
image was present in the re-provided bundle.

## Media enhancement

- Non-destructive `enhancedUrl` support while preserving `originalUrl`.
- Gentle enhanced working copies included for compressed photographs.
- New `tools/enhance_media.py` utility and `MEDIA_ENHANCEMENT.md` instructions.
- The supplied social-media copy of the dolphin drone footage can later be
  replaced in place by the genuine HD file without changing the journal entry.

## Voyage and identity polish

- Mouse-wheel zoom enabled on the public voyage map.
- Improved map timeline, marker tooltips and selected-stop details.
- Nautical terminology standardised to `Underway`, `Moored` and `At anchor`.
- Date-label and place-name tidy-up without changing supplied coordinates.
- J7 favicon and visual identity added across the public and admin pages.

## Data safety

- The supplied route snapshot and manual sea-route geometry are retained.
- `content/routes/route-so-far.json` is aligned to the deduplicated 35-stop
  public route, ending alongside in Vis on 11 July.
- Original media remains preserved; enhanced files are separate working copies.

## Recommended installation — release branch

Do not apply this release directly to `main`.

1. From the root of the existing repository, create the release branch:

   ```bash
   git switch main
   git pull
   git status
   git switch -c release/v2.2.0
   ```

2. Extract the ZIP to a temporary folder. Copy everything **inside** its
   `Junos7Journal-main` folder over the root of the existing repository. Allow
   Windows to merge folders and replace files.

3. Rebuild and review:

   ```bash
   python tools/build_site.py
   git status
   git add .
   git commit -m "Release v2.2.0 Journal Experience"
   git push -u origin release/v2.2.0
   ```

4. Explore locally before merging:

   ```bash
   python -m http.server 8000 --directory docs
   ```

   Open `http://localhost:8000`.

5. Once satisfied, merge and tag:

   ```bash
   git switch main
   git pull
   git merge --no-ff release/v2.2.0
   git push
   git tag -a v2.2.0 -m "Juno's 7 Journal v2.2.0"
   git push origin v2.2.0
   ```

For normal route publishing after installation, continue to use:

```text
Start Captains Dashboard.bat
```
