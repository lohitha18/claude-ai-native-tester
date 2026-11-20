# MCP Server Notes

## Server

- Name: `github-readonly`
- Transport: Streamable HTTP
- Endpoint: `https://api.githubcopilot.com/mcp/x/repos/readonly`
- Package/provenance: official GitHub-hosted GitHub MCP Server, published by `github/github-mcp-server`; MIT licensed. Official repository: https://github.com/github/github-mcp-server
- Claude Code configuration: project-scoped `.mcp.json`

## Permission scope

- Repository toolset only (`repos`).
- URL-path read-only mode disables write tools.
- `X-MCP-Lockdown: true` enables public-content filtering for files or issue content authored by users without repository push access. Lockdown is a prompt-injection risk filter, not an authorization boundary.
- Authentication uses `GITHUB_PAT` from the process environment only. No token is stored in `.mcp.json`, source control, or this document.
- Use a fine-grained PAT limited to the specific public or private repositories needed. Do not grant administration, write, workflow, merge, or release permissions.

## Official evidence checked

- Claude Code MCP setup and project scope: https://code.claude.com/docs/en/mcp
- GitHub MCP server official repository and README: https://github.com/github/github-mcp-server
- GitHub remote server read-only and toolset documentation: https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md
- GitHub server configuration read-only mode: https://github.com/github/github-mcp-server/blob/main/docs/server-configuration.md
- Claude Code GitHub installation guide: https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md

## Setup

Before restarting Claude Code, set the environment variable in your shell; use a read-only fine-grained PAT:

```text
export GITHUB_PAT="<read-only fine-grained PAT>"
```

Do not place the token in `.mcp.json`, shell history, reports, source control, or chat output. `.env` is already excluded by `.gitignore`.

Restart Claude Code after setting the environment variable. Project-scoped MCP servers require workspace trust and approval. In Claude Code, run:

- `/mcp` to approve, authenticate, and verify the server status.
- `claude mcp list` in a shell to list server health.
- `claude mcp get github-readonly` for configuration details.

## Verification evidence

- Claude Code version: `2.1.126` from `claude --version`.
- Docker is not installed, so the local Docker server was not used.
- `GITHUB_PAT` was unset during initial setup, as verified by an environment-presence check that printed no token.
- `.mcp.json` uses the documented `/x/repos/readonly` GitHub endpoint and project environment expansion for `GITHUB_PAT`.
- `claude mcp get github-readonly` reported project scope and `✗ Failed to connect` because no authorization was available.
- An unauthenticated MCP initialize request to the official endpoint returned `bad request: missing required Authorization header`, proving the endpoint is reached and requires credentials.
- `/mcp` verification requires an interactive Claude Code session and user approval/authentication; shell status alone does not prove the server can complete a tool call.

## Read-only demonstration status

A read-only MCP tool call could not complete during setup because `GITHUB_PAT` was unset and no write/admin credential is available. No credential was prompted for or printed.

After setting `GITHUB_PAT` in a new shell and restarting Claude Code, perform this read-only request:

1. Open `/mcp`.
2. Approve `github-readonly` for this workspace and verify it is connected.
3. Ask Claude Code: `Use github-readonly to read README.md from sharmaanku/git-demo at the default branch.`
4. Record the tool name, success result, and whether it returned only repository content. Do not ask for mutations.

The shell fallback is `curl` against GitHub's public REST API, but that fallback is not an MCP request. It can validate repository availability only and must not be used as proof of MCP authentication.

## Fallback plan

MCP unavailability must not stop the rest of the project:

1. Continue repository inspection with workspace file tools and direct read-only Git operations.
2. Run unit/API/browser/RAG tests from the Python virtual environment or Maven as applicable.
3. Do not weaken assertions or hide failures because MCP is unavailable.
4. Record exact commands and pass/fail totals in the final report.
5. Keep payment testing mock-only or local; never reach a production or live payment service.

## Risks and limitations

- `/mcp` and `/mcp` tool availability depend on workspace trust and interactive approval.
- A fine-grained PAT may expose only the repository and permission scope granted to it. It can still be misused by any process able to read the shell environment.
- Read-only mode is a server tool filter; the credential should remain read-only as defense in depth.
- Remote MCP traffic leaves the local environment and is subject to GitHub service availability.
