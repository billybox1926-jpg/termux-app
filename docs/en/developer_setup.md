# Developer Setup

Onboarding guide for new contributors to the termux-app repository.

## Prerequisites

- **Android Studio** (latest stable) or **IntelliJ IDEA** with Android plugin
- **JDK 17** (required by the project)
- **Android SDK** with API 30 (compileSdk) and build-tools
- **Git** 2.40+
- At least 8 GB RAM free for Gradle daemon

## Bootstrap locally

```bash
git clone https://github.com/billybox1926-jpg/termux-app.git
cd termux-app
```

Open in Android Studio:
1. File → Open → select the `termux-app` directory
2. Wait for Gradle sync to complete
3. Accept Android SDK license prompts if shown

Or build from the command line:

```bash
./gradlew assembleDebug
```

## Project structure

| Module | Purpose |
|--------|---------|
| `app/` | Main Android application |
| `terminal-emulator/` | Terminal emulation library (pure JVM) |
| `terminal-view/` | TerminalView Android widget |
| `termux-shared/` | Shared utilities |

See `docs/en/architecture.md` for the full dependency graph.

## Running tests

```bash
# All tests
./gradlew test

# Debug unit tests only
./gradlew testDebugUnitTest
```

## Build variants

The project builds only the `apt-android-7` variant (minSdk 24). The `apt-android-5` variant has been removed from CI.

## Branch and PR workflow

1. Create a branch from `main`.
2. Make your changes and add tests.
3. Run `./gradlew test` locally.
4. Push and open a PR with a clear description.
5. CI will run the debug build and tests automatically.
6. Merge only when CI checks pass.

## Common issues

- **Gradle sync fails**: Ensure JDK 17 is selected in Android Studio (File → Project Structure → SDK Location → JDK).
- **Build fails with SDK errors**: Run `sdkmanager "platforms;android-30"` from the Android SDK command-line tools.
- **Tests fail on KeyHandlerTest**: This is a known upstream test that may need adjustment for custom key handling changes.
