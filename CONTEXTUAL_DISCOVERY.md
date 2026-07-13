# Contextual Discovery

## Purpose

Contextual Discovery asks one question at each voyage stop:

> What remarkable thing was right beside Cameron and Sophie?

It is not a tourist guide and it does not force a fact into every location. One strong, relevant story is better than a list of generic attractions.

## Editorial rules

- **Gold:** normally within 250 metres.
- **Silver:** normally within 500 metres.
- **Bronze:** up to 1 kilometre only when exceptional, visible from the yacht, present in the media, passed by the route, or fundamental to understanding the place.
- **Underway:** no automatic search unless the route itself passes a relevant feature.
- No discovery is better than forced trivia.
- Every published discovery needs a named source and HTTPS URL.
- Inference must be labelled as inference; private events must never be invented.

## Source of truth

```text
content/discoveries/contextual-discoveries.json
```

The public build is generated at:

```text
docs/data/discoveries.json
site/data/discoveries.json
```

## Build and validation

```bash
python tools/contextual_discovery.py --check
python tools/build_site.py
```

The build validates:

- route-stop matching;
- journal-entry matching where a discovery is attached to a chapter;
- proximity and exceptional-distance policy;
- evidence overrides;
- unique discovery and journal-entry relationships;
- source title and HTTPS URL.

## Adding a discovery

Add a curated item to `content/discoveries/contextual-discoveries.json` with:

- a unique `id`;
- the exact `routeStopTitle`;
- optional `journalEntryId`;
- category, title and short story;
- proximity and either `distanceMetres` or `contextualArea: true`;
- the reason it qualifies;
- the original source.

Run the validator before publishing. A candidate that falls outside the normal radius must be both exceptional and supported by an evidence override such as `visible-from-yacht` or `appears-in-media`.
