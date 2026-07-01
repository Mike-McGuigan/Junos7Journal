# Commit 4 – Presentation & Identity

Introduces a clear separation between the human voyage title and inferred geographic metadata.

## Data model

- Adds `routePoint.title` for the human-entered narrative name.
- Keeps `routePoint.name` as a backwards-compatible alias.
- Writes `tracker.latestLocationTitle` alongside `tracker.latestFriendlyLocation`.

## Presentation

- Dashboard and map popups use the human title as the headline.
- Geographic lookup information is shown as supporting subtitle text.
- Existing route entries without `title` still render via `name`.
