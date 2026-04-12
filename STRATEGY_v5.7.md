# v5.7 TRADING STRATEGY — COMPLETE REFERENCE
## Wilson's Dip-in-Momentum Scanner
## Last Updated: 2026-04-12 03:21 UTC

---

## 🎯 THE CORE IDEA

**Buy the dip in a momentum breakout.**

Find coins that:
1. Have proven momentum (strong h1 or 24h move)
2. Have pulled back 15-40% from their local peak (dip)
3. Are young (< 3 hours, focus on < 15 min)
4. Ride the recovery to TP targets

**The goal:** Turn 1 SOL → 100 SOL via compounding TP5 winners on pump.fun tokens.

---

## 📊 ENTRY FILTERS

### Mcap
- **MIN:** $4,000
- **MAX:** $75,000
- Fresh tokens start below $4K — that's the entry sweet spot

### Age
- **MAX:** 180 minutes (3 hours)
- **FOCUS:** < 15 minutes (youngest = highest upside)
- Reject if: age > 180 min

### Momentum (h1 / 24h)
- **REQUIRED:** h1 > +50% OR 24h > +50%
- This proves the coin has actual momentum, not just noise
- Reject if: h1 AND 24h both < +50%

### Dip (Pullback from Peak)
- **RANGE:** 15% - 40%
- Dip = (local peak price - current price) / local peak price
- Peak is measured over PEAK_WINDOW (90s for <10min pairs, 180s for older)
- Reject if: dip < 15% (not enough pullback)
- Reject if: dip > 40% (too deep — may be a dump)

### PARABOLIC EXCEPTION
- If h1 > +150% AND age < 10 min AND chg5 > 0:
  → Treat dip as 5% (the "dip" is just a brief pause in an ongoing pump)
  → Still subject to all other filters

### Volume
- **5min volume:** $1,000+ (for coins > 20 min old)
- Younger coins can have lower volume initially
- Reject if: age ≥ 20 min AND 5min vol < $1,000

### Holders
- **MIN:** 15 holders
- Reject if: holders < 15 (bot farm or dead token)

### Top 10 Holder %
- **MAX:** 50%
- Reject if: top 10 holders own > 50% (dumper risk)

### Buy/Sell Ratio
- **MIN:** 1.5 (for raydium pairs)
- Pump.fun BS = 0 is OK (not applicable)
- Reject if: BS ratio < 1.5 on raydium

### Anti-Momentum (Chasing Filter)
- If 5min change > +15% AND h1 change < 15%: REJECT (chasing)
- **EXCEPTION:** If h1 > +100% AND mcap < $60K AND holders growing → allow chg5 up to +50%

### Falling Knife
- Track price across 3 consecutive scans
- If price dropped all 3 times → REJECT
- Protects against continuous dumps

### Blacklist
- **PERMANENT:** Any token that has been bought is NEVER bought again
- Even after stop loss — if it's in the trade file as closed, it's blacklisted

---

## 📁 DATA SOURCES

### Primary: DexScreener
- Token list: `https://api.dexscreener.com/token-profiles/latest/v1` (top 50)
- Token data: `https://api.dexscreener.com/latest/dex/tokens/{addr}`
- Used for: mcap, volume, price changes, liquidity, market cap

### Backup: GMGN
- Called when DexScreener shows 0 holders OR top10 OR mcap > $50K
- Used for: holder_count, top_10_holder_rate, liquidity
- GMGN returns STRINGS — must cast to float/int

---

## 💰 POSITION MANAGEMENT

### Position Size
- **0.1 SOL** per trade
- Never more than this per position

### Max Open Positions
- **5 positions** at a time
- Prevents over-diversification

### Re-Entry Lockout
- After closing a position (any reason), cannot re-buy for **30 minutes**
- Exception: if BS ≥ 3.0 AND chg60 ≥ +50%, can re-enter early

---

## 📈 EXIT PLAN (TP Targets)

### TP1: +35% → HOLD (don't sell)
- After hitting +35%, **hold and trail**
- Activate trailing stop: sell if 20% drop from peak

### TP2: +100% → Sell 40% of position
- Takes profit, leaves 60% running
- New peak = price at TP2 hit
- Trailing stop on remaining: 25%

### TP3: +200% → Sell 30% of remaining
- Takes more profit, leaves 30% running
- New peak = price at TP3 hit
- Trailing stop on remaining: 20%

### TP4: +500% → Sell 50% of remaining
- Takes more profit, leaves 15% running
- New peak = price at TP4 hit
- Trailing stop on remaining: 15%

### TP5/FINAL: +1000% → Sell remaining 15%
- Last exit — full position closed
- Celebrate 🎉

### STOP LOSS: -20%
- If price drops 20% from entry → sell everything, immediately
- This is non-negotiable

