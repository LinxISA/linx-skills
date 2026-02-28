#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_git(repo: Path, *args: str) -> str:
    out = subprocess.check_output(["git", "-C", str(repo), *args], text=True)
    return out.strip()


def list_skill_dirs_from_tree(repo: Path, ref: str) -> set[str]:
    out = run_git(repo, "ls-tree", "-d", "--name-only", ref)
    skills = set()
    for line in out.splitlines():
        name = line.strip()
        if name.startswith("linx-"):
            skills.add(name)
    return skills


def list_changed_skill_dirs(repo: Path, base: str) -> set[str]:
    out = run_git(repo, "diff", "--name-only", f"{base}...HEAD")
    changed = set()
    for line in out.splitlines():
        path = line.strip()
        if not path:
            continue
        top = path.split("/", 1)[0]
        if top.startswith("linx-"):
            changed.add(top)
    return changed


def list_worktree_skill_changes(repo: Path) -> tuple[set[str], set[str]]:
    out = run_git(repo, "status", "--porcelain")
    changed: set[str] = set()
    removed: set[str] = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        path = line[3:]
        if " -> " in path:
            left, right = path.split(" -> ", 1)
            candidates = [left.strip(), right.strip()]
        else:
            candidates = [path.strip()]
        for candidate in candidates:
            top = candidate.split("/", 1)[0]
            if top.startswith("linx-"):
                changed.add(top)
                if "D" in status:
                    removed.add(top)
    return changed, removed


def main() -> int:
    ap = argparse.ArgumentParser(description="Guard linx-skills against broad destructive changes.")
    ap.add_argument("--repo-root", default=".", help="Path to linx-skills repo")
    ap.add_argument("--base", default="origin/main", help="Base ref for scope comparison")
    ap.add_argument("--max-changed-skills", type=int, default=8)
    ap.add_argument("--max-removed-skills", type=int, default=0)
    ap.add_argument("--allow-remove-skill", action="append", default=[])
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    allow_remove = {x.strip() for x in args.allow_remove_skill if x.strip()}

    changed_skills = list_changed_skill_dirs(repo, args.base)
    worktree_changed, worktree_removed = list_worktree_skill_changes(repo)
    changed_skills |= worktree_changed
    base_skills = list_skill_dirs_from_tree(repo, args.base)
    head_skills = list_skill_dirs_from_tree(repo, "HEAD")
    removed_skills = sorted((base_skills - head_skills) | worktree_removed)

    errors: list[str] = []
    if len(changed_skills) > args.max_changed_skills:
        errors.append(
            f"changed skill count {len(changed_skills)} exceeds limit {args.max_changed_skills}"
        )

    blocked_removed = [s for s in removed_skills if s not in allow_remove]
    if len(blocked_removed) > args.max_removed_skills:
        errors.append(
            f"removed skill count {len(blocked_removed)} exceeds limit {args.max_removed_skills}: {blocked_removed}"
        )

    payload = {
        "ok": len(errors) == 0,
        "base": args.base,
        "changed_skills": sorted(changed_skills),
        "removed_skills": removed_skills,
        "allowed_removed_skills": sorted(allow_remove),
        "blocked_removed_skills": blocked_removed,
        "limits": {
            "max_changed_skills": args.max_changed_skills,
            "max_removed_skills": args.max_removed_skills,
        },
        "errors": errors,
    }

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    if errors:
        print("error: skill change scope guard failed", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    print(
        "ok: skill change scope guard passed "
        f"(changed={len(changed_skills)}, removed={len(removed_skills)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
