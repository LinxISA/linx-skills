---
name: linx-konata-renderer-debug
description: Konata renderer and UI triage workflow for Linx traces. Use when traces validate structurally but the UI shows missing pipeline bars, missing assembly labels, collapsed rows, style/contrast issues, or stale-file navigation problems.
---

# Linx Konata Renderer Debug

## Overview

Use this skill after trace validation passes and rendering still looks wrong.

## Entry condition

- Start only when `linx-konata-trace-validate` has passed for the same `.konata` file.

## Triage workflow

1. Reproduce with a known-good validated trace.
2. Classify symptom.
- no pipeline bars,
- missing left-pane assembly labels,
- collapsed or duplicated rows,
- stale open-path behavior.
3. Inspect renderer/parser hotspots.
4. Re-test with same trace and compare screenshots.

## Common fix points

- `/Users/zhoubot/Konata/onikiri_parser.js`
- `/Users/zhoubot/Konata/konata_renderer.js`
- `/Users/zhoubot/Konata/theme/dark/style.json`
- `/Users/zhoubot/Konata/theme/light/style.json`
- `/Users/zhoubot/Konata/config.js`

## Known bug patterns

- Numeric field coercion bugs in drawing layout (`curX`, `marginLeft`).
- Missing or empty `L type=0` labels per row.
- UID namespace collision between block and uop rows.
- Default open-directory misconfiguration leading to stale tabs/workspace confusion.

## References

- `references/renderer_triage.md`
