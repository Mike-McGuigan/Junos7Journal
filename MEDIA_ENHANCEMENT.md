# Media Enhancement — v2.2.0

v2.2.0 supports an optional `enhancedUrl` on journal media items. The website
uses that working copy when present while retaining `originalUrl` for the
untouched source.

This is intended for compressed Messenger/social-media photographs while the
full-resolution file from Cameron or Sophie is still awaited. It is not a
replacement for the original.

## Create a working copy

```bash
python tools/enhance_media.py docs/media/photos/example.jpg \
  docs/media/photos/enhanced/example-enhanced.jpg
```

Then add these optional fields to the item in `docs/data/journal.json` and
`docs/data/media.json`:

```json
{
  "originalUrl": "media/photos/example.jpg",
  "enhancedUrl": "media/photos/enhanced/example-enhanced.jpg",
  "enhancement": {
    "status": "enhanced-working-copy",
    "originalPreserved": true
  }
}
```

The story view displays images uncropped. The gallery intentionally uses
cropped thumbnails for quick browsing.
