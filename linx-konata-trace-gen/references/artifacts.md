# Konata Artifact Contract

## Minimal bundle

- `<name>.konata`
- `<name>.commit.jsonl`
- `<name>.commit.txt`
- `<name>.raw_events.jsonl`
- `<name>.map.json`

## Format contract

- `.konata` header must be `Kanata\t0005`.
- UID assignment must be deterministic for same seed/image.
- Record order must preserve parser expectations.

## Handoff

Every generated trace should be validated by stage/record checks before UI debugging.
