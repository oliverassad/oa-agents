# Tests and the gate

- TG-1: Failing test first. Red, green, refactor. See the test fail and record that run.
- TG-2: New behaviour with no test is incomplete. Test and code land together.
- TG-3: Pick the layer by what you prove (table below).
- TG-4: Run the tests of your package before a push. CI confirms, it does not discover.
- TG-5: A green gate proves no database contract and no rendered surface. Say what you did not prove.
- TG-6: Never commit on a red tree.
- TG-7: Never skip, disable, `.only` or quarantine a test to reach green. Delete a test only when its behaviour is deleted, and say so.
- TG-8: A check that matches no file throws. A gate over an empty set reports success and everyone believes it.
- TG-9: A second red on rerun is real until proven flake. Quote the proving log line.

| Proving | Layer |
| --- | --- |
| Pure decision | unit, beside the code |
| API procedure with fake dependencies | contract |
| Database contract | integration, on an emulator |
| Rendered component | story, headless |
| Screen matches its print | fidelity probe |
| Route a person walks | end to end |

Probe rules: compare geometry, colour and rule shape, never text. A missing element is the loudest failure. Tolerance is half a pixel, lengths only.
