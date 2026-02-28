# Flow Checks

## Required after semantic changes

- regenerate build outputs,
- run examples,
- run sims,
- keep first failing test and seed in report.

## Cross-stack handoff

When behavior changes, attach:
- `.pyc` input,
- generated output artifact,
- expected commit/trace markers for LinxCore/QEMU parity.
