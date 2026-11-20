---
name: test-plan
description: Inspect reuirements or code changes and create a risk-based test plan
---

# Test Plan Workflow

1. Read the issue or acceptance criteria and inspect the relevant code.
2. Separate confirmed facts from assumptions and open questions.
3. Cover happy, negative, boundary, permissions, state-transition, accessibility, and regression risks.
4. Map each test to a requirement and an expected result.
5. Identify the unit, API, browser, or RAG layer for each test.
6. Do not invent selectors, APIs, credentials, or business rules.
7. Return the plan as a table with these columns: `ID`, `Risk`, `Preconditions`, `Steps`, `Expected result`, `Automation layer`.
8. Flag cases that cannot be tested safely or deterministically.
