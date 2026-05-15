# SMART WALLET PnL TRACKING SYSTEM
# Updated: 2026-05-15 20:02 UTC
# Purpose: Track live PnL and performance of all tracked wallets

## 📊 CURRENT WALLET PERFORMANCE (Live Data)

### 🏆 TIER 1 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|-----|--------|
| 1 | Cowboy🔶BNB | +$12,554 | **+$15,312** | +$2,758 ✅ | 54.2% | PROFITABLE |
| 2 | 65kmABTf | +$5,066 | **+$5,138** | +$72 ✅ | 62.3% | PROFITABLE |
| 3 | 3jSHy | +$6,437 | **+$6,225** | -$212 ⚠️ | 56.5% | WATCH |
| 4 | H2KAvWyc | +$27 | **+$5,791** | +$5,764 📈 | 45.2% | PROMOTE CANDIDATE |
| 5 | Stigman | +$8,382 | **+$7,701** | -$681 🚨 | 43.1% | ALERT - Demotion Risk |
| 6 | 7BWy2m | +$4,898 | **+$4,886** | -$12 | 68.1% | STABLE |
| 7 | Meskxy | +$2,941 | **+$3,249** | +$308 ✅ | 70.0% | PROFITABLE |
| 8 | FdwVhb | +$4,570 | **+$4,989** | +$419 ✅ | 44.0% | PROFITABLE |
| 9 | tCPHCK | +$3,791 | **+$4,273** | +$482 ✅ | 43.0% | PROFITABLE |
| 10 | 1aC2Fg | +$4,637 | **+$4,578** | -$59 | 43.5% | STABLE |
| 11 | Ab2iXB | +$3,745 | **+$3,960** | +$215 ✅ | 72.7% | PROFITABLE |
| 12 | Bkqxrg | +$1,765 | **+$1,771** | +$6 | 57.9% | STABLE |

**Tier 1 Total Live PnL: +$67,883** (vs +$57,581 yesterday) | **Change: +$10,302**

### 🎯 TIER 2 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|-----|--------|
| 1 | CNDX | +$847 | **+$508** | -$339 ⚠️ | 43.1% | WATCH - WR Drop |
| 2 | 43QmFc | +$114 | **+$895** | +$781 📈 | 62.8% | PROMOTE CANDIDATE |
| 3 | 3wccdTM | +$5,778 | **+$6,266** | +$488 ✅ | 46.9% | PROFITABLE |
| 4 | 9cxLzx | +$4,463 | **+$4,860** | +$397 ✅ | 51.9% | PROFITABLE |
| 5 | FhaYN5 | +$2,084 | **+$3,065** | +$981 📈 | 34.7% | PROMOTE CANDIDATE |
| 6 | DphoNs | +$3,967 | **+$4,329** | +$362 ✅ | 40.1% | PROFITABLE |

**Tier 2 Total Live PnL: +$19,923** (vs +$17,253 yesterday) | **Change: +$2,670**

### 👀 TIER 3 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|--------|
| 1 | S2CR7k | +$116 | **+$970** | +$854 📈 | 41.4% | PROMOTE CANDIDATE |
| 2 | 5kvMnk | +$123 | **+$768** | +$645 📈 | 34.5% | WATCH - WR Low |
| 3 | C2mWdS | +$136 | **+$863** | +$727 📈 | 37.9% | PROMOTE CANDIDATE |

**Tier 3 Total Live PnL: +$2,601** (vs +$375 yesterday) | **Change: +$2,226**

---

## 📈 PnL CHANGE DETECTION (2026-05-15)

### 🚨 ALERTS

| Wallet | Previous | Current | Change | Direction | Action |
|--------|----------|---------|--------|-----------|--------|
| H2KAvWyc | +$27 | +$5,791 | +$5,764 | 📈 UP | **PROMOTE TO TIER 1** |
| Stigman | +$8,382 | +$7,701 | -$681 | 🔻 DOWN | **WATCH - Demotion Risk** |
| S2CR7k | +$116 | +$970 | +$854 | 📈 UP | **PROMOTE TO TIER 2** |
| FhaYN5 | +$2,084 | +$3,065 | +$981 | 📈 UP | **PROMOTE TO TIER 1** |
| 43QmFc | +$114 | +$895 | +$781 | 📈 UP | **PROMOTE TO TIER 1** |

