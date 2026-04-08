# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "auto_scanner|gmgn_buyer|position_monitor|alert_sender" | grep -v grep`
2. Check signals: `ls -lt signals/ | head -5`
3. Check trades: `tail -3 trades/sim_trades.jsonl`

## Current Strategy (AGGRESSIVE - 1 SOL to 100 SOL)
- EXIT PLAN: TP1 +100% (sell 50%), TP2 +200% (sell 25%), TP3 +500% (sell 25%), Trailing 30%
- FILTERS: Mcap $8.5K-$75K | BS 1.5+ | Holders 30+ | Max 5 positions
- EARLY MOMENTUM TIER: $8.5K-$12K mcap + 1x+ 5min vol/mcap ratio = buy signal
- SIM RESET: 1.0 SOL starting balance

## Format for Chris (15-min update):

```
📊 15-MINUTE UPDATE | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL (+XX.XX%)
📈 Record: XW/XL | WR: XX%
🔒 Open: X positions (max 5)

📋 OPEN POSITIONS:
• TOKEN | entry $XX,XXX | +XX%

📋 RECENT CLOSES:
• TOKEN | WIN/LOSS | +X.XXXX SOL

🧠 WHAT I'M LEARNING:
- Pattern insight
```

## If systems down
```bash
cd /root/Dex-trading-bot
kill $(ps aux | grep -E "auto_scanner|gmgn_buyer|position_monitor|alert_sender" | grep -v grep | awk '{print $2}') 2>/dev/null
nohup python3 -u auto_scanner.py >> auto_scanner.log 2>&1 &
nohup python3 -u gmgn_buyer.py >> gmgn_buyer.log 2>&1 &
nohup python3 -u position_monitor.py >> position_monitor.log 2>&1 &
nohup python3 -u alert_sender.py >> alert_sender.log 2>&1 &
echo "All restarted"
```

## Git push (hourly)
```bash
git -C /root/Dex-trading-bot add -A && git -C /root/Dex-trading-bot commit -m "Update $(date)" && git -C /root/Dex-trading-bot push origin master
git -C /root/.openclaw/workspace add -A && git -C /root/.openclaw/workspace commit -m "Update $(date)" && git -C /root/.openclaw/workspace push origin master
```

## Whale Database
- 16 whales analyzed
- Avg WR: 55.4% | Avg hold: 118h
- Strategy: Quality over quantity, hold for 2-5x wins

## Chris Market Insights
- 1:1 mcap/vol ratio in first 5min = early momentum signal (good entry point)
- Usually evolves to 1:3 mcap/vol ratio as pump develops = hold longer confirmation
- Sweet spot: $8.5K-$12K mcap range for early entries