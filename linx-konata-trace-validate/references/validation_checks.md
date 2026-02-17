# Validation Checks

## Structural checks

- Required stage IDs present.
- Record counts (`I`, `R`, `P`) are internally consistent.
- UID space has no collisions.

## Label checks

- `L type=0` labels exist for rows expected in left pane.
- Detail labels (`L type=1`) remain parseable.

## Decision rule

- Fail fast on structural mismatch.
- Only proceed to renderer debugging after structure is confirmed.
