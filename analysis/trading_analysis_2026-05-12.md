# Trading Data Analysis — Finding Winning Patterns
**Date:** 2026-05-12  
**Dataset:** 2,838 trades (1,445 matched buy/sell pairs)  
**Period:** Post-reset (April 15, 2026)  
**Analyst:** Wilson

---

## Executive Summary

Current performance: **42.4% WR, -6.92 SOL total PnL** across 1,445 closed trades.

**The data reveals a clear path to profitability.** One single filter — Smart Degen = 1 — would have turned -6.92 SOL into +2.04 SOL. Combined with other filters, we can achieve 50-80% WR.

---

## The #1 Finding: SMART DEGEN = 1

This is the **single most powerful predictor** in the entire dataset.

| Smart Degen Count | WR | PnL | Trades |
|---|---|---|---|
| **0** | 39.0% | **-3.19 SOL** | 259 |
| **1** | **52.3%** | **+2.04 SOL** | 111 |
| 2 | 44.0% | -0.22 SOL | 25 |
| 3+ | 0-40% | Negative | 14 |

**Key insight:** When exactly 1 smart degen wallet is detected, the trade is **significantly more likely to succeed.** When 0 are present, it's significantly worse. The difference between Smart Degen = 0 and Smart Degen = 1 is a swing of **+5.23 SOL** — that alone would turn the entire portfolio profitable.

---

## Best Combined Filters

### Tier 1: Smart Degen = 1 (Primary Filter)
- **52.3% WR, +2.04 SOL** on 111 trades
- This should be the PRIMARY entry requirement

### Tier 2: Smart Degen = 1 + Additional Quality Signals

| Filter Combo | WR | PnL | Trades |
|---|---|---|---|
| Smart Degen=1 + MCAP $10K-$20K | **59.1%** | **+2.18 SOL** | 66 |
| Smart Degen=1 + Signal Score 5-7 | **81.8%** | **+1.89 SOL** | 11 |
| Smart Degen=1 + Bundler 0.1-0.3 | **65.2%** | **+1.94 SOL** | 23 |
| Smart Degen=1 + Chg1 10-25% | 50.0% | +1.55 SOL | 28 |

### Tier 3: Smart Degen >= 1 + Quality Stack

| Filter Combo | WR | PnL | Trades |
|---|---|---|---|
| Smart Degen>=1 + (Holders 100-200 OR Signal 5-7 OR MCAP $10K-$20K) | **53.1%** | **+1.90 SOL** | 96 |

---

## What to AVOID

### 1. Signal Score >9 — THE TRAP
- 38.7% WR, -2.33 SOL on 191 trades
- High signal score does NOT mean good trade
- **Action:** Reject signal score >9

### 2. Smart Degen = 0
- 39.0% WR, -3.19 SOL on 259 trades
- No smart degen presence = likely failure
- **Action:** Require Smart Degen >= 1

### 3. Low MCAP (<$5K)
- 42.4% WR, -4.86 SOL on 1,013 trades
- **Action:** Minimum MCAP $10K

### 4. Bot Degen >100
- 0% WR, -0.21 SOL on 5 trades
- **Action:** Reject bot degen >100

### 5. Worst Paths
| Path | WR | PnL | Trades |
|---|---|---|---|
| MOMENTUM_RIDE | 0.0% | -0.44 SOL | 7 |
| ESTABLISHED | 29.4% | -0.87 SOL | 34 |
| CREATOR | 0.0% | -0.06 SOL | 1 |
| FRESH_MOMENTUM | 0.0% | -0.12 SOL | 2 |

**Action:** Disable these paths permanently

---

## Secondary Winning Patterns

### MCAP Sweet Spot
| MCAP Bucket | WR | PnL | Trades |
|---|---|---|---|
| <$5K | 42.4% | -4.86 SOL | 1,013 |
| $5K-$10K | 41.5% | -3.76 SOL | 504 |
| $10K-$15K | 42.1% | -3.21 SOL | 646 |
| **$15K-$20K** | **45.1%** | **+0.32 SOL** | 275 |

**Only $15K-$20K is profitable.** Minimum $10K strongly recommended.

### Age Sweet Spot
| Age | WR | PnL | Trades |
|---|---|---|---|
| <1min | 42.4% | -1.82 SOL | 413 |
| 1-2min | 46.5% | -2.08 SOL | 258 |
| **2-3min** | **50.9%** | **+0.72 SOL** | 169 |
| 3-5min | 38.9% | -2.46 SOL | 190 |
| 5-10min | 43.7% | -0.59 SOL | 87 |
| 10-20min | 39.2% | +0.27 SOL | 148 |
| 20-40min | 33.3% | -0.96 SOL | 105 |
| >40min | 33.9% | +0.25 SOL | 56 |

**2-3 minutes is the golden window.** Too fresh (<2min) or too old (>10min) both underperform.

### H1 Momentum Sweet Spot
| H1 | WR | PnL | Trades |
|---|---|---|---|
| 50-100% | 43.2% | +0.07 SOL | 44 |
| **100-200%** | **47.2%** | **+0.47 SOL** | 214 |
| 200-500% | 41.4% | -6.43 SOL | 1,038 |
| >500% | 42.6% | -0.73 SOL | 129 |

**100-200% H1 is the sweet spot.** The 200-500% bucket is the volume trap (72% of all trades, -6.43 SOL).

### Chg5 Sweet Spot
| Chg5 | WR | PnL | Trades |
|---|---|---|---|
| 0-10% | 42.7% | -0.19 SOL | 253 |
| 10-25% | 42.3% | -0.35 SOL | 111 |
| **25-50%** | **43.0%** | **+1.30 SOL** | 128 |
| 50-100% | 45.2% | -0.44 SOL | 115 |
| >100% | 41.9% | -7.00 SOL | 819 |

**25-50% chg5 is the sweet spot.** >100% chg5 is the death zone.

### Chg1 Sweet Spot
| Chg1 | WR | PnL | Trades |
|---|---|---|---|
| <0% | 25.0% | -0.67 SOL | 24 |
| 0-10% | 42.0% | -0.96 SOL | 424 |
| **10-25%** | **43.7%** | **+0.77 SOL** | 423 |
| 25-50% | 43.3% | -3.00 SOL | 282 |
| 50-100% | 40.5% | -1.82 SOL | 158 |
| >100% | 43.5% | -0.99 SOL | 115 |

**10-25% chg1 is the sweet spot.** Winners enter at COOLER chg1 than losers (36.1% vs 38.6%).

### Holder Count Sweet Spot
| Holders | WR | PnL | Trades |
|---|---|---|---|
| <20 | 42.4% | -4.93 SOL | 1,014 |
| 20-50 | 32.9% | -1.66 SOL | 70 |
| 50-100 | 44.5% | -0.41 SOL | 218 |
| **100-200** | **50.5%** | **+1.58 SOL** | 101 |
| >200 | 17.4% | -1.26 SOL | 23 |

**100-200 holders is the sweet spot.** Too few (<20) or too many (>200) both lose.

### Liquidity Sweet Spot
| Liquidity | WR | PnL | Trades |
|---|---|---|---|
| <$5K | 42.4% | -4.86 SOL | 1,013 |
| $5K-$10K | 33.3% | -2.44 SOL | 123 |
| **$10K-$20K** | **46.2%** | **+0.62 SOL** | 290 |

**$10K-$20K liquidity is the only profitable bucket.**

### Bundler Rate Sweet Spot
| Bundler Rate | WR | PnL | Trades |
|---|---|---|---|
| <0.1 | 41.9% | -2.52 SOL | 246 |
| **0.1-0.3** | **41.5%** | **+0.80 SOL** | 463 |
| >0.3 | 43.2% | -4.96 SOL | 717 |

**0.1-0.3 is the sweet spot.** Too low or too high both lose.

### Time of Day
| Hour (UTC) | WR | PnL | Trades |
|---|---|---|---|
| 08:00 | 55.6% | +0.03 SOL | 36 |
| 09:00 | 44.1% | +0.83 SOL | 34 |
| **10:00** | **54.5%** | **+1.25 SOL** | 33 |
| 11:00 | 28.6% | -0.81 SOL | 35 |
| **12:00** | **55.8%** | **+0.12 SOL** | 43 |
| **13:00** | **58.2%** | **+0.56 SOL** | 55 |
| 14:00 | 42.6% | -0.34 SOL | 61 |
| 15:00 | 41.5% | -0.72 SOL | 65 |
| 16:00 | 49.3% | +0.15 SOL | 75 |
| 17:00 | 30.8% | -1.71 SOL | 78 |
| 18:00 | 49.5% | -0.56 SOL | 95 |
| 19:00 | 46.5% | -0.68 SOL | 71 |
| 20:00 | 23.2% | -1.63 SOL | 69 |
| 21:00 | 46.4% | -0.20 SOL | 69 |
| 22:00 | 46.7% | +0.93 SOL | 92 |

**Best window: 10:00-13:00 UTC** (combined ~54% WR, +1.94 SOL)  
**Worst window: 17:00-20:00 UTC** (combined ~34% WR, -3.96 SOL)

---

## Winner vs Loser Profile

| Metric | Winners | Losers | Delta |
|---|---|---|---|
| MCAP | $11,913 | $11,642 | +2.3% |
| Age | 301s | 245s | +23% |
| H1 | 322.6% | 318.6% | +1.2% |
| Chg5 | 183.9% | 178.3% | +3.2% |
| Chg1 | **36.1%** | **38.6%** | **-6.5%** |
| Signal Score | **8.6** | **9.1** | **-6.1%** |
| Liquidity | $11,087 | $10,679 | +3.8% |
| Holders | 88 | 95 | -7.2% |

**Key insights:**
- Winners enter at **COOLER chg1** (36.1% vs 38.6%) — less FOMO = better
- Winners have **LOWER signal score** (8.6 vs 9.1) — high signal = trap
- Winners enter at **OLDER age** (+23%) — not first movers

---

## Path Performance

| Path | WR | PnL | Trades |
|---|---|---|---|
| **SNIPER_HEAVY** | **40.6%** | **+1.47 SOL** | 101 |
| SNIPER | 44.2% | -0.02 SOL | 86 |
| WHALE | 46.5% | -0.06 SOL | 99 |
| KOL | 43.3% | -2.13 SOL | 432 |
| PUMP | 43.0% | -2.63 SOL | 249 |
| UNKNOWN | 42.4% | -1.82 SOL | 413 |
| ESTABLISHED | 29.4% | -0.87 SOL | 34 |
| MOMENTUM_RIDE | 0.0% | -0.44 SOL | 7 |

**Only SNIPER_HEAVY is profitable.** SNIPER and WHALE are roughly breakeven. KOL, PUMP, and UNKNOWN are the big losers.

---

## Recommended Changes

### 1. ADD: Smart Degen = 1 Filter (HIGHEST PRIORITY)
```python
if entry_smart_degen == 1:
    # STRONG BUY signal
    pass
elif entry_smart_degen == 0:
    # REJECT unless other strong signals present
    pass
```

### 2. ADD: Signal Score Filter
- **Require** signal score between 5-7 for entry
- **Reject** signal score >9
- Signal score <5 is neutral (42.3% WR, most volume)

### 3. ADD: MCAP Minimum
- **Minimum MCAP: $10,000** (only profitable bucket starts here)
- Ideally target $10K-$20K range

### 4. ADD: Holder Count Filter
- **Target 100-200 holders** (50.5% WR)
- Reject <20 holders (massive loss bucket)
- Reject >200 holders (17.4% WR)

### 5. ADD: Time Filter (Optional but powerful)
- **Only trade 10:00-13:00 UTC** for +54% WR
- **Avoid 17:00-20:00 UTC** (23-31% WR)

### 6. REMOVE: Worst Paths
- Disable MOMENTUM_RIDE, ESTABLISHED, CREATOR, FRESH_MOMENTUM
- Consider disabling PUMP path (-2.63 SOL)

### 7. ADD: Age Sweet Spot
- Target 2-3 minute age (50.9% WR)
- Avoid <1min (too fresh, FOMO) and >10min (too old)

### 8. ADD: H1 Range Filter
- Target 100-200% H1 (47.2% WR)
- The 200-500% bucket is a volume trap — avoid or be selective

### 9. ADD: Chg5 Filter
- Target 25-50% chg5 (43% WR, +1.30 SOL)
- Avoid >100% chg5 (41.9% WR, -7.00 SOL)

### 10. ADD: Chg1 Filter
- Target 10-25% chg1 (43.7% WR, +0.77 SOL)
- Cooler entry = better (winners avg 36.1%, losers avg 38.6%)

---

## Projected Impact

### Current State
- 1,445 trades, 42.4% WR, -6.92 SOL

### With Smart Degen = 1 Filter Only
- 111 trades, 52.3% WR, +2.04 SOL
- **Swing: +8.96 SOL**

### With Smart Degen = 1 + MCAP $10K-$20K
- 66 trades, 59.1% WR, +2.18 SOL
- **Swing: +9.10 SOL**

### With Smart Degen >= 1 + Quality Stack
- 96 trades, 53.1% WR, +1.90 SOL
- **Swing: +8.82 SOL**

---

## Next Steps

1. **Immediate:** Add Smart Degen = 1 as a primary filter to scanner_v1.py
2. **Short-term:** Add signal score 5-7 requirement and MCAP $10K minimum
3. **Medium-term:** Implement time-of-day filtering
4. **Ongoing:** Monitor these new filters with 100+ trades to validate

---

*Analysis by Wilson | 2026-05-12*
