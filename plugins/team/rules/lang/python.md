# Python

- PY-1: Standard library first. A new dependency is a decision (area/deps).
- PY-2: Type hints on every public function. Small pure functions.
- PY-3: Fail loudly. No bare `except`; an `except` logs, re-raises, or returns a checked value.
- PY-4: Tests with `unittest` or the runner the project names. Failing test first.
- PY-5: Scripts that read untrusted files run with `python3 -I`.
- PY-6: `pathlib` over `os.path`. f-strings. No mutable default arguments.
