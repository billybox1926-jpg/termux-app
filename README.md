# Termux app fork maintenance

This repository is a maintenance fork of the upstream [Termux application](https://github.com/termux/termux-app). It is used for focused bug-fix work, runtime testing, and preparing changes before they are split into clean upstream pull requests.

This is not the official Termux release repository. Users who only want to install Termux should normally use the official Termux channels and documentation. This fork exists so we can keep a controlled workbench while learning the app, testing fixes, and building a reliable local Android/Termux stack.

## 2026 maintenance status

Current maintenance rule: keep one active workbench lane, make small fixes, push only after the branch is clean, and let GitHub Actions decide whether the source is healthy.

The expected active branch for this fork is:

```text
workbench-app-issue-factory
```

Do not push directly to `master` or `main` unless that is explicitly requested. Treat the workbench branch as the integration lane and create upstream PR branches from clean, reviewable slices.

## What this repo contains

The `termux-app` repository is the Android app itself: the terminal UI, session management, app lifecycle, terminal emulator integration, storage access, Android intents, and plugin-facing integration points.

Packages installed inside Termux are maintained separately in [termux/termux-packages](https://github.com/termux/termux-packages). Termux:API command wrappers and plugin behavior live in separate repositories. When debugging app/API behavior, keep the boundary clear:

```text
Termux app          -> terminal, sessions, UI, app lifecycle
Termux:API app      -> Android API receiver/listener implementation
termux-api package  -> shell commands and native wrapper binaries
termux-packages     -> packages installed inside Termux
```

## Branch discipline

Use this branch model unless the maintainer intentionally changes it:

```text
origin/master or origin/main   -> upstream/default history
workbench-app-issue-factory    -> local integration lane
fix/<topic>                    -> optional short-lived PR branch
```

Rules:

- keep `workbench-app-issue-factory` clean and buildable;
- prefer five small source fixes over one giant rewrite;
- do not rewrite Gradle, SDK, workflow, or manifest configuration while fixing unrelated issues;
- use revert or `--force-with-lease` only when deliberately repairing a workbench branch;
- preserve phone/runtime fixes unless CI proves they broke source;
- preserve upstream behavior unless the issue specifically requires a behavior change.

## Build gate

GitHub Actions is the main green/red gate for this fork. Local Windows or phone builds are useful for quick feedback, but local tooling failures are suspect until Actions confirms the problem.

For a local Windows build, use PowerShell from the repository root:

```powershell
cd C:\Users\Billy\Documents\GitHub\termux-app
.\gradlew.bat clean :app:assembleDebug --no-daemon --console=plain
```

When a build fails, chase the first real compiler, lint, or test error. Ignore surrounding Gradle noise until the first source failure is understood.

## Runtime testing

A green build only proves the app compiles. It does not prove Android package identity, signatures, shared UID behavior, plugin wiring, or phone runtime behavior.

Before declaring a fix done, test the relevant path on a device when possible:

```powershell
adb devices
adb install -r path\to\app-debug.apk
adb shell am start -n com.termux/.app.TermuxActivity
adb logcat -d | findstr /i "termux crash exception fatal"
```

For plugin/API work, test the whole stack that participates in the behavior. Many bugs sit in the seams between the app, plugin APK, package wrapper, socket listener, broadcast receiver, and Android process lifecycle.

## Package identity and signing warning

Termux and its plugins use Android package identity and signing rules that are easy to break. Do not mix APKs from unrelated sources.

Important rules:

- F-Droid Termux and F-Droid plugins must stay together.
- GitHub/debug builds must stay with matching GitHub/debug plugin builds.
- Different signing keys can trigger `INSTALL_FAILED_UPDATE_INCOMPATIBLE` or `INSTALL_FAILED_SHARED_USER_INCOMPATIBLE`.
- Side-by-side debug builds need deliberate package names and wrappers that target the matching package.
- Do not install a debug build over a working phone stack unless the whole stack is intentionally being replaced.

If runtime behavior makes no sense, verify the installed packages first:

```powershell
adb shell pm list packages | findstr termux
adb shell dumpsys package com.termux | findstr /i "versionName userId signatures"
adb shell dumpsys package com.termux.api | findstr /i "versionName userId signatures"
```

## Workflow maintenance

The workflows should prove source health, not hide source problems. Keep workflow edits small and boring.

Do not casually change:

- Gradle wrapper version;
- Android Gradle Plugin version;
- compile SDK / target SDK;
- signing configuration;
- manifest package identity;
- shared UID behavior;
- artifact names used by install/test scripts.

If a workflow breaks after a source fix, inspect the first failing command and compare with the last green commit before changing build infrastructure.

## Issue-fix workflow

For each issue or bug:

1. Start from the clean workbench branch.
2. Understand the runtime path before editing.
3. Make the smallest source change that can fix the behavior.
4. Run a targeted local check if it is cheap.
5. Commit with a clear message.
6. Push to the workbench branch.
7. Use GitHub Actions as the gate.
8. Batch PR work later from clean slices.

Preferred commit style:

```text
fix: guard session exit null command
fix: preserve ctrl modifier for page navigation
docs: refresh fork maintenance README
```

## Android areas that matter most

For 2026 maintenance, the important study lanes are:

- Android app lifecycle: `Application`, `Activity`, `Service`, `BroadcastReceiver`, process death, and background limits.
- Android package identity: `applicationId`, debug suffixes, signatures, `sharedUserId`, and plugin compatibility.
- Terminal/session lifecycle: session creation, session exit, command execution, notification updates, and null-safety around process state.
- Storage and file intents: SAF, content URIs, permissions, and Android version differences.
- GitHub Actions: build/test gates, artifacts, signing paths, and avoiding workflow churn.

## Relationship to upstream

Keep this fork upstream-friendly. Workbench commits can be practical and messy while a problem is being understood, but upstream pull requests should be small, focused, and easy to review.

Before opening upstream PRs:

- split unrelated fixes;
- remove fork-only notes from code changes;
- verify formatting and tests;
- explain the user-visible bug;
- explain why the fix is narrow;
- include runtime proof when the issue depends on Android behavior.

## Useful links

- [Official Termux site](https://termux.dev)
- [Official Termux app repository](https://github.com/termux/termux-app)
- [Termux packages](https://github.com/termux/termux-packages)
- [Termux Wiki](https://wiki.termux.dev/wiki/Main_Page)
- [Termux:API](https://github.com/termux/termux-api)
- [Android logcat documentation](https://developer.android.com/studio/command-line/logcat)

## Maintainer note

The goal is not only to patch Termux. The goal is to build enough operational experience to maintain our own Android/Termux-style tools with discipline: clean branches, boring builds, clear runtime tests, and no mystery changes hiding in the machinery.
