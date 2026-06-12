---
page_ref: /docs/apps/termux/index.html
---

# Termux App Docs

Welcome to the Termux app documentation.

## Android 12+ Compatibility

Termux may be unstable on Android 12 and higher. The OS aggressively terminates "phantom processes" (limit of 32 system-wide) and processes using excessive CPU. This can cause sessions to end with `[Process completed (signal 9) — press Enter]`.

- Related: [issue #2366](https://github.com/termux/termux-app/issues/2366), [Android issue tracker](https://issuetracker.google.com/u/1/issues/205156966)
- A proper docs page is planned. Android 12L/13 may provide options to disable this behavior.

## Debugging

### Log Levels

Set the log level in Termux app settings → Debugging → Log Level (requires v0.118.0+).

| Level | Description |
|-------|-------------|
| Off | No logging |
| Normal | Errors, warnings, info, stacktraces |
| Debug | Debug-level messages |
| Verbose | All information (may include private data) |

Revert to `Normal` after debugging. Verbose mode may expose private data to logcat and increases execution time.

Plugin apps send execution intents to the main Termux app. Set log levels for **both** the plugin and the main app to get full info.

### Viewing Logs

- **In Termux:** `logcat` for realtime output, or `logcat -d > logcat.txt` for a dump
- **From PC:** Use `logcat` via ADB. See the [Android logcat guide](https://developer.android.com/studio/command-line/logcat)

### Reporting Issues

Long-hold the terminal → **More** → **Report Issue** to generate a debug report with file stats and logcat dump.

- Post the **complete report as text** when filing issues
- Issues with screenshots of reports instead of text will be closed
- If the report is too large, use **Save To File** (3-dot menu) to share it

## Important Links

### Community

- [Reddit](https://reddit.com/r/termux)
- [Matrix / Gitter (users)](https://matrix.to/#/#termux_termux:gitter.im)
- [Matrix / Gitter (dev)](https://matrix.to/#/#termux_dev:gitter.im)
- [X (Twitter)](https://twitter.com/termuxdevs)
- [Support email](mailto:support@termux.dev)

### Wikis

- [Termux Wiki](https://wiki.termux.com/wiki/)
- [App Wiki](https://github.com/termux/termux-app/wiki)
- [Packages Wiki](https://github.com/termux/termux-packages/wiki)

### Reference

- [XTerm control sequences](https://invisible-island.net/xterm/ctlseqs/ctlseqs.html)
- [vt100.net](https://vt100.net/)
- [Terminal codes (ANSI/terminfo)](https://wiki.bash-hackers.org/scripting/terminalcodes)

## Architecture

- [Intent & Execution Architecture](execution-architecture.md) — how Termux receives intents, routes them through the trampoline pattern, and executes commands securely
- [Module Architecture](architecture.md) — module layout, dependency graph, and folder responsibilities

## Development

- [Developer Setup](developer_setup.md) — onboarding guide for new contributors
- [Developer Experience](devex.md) — build commands, validation, coding standards, PR hygiene

## Repository

- [Repository Setup](repository_setup.md) — GitHub settings, branch protection, CI checks
- [Repository Standards](repository_standards.md) — branch naming, commit style, labels, milestones
