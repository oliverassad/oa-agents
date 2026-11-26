import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOK = Path(__file__).with_name("status.py")
PLUGIN = HOOK.parent.parent


def run_in(project, *args):
    env = {"CLAUDE_PLUGIN_ROOT": str(PLUGIN), "CLAUDE_PROJECT_DIR": str(project), "PATH": "/usr/bin:/bin", "HOME": str(project)}
    done = subprocess.run([sys.executable, str(HOOK), *args], input="{}", capture_output=True, text=True, env=env, cwd=project)
    return done.returncode, json.loads(done.stdout) if not args else done.stdout


def git_repo(d, origin="https://github.com/acme/widgets.git"):
    subprocess.run(["git", "init", "-q", "-b", "dev"], cwd=d, check=True)
    subprocess.run(["git", "remote", "add", "origin", origin], cwd=d, check=True)


class Status(unittest.TestCase):
    def test_empty_folder_reports_missing(self):
        with tempfile.TemporaryDirectory() as d:
            code, out = run_in(d)
            self.assertEqual(code, 0)
            msg = out["systemMessage"]
            self.assertIn("project AGENTS.md missing", msg)
            self.assertIn("Linear: missing", msg)
            self.assertIn("GitHub: missing", msg)
            self.assertIn("rtk missing (hook off)", msg)
            self.assertIn(msg, out["hookSpecificOutput"]["additionalContext"])

    def test_project_with_tracker_and_origin(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "AGENTS.md").write_text("# X\n\n## Tracker\n\nLinear team Recfo (`REC`), project demo.\n")
            git_repo(d)
            code, out = run_in(d)
            msg = out["systemMessage"]
            self.assertEqual(code, 0)
            self.assertIn("Linear: Linear team Recfo (`REC`), project demo.", msg)
            self.assertIn("GitHub: acme/widgets on dev", msg)
            self.assertIn("team AGENTS.md ok", msg)
            self.assertIn("MCP: config none; Composio check", msg)
            self.assertEqual(len(msg.splitlines()), 7)

    def test_linear_project_defaults_to_repository_name(self):
        with tempfile.TemporaryDirectory() as d:
            git_repo(d)
            _, out = run_in(d)
            self.assertIn("Linear: project widgets (repository name)", out["systemMessage"])

    def test_text_rerun_prints_block_only(self):
        with tempfile.TemporaryDirectory() as d:
            _, out = run_in(d)
            code, text = run_in(d, "--text")
            self.assertEqual(code, 0)
            self.assertEqual(text.strip(), out["systemMessage"])
            self.assertIn("--text", out["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
