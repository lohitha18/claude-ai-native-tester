# Payment Test Policy

## Mock-only boundary
- All payment tests must use local mocks or stubs.
- Do not use real card data, production gateways, live credentials, or external provider requests.

## Idempotency
- Repeated submission with the same idempotency key must not create duplicate success or duplicate mutation.
- Payment status and retry behavior must be explicit in an implemented contract before assertions are written.

## Failure handling
- Declined, timeout, and rejected responses must never be counted as successful payments.
- A timeout must remain an unknown or retryable state according to the implemented contract; it must not be inferred as success.
- Safely expose an error code rather than card details or secrets.

## Logging and secrets
- Never log API keys, card numbers, CVV values, passwords, access tokens, or full provider responses containing secrets.
- Test fixtures must contain only synthetic data.

## Open-question rule
- Unsupported amounts, currencies, status codes, retry rules, and idempotency contracts must be recorded as open questions rather than invented.
