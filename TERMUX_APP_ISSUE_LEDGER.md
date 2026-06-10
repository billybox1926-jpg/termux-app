# TERMUX_APP_ISSUE_LEDGER

## Summary
- Total upstream open issues: 474
- Fixed in this fork: 3 (so far in this session)
- Remaining actionable: ~471

## Fixed Issues (this session)

### App repo (termux-app)
- #5144 Resource leak: Streams and Process not closed in AndroidUtils.getSystemProperties() → Fixed (finally block for cleanup) — commit a8390f92 — CI pending

### Package repo (termux-api-package)  
- #224 run_api_command leaks file descriptors → Fixed (close server sockets) — commit 961ca8c — CI green
- #200 termux-api command should detect if Termux:API plugin is not installed → Fixed (is_termux_api_installed check) — commit 931a7ba — CI green

## Bucket Counts
- Bucket A: 3 (quick wins — crash/ANR bugs)
- Bucket B: 4 (patches/features)
- Bucket C: 235 (mostly device-specific/vague)
- Bucket D: 6 (features)
- Bucket E: 31 (environment/install issues)
- Bucket F: 13 (medium features)
- Bucket G: 182 (feature requests/enhancements)

## Next Targets (Bucket A - Quick Wins)
- #3478: [Bug]: Termux Auto Crash (vague, needs investigation)
- #152: big crash bug (old, CyanogenMod era)

## Recently Fixed (by phone Hermes, confirmed in code)
- #5092: ANR / main-thread blocking in FileReceiverActivity → Fixed (background thread) — commits 631bb060, 3c4830bb, d88e6b78
