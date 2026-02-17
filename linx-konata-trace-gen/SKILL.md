---
name: linx-konata-trace-gen
description: Konata trace generation workflow for LinxCore. Use when producing Konata v0005 traces from LinxCore runs, generating companion commit/raw-event artifacts, or preparing trace bundles for pipeline debugging and cross-checking.
---

# Linx Konata Trace Generation

## Overview

Use this skill to generate complete trace bundles for Konata analysis from LinxCore simulations.

## Canonical command

```bash
bash /Users/zhoubot/LinxCore/tools/konata/run_konata_trace.sh <memh> <max_commits>
```

## Required artifacts

- `*.konata`
- `*.commit.jsonl`
- `*.commit.txt`
- `*.raw_events.jsonl`
- `*.map.json`

Default path family:
- `/Users/zhoubot/LinxCore/generated/konata/<bench>/`

## Generation checklist

1. Confirm input MEMH and commit budget.
2. Run trace generator.
3. Verify file set exists and is non-empty.
4. Verify `.konata` header is `Kanata\t0005`.
5. Hand off trace to validation skill before renderer triage.

## Guardrails

- Do not change commit JSON field contracts during routine trace generation.
- Keep UIDs stable and deterministic for repeated runs with same seed/image.

## References

- `references/artifacts.md`
