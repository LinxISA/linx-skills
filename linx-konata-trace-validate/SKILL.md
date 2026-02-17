---
name: linx-konata-trace-validate
description: Konata trace validation workflow for LinxCore. Use when verifying stage visibility, row ordering, UID integrity, record counts, and commit-window consistency before consuming traces in Konata UI or CI gates.
---

# Linx Konata Trace Validation

## Overview

Use this skill to validate trace correctness before debugging renderer behavior.

## Canonical validator

```bash
python3 /Users/zhoubot/LinxCore/tools/konata/check_konata_stages.py \
  <konata-file> --require-stages F0,D3,IQ,ROB,CMT
```

## Validation workflow

1. Run stage validator.
2. Count `I`, `R`, and `P` records and compare with expected commit window.
3. Verify UID uniqueness across visible rows.
4. Verify label records exist for rows expected in left pane.
5. Fail trace on structural mismatch before renderer triage.

## Failure classes

- Missing required stages.
- Broken record cardinality (`R` count mismatch).
- UID collisions causing collapsed/duplicate rows.
- Missing label records for display rows.

## Exit policy

- If validation fails: fix trace generation first.
- If validation passes but UI still wrong: switch to `linx-konata-renderer-debug`.

## References

- `references/validation_checks.md`
