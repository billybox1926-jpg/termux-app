# TERMUX_APP_ISSUE_LEDGER

## Summary
- Total upstream open issues: check `gh issue list -R termux/termux-app --state open`
- Fixed in this fork (merged to master): see below

## Fixed Issues (this fork — all merged to master)

### termux-app repo
| Issue | Description | Commit | Status |
|-------|-------------|--------|--------|
| #4157 | Allow termux.properties to be a symlink | e9870539 | Merged to master |
| #4281 | Treat Caps Lock as Ctrl on physical keyboard | 6611b487+7484ca0f | Merged to master |
| #3935 | Route non-file URI schemes to url-opener | 65942a0c | Merged to master |
| #3884 | Re-show keyboard after clipboard copy | 7e82ec67 | Merged to master |
| #5093 | Main-thread blocking in FileReceiverActivity | ff28b2d6 | Merged to master |
| #4706 | ListView adapter crash from background thread | c67f6423 | Merged to master |
| #3945 | termux: URI scheme handling | c00584de | Merged to master |
| #3896 | Ctrl+Space not working | c00584de | Merged to master |
| #3565 | Scoped storage compatibility | c00584de, 15546aeb, 5d50a85f | Merged to master |
| #4957 | File save issue | c00584de | Merged to master |
| #4707 | CPU info | c00584de | Merged to master |
| #3549 | Extra keys on wrapped line | 74cf39ef | Merged to master |

### Earlier fixes (cherry-picked from upstream)
- #5119 ESC paste crash → merged upstream
- #5047 FLAG_IMMUTABLE → merged upstream
- #5027 ListView concurrency → merged upstream
- #5014 Keyboard flicker → merged upstream
- #3478 SafeViewPager crash → merged upstream
- #5048 Session notification rename → merged upstream
- #5145 Crash notification SecurityException → merged upstream
- #5092 FileReceiverActivity ANR → merged upstream
- #5144 AndroidUtils resource leak → merged upstream

### New fixes (not from upstream issues)
- #140 Hide extra keys row when keyboard is hidden → e6af5653
- #101 PageUp/PageDown gesture mapping in alternate buffer → bad67ef9
- #212 Add backspace-behaviour preference for BS vs DEL → 54cf50ab

### termux-api-package repo (separate)
- #224 run_api_command file descriptor leak → Fixed, CI green
- #200 detect missing Termux:API plugin → Fixed, CI green
