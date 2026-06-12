# Termux Intent & Execution Architecture

Internal reference for how Termux receives, routes, and executes commands from Android intents.

---

## 1. Android Intent Filters

### `TermuxActivity` (main entry)
```xml
<action android:name="android.intent.action.MAIN" />
<category android:name="android.intent.category.LAUNCHER" />
```
Standard launcher entry point. `exported="true"`, `singleTask` launch mode.

### `TermuxSchemeOpenerActivity` (URI handler)
```xml
<action android:name="android.intent.action.VIEW" />
<category android:name="android.intent.category.DEFAULT" />
<category android:name="android.intent.category.BROWSABLE" />
<data android:scheme="termux" />
```
`exported="true"`, translucent, no history. Only the `termux:` scheme is accepted. Cannot be launched by LAUNCHER category — only by URI intent. On Android 12+ with package visibility, other apps can still reach this because `BROWSABLE` + scheme filter makes it an implicit resolver target for `termux://` links.

### `FileShareReceiverActivity` / `FileViewReceiverActivity`
Both are `activity-alias` targeting `FileReceiverActivity` (which has `exported="false"`). The alias is the public face; the target activity stays private. Accepts `ACTION_SEND` and `ACTION_VIEW` with broad MIME types.

### `RunCommandService`
```xml
<action android:name="${TERMUX_PACKAGE_NAME}.RUN_COMMAND" />
android:permission="${TERMUX_PACKAGE_NAME}.permission.RUN_COMMAND"
```
`exported="true"` but gated by a `dangerous`-level permission. Only apps that request `com.termux.permission.RUN_COMMAND` and are granted it (runtime permission on Android 6+) can invoke it.

---

## 2. Exported Components

| Component | exported | Why |
|-----------|----------|-----|
| `TermuxActivity` | true | Launcher entry point |
| `TermuxSchemeOpenerActivity` | true | URI handler for `termux:` links from browser/other apps |
| `FileShareReceiverActivity` (alias) | true | Receive shared files from other apps |
| `FileViewReceiverActivity` (alias) | true | View files from other apps (file manager) |
| `RunCommandService` | true | Allow external apps to run commands (gated by permission) |
| `TermuxService` | false | Internal use only |
| `TermuxOpenReceiver` | false | Internal broadcast receiver |
| `FileReceiverActivity` (target) | false | Behind the aliases — not directly reachable |
| `SettingsActivity` | true | Allow opening settings from external triggers |

---

## 3. Trampoline Activity Pattern

`TermuxSchemeOpenerActivity` receives the public intent, then immediately forwards it:

```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    Intent receiverIntent = new Intent(this, TermuxOpenReceiver.class);
    receiverIntent.setData(data);
    receiverIntent.setAction(intent.getAction());
    if (intent.getExtras() != null) receiverIntent.putExtras(intent.getExtras());
    sendBroadcast(receiverIntent);
    finish();
}
```

Why a trampoline?
- `exported="true"` Activity can be reached by any app on the device. A malicious app could fire intents at it.
- The Activity itself does no processing — it just rebroadcasts to the internal `TermuxOpenReceiver`.
- The Activity is translucent + noHistory — the user never sees it.
- All validation and execution logic stays in `TermuxOpenReceiver` / `TermuxService`, which are internal.
- The Activity finishes in <1ms — no process lifecycle overhead.

---

## 4. BroadcastReceiver vs Service Execution

**TermuxOpenReceiver** (`exported="false"`):
- Receives the rebroadcast from `TermuxSchemeOpenerActivity`
- Also receives internal broadcasts from `FileReceiverActivity`/`TermuxActivity`
- Routes `scheme` field to determine handling:
  - `termux:` scheme → `handleTermuxScheme()` → starts `TermuxService`
  - Other URI schemes (http, https, etc.) → `context.startActivity(urlIntent)` (opens in browser)
  - `file:` scheme → share via `Intent.ACTION_SEND`/`ACTION_VIEW` with ContentProvider URI

**TermuxRunCommandService** (`exported="true"`, permission-gated):
- Receives explicit intents from external apps with `RUN_COMMAND` permission
- Parses `ExecutionCommand` from intent extras
- Starts `TermuxService` to execute the command

**TermuxService** (`exported="false"`):
- The actual execution engine
- Manages terminal sessions (`TerminalSession`) and background app shells (`AppShell`)
- Maintains session list, handles stdin/stdout/stderr pipes
- Shows foreground notification to avoid being killed by Android

---

## 5. ExecutionCommand Model

### Intent Action: `ACTION_SERVICE_EXECUTE`
```
com.termux.service_execute
```

### Key Extras

| Extra | Type | Purpose |
|-------|------|---------|
| `EXTRA_ARGUMENTS` | `String[]` | Arguments to the executable |
| `EXTRA_STDIN` | `String` | stdin content (before any pipe) |
| `EXTRA_WORKDIR` | `String` | Working directory |
| `EXTRA_BACKGROUND` | `boolean` | `true` = AppShell (background), `false` = TerminalSession (foreground) |
| `EXTRA_RUNNER` | `String` | `"terminal-session"` or `"app-shell"` |
| `EXTRA_SHELL_NAME` | `String` | Named shell session |
| `EXTRA_SHELL_CREATE_MODE` | `String` | `"always"` or `"no-shell-with-name"` |
| `EXTRA_BACKGROUND_CUSTOM_LOG_LEVEL` | `String` | Custom log level for background commands |

### Runner Types

- **TERMINAL_SESSION**: Creates or reuses a `TerminalSession` — command runs in a visible terminal. User sees output.
- **APP_SHELL**: Creates an invisible `AppShell` — command runs in background. No terminal UI. Used by plugins.

### Execution States
`PRE_EXECUTION` → `EXECUTING` → `EXECUTED` → `SUCCESS` / `FAILED`

`FAILED` means an internal error/exception — NOT a non-zero shell exit code. A command that exits with code 1 still counts as `SUCCESS` from Termux's perspective.

---

## 6. URI Security Rules

1. **Never eval the URI.** The URI from an intent is untrusted input. Treat it as data, never as code.

2. **Never concatenate into shell.** If forwarding to a script, pass it as an argument (`argv`), never interpolate into a shell command string:
   ```java
   // SAFE: passed as argument
   executeIntent.putExtra(EXTRA_ARGUMENTS, new String[]{uri.toString()});
   
   // UNSAFE: string interpolation into shell
   String cmd = "process_url.sh '" + uri.toString() + "'";  // NEVER DO THIS
   ```

3. **Pass as argv.** The ExecutionCommand model uses `String[] arguments` — this maps to `execv()` with proper argument boundaries, no shell interpretation.

4. **Path validation in ContentProvider.** `TermuxOpenReceiver.ContentProvider.openFile()` validates:
   - File must be under `$PREFIX` or external storage path
   - `allow_external_apps` property must be `"true"`
   - Properties files are forced to read-only mode even if write was requested

---

## 7. Script Trust Boundary

`$HOME/bin/termux-scheme-opener` is **user-controlled code**. The app treats it as a plugin hook:

- The app only invokes it if the file exists at the expected path
- The script receives the URI as `argv[1]` — it is responsible for validation
- The app does not inspect or sanitize the URI before passing it
- If the script is missing, the app logs a warning and does nothing (no crash)
- The script runs in the user's own shell environment with their own permissions

This is the same trust model as `termux-file-editor` and `termux-url-opener` — these are all user-provided scripts. The app is just the launcher. The security boundary is the user's own filesystem and shell. The app's job is to invoke the script with the right arguments and nothing more.
