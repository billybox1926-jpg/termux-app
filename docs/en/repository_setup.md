# Repository Setup Notes

Guidance for configuring the termux-app GitHub repository.

## Default branch

`main` — the default branch. All changes flow through pull requests.

## Branch protection

Recommended settings for the default branch:
- Require pull requests before merging
- Require at least one approval before merging
- Require status checks before merging
- Block force pushes on protected branches

## Required status checks

At minimum, require the main CI workflow:
- `debug_build` — builds the debug APK
- `run_tests` — runs unit tests

## Merge methods

- **Squash merge** for small feature, docs, and fix PRs
- **Merge commit** for larger work where branch history helps review

## Release workflow

This fork does not publish releases. The upstream termux/termux-app handles releases. CI builds debug APKs for validation only.

## Practical setup order

1. Fork the repository from `termux/termux-app`.
2. Clone locally and verify `./gradlew assembleDebug` succeeds.
3. Configure CI by enabling GitHub Actions.
4. Verify the debug build and test workflows pass.
5. Enable branch protection and required checks.
