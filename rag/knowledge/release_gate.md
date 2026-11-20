# Release Gate

## Required evidence
- Authentication behavior is implemented and tested.
- Payment behavior is mock-only and declined or timeout outcomes cannot be reported as success.
- Idempotency behavior is implemented or explicitly documented as an open question.
- Logs contain no secrets or real card data.
- API and browser tests use real documented contracts and selectors.

## Blockers
- Unsupported behavior must not be assumed.
- Placeholder assertions are blockers for behavioral release claims.
- Live payment credentials or real card fixtures are blockers.
