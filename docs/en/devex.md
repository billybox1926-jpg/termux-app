# Developer Experience Standards

Lightweight DevEx conventions for the termux-app repository.

## Local workflow

1. Read `README.md` for project purpose and prerequisites.
2. Open the project in Android Studio or build from the command line with `./gradlew`.
3. Make a focused change on a short-lived branch.
4. Run `./gradlew test` before opening a pull request.
5. Open a PR with validation notes and any relevant screenshots or logs.

## Build commands

| Command | Purpose |
|---------|---------|
| `./gradlew assembleDebug` | Build debug APK |
| `./gradlew test` | Run unit tests |
| `./gradlew testDebugUnitTest` | Run debug unit tests only |

## Validation

Run tests before pushing:

```bash
./gradlew test
```

CI runs on every push to `master` via GitHub Actions (`.github/workflows/`).

## Coding standards

- Keep changes focused and easy to review.
- Follow existing code style (4-space indentation, no tabs).
- Keep `terminal-emulator` free of Android dependencies.
- Add tests for new behavior in the module's `src/test/` directory.
- Update docs when behavior, setup, or architecture changes.
- Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.

## Pull request hygiene

A healthy PR should include:
- A clear summary of what changed and why
- Linked issues when applicable
- Test results (`./gradlew test` passing)
- Screenshots for UI changes
- Documentation updates for user-facing changes
