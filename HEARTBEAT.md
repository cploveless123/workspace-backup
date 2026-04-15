# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "gmgn_scanner|position_monitor|alert_sender" | grep -v grep`
2. Check signals: `ls -lt signals/ | head -5`
3. Check trades: `tail -3 trades/sim_trades.jsonl`

## LIVE TRADING STATUS (v7.2)
- Balance: 1.0 SOL | Record: 0W/0L | Open: 0
- sim_trades.jsonl: EMPTY (fresh start)
- Starting balance: 1.0 SOL

## 🛡️ IRONCLAD RULES (NEVER BREAK)
1. Permanent Blacklist: Any token ever bought = NEVER buy again
2. Max Open Positions: 5 concurrent
3. Position Size: 0.1 SOL per trade
4. Never Re-buy: Even if dropped 90% after selling — NO
5. Only pump.fun / raydium / pumpswap: Reject all other exchanges

## API Safety (CRITICAL):
- GMGN primary | DexScreener backup
- ALWAYS fresh data before decisions
- DexScreener: stop calls after 5 consecutive failures
- GMGN + DexScreener BOTH fail → 🚨 STOP ALL BUYS + alert Chris

## v7.2 Entry Filters:
- Mcap: $6K-$25K
- Holders: ≥20
- Dip: 20-45% from ATH
- h1: ≤250% (avoid late entries)
- Fallen Giant: h1 >400% + mcap <$20K → REJECT
- Symbol blacklist: no repeat buys

## v7.2 Exit Rules:
- TP1 +30%: HOLD (watch only, 40% trailing)
- TP2 +100%: Sell 40% (40% trail)
- TP3 +200%: Sell 30% (40% trail)
- TP4 +300%: Sell 20% (40% trail)
- TP5 +1000%: Sell remaining 10% (35% trail)
- Stop: -30%

## If systems down - RESTART COMMAND:
```bash
cd /root/Dex-trading-bot
kill $(ps aux | grep -E "gmgn_scanner|position_monitor|alert_sender" | grep -v grep | awk '{print $2}') 2>/dev/null
rm -rf __pycache__
nohup /root/Dex-trading-bot/venv/bin/python -u /root/Dex-trading-bot/gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
nohup /root/Dex-trading-bot/venv/bin/python -u /root/Dex-trading-bot/position_monitor.py >> position_monitor.log 2>&1 &
nohup /root/Dex-trading-bot/venv/bin/python -u /root/Dex-trading-bot/alert_sender.py >> alert_sender.log 2>&1 &
echo "All restarted at $(date)"
```

## Format for Chris:
```
📊 STATUS | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL
📈 Record: XW/XL | WR: XX%
🔒 Open: X positions (max 5)

Recent CLOSES:
• TOKEN | WIN/LOSS | +X.XXXX SOL
```

## Git push (hourly):
```bash
git -C /root/Dex-trading-bot add -A && git -C /root/Dex-trading-bot commit -m "Update $(date)" && git -C /root/Dex-trading-bot push origin master
git -C /root/.openclaw/workspace add -A && git -C /root/.openclaw/workspace commit -m "Update $(date)" && git -C /root/.openclaw/workspace push origin master
```

## Integrity Check:
```
cd /root/Dex-trading-bot && python3 integrity_monitor.py
```
