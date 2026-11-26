"""Checks for the build and the Claude hooks. Run: python3 -I -m unittest discover -s scripts"""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "plugins/team/hooks" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Hooks(unittest.TestCase):
    def test_outputs_match_sources(self):
        run = subprocess.run([sys.executable, "-I", "scripts/build.py", "--check"], cwd=ROOT)
        self.assertEqual(run.returncode, 0)

    def test_role_gets_its_rules_and_only_used_languages(self):
        inject = load("inject_rules")
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "apps/web").mkdir(parents=True)
            (Path(tmp) / "apps/web/svelte.config.js").write_text("")
            files = inject.files_for("SubagentStart", {"agent_type": "team:engineer-ui", "cwd": tmp})
        self.assertIn("area/ui", files)
        self.assertIn("lang/svelte", files)
        self.assertNotIn("lang/typescript", files)

    def test_foreign_agent_gets_modes_only(self):
        inject = load("inject_rules")
        self.assertEqual(inject.files_for("SubagentStart", {"agent_type": "Explore"}), inject.FOREIGN)

    def test_absolute_tool_path_is_caught(self):
        guard = load("rtk_guard")
        self.assertEqual(guard.ABSOLUTE.search("cd x && /usr/bin/git status").group(1), "git")
        self.assertIsNone(guard.ABSOLUTE.search("git status"))


class Models(unittest.TestCase):
    def test_role_map_must_match_agents_and_tiers(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from build import check_models
        models = {"tiers": {"build": {}}, "roles": {"tester": "build"}}
        check_models(models, {"tester"})
        with self.assertRaises(ValueError):
            check_models(models, {"tester", "debugger"})
        with self.assertRaises(ValueError):
            check_models({"tiers": {}, "roles": {"tester": "build"}}, {"tester"})


class VersionGuard(unittest.TestCase):
    def test_output_change_needs_a_new_version(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from version_guard import decide
        self.assertIsNotNone(decide(["plugins/team/agents/tester.md"], "0.1.1", "0.1.1"))
        self.assertIsNone(decide(["plugins/team/agents/tester.md"], "0.1.1", "0.2.0"))
        self.assertIsNone(decide(["README.md"], "0.1.1", "0.1.1"))


if __name__ == "__main__":
    unittest.main()
