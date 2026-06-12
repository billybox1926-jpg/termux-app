# TERMUX_APP_ISSUE_LEDGER

## Summary
- Total upstream open issues: check `gh issue list -R termux/termux-app --state open`
- Fixed in this fork (workbench-app-issue-factory branch): see below

## Fixed Issues (this fork)

### termux-app repo
| Issue | Description | Commit | Status |
|-------|-------------|--------|--------|
| #4157 | Allow termux.properties to be a symlink | e9870539 | Merged via PR #5 |
| #4281 | Treat Caps Lock as Ctrl on physical keyboard | 6611b487+7484ca0f | Merged via PR #5 |
| #3935 | Route non-file URI schemes to url-opener | 65942a0c | Current branch |
| #3884 | Re-show keyboard after clipboard copy | 7e82ec67 | Current branch |
| #5093 | Main-thread blocking in FileReceiverActivity | ff28b2d6 | Current branch |
| #4706 | ListView adapter crash from background thread | c67f6423 | Current branch |

### Earlier fixes (from PR #1-4, cherry-picked upstream)
- #5119 ESC paste crash → merged upstream
- #5047 FLAG_IMMUTABLE → merged upstream
- #5027 ListView concurrency → merged upstream
- #5014 Keyboard flicker → merged upstream
- #3478 SafeViewPager crash → merged upstream
- #5048 Session notification rename → merged upstream
- #5145 Crash notification SecurityException → merged upstream
- #5092 FileReceiverActivity ANR → merged upstream
- #5144 AndroidUtils resource leak → merged upstream

### termux-api-package repo (separate)
- #224 run_api_command file descriptor leak → Fixed, CI green
- #200 detect missing Termux:API plugin → Fixed, CI green
