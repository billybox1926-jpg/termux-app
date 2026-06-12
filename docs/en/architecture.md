# Architecture

This document describes the module layout and dependency structure of the termux-app repository.

## Layout

```
app/                  — Main Android application module
terminal-emulator/    — Terminal emulation library (JVM)
terminal-view/        — TerminalView widget (Android)
termux-shared/        — Shared utilities used by app and plugins
docs/                 — Documentation
.github/workflows/    — CI/CD workflows
gradle/               — Gradle wrapper
art/                  — Icon generation scripts and assets
```

## Module responsibilities

### `app/`

The main Android application. Contains activities, services, broadcast receivers, and the Android manifest.

Key components:
- `TermuxActivity` — main launcher activity
- `TermuxService` — foreground service managing terminal sessions
- `TermuxOpenReceiver` — internal broadcast receiver for URI handling
- `RunCommandService` — external command execution (permission-gated)
- `FileReceiverActivity` — file receive handler (behind activity-alias)
- `TermuxSchemeOpenerActivity` — trampoline for `termux:` URI scheme

### `terminal-emulator/`

Pure JVM terminal emulation library. No Android dependencies.

Contains:
- `TerminalEmulator` — terminal state machine
- `TerminalSession` — session management
- `KeyHandler` — key code translation
- `TerminalRow`, `ScreenBuffer` — screen buffer management
- `ByteQueue`, `ControlSequenceIntroducer` — input parsing

### `terminal-view/`

Android `View` widget for rendering terminal output.

Contains:
- `TerminalView` — the terminal rendering view
- `TerminalViewClient` — interface for key handling callbacks
- `GestureAndScaleRecognizer` — touch gesture handling

### `termux-shared/`

Shared library used by the main app and plugin apps.

Contains:
- `TermuxPropertyConstants`, `TermuxSharedProperties` — termux.properties parsing
- `Logger` — logging utilities
- `FileUtils`, `PackageUtils`, `ShellUtils` — common helpers
- `ExecutionCommand` — execution command model

## Dependency direction

```
app → terminal-view → terminal-emulator
app → termux-shared
terminal-view → termux-shared
terminal-emulator → (no internal dependencies)
```

`terminal-emulator` is the leaf module — it depends on no other project modules. `termux-shared` is the utility layer. `terminal-view` depends on both. `app` depends on all three.

## Extension pattern

When adding a new capability:

1. Add domain logic to the appropriate module (`terminal-emulator` for terminal behavior, `termux-shared` for shared utilities, `terminal-view` for UI, `app` for Android integration).
2. Keep `terminal-emulator` free of Android dependencies.
3. Keep `core` logic separate from Android framework code.
4. Add tests under the module's `src/test/` directory.
5. Update `docs/en/execution-architecture.md` if the intent/execution flow changes.
