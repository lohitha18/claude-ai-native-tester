# Payment-Login Test Matrix

## Scope and evidence

This matrix consolidates read-only analysis of the starter repository. No files were edited and no tests or application commands were run.

Confirmed evidence:

- Maven configuration uses Java 17 and JUnit 5: `starter-repo/pom.xml:5-14`, `starter-repo/pom.xml:20-27`.
- The console entry point only prints messages and states that login is unimplemented: `starter-repo/src/main/java/com/technova/payment/Main.java:3-8`.
- `LoginService.login()` is a placeholder that throws `UnsupportedOperationException`: `starter-repo/src/main/java/com/technova/payment/auth/LoginService.java:7-12`.
- `UserRepository` contains one synthetic demo account: `starter-repo/src/main/java/com/technova/payment/auth/UserRepository.java:8-16`.
- `User` stores the starter password as a plain-text field: `starter-repo/src/main/java/com/technova/payment/auth/User.java:5-17`.
- The existing login tests are placeholders with `assertTrue(true)`: `starter-repo/src/test/java/com/technova/payment/auth/LoginServiceTest.java:7-27`.
- No payment implementation, web UI, HTTP routes, port, browser configuration, or live payment integration was found in the extracted starter inventory.

## Consolidated test matrix

| ID | Priority | Preconditions | Scenario | Expected result | Layer | Status/evidence |
|---|---:|---|---|---|---|---|
| AUTH-01 | P0 | Authentication implementation exists; synthetic fixture is isolated | Valid username/password authenticates | A documented authenticated result or session is returned; no requirement details are assumed | Unit/integration | Proposed; implementation missing |
| AUTH-02 | P0 | Authentication implementation exists | Invalid password rejects login | No authenticated state or session is created; a documented error contract is returned | Unit | Proposed; implementation missing |
| AUTH-03 | P0 | Authentication implementation exists | Unknown username rejects login | Response does not confirm whether the username exists unless policy requires it | Unit/integration | Proposed; exact contract unknown |
| AUTH-04 | P0 | Authentication implementation exists | Blank, null, whitespace-only, and excessively long inputs | Inputs fail safely using documented validation rules | Unit | Proposed; limits and contract unknown |
| AUTH-05 | P0 | Deterministic auth service and clock/store mock exist | Repeated incorrect credentials | Documented throttling or lockout policy applies without timing flakiness | Unit/integration | Proposed only; policy unknown |
| AUTH-06 | P0 | Session mechanism exists | Attempt protected operation before login, after failed login, and after logout | Access is denied and stale state is rejected | Unit/integration | Unknown mechanism |
| AUTH-07 | P0 | Role model and protected operations exist | Authorized and unauthorized roles access protected operations | Only explicitly authorized roles succeed | Unit/integration | Unknown permission model |
| AUTH-08 | P1 | Authentication implementation exists | Login/logout/re-login/duplicate-login transitions | Only documented transitions succeed and prior authentication cannot persist | Unit/state | Unknown state machine |
| VAL-01 | P0 | Repository and logging implementation exist | Special characters and encoding-sensitive inputs | No injection or unintended behavior; exact validation contract is documented | Unit/integration | Unknown storage/query behavior |
| VAL-02 | P1 | Login response contract exists | Compare invalid-username and invalid-password responses | Responses follow a documented user-enumeration policy | Integration/API | API contract unknown |
| PAY-01 | P0 | A mocked payment boundary is introduced | Attempt payment-adjacent operation with no live gateway configured | No real card, provider, or network request occurs; test only reaches mock/local mode | Unit/integration | Missing implementation |
| PAY-02 | P0 | Mock payment boundary and documented amount/currency rules exist | Invalid amount, currency, replay, or state transition | Operation is rejected safely and state is not mutated without explicit success | Unit/state | Rules unknown |
| PAY-03 | P1 | Authentication and a local/mock payment boundary exist | Authenticated-to-payment boundary and denied-session boundary | Authorization and state rules match the implementation; no live provider is used | Integration | Missing UI/API/payment evidence |
| REG-01 | P1 | Placeholder assertions are replaced with behavior assertions | Run focused and full Maven test suites | Suite reports real pass/fail totals; no placeholder test can pass without testing behavior | Build/unit | Replace `assertTrue(true)` placeholders |
| A11Y-01 | P2 | Login UI and evidence of labels/roles exist | Keyboard navigation and accessible names for login controls/errors | Controls have meaningful accessible names and are operable; messages are exposed accessibly | Browser | UI not found; no locator evidence |
| BROWSER-01 | P2 | Browser application, route, DOM labels/test IDs, and local base URL are confirmed | Login success/failure and validation behavior | pytest-playwright assertions match confirmed UI behavior | Browser | Not currently testable; evidence missing |

## Security review and disagreements

- **Agreement:** Unit coverage can safely target valid, invalid, blank, boundary, state, session, permission, and mocked payment cases only after implementation exists.
- **Agreement:** Browser, payment, and live-service scenarios must remain mocked/local and isolated.
- **Disagreement/limitation:** The proposed matrix must not be treated as executable current coverage. `LoginService` is unimplemented and existing tests are placeholders, so the matrix is future coverage.
- **Disagreement/limitation:** Brute-force or lockout assertions require a concrete policy and deterministic clock/store dependencies.
- **Security finding — High:** Plain-text password storage is an insecure starter default. Impact: credential exposure or insecure implementation; remediation: use salted password hashing and timing-safe verification, and exclude password data from logging/serialization. Evidence: `starter-repo/src/main/java/com/technova/payment/auth/User.java:5-17`.
- **Security finding — Medium:** Placeholder authentication has no meaningful behavior. Evidence: `starter-repo/src/main/java/com/technova/payment/auth/LoginService.java:7-12`.
- **Security finding — Medium:** Placeholder tests can falsely appear to pass. Evidence: `starter-repo/src/test/java/com/technova/payment/auth/LoginServiceTest.java:7-27`.
- **Security finding — Low:** `demo.user` is synthetic starter data, but must remain test-only and must never be reused or documented as a production credential. Evidence: `starter-repo/src/main/java/com/technova/payment/auth/UserRepository.java:8-16`.
- No unsafe logging, real-service calls, live payment integration, real credentials, or real card data were found in the extracted starter.

## Missing evidence

The following values are required before executable tests or source changes:

- Implemented `LoginService` behavior, method contract, return values, and exceptions.
- Authentication credential source, password format, validation limits, and error messages.
- Session/token mechanism, expiration, invalidation, replay, and logout behavior.
- Authorization role model and protected operations.
- Lockout or throttling policy and deterministic test seams.
- HTTP/API routes, status codes, and response bodies, if an API is introduced.
- Browser startup command, local URL/port, DOM labels, roles, and stable test IDs.
- Payment API or UI contract and a supported local/mock payment mode.
- Payment amount/currency/retry/refund/idempotency rules.
- Maven test command and exact test inventory.
- Accessibility requirements and keyboard behavior.

## Unsafe or nondeterministic cases

- No live login, payment gateway, or production system testing.
- No real credentials or card data.
- No arbitrary sleeps or timing-only lockout assertions.
- No inferred URLs, selectors, accounts, API paths, status codes, or payment business rules.
- No claim that placeholder `assertTrue(true)` tests provide authentication coverage.
