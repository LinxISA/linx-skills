---
name: linx-isa
description: LinxISA v0.58 architecture workflow for normative contracts, encodings, assembly, PTO common-subset alignment, Sail coverage, and downstream requirements.
---

# Linx ISA

## Authority

Use the checked-in v0.58 sources in the LinxISA superproject. The compiled
catalog is `isa/v0.58/linxisa-v0.58.json`; `isa/v0.58/state/` and
`isa/v0.58/release_manifest.json` carry its machine-readable inputs and
identity. PTO-common definitions are imported from the exact release recorded
in `isa/v0.58/pto-spec.lock.json`. Never reconstruct an active rule from an
archived v0.57 page or from a downstream compiler, emulator, model, or
workload table.

## v0.58 hard-break invariants

- The four semantic execution engines are exactly `VEC`, `TLSU`, `CUBE`, and
  `SFU`.
- `VEC` contains elementwise operations, including active `TFMA`. `SFU`
  contains operations whose semantics require complex special-function
  hardware. `TLSU` owns tile load/store movement. `CUBE` owns matrix/cube
  operations.
- `TEPL` remains the unchanged encoded carrier and compatibility spelling. It
  is not a semantic engine. Canonical software may use `BSTART.VEC` and
  `BSTART.SFU`; both select existing TEPL encodings and must preserve exact raw
  words.
- `B.IOD` and `BSTART.PAR` are permanently deleted spellings. They retain no
  encoding reservation. `B.IOS` owns the former B.IOD slot, while the former
  BSTART.PAR bits may be assigned to an active v0.58 form.
- `B.IOS` binds absolute core-private shared tile registers `S0..S255` visible
  to the four PEs of one core. Its four-bit PE mask permits multiple bits;
  zero is a strict no-op. TSize codes `1..7` encode 128 B through 8 KiB per
  participating PE.
- `B.IOT` is local-tile-only and admits only the five catalogued v0.58 forms.
  Do not revive old B.IOT layouts, destination codes, or implicit meanings.
- Scalar/block common-subset forms and raw encodings must match the locked PTO
  release exactly. Linx-only vector definitions remain Linx-only; PTO must
  reserve their occupied encoding space rather than collide with it.
- Objects and executables carry the exact `.note.pto.isa` identity required by
  the locked release. Missing, old, mixed, or mismatched identities fail
  closed.
- Mnemonic presence, decode coverage, and semantic completeness are separate
  claims. Report them separately and bind every claim to an exact commit.

Before changing a variable-selector form, enumerate its raw words against all
generic selectors at the same instruction length. Before joining adjacent
fields, prove their original instruction boundaries, PC bases, operand roles,
and side effects. Decoder priority is not an architectural repair.

## Mandatory v0.58 gates

Run from the LinxISA superproject root:

```bash
python3 tools/isa/build_golden.py --profile v0.58 --check
python3 tools/isa/validate_spec.py --profile v0.58
python3 tools/isa/test_v058_profile.py
python3 tools/isa/check_pto_v058_manifest.py --root .
python3 tools/isa/check_canonical_v058.py --root .
python3 tools/isa/check_agent_navigation.py --root .
python3 tools/isa/gen_qemu_codec.py --check
python3 tools/isa/gen_c_codec.py --check
python3 tools/isa/gen_sail_decode.py --check
python3 tools/isa/gen_sail_status.py --check
python3 tools/isa/sail_coverage.py --check
python3 docs/check_documentation.py --root .
bash tools/ci/check_repo_layout.sh
```

Formal release additionally requires the hosted Sail parser and C-backend lane
pinned by `isa/sail/toolchain.json`. Missing, skipped, pending, or different-SHA
results are not success.

## Workflow

1. Start from the v0.58 authority and exact PTO lock.
2. Update the normative source once; regenerate projections rather than adding
   parallel explanations.
3. Cross-check common forms and occupied Linx-only encoding space.
4. Update compiler, QEMU, Linux, RTL/model, and workload requirements only
   after the architecture contract is unambiguous.
5. Run the mandatory gates and record the exact reviewed head and tree.

## Skill evolve closeout

Report either `skill-evolve: update linx-isa (...)` or
`skill-evolve: no-update linx-isa (...)`. Update this skill only for reusable
architecture invariants, authority changes, or mandatory gate changes. Validate
changes with:

```bash
python3 /Users/zhoubot/.codex/skills/.system/skill-creator/scripts/quick_validate.py linx-isa
python3 scripts/check_skill_change_scope.py --repo-root . --base origin/main
```

## References

- `references/spec_alignment.md`
