# SMART WALLET PnL TRACKING SYSTEM
# Updated: 2026-05-16 20:28 UTC
# Purpose: Track live PnL and performance of all tracked wallets

## 📊 CURRENT WALLET PERFORMANCE (Live Data)

### 🏆 TIER 1 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|-----|--------|
| 1 | Cowboy🔶BNB | +$15,312 | **+$19,787** | +$4,475 ✅ | 53.8% | PROFITABLE |
| 2 | 65kmABTf | +$5,138 | **+$1,996** | -$3,142 🚨 | 55.7% | ALERT - Demotion Risk |
| 3 | 3jSHy | +$6,225 | **+$557** | -$5,668 🚨 | 55.1% | ALERT - Demotion Risk |
| 4 | H2KAvWyc | +$5,791 | **+$5,518** | -$273 ⚠️ | 46.9% | WATCH |
| 5 | Stigman | +$7,701 | **+$5,467** | -$2,234 🚨 | 42.0% | ALERT - Demotion Risk |
| 6 | 7BWy2m | +$4,886 | **+$4,156** | -$730 ⚠️ | 67.3% | WATCH |
| 7 | Meskxy | +$3,249 | **+$3,262** | +$13 | 71.1% | STABLE |
| 8 | FdwVhb | +$4,989 | **+$5,679** | +$690 ✅ | 46.1% | PROFITABLE |
| 9 | tCPHCK | +$4,273 | **+$5,048** | +$775 ✅ | 44.6% | PROFITABLE |
| 10 | 1aC2Fg | +$4,578 | **+$5,235** | +$657 ✅ | 44.1% | PROFITABLE |
| 11 | Ab2iXB | +$3,960 | **+$3,687** | -$273 ⚠️ | 66.7% | WATCH |
| 12 | Bkqxrg | +$1,771 | **+$1,323** | -$448 ⚠️ | 52.6% | WATCH |

**Tier 1 Total Live PnL: +$60,168** (vs +$67,883 yesterday) | **Change: -$7,715**

### 🎯 TIER 2 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|-----|--------|
| 1 | CNDX | +$508 | **+$1,356** | +$848 📈 | 42.7% | PROMOTE CANDIDATE |
| 2 | 43QmFc | +$895 | **+$424** | -$471 ⚠️ | 61.7% | WATCH |
| 3 | 3wccdTM | +$6,266 | **+$5,837** | -$429 ⚠️ | 47.1% | WATCH |
| 4 | 9cxLzx | +$4,860 | **+$5,239** | +$379 ✅ | 51.4% | PROFITABLE |
| 5 | FhaYN5 | +$3,065 | **+$2,798** | -$267 ⚠️ | 33.3% | WATCH - WR Low |
| 6 | DphoNs | +$4,329 | **+$3,970** | -$359 ⚠️ | 40.9% | WATCH |

**Tier 2 Total Live PnL: +$19,624** (vs +$19,923 yesterday) | **Change: -$299**

### 👀 TIER 3 WALLETS — LIVE PnL

| # | Wallet | Initial PnL | Live PnL | Change | WR | Status |
|---|--------|-------------|----------|--------|--------|
| 1 | S2CR7k | +$970 | **+$787** | -$183 ⚠️ | 44.4% | WATCH |
| 2 | 5kvMnk | +$768 | **+$460** | -$308 ⚠️ | 37.0% | WATCH - WR Low |
| 3 | C2mWdS | +$863 | **+$651** | -$212 ⚠️ | 40.7% | WATCH |

**Tier 3 Total Live PnL: +$1,898** (vs +$2,601 yesterday) | **Change: -$703**

---

## 📈 PnL CHANGE DETECTION (2026-05-16)

### 🚨 ALERTS (PnL Drop > $500)

