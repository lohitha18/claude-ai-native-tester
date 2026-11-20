---
name: playwright-author
description: Author and run deterministic pytest-playwright browser tests
---

# Playwright Author Workflow

- Inspect the actual DOM, application source, and visible labels before choosing locators.
- Use `pytest-playwright` fixtures and web-first assertions.
- Prefer `get_by_role`, `get_by_label`, `get_by_text`, and stable test IDs.
- Write one behavior per test and name the test after the expected behavior.
- Do not use fixed sleeps; wait for observable state or assertions.
- Isolate test data and never call a real payment provider.
- Include negative cases and validation messages.
- On failure, capture the error, screenshot or trace, and the likely cause.
- Never silently change expected results to make a test pass.
- Run the test and report the exact command and result.