### TRAILING STOP DETAIL
- Trailing stop sells ONLY if price drops X% from the PEAK since entry
- If price goes up 50%, peak = entry + 50%
- If price then drops 20% from peak → STOP triggered
- Trailing stops lock in profits while letting winners run

### Low Volume Exit
- If 5min volume < $600 → exit immediately
- Low volume = no buyers = likely to dump

---

## 🔄 SCANNING SCHEDULE

### whale_momentum_scanner.py
- Runs every **15 seconds**
- Scans top 50 tokens from DexScreener
- Checks ALL entry filters
- Logs candidates that nearly pass

### auto_scanner.py
- Backup scanner, runs independently
- Also follows same v5.7 filters

### position_monitor.py
- Runs every **5 seconds**
- Checks all open positions against TP/stop targets
- Executes sells automatically
- Sends Telegram alerts on every action

### alert_sender.py
- Runs every **30 seconds**
- Sends Telegram alerts for all trades

### scan_report.sh
- Runs every **10 minutes**
- Does independent live scan
- Reports to Chris via Telegram

---

## 🔧 SYSTEM HEALTH

- Check systems: `ps aux | grep -E "whale_momentum|position_monitor|alert_sender|auto_scanner" | grep -v grep | wc -l`
- Expected: 4 processes running
- Balance check: `cd /root/Dex-trading-bot && python3 -c "from alert_sender import get_status; print(get_status())"`

---

## 📋 TRADING LOGIC FLOW (Priority Order)

```
1. Fetch 50 tokens from DexScreener
2. Skip if: token in permanent blacklist (_sold_tokens set)
3. Skip if: already have 5 open positions
4. For each token:
   a. Get DexScreener data (mcap, vol, chg5, chg60, chg24)
   b. If mcap < $4K or > $75K → REJECT
   c. If age > 180 min → REJECT
   d. If holders < 15 (DS) → try GMGN, if < 15 → REJECT
   e. If top10 > 50% → REJECT
   f. If h1 < +50% AND 24h < +50% → REJECT (no momentum)
   g. If chg5 < 0 → REJECT (falling knife early)
   h. Calculate dip from peak tracking
   i. If dip < 15%:
      - Parabolic exception: if h1 > +150% AND age < 10min AND chg5 > 0 → continue
      - Else → REJECT
   j. If dip > 40% → REJECT (too deep)
   k. If age ≥ 20min AND 5min vol < $1000 → REJECT
   l. If raydium AND BS < 0.9 → REJECT
   m. Anti-momentum: if chg5 > +15% AND chg60 < +15% → REJECT
   n. If falling knife (3 consecutive drops) → REJECT
   o. If all pass → BUY
```

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `/root/Dex-trading-bot/whale_momentum_scanner.py` | Main scanner |
| `/root/Dex-trading-bot/auto_scanner.py` | Backup scanner |
| `/root/Dex-trading-bot/position_monitor.py` | TP/Stop executor |
| `/root/Dex-trading-bot/alert_sender.py` | Telegram alerts |
| `/root/Dex-trading-bot/trading_constants.py` | All constants |
| `/root/Dex-trading-bot/trades/sim_trades.jsonl` | Trade history |
| `/root/Dex-trading-bot/whales/whale_db.json` | Whale database |

---

## 🐋 WHALE DATABASE

- 10 whales tracked
- Only whales with winrate ≥ 50% AND buy_count ≥ 3 are used
- Whales are monitored for momentum signals
- 189 previously sold tokens blacklisted

---

## 🔒 SAFETY RULES

1. **Never re-buy a closed token** — permanent blacklist
2. **Stop loss is -20%** — non-negotiable
3. **Max 5 open positions** — prevents overtrading
4. **30 min re-entry lockout** — prevents revenge trading
5. **Low vol exit** — protects against illiquidity
6. **Anti-momentum** — prevents buying the top

---

## 📊 v5.7 vs v5.5 SETTINGS COMPARISON

| Setting | v5.5 | v5.7 |
|---------|------|------|
| MIN_MCAP | $8,500 | $4,000 |
| MAX_MCAP | $75,000 | $75,000 |
| MAX_AGE | 60 min | 180 min |
| PEAK_WINDOW | 90s/180s | 90s/180s |
| DIP_MIN | 15% | 15% |
| DIP_MAX | 35% | 40% |
| STOP_LOSS | 20% | 20% |
| TP1 | +35% HOLD | +35% HOLD |
| TP2 | +100% | +100% |
| TP3 | +200% | +200% |
| TP4 | +500% | +500% |
| TP5 | +1000% | +1000% |
| Parabolic h1 | N/A | +150% (< 10 min) |

---

## 🚀 GOAL

**Turn 1.0 SOL → 100 SOL**

- One TP5 winner (+1000%) turns 0.1 SOL → 1.0 SOL
- Compound that and you get to 100 SOL
- Every trade is 0.1 SOL
- Max 5 open positions at a time

---

_v5.7 Strategy Document — Wilson Bot_