# Juno’s 7 Journal v2.3.2

## Captain’s Dashboard Polish

### Dashboard improvements
- New Position, Voyage Route Editor and Voyage Stop Editor are independently collapsible.
- Open/closed state is remembered in the browser.
- Voyage legs are listed newest first and the latest leg is selected by default.
- Route-editor zoom and centre are preserved while adding, undoing or clearing waypoints.
- A Fit Route control is available when a full-leg view is wanted.

### Journal additions
- 14 July: Dawn over Komiža.
- 15 July: Calm Before the Storm at Smokvica Vela, including Sophie’s two updates.
- 16 July: North through Kornati to the Gujak anchorage.
- Two new photographs, with originals preserved and restrained enhanced working copies.

### Metadata
- Root VERSION updated to 2.3.2.
- Release panel updated to Captain’s Dashboard Polish.

## Apply
Extract this changed-files patch over the repository root on a release branch, then run:

```bash
python tools/build_site.py
python -m http.server 8000 --directory docs
```
