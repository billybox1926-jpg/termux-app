# Repository Standards

Branch naming, commit style, and release conventions for termux-app.

## Branch strategy

- Default branch: `main`
- Short-lived feature/fix branches:
  - `feat/<short-description>`
  - `fix/<short-description>`
  - `chore/<short-description>`
  - `docs/<short-description>`

## Commit style

Conventional commit prefixes:

| Prefix | Use for |
|--------|---------|
| `feat:` | New functionality |
| `fix:` | Bug fixes |
| `docs:` | Documentation-only changes |
| `chore:` | Maintenance and tooling |
| `refactor:` | Internal improvements |
| `test:` | Test additions/updates |
| `ci:` | CI workflow changes |
| `build:` | Build system changes |

References to issues should include the issue number: `fixes: #3945`.

## Pull request standards

- Keep changes focused and reviewable.
- Link related issue(s) in PR description.
- Include validation steps (test results, build output).
- Update docs when behavior changes.
- One logical change per PR.

## Label taxonomy

| Category | Labels |
|----------|--------|
| Type | `type: bug`, `type: feature`, `type: docs`, `type: chore` |
| Priority | `priority: p0`, `priority: p1`, `priority: p2` |
| Status | `status: needs-triage`, `status: blocked`, `status: ready` |

## Documentation standards

- Use clear headings (`#`, `##`, `###`) and concise sections.
- Place docs in `docs/en/` for English documentation.
- Keep the execution architecture doc in sync with code changes.
- Use the issue ledger (`TERMUX_APP_ISSUE_LEDGER.md`) to track upstream issue fixes.
