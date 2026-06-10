## Issue #4589
Status: Requires Review
Reason: Needs runtime/device-specific verification or larger change; not safe for minimal static patch.
Commit SHA: none
CI: none

## Issue #5128
Status: Requires Review
Reason: Needs runtime/device-specific verification or larger change; not safe for minimal static patch.
Commit SHA: none
CI: none

## Issue #5119 — ESC character paste crash
Status: Fixed
Verification: GitHub Actions Build
Why it matters for our fork: Pasting a bare ESC character (\u001B) crashes the app with IllegalArgumentException in ByteQueue.write(). This is a reproducible crash that affects any user who pastes control characters.
Files inspected:
- terminal-emulator/src/main/java/com/termux/terminal/TerminalEmulator.java
- terminal-emulator/src/main/java/com/termux/terminal/ByteQueue.java
Files changed:
- terminal-emulator/src/main/java/com/termux/terminal/TerminalEmulator.java
Code commit SHA:
- 0a84468d
CI run ID:
- 27295347349
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27295347349
- apt-android-5: arm64-v8a, armeabi-v7a, x86, x86_64, universal, sha256sums
- apt-android-7: arm64-v8a, armeabi-v7a, x86, x86_64, universal, sha256sums
Notes:
- After stripping control characters, if the text is empty, paste() returns early instead of calling mSession.write("") which would trigger ByteQueue.write() with length 0.
- Both Android 5 and Android 7 build matrices passed.

## Issue #5048 — Session notification not updated on rename
Status: Fixed
Verification: GitHub Actions Build
Why it matters for our fork: When a user renames a session via long-press, the persistent notification continues showing the old name. This is a UI inconsistency that confuses users.
Files inspected:
- app/src/main/java/com/termux/app/terminal/TermuxTerminalSessionActivityClient.java
- app/src/main/java/com/termux/app/TermuxService.java
Files changed:
- app/src/main/java/com/termux/app/terminal/TermuxTerminalSessionActivityClient.java
- app/src/main/java/com/termux/app/TermuxService.java
Code commit SHA:
- bda4bd9c
CI run ID:
- 27295347349
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27295347349
Notes:
- Added updateNotificationPublic() wrapper in TermuxService.
- onTitleChanged() now calls updateNotificationPublic() when the renamed session is the current one.

## Issue #5145 — Crash report notification SecurityException
Status: Fixed
Verification: GitHub Actions Build
Why it matters for our fork: When a plugin sends a crash notification from a different package context, the notification manager throws SecurityException ("Package X does not belong to Y"), crashing the app.
Files inspected:
- termux-shared/src/main/java/com/termux/shared/termux/crash/TermuxCrashUtils.java
Files changed:
- termux-shared/src/main/java/com/termux/shared/termux/crash/TermuxCrashUtils.java
Code commit SHA:
- 956f002b
CI run ID:
- 27295347349
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27295347349
Notes:
- Wrapped notificationManager.notify() in try-catch for SecurityException.
- Error is logged instead of crashing the app.

## Issue #5027 — ListView adapter crash from background thread
Status: Fixed
Verification: GitHub Actions Build
Why it matters our fork: When sessions are added/removed from background threads (e.g. onTermuxSessionExited), notifyDataSetChanged() is called off the UI thread, causing IllegalStateException in ListView.
Files inspected:
- app/src/main/java/com/termux/app/TermuxActivity.java
- app/src/main/java/com/termux/app/TermuxService.java
- app/src/main/java/com/termux/app/terminal/TermuxSessionsListViewController.java
Files changed:
- app/src/main/java/com/termux/app/TermuxActivity.java
Code commit SHA:
- a5ce7563
CI run ID:
- 27295347349
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27295347349
Notes:
- termuxSessionListNotifyUpdated() now uses runOnUiThread() to ensure notifyDataSetChanged() always runs on the UI thread.

## Issue #5014 — Soft keyboard flicker on return via launcher
Status: Fixed
Verification: GitHub Actions Build
Why it matters for our fork: When returning to Termux via launcher (not recents), the 300ms fixed delay for showing the soft keyboard may fire before window focus arrives, causing the keyboard to flicker and disappear.
Files inspected:
- app/src/main/java/com/termux/app/terminal/TermuxTerminalViewClient.java
Files changed:
- app/src/main/java/com/termux/app/terminal/TermuxTerminalViewClient.java
Code commit SHA:
- c8192808
CI run ID:
- 27295347349
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27295347349
Notes:
- Replaced fixed 300ms postDelayed with showSoftKeyboardWithRetry() that checks hasWindowFocus() and retries up to 3 times with 100ms delays.

## Issue #3478 — ViewPager pointerIndex out of range crash
Status: Fixed
Verification: GitHub Actions Build
Files changed:
- app/src/main/java/com/termux/app/terminal/io/SafeViewPager.java
- app/src/main/res/layout/activity_termux.xml
Code commit SHA:
- 2a7d23b43ffedf8999ce94cf14455fbebeabf41f
CI run ID:
- 27276218332
CI status:
- success
Artifacts:
- Saved outside repo at C:\Users\Billy\Documents\GitHub\termux-app-artifacts\run-27276218332
- apt-android-5: arm64-v8a, armeabi-v7a, x86, x86_64, universal, sha256sums
- apt-android-7: arm64-v8a, armeabi-v7a, x86, x86_64, universal, sha256sums
Notes:
- SafeViewPager prevents the pointerIndex out of range crash by catching IllegalArgumentException in onInterceptTouchEvent and returning false.
- activity_termux.xml now uses SafeViewPager for terminal_toolbar_view_pager.
- Both Android 5 and Android 7 build matrices passed.

## Issue #5092 — UI-thread blocking in file-receive flow
Status: Fixed
Verification: GitHub Actions Build
Files inspected:
- app/src/main/java/com/termux/app/api/file/FileReceiverActivity.java
Files changed:
- app/src/main/java/com/termux/app/api/file/FileReceiverActivity.java
Code commit SHA:
- f8f9e4c0dd5b57e3c8e4cf6285cf191eeb47c61a
Verification commit SHA:
- dcc970fe6fac068715cd3780169034f3b7262052
CI run ID:
- 27275107309
CI status:
- success
Notes:
- File-receive stream open and stream-copy work are no longer performed on the UI thread.
- UI actions and error dialogs are marshaled through runOnUiThread.
- InputStream is closed after save/copy completion.
- Build verification passed on successor commit dcc970fe, which contains the #5092 code fix.
