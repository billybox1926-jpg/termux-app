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
