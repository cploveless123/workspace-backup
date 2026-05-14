# CRITICAL REMINDERS - READ BEFORE EVERY ANALYSIS

## ⚠️ MANDATORY CHECKLIST

### Before ANY Analysis:
- [ ] Verify data source is current (check timestamps)
- [ ] Count total records, not grouped/subset
- [ ] Check for multiple records per token (partial sells)
- [ ] Verify status fields (open vs closed)
- [ ] Cross-check with a second method
- [ ] Test script on known data first

### Before Reporting:
- [ ] Does this match expected performance?
- [ ] Are numbers reasonable? (27 open positions = red flag)
- [ ] Can I explain every number?
- [ ] Have I double-checked with alternative query?

### Code Changes:
- [ ] NEVER without explicit Chris approval
- [ ] ALWAYS backup first
- [ ] ALWAYS test after
- [ ] ALWAYS report before deploying
- [ ] ALWAYS update memory files

## TODAY'S FAILURES (2026-05-14):
1. Reported 27 open positions (actual: 1) - didn't check status field
2. Reported 43 sells (actual: 65+) - grouped by token instead of counting all
3. Reported -0.14 SOL loss (actual: +0.78 SOL profit) - wrong methodology
4. Reported 27.9% WR (actual: 68.9%) - incomplete data

## ROOT CAUSE:
- Wrote analysis scripts without testing
- Didn't verify results against known good data
- Didn't cross-check with simple alternative methods
- Trusted first output without questioning

## CONSEQUENCES:
- Wasted Chris's time with wrong information
- Nearly caused unnecessary strategy changes
- Eroded trust

## PREVENTION:
- ALWAYS use multiple verification methods
- ALWAYS question results that seem off
- ALWAYS test scripts on small known datasets first
- WHEN IN DOUBT: say "let me verify" instead of reporting