### ⚠️ WATCH LIST

| Wallet | Previous | Current | Change | Direction | Concern |
|--------|----------|---------|--------|-----------|---------|
| 3jSHy | +$6,437 | +$6,225 | -$212 | 🔻 DOWN | Small loss, monitor |
| CNDX | +$847 | +$508 | -$339 | 🔻 DOWN | WR dropped to 43.1% |
| 5kvMnk | +$123 | +$768 | +$645 | 📈 UP | WR still low at 34.5% |

---

## 🔄 LIVE TRACKING PROCESS

### Daily PnL Check (20:00 UTC):
1. Query `gmgn-cli portfolio stats` for all wallets
2. Compare to previous day's PnL
3. Flag wallets with significant changes (±$500)
4. Update tracking file

### Weekly Performance Review (Sundays):
1. Calculate weekly PnL change for all wallets
2. Identify trending up/down
3. Consider tier promotions/demotions
4. Document in weekly report

### Monthly Full Audit:
1. Complete PnL history for all tiers
2. Calculate average WR trends
3. Identify wallets losing edge
4. Update blacklist if needed

---

## 🚨 ALERT CRITERIA

### Promote to Higher Tier:
- PnL increases by >$1,000 in 1 week
- WR improves by >5%
- Consistent daily activity

### Demote to Lower Tier:
- PnL decreases by >$500 in 1 week
- WR drops by >5%
- No activity for 3+ days

### Blacklist:
- PnL turns negative over 2+ weeks
- WR drops below 35%
- Suspicious trading patterns

---

## 📊 PERFORMANCE METRICS

### Overall Portfolio Health:
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total Tracked Wallets | 21 | 20-30 | ✅ Good |
| Tier 1 Wallets | 12 | 8-15 | ✅ Good |
| Avg Tier 1 WR | 54.3% | >50% | ✅ Good |
| Avg Tier 1 PnL | +$5,657 | >$2K | ✅ Good |
| Total Live PnL | +$90,407 | Growing | ✅ Good |

### Risk Indicators:
| Indicator | Value | Threshold | Status |
|-----------|-------|-----------|--------|
| Wallets losing PnL | 2 | <3 | ⚠️ Watch |
| Wallets inactive | 0 | <5 | ✅ Safe |
| Avg WR declining | No | No | ✅ Safe |
| Wallets with WR <40% | 2 | <3 | ⚠️ Watch |

---

## 🎯 NEXT ACTIONS

### Immediate:
- [x] Daily PnL check completed (2026-05-15 20:02 UTC)
- [ ] Review H2KAvWyc for Tier 1 promotion (+$5,764 gain)
- [ ] Review Stigman for potential demotion (-$681 loss, WR 43.1%)
- [ ] Review S2CR7k for Tier 2 promotion (+$854 gain)
- [ ] Review FhaYN5 for Tier 1 promotion (+$981 gain)
- [ ] Review 43QmFc for Tier 1 promotion (+$781 gain)

### This Week:
- [ ] First weekly performance review (Sunday)
- [ ] Check all Tier 1 wallets for consistency
- [ ] Update any tier assignments based on performance

### Ongoing:
- [ ] Daily PnL tracking
- [ ] Weekly performance reviews
- [ ] Monthly full audits
- [ ] Quarterly strategy adjustments

---

## 📋 NOTES

**Last Updated:** 2026-05-15 20:02 UTC
**Next Update:** 2026-05-16 20:00 UTC (daily check)
**Next Review:** 2026-05-18 (weekly)

**Key Insights:**
1. **HUGE GAIN:** H2KAvWyc went from +$27 to +$5,791 (+$5,764) — massive activity detected!
2. **Stigman Alert:** Dropped -$681, WR down to 43.1% — potential demotion candidate
3. **Tier 3 Surge:** All Tier 3 wallets gained significantly (+$645 to +$854 each)
4. **Overall Portfolio:** +$15,198 total gain since yesterday (+26.4% increase)

**All wallets are active** — no inactive wallets detected.

**Recommendation:** Consider promoting H2KAvWyc, FhaYN5, and 43QmFc to Tier 1. Monitor Stigman for demotion if losses continue.
