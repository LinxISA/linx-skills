# Renderer Triage

## Symptom map

- Missing bars: parser presence events or row ordering issue.
- Missing assembly labels: label emission or renderer fallback issue.
- Collapsed rows: UID collision.
- Invisible labels: theme contrast issue.
- Stale open path: config/dialog defaults.

## High-value files

- `onikiri_parser.js`
- `konata_renderer.js`
- `theme/dark/style.json`
- `theme/light/style.json`
- `config.js`

## Numeric coercion checks

Ensure drawing math uses numeric values, not string concatenation, for x-position and margins.
