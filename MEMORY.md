# MEMORY.md - Long-Term Memory

## Trading Bot Setup
- Location: `/root/Dex-trading-bot/`
- Git remote: https://github.com/cploveless123/Dex-trading-bot.git
- Workspace backup: https://github.com/cploveless123/workspace-backup.git
- Telegram alerts via @WilsonVultrBot (token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg)
- Chat ID: 6402511249 (Chris - "please grow good weed")

## System Status (2026-04-15 06:30 UTC) - LIVE TRADING
- sim_trades.jsonl: EMPTY
- sim_wallet.json: 1.0 SOL
- Starting balance: 1.0 SOL
- Record: 0W / 0L
- Position peak cache: cleared
- All scanners STOPPED

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

## Chris Preferences:
- "Either buy or pass - no presenting signals"
- Wants continuous scanning and trading
- Prefers fast decisions over perfect analysis
- Very detail-oriented on alert/report format
- All Telegram must go to chat_id 6402511249 (his Telegram, not "Chris")