| Wallet | Previous | Current | Change | Direction | Action |
|--------|----------|---------|--------|-----------|--------|
| 65kmABTf | +$5,138 | +$1,996 | -$3,142 | 🔻 DOWN | **DEMOTE TO TIER 2** |
| 3jSHy | +$6,225 | +$557 | -$5,668 | 🔻 DOWN | **DEMOTE TO TIER 2** |
| Stigman | +$7,701 | +$5,467 | -$2,234 | 🔻 DOWN | **DEMOTE TO TIER 2** |
| 7BWy2m | +$4,886 | +$4,156 | -$730 | 🔻 DOWN | **WATCH - Monitor** |
| Bkqxrg | +$1,771 | +$1,323 | -$448 | 🔻 DOWN | **WATCH - Near threshold** |

### 📈 PROMOTE CANDIDATES (PnL Gain > $500)

| Wallet | Previous | Current | Change | Direction | Action |
|--------|----------|---------|--------|-----------|--------|
| Cowboy🔶BNB | +$15,312 | +$19,787 | +$4,475 | 📈 UP | **TOP PERFORMER** |
| FdwVhb | +$4,989 | +$5,679 | +$690 | 📈 UP | **STABLE PROFITABLE** |
| tCPHCK | +$4,273 | +$5,048 | +$775 | 📈 UP | **STABLE PROFITABLE** |
| 1aC2Fg | +$4,578 | +$5,235 | +$657 | 📈 UP | **STABLE PROFITABLE** |
| CNDX | +$508 | +$1,356 | +$848 | 📈 UP | **PROMOTE TO TIER 1** |

### ⚠️ WR DROPS > 5%

| Wallet | Previous WR | Current WR | Change | Status |
|--------|-------------|------------|--------|--------|
| FhaYN5 | 34.7% | 33.3% | -1.4% | Still low |
| 5kvMnk | 34.5% | 37.0% | +2.5% | Improving |

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
| Avg Tier 1 WR | 52.6% | >50% | ✅ Good |
| Avg Tier 1 PnL | +$5,014 | >$2K | ✅ Good |
| Total Live PnL | +$81,690 | Growing | ⚠️ Declined |

### Risk Indicators:
| Indicator | Value | Threshold | Status |
|-----------|-------|-----------|--------|
| Wallets losing PnL | 5 | <3 | 🚨 HIGH |
| Wallets inactive | 0 | <5 | ✅ Safe |
| Avg WR declining | Yes | No | 🚨 HIGH |
| Wallets with WR <40% | 2 | <3 | ⚠️ Watch |

---

## 🎯 NEXT ACTIONS

### Immediate:
- [x] Daily PnL check completed (2026-05-16 20:28 UTC)
- [ ] **DEMOTE** 65kmABTf to Tier 2 (-$3,142 loss)
- [ ] **DEMOTE** 3jSHy to Tier 2 (-$5,668 loss)
- [ ] **DEMOTE** Stigman to Tier 2 (-$2,234 loss)
- [ ] **PROMOTE** CNDX to Tier 1 (+$848 gain)
- [ ] Review all Tier 1 wallets for consistency

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

**Last Updated:** 2026-05-16 20:28 UTC
**Next Update:** 2026-05-17 20:00 UTC (daily check)
**Next Review:** 2026-05-18 (weekly)

**Key Insights:**
1. **MAJOR DRAWDOWN:** Total portfolio dropped -$8,717 (-9.6%) since yesterday
2. **Tier 1 Hit Hard:** 5 of 12 Tier 1 wallets lost PnL, total -$7,715
3. **65kmABTf CRASH:** Dropped from +$5,138 to +$1,996 (-61% PnL loss)
4. **3jSHy CRASH:** Dropped from +$6,225 to +$557 (-91% PnL loss)
5. **Cowboy🔶BNB:** Only major gainer, +$4,475 — now top performer at +$19,787
6. **All wallets active** — no inactive wallets detected.

**Recommendation:** 
- **URGENT:** Demote 65kmABTf, 3jSHy, and Stigman to Tier 2 immediately
- **PROMOTE:** CNDX to Tier 1 (+$848 gain, active trading)
- **MONITOR:** Market-wide drawdown affecting most wallets
- **HOLD:** Cowboy🔶BNB as anchor performer

**Risk Level:** 🚨 HIGH — 5 wallets with significant PnL drops, market-wide decline
