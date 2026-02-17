---
name: linx-ide
description: Linx tooling and observability workflow across emulator, RTL, pyCircuit, and Konata. Use when building debug pipelines, generating and validating traces, triaging renderer issues, or coordinating model/emulator/RTL alignment.
---

# Linx IDE

## Overview

Use this skill as the consolidated developer-tooling surface for Linx debug, observability, and model alignment.

## Owned areas

- emulator debug workflow (`linx` QEMU-like behavior),
- pyCircuit MLIR/tool flow,
- RTL observability integration,
- Konata trace generation/validation/renderer triage.

## Standard tooling loop

1. reproduce on emulator or model,
2. gather commit/trace artifacts,
3. compare against RTL/model expectations,
4. localize first divergence,
5. rerun strict gates.

## Konata workflow

```bash
bash /Users/zhoubot/LinxCore/tools/konata/run_konata_trace.sh <memh> <max_commits>
python3 /Users/zhoubot/LinxCore/tools/konata/check_konata_stages.py <konata> --require-stages F0,D3,IQ,ROB,CMT
```

If structural validation passes but UI is wrong, debug parser/renderer/theme paths.

## Included scope

This consolidated skill absorbs prior `isa-emulator`, `mlir-pycircuit`, `rtl-development`, and Konata split skills.

## References

- `references/tooling_matrix.md`
