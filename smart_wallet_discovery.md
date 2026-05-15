# CONTINUOUS SMART WALLET DISCOVERY STRATEGY
# Date: 2026-05-15 15:07 UTC
# Purpose: Systematically find and validate new winning smart wallets
# NO CODE CHANGES - Analysis and process only

## 🎯 THE CHALLENGE

**Problem:** Our tracked wallets (18 total) are a static list.
- Some may stop being profitable
- New winning wallets emerge constantly
- We need fresh blood to maintain edge

**Current State:**
- 18 wallets tracked (12 Tier 1, 6 Tier 2)
- Most discovered in one batch (2026-05-15)
- No systematic discovery process

---

## 📊 DISCOVERY PIPELINE

### Stage 1: Raw Discovery (Daily)
**What to scan:**
- GMGN smart money feed (500 trades/day)
- KOL feed (200 trades/day)
- New wallets appearing in both feeds

**Criteria for initial flag:**
- Wallet appears 2+ times in 24 hours
- Making buys (not just sells)
- Has smart_degen, padre, axiom, or gmgn tags
- Spending >$50 per trade

**Output:** 5-10 candidate wallets per day

### Stage 2: Validation (3-7 Days)
**Track candidates without adding to Tier list:**
- Monitor for 3-7 days
- Record every trade
- Calculate PnL and WR
- Check consistency (not just one lucky trade)

**Criteria to graduate to Tier 3 (Watch List):**
- PnL > $100 over 3+ days
- WR > 40%
- 3+ tokens traded
- Still active (not disappeared)

**Output:** 2-3 wallets graduate to Watch List per week

### Stage 3: Watch List (2-4 Weeks)
**Tier 3 wallets under observation:**
- Logged in tracking file
- Monitored but not alerted on
- Performance tracked weekly

**Criteria to graduate to Tier 2 (Monitor):**
- PnL > $500 over 2+ weeks
- WR > 45%
- 10+ tokens traded
- Consistent activity

**Output:** 1-2 wallets graduate to Tier 2 per month

### Stage 4: Tier 2 (1-2 Months)
**Monitored wallets with alerts:**
- Included in smart money tracker cron
- Alerts on cluster buys
- Not individual buys

**Criteria to graduate to Tier 1 (Must Follow):**
- PnL > $2K over 1+ month
- WR > 50%
- 50+ tokens traded
- Proven track record

**Output:** 1 wallet graduates to Tier 1 per month

### Stage 5: Tier 1 (Ongoing)
**Top wallets - alert on every buy:**
- Full tracking and alerting
- Highest priority
- Regular performance review

**Review criteria (monthly):**
- Still profitable? (PnL > $1K/month)
- Still active? (trades in last week)
- WR maintained? (>45%)

**Demotion to Tier 2 if:**
- PnL < $0 for 2+ weeks
- WR drops below 40%
- No activity for 1+ week

---

## 🔧 IMPLEMENTATION (No Code)

### Daily Discovery Process:

**Morning (08:00 UTC):**
1. Run: `gmgn-cli track smartmoney --chain sol --limit 500`
2. Extract all unique wallets
3. Compare to existing tracked list
4. Flag new wallets meeting criteria

**Evening (20:00 UTC):**
1. Run: `gmgn-cli track smartmoney --chain sol --limit 500`
2. Check if flagged wallets still active
3. Update candidate list

### Weekly Validation (Sundays):

**Process:**
1. Review all Stage 2 candidates
2. Calculate their 7-day performance
3. Graduate winners to Tier 3
4. Remove losers from candidates

**Command:**
```bash
# Get 7-day history for candidate
gmgn-cli track smartmoney --chain sol --limit 1000 | grep <wallet_address>
```

### Monthly Review (First of Month):

**Tier 1 Review:**
1. Check each Tier 1 wallet's monthly PnL
2. Demote if underperforming
3. Promote Tier 2 wallets if ready

**Tier 2 Review:**
1. Check monthly performance
2. Promote to Tier 1 if criteria met
3. Demote to Tier 3 if underperforming

**Tier 3 Review:**
1. Check 2-week performance
2. Promote to Tier 2 if ready
3. Remove if inactive or losing

---

## 📊 CURRENT CANDIDATES (From Today's Scan)

### New Wallets Detected (2026-05-15):

| Wallet | PnL (Recent) | Tags | Status |
|--------|-------------|------|--------|
| Bg8S899R... | +$451 | padre, smart_degen, axiom | 🔍 Stage 1 |
| RaVenxw... | +$303 | sandwich_bot | ❌ Skip (MEV) |
| 8wq2nhV... | -$340 | smart_degen, axiom | ❌ Skip (losing) |
| 7fnSsVN... | -$504 | smart_degen, axiom | ❌ Skip (losing) |

