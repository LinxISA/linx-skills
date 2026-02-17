# Static and Shared Runtime Policy

## Build phase

Run `MODE=phase-b` build and record `M1`, `M2`, and `M3` outcomes.

## Runtime phase

Run static and shared smoke independently.

Required artifacts:
- `summary_static.json`
- `summary_shared.json`

## Combined status

Global runtime pass requires both static and shared pass.

If shared is deferred, defer must be explicit and documented in report metadata.

## Mandatory failure visibility

Report exact sample and signature for each failure (`runtime_timeout`, `kernel_panic`, `block_trap`, etc.).
