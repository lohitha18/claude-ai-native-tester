# Login Requirements

## Synthetic credential validation
- A valid login uses the synthetic demo username and synthetic password only in test environments.
- Trim username input before lookup, and reject blank or whitespace-only usernames.
- Reject blank or whitespace-only passwords.
- Return no more than a generic authentication failure for unknown usernames and invalid passwords.
- Do not log usernames or passwords.

## Lockout
- The starter repository does not define a lockout threshold or duration.
- Until a policy is approved, do not assume lockout behavior exists.
- Repeated failures must not produce a successful login or reset authentication state.
- Any lockout implementation must be deterministic in tests and must use a documented policy.

## Open questions
- Whether lockout uses a count, time window, account lock, or IP-level control is not specified.
- Whether an account can re-login after lockout is not specified.
