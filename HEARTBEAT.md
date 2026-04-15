# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "gmgn_scanner|position_monitor|alert_sender" | grep -v grep`
2. Check signals: `ls -lt signals/ | head -5`
3. Check trades: `tail -3 trades/sim_trades.jsonl`

## Current Strategy: v7.2 (RESET 2026-04-15)
### RESET - Fresh Start
- sim_trades.jsonl: EMPTY
- sim_wallet.json: 1.0 SOL
- Starting balance: 1.0 SOL
- Record: 0W / 0L

### v7.2 Entry Filters:
- Mcap: $6K-$25K
- Holders: ≥20
- Dip: 20-45% from ATH
- h1: ≤250% (avoid late entries)
- Fallen Giant: h1 >400% + mcap <$20K → REJECT
- Symbol blacklist: no repeat buys of same symbol
- Only pump.fun / raydium / pumpswap

### Exit Rules (v7.2 Chris Update):
- TP1 +30%: HOLD (watch only, 40% trailing stop from peak)
- TP2 +100%: Sell 40% (35% trailing on remaining 60%)
- TP3 +200%: Sell 30% (40% trailing on remaining 30%)
- TP4 +300%: Sell 20% (40% trailing on remaining 10%)
- TP5 +1000%: Sell remaining 10%
- Stop: -30%

### Fresh Data Rule:
- ALWAYS fetch fresh data before any decision
- GMGN primary, DexScreener backup
- If GMGN unavailable → alert + pause
- If DexScreener throttled (5+ fails) → skip until recovers

### Throttle Alerts:
- If GMGN or DexScreener throttled → Telegram alert immediately

## Format for Chris:

```
📊 STATUS | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL
📈 Record: XW/XL | WR: XX%
🔒 Open: X positions

Recent CLOSES:
• TOKEN | WIN/LOSS | +X.XXXX SOL

🧠 Notes:
```

## If systems down
```bash
cd /root/Dex-trading-bot
kill $(ps aux | grep -E "gmgn_scanner|position_monitor|alert_sender" | grep -v grep | awk '{print $2}') 2>/dev/null
nohup /root/Dex-trading-bot/venv/bin/python -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
nohup /root/Dex-trading-bot/venv/bin/python -u position_monitor.py >> position_monitor.log 2>&1 &
nohup /root/Dex-trading-bot/venv/bin/python -u alert_sender.py >> alert_sender.log 2>&1 &
echo "All restarted"
```

## Git push (hourly)
```bash
git -C /root/Dex-trading-bot add -A && git -C /root/Dex-trading-bot commit -m "Update $(date)" && git -C /root/Dex-trading-bot push origin master
git -C /root/.openclaw/workspace add -A && git -C /root/.openclaw/workspace commit -m "Update $(date)" && git -C /root/.openclaw/workspace push origin master
```

## Integrity Check
```
cd /root/Dex-trading-bot && python3 integrity_monitor.py
```
