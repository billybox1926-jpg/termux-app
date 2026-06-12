# Issue Factory Progress

Tracks which upstream termux-app issues have been inspected and fixed in this fork.

## Fix Status Legend
- **Fixed** — Patch applied and verified
- **Requires Review** — Needs runtime testing or larger refactoring

---

## Fixed Issues

### #5119 — ESC character paste crash
Status: Fixed (upstream, cherry-picked)
Why it matters: Pasting a bare ESC character crashes the app with IllegalArgumentException in ByteQueue.write().
Files changed: `terminal-emulator/.../TerminalEmulator.java`
Fix: paste() strips control characters; returns early if text is empty after stripping.

### #5048 — Session notification not updated on rename
Status: Fixed (upstream, cherry-picked)
Why it matters: Renaming a session via long-press doesn't update the persistent notification.
Files changed: `TermuxTerminalSessionActivityClient.java`, `TermuxService.java`

### #5145 — Crash report notification SecurityException
Status: Fixed (upstream, cherry-picked)
Why it matters: Plugin crash notifications from different package contexts throw SecurityException.
Files changed: `TermuxCrashUtils.java`
Fix: Wrap notificationManager.notify() in try-catch for SecurityException.

### #5027 — ListView adapter crash from background thread
Status: Fixed (upstream, cherry-picked)
Why it matters: Session list modified on background thread causes IllegalStateException in ListView.
Files changed: `TermuxActivity.java`

### #5014 — Soft keyboard flicker on return via launcher
Status: Fixed (upstream, cherry-picked)
Why it matters: Fixed 300ms delay fires before window focus arrives when returning via launcher.
Files changed: `TermuxTerminalViewClient.java`
Fix: showSoftKeyboardWithRetry() checks hasWindowFocus() and retries.

### #3478 — ViewPager pointerIndex out of range crash
Status: Fixed (upstream, cherry-picked)
Files changed: `SafeViewPager.java`, `activity_termux.xml`

### #5092 — UI-thread blocking in file-receive flow
Status: Fixed (upstream, cherry-picked)
Files changed: `FileReceiverActivity.java`

### #5144 — AndroidUtils resource leak
Status: Fixed (upstream, cherry-picked)
Files changed: `AndroidUtils.java`

### #3935 — Route non-file URI schemes to url-opener
Status: Fixed (workbench-app-issue-factory)
Files changed: `FileReceiverActivity.java`, `FileReceiverActivityTest.java`

### #3884 — Re-show keyboard after clipboard copy
Status: Fixed (workbench-app-issue-factory)
Files changed: `TermuxTerminalSessionActivityClient.java`

### #4157 — Allow termux.properties to be a symlink
Status: Fixed (workbench-app-issue-factory)
Files changed: `SharedProperties.java`

### #4281 — Treat Caps Lock as Ctrl on physical keyboard
Status: Fixed (workbench-app-issue-factory)
Files changed: `TerminalView.java`, `TerminalViewClient.java`, `TermuxTerminalViewClientBase.java`

### #5093 — Main-thread ContentResolver.query() in FileReceiverActivity
Status: Fixed (workbench-app-issue-factory)
Files changed: `FileReceiverActivity.java`
Fix: Moved query() into background thread alongside openInputStream().

### #4706 — ListView adapter crash (session list concurrency)
Status: Fixed (workbench-app-issue-factory)
Files changed: `TermuxActivity.java`
Fix: Use postAtFrontOfQueue for notifyDataSetChanged to prevent stale data during layout.

---

## Requires Review

### #4589 — extra-keys malfunctioning
Reason: Needs runtime/device-specific verification.

### #5128 — Idle timeout / power drain guard
Reason: Needs runtime/device-specific verification.
