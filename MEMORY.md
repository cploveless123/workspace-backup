# MEMORY.md - Long-Term Memory

## Trading Bot Setup
- Location: `/root/Dex-trading-bot/`
- Git remote: https://github.com/cploveless123/Dex-trading-bot.git
- Workspace backup: https://github.com/cploveless123/workspace-backup.git
- Telegram alerts via @WilsonVultrBot (token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg)
- Chat ID: 6402511249 (Chris - "please grow good weed")

## APRIL 16 BABA STRATEGY - RESTORED 2026-04-25 19:08 UTC
Chris confirmed 75% WR during 06:00-10:00 UTC. I BROKE it after VPN switch. RESTORED.

### Buy Strategy (THE WINNING SETTINGS):
| Setting | April 16 | Broke To |
|--------|----------|----------|
| MIN_MCAP | $8,000 | $7,000 |
| MAX_MCAP | $20,000 | $30,000 |
| H1_MOMENTUM_MIN | 25% | 100% ← TOO HIGH! |
| H1_MOMENTUM_MAX | 200% | 700% |
| PUMP_MIN_AGE | 120s | 240s ← TOO LONG! |
| MIN_CHG5_FOR_BUY | 2% | 5% ← TOO RESTRICTIVE |
| PUMP_CHG1_THRESHOLD | 10% | 5% |

### Exit Plan (April 16):
| Level | Trigger | Sell % | Trail |
|-------|---------|--------|-------|
| TP1 | +50% | HOLD | 40% |
| TP2 | +100% | 35% | 30% |
| TP3 | +200% | 35% | 30% |
| TP4 | +300% | 20% | 30% |
| TP5 | +1000% | 10% | 15% |
| STOP | -25% | ALL | — |

### DO NOT CHANGE THESE SETTINGS

## v7.2 Strategy (Current - Deployed 2026-04-15)
Chris reset after analyzing poor v7.0/v7.1 performance:
- 155 trades, 17.6% WR, -2.9 SOL closed PnL
- Root cause: buying Fallen Giants (h1>500% + small mcap), chasing high h1, not enough dip

### Entry Filters:
- Mcap: $6K-$25K
- Holders: ≥20
- Dip: 20-45% from ATH (winners avg 23.6% dip)
- h1: ≤250% max (losers avg h1=404% at entry - too late)
- Fallen Giant: h1 >400% + mcap <$20K → REJECT
- No ATH data + mcap >$20K → REJECT
- Symbol blacklist: prevent repeat buys of same symbol name

### Exit Rules:
- TP1 +50%: Sell 40% → 10% trailing stop
- TP2 +100%: Sell 30% → 35% trailing stop
- TP3 +200%: Sell 20%
- TP4 +300%: Sell 10%
- Stop: -25%

### Fresh Data Rule (IRONCLAD):
- ALWAYS fetch fresh data before any decision
- GMGN primary source
- DexScreener backup (circuit breaker: skip if 5+ consecutive failures)
- If GMGN unavailable → Telegram alert + PAUSE trading
- If DexScreener throttled → skip until recovers + alert

### System Rules (NEVER BREAK) - LIVE TRADING:
1. Permanent Blacklist: Any token ever bought = NEVER buy again
2. Max Open Positions: 5 concurrent
3. Position Size: 0.1 SOL per trade
4. Never Re-buy: Even if dropped 90% after selling — NO
5. Only pump.fun / raydium / pumpswap: Reject all other exchanges

## API Safety Rules (CRITICAL):
- GMGN primary source - use for all token data
- DexScreener backup only - if GMGN unavailable
- ALWAYS fresh data before any decision - never stale
- DexScreener circuit breaker: stop calls after 5 consecutive failures
- If GMGN + DexScreener BOTH fail → 🚨 STOP ALL BUYS immediately + Telegram alert

