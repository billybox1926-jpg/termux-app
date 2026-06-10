# TERMUX_APP_FIRST_BATCH_PLAN

## Selected Issues

- Bucket A: #5092: [Bug]: Yet another potential ANR / main-thread blocking risk
- Bucket A: #3478: [Bug]: Termux Auto Crash
- Bucket A: #152: big crash bug
- Bucket B: #5128: [Patch] | PR BLOCKED . posting patch as issue instead | idle timeout : idle drain safe guard . remove from power intensive apps
- Bucket B: #4589: "extra-keys" of "termux.properties" malfunctioning
- Bucket B: #3245: [Feature]: Need Double-width rendering of ambiguous characters
- Bucket B: #787: Are javadocs for termux source online anywhere?

## Rationale

First batch is limited to buckets A and B only: high-confidence app-code crashes and low-risk static/code-health fixes.

Do not batch-fix these automatically. Pick one issue, inspect source, make the smallest patch, and use GitHub Actions as the gate.