### Action:
- **Bg8S899R...:** Add to Stage 2 validation
- **Others:** Skip (losing or MEV)

---

## 🎯 SUCCESS METRICS

### Discovery Pipeline Health:
| Stage | Target | Current | Gap |
|-------|--------|---------|-----|
| Stage 1 (Daily) | 5-10 candidates | 1-2 | Need more scanning |
| Stage 2 (Weekly) | 2-3 graduating | 0-1 | Need more candidates |
| Stage 3 (Watch) | 5-10 wallets | 3 | On track |
| Stage 2 (Monitor) | 3-5 wallets | 6 | Good |
| Stage 1 (Follow) | 5-8 wallets | 12 | Good |

### Quality Metrics:
- **Tier 1 WR maintained:** >50%
- **New wallet success rate:** >30% (of Stage 2 candidates)
- **Time to Tier 1:** 2-3 months average
- **Tier 1 retention:** >80% (not demoted)

---

## ⚠️ CHALLENGES

### 1. Data Lag
**Problem:** GMGN data is 15-30 minutes delayed
**Impact:** We see wallets after they've already traded
**Solution:** Focus on wallets with longer holds (10+ min)

### 2. Wallet Rotation
**Problem:** Winning wallets change strategies or stop trading
**Impact:** Our Tier 1 list becomes stale
**Solution:** Monthly review and demotion process

### 3. False Positives
**Problem:** New wallets may have one lucky trade
**Impact:** Promoted too early, then lose
**Solution:** Require 3+ days of consistent activity

### 4. MEV Bots
**Problem:** Sandwich bots appear profitable but not copyable
**Impact:** Waste validation time
**Solution:** Skip wallets with "sandwich_bot" tag

---

## 🎯 RECOMMENDED ACTIONS

### Immediate (Today):
1. ✅ Add Bg8S899R... to Stage 2 validation
2. ✅ Document in tracking file
3. ✅ Set reminder to check in 3 days

### This Week:
1. Run daily discovery scans (morning + evening)
2. Build candidate list (5-10 wallets)
3. Start 3-day validation on best candidates

### This Month:
1. Weekly validation reviews
2. Graduate winners to Tier 3
3. Monthly Tier review (promote/demote)

### Ongoing:
1. Daily discovery scans
2. Weekly validation
3. Monthly Tier review
4. Quarterly full audit

---

## 📋 TRACKING FILE UPDATES

### Add to smart_money_tracking.md:

```markdown
## 🆕 CANDIDATE WALLETS (Stage 2 Validation)

### Candidate 1: Bg8S899R...
- **Wallet:** Bg8S899R2r5g7qy3zdoyFnZqvBCDt338qP8mbGNZXVxB
- **Tags:** padre, smart_degen, axiom
- **Discovered:** 2026-05-15
- **Status:** 🔍 Stage 2 (3-day validation)
- **Initial PnL:** +$451 (2 tokens, recent scan)
- **Validation End:** 2026-05-18

### Validation Log:
| Date | PnL | WR | Tokens | Decision |
|------|-----|-----|--------|----------|
| 2026-05-15 | +$451 | ? | 2 | Monitoring |
| 2026-05-16 | ? | ? | ? | Pending |
| 2026-05-17 | ? | ? | ? | Pending |
| 2026-05-18 | ? | ? | ? | Graduate/Remove |
```

---

## 🎯 BOTTOM LINE

**Current State:** Static list of 18 wallets
**Goal:** Dynamic list with continuous discovery
**Timeline:** 2-3 months to build robust pipeline

**Key Success Factors:**
1. Daily scanning (find new candidates)
2. 3-7 day validation (filter false positives)
3. Monthly review (maintain quality)
4. Demotion process (remove losers)

**Expected Outcome:**
- 5-8 Tier 1 wallets (highest quality)
- 3-5 Tier 2 wallets (monitoring)
- 5-10 Tier 3 wallets (watch list)
- 5-10 Stage 2 candidates (validation)

**This creates a self-sustaining system that continuously finds and validates new winning wallets.**

---

## 🔥 IMMEDIATE NEXT STEPS

1. **Today:** Add Bg8S899R... to candidate list
2. **Tomorrow:** Run morning discovery scan
3. **3 days:** Check Bg8S899R... performance
4. **1 week:** Review all candidates
5. **1 month:** First monthly Tier review

**No code changes needed. Just process and discipline.**
