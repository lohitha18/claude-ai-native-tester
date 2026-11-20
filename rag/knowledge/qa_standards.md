# QA Standards

## Evidence
- Report exact commands, exit codes, pass/fail totals, changed files, and relevant failures.
- Do not claim a test passed unless it ran and output was checked.

## Assertions
- One behavior per test where practical.
- Prefer role, label, and test-id locators for browser tests.
- Never weaken an assertion to make a test pass.
- Use observable waits and web-first assertions instead of fixed sleeps.

## Synthetic data
- Keep credentials, cards, and provider responses synthetic and isolated.
- Mark missing implementation or undocumented behavior as unsupported, not as passing coverage.
