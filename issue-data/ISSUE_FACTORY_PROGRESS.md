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