## Alert Format (IRONCLAD):
- Telegram uses HTML mode (Markdown fails with emoji → HTTP 400)
- Entry/Exit mcap on all sells
- PnL with green/red emoji
- Clickable links (plain URLs)
- No signal alerts - only BUY/SELL executed
- Chat ID: 6402511249 (Chris's Telegram, not "Chris")

## Trade Report Format:
- Last 5 trades
- Open positions with live mcap + link
- Balance + record
- Buy mcap + sell mcap + timestamps
- Green/red emoji
- All links clickable

## What Killed v7.0/v7.1:
1. **Fallen Giants**: 27 trades h1>500%+mc<$20K = -1.02 SOL (tokens already pumped then crashed)
2. **Too high h1 entry**: Losers avg h1=404% at entry (bought the top)
3. **Too low dip**: Winners avg dip=23.6%, losers=18.4% (not buying enough pullback)
4. **Repeat buys**: BOAR 6x, XVIDEOS 5x, FatCat 4x = all losers
5. **DexScreener spam**: 374 throttle failures from over-calling

## v7.2 Expected Improvement:
- Historical analysis: h1≤200% filters keep 54 quality trades, removes 94 bad
- Expected WR: 17% → 35%+
- Expected: Break even at 31.6% WR, profitable above that

## Systems Running:
- `gmgn_scanner.py`: GMGN primary scanner, v7.2
- `position_monitor.py`: TP/stop monitoring every 60s
- `alert_sender.py`: Telegram delivery every 30s

## GMGN Throttle Alerts:
- GMGN throttled → immediate Telegram alert
- DexScreener throttled → immediate Telegram alert
- Both have circuit breakers to prevent spam

## HOURLY BACKUP (CRITICAL - DO NOT SKIP)
Hourly cron job backs up to GitHub — runs every :30 at :30 UTC:
- Workspace files: *.md, skills/
- Cron jobs: /root/.openclaw/cron/jobs.json
- System skills: /opt/node22/lib/node_modules/openclaw/skills/
Job ID: 16429a40-b0b6-470e-8c3e-8c154b57862a (hourly-bot-backup)
Runs at :30 every hour

## Key Lessons (v7.0/v7.1 failures):
- pump.fun allows DUPLICATE SYMBOL NAMES with different addresses → symbol blacklist needed
- Stale data kills → always fetch fresh before decisions
- DexScreener rate limits fast → need circuit breaker
- Position count in scanner vs actual open can differ → always use fresh count
- Python subprocess buffering → use `nohup python -u` for unbuffered output
- `.last_alert_index` can go stale → reset with trades file

## GMGN Skills Installed (2026-04-25)
- Location: `~/.openclaw/workspace/.agents/skills/`
- 6 skills: gmgn-token, gmgn-market, gmgn-portfolio, gmgn-swap, gmgn-cooking, gmgn-track
- All use `gmgn-cli` command interface (not raw API)
- Skills available via: `npx skills add GMGNAI/gmgn-skills`

## H1 Scoring FIXED (2026-04-25)
- WAS: Lower H1 = higher score (inverted logic)
- NOW: Higher H1 = higher score (matches actual data)
- Data: TP2+ winners avg H1=260% vs losers avg H1=238%
- Win rates by H1: ≤50%=0%, 51-100%=22.4%, 101-200%=17.6%, 201-400%=22.3%, >400%=25.5%
- New scoring: >400% → +2pts | 251-400% → +1.5 | 151-250% → +1 | 51-150% → +0.5 | ≤50% → +0

## Whale Signals Added to Scanner (2026-04-25)
- `entry_smart_degen`: Smart money wallets (proven profitable traders)
- `entry_renowned`: KOL/influencer wallets
- `entry_bot_degen`: Bot degen count
- Whale score = smart_degen + (renowned × 1.5)
- New scoring: ≥10 → +2pts | 6-9.9 → +1.5 | 3-5.9 → +1 | 1-2.9 → +0.5 | 0 → +0
- Score max now 18 (was 16)

## Additional GMGN Fields Now Logged (2026-04-25)
| Field | Signal | Logged |
|-------|--------|--------|
| top10holderpercent | Holder concentration | ✅ entry_top10_pct |
| liquidity | Pool depth | ✅ entry_liquidity |
| initial_liquidity | Compare vs current for drain | ✅ entry_initial_liq |
| creator_close | Dev sold out (big red flag) | ✅ entry_creator_close |
| rug_ratio | Rug risk score (0.3+ = dangerous) | ✅ entry_rug_ratio |
| hot_level | Trending intensity | ✅ entry_hot_level |
| sniper_count | Snipers at launch | ✅ entry_sniper_count |
| bundler_rate | Bot buys (manipulation signal) | ✅ entry_bundler_rate |
| is_wash_trading | Fake volume | ✅ entry_wash_trading |
| bluechip_owner_pct | Smart money presence | ✅ entry_bluechip_pct |

## Safety Scoring in signal_scorer (v7.5)
- Clean safety profile: +0.5 bonus points
- Creator close (dev sold): zone=danger, no points
- rug_ratio ≥ 0.3: zone=high_risk, no points
- rug_ratio ≥ 0.2: zone=warn, -0.5 points
- top10_pct ≥ 50%: zone=concentration, -0.5 points
- bundler_rate ≥ 50%: zone=bot_heavy, -0.5 points

## Chris Preferences:
- "Either buy or pass - no presenting signals"
- Wants continuous scanning and trading
- Prefers fast decisions over perfect analysis
- Very detail-oriented on alert/report format
- All Telegram must go to chat_id 6402511249 (his Telegram, not "Chris")
