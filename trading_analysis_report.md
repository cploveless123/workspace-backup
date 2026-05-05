# 📊 Trading Analysis Report — sim_trades.jsonl
**708 completed trades | 208W / 500L | WR: 29.4%**

---

## 🏆 TOP 3 WINNING PATTERNS

### 1. **A Grade + Creator SOLD** → 49.2% WR, +33% avg PnL (n=65)
- **Counter-intuitive**: Tokens where creator already sold outperform
- Likely indicates fair launch / no rug risk vs. creator waiting to dump
- Signal score 9-10.5 is the sweet spot (51.9% WR)

### 2. **Smart Degen Present** → 49.1% WR, +56% avg PnL (n=175)
- Even 1 smart degen wallet = 55.1% WR
- 0 smart degens = 22.9% WR
- **Strongest single predictor after h1**

### 3. **High Volume + High H1** → 41.3% WR, +37% avg PnL (n=286)
- Volume >$10K + h1 >200%
- Real momentum with real money flowing

---

## 💀 TOP 3 LOSING PATTERNS (AVOID)

### 1. **Low H1 < 50%** → 1.8% WR (n=222)
- The #1 killer. No momentum = death.
- Same group has low volume <3000 (also 1.8% WR)

### 2. **Very Young <60s + Low Bundler <0.30** → 8.3% WR (n=265)
- Too fresh + no bundling = pump & dump bait
- Wait for tokens to prove themselves (120s+)

### 3. **Low Signal Score < 7** → 13.4% WR (n=298)
- Nearly half the trades are low-quality signals
- chg_ratio < 0.05 (flat momentum) = 12.1% WR

---

## 🔧 RECOMMENDED FILTER CHANGES

| Current | Recommended | Expected Impact |
|---------|-------------|-----------------|
| h1 > 0 | **h1 >= 100** | Eliminates 222 losers, keeps 60.5% WR zone |
| chg5 > 0 | **chg5 >= 50** | Eliminates 249 losers, 48-58% WR zone |
| chg1 > 0 | **chg1 >= 10** | Eliminates 264 losers, 43% WR zone |
| age any | **age >= 120s** | Avoids 256 pump dumps, 41-63% WR |
| holders any | **holders >= 50** | Eliminates 235 losers, 43-50% WR |
| volume any | **volume >= 6000** | Eliminates 222 losers, 40% WR |
| signal any | **signal >= 7** | Eliminates 239 losers, 42-52% WR |
| bundler any | **bundler >= 0.15** | Eliminates 270 losers, 43-47% WR |

### **COMBINED STRICT FILTER** (all of above):
- Estimated trades: ~150-200 (down from 708)
- **Projected WR: 45-55%** (vs current 29.4%)
- **Projected avg PnL: +35-50%**

---

## 🤯 SURPRISING INSIGHTS

1. **Creator SOLD is GOOD** (46.6% WR vs 22.4%)
   - Your current code treats creator_close as danger
   - **FLIP THIS**: Creator sold = fair launch signal
   - Creator holding = waiting to rug

2. **Older is Better** (600s+ = 62.8% WR)
   - Your 15s scanner buys too fast
   - Tokens that survive 10+ minutes are more legit
   - Consider minimum age filter 120s

3. **Bundler Rate Sweet Spot** (0.15-0.30 = 47% WR)
   - Zero bundling (<0.15) = 8.2% WR (worse!)
   - Some bundling = organic community forming
   - Too much (>0.45) = 31.6% WR

4. **Signal Score Inverted U-Curve**
   - 9-10.5 = 51.9% WR (best)
   - >10.5 = 34.1% WR (overfit / too strict)
   - Don't chase perfect scores

5. **Time of Day Matters**
   - 16-20 UTC: 45.6% WR
   - 8-16 UTC: ~18% WR (avoid midday)
   - Consider trading window filter

6. **Top Performers vs Bottom Look Similar**
   - Same avg mcap (~11K), h1 (~300), chg5 (~250)
   - Difference: **creator_sold 43% vs 34%**, **smart_degen presence**
   - The edge is subtle — it's WHO is trading, not just the numbers

---

## 📈 CORRELATION RANKING (with PnL%)

| Factor | Correlation |
|--------|-------------|
| h1 | **+0.140** |
| liquidity | +0.132 |
| age_sec | +0.112 |
| chg5 | +0.110 |
| mcap | +0.103 |
| volume | +0.087 |
| signal_score | +0.068 |
| smart_degen | +0.057 |
| bundler_rate | +0.056 |
| holders | +0.037 |
| chg_ratio | +0.027 |
| chg1 | **-0.018** (slight negative!) |

**Key insight**: chg1 has slight NEGATIVE correlation. Recent spike (high chg1) often means buying the local top. chg5 (5min trend) is more predictive.

---

## 🎯 ACTION ITEMS

1. **FLIP creator_close logic** → treat as GREEN light, not red
2. **Add minimum h1 >= 100** filter
3. **Add minimum chg5 >= 50** filter  
4. **Add minimum age >= 120s** filter
5. **Add minimum holders >= 50** filter
6. **Add minimum volume >= 6000** filter
7. **Add minimum bundler >= 0.15** filter
8. **Consider time window**: trade 16-20 UTC and 0-4 UTC only
9. **Weight smart_degen heavily** in signal score
10. **Don't over-optimize signal score** — 9-10.5 is the sweet spot

---
*Analysis of 708 completed trades from sim_trades.jsonl*
