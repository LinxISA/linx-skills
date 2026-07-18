#!/usr/bin/env python3
from __future__ import annotations

import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_skill_change_scope


class WorktreeScopeTests(unittest.TestCase):
    @patch.object(check_skill_change_scope, "run_git")
    def test_deleted_file_does_not_remove_its_skill(self, run_git) -> None:
        run_git.return_value = (
            " D linx-isa/references/retired.md\n"
            " M linx-isa/SKILL.md\n"
            " D linx-compiler\n"
        )

        changed, removed = check_skill_change_scope.list_worktree_skill_changes(Path("."))

        self.assertEqual(changed, {"linx-isa", "linx-compiler"})
        self.assertEqual(removed, {"linx-compiler"})


if __name__ == "__main__":
    unittest.main()
