# TESTING

Layers and rules: shared `area/testing`. This file holds the project facts.

## Commands

| Proving | Command | Runs in CI |
| --- | --- | --- |
| Unit and contract | <bun test> | yes |
| Integration | <bun run test:integration> | <yes / weekly> |
| End to end | <bun run test:e2e> | <after deploy> |

## Where each proof runs

- Local before push: <check, package tests>.
- CI on each pull request: <the required check>.
- After deploy: <journeys on dev>.
- Weekly: <the rest, forced>.

## Test data

<Emulators or throwaway databases, how to start them, the guard that refuses a real store.>
