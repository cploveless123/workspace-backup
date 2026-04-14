# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "gmgn_scanner|position_monitor|alert_sender" | grep -v grep`
2. Check signals: `ls -lt signals/ | head -5`
3. Check trades: `tail -3 trades/sim_trades.jsonl`
4. Check wallet: `cat sim_wallet.json`

## v6.7 Strategy
### Entry Filters:
- Mcap: $3.5K-$60K
- Age: 2-90 min
- Holders: 15+
- h1 or 24h > +5%
- Dip: 0-50% from ATH
- BS ratio: >0.15 (<15min) / >0.8 (≥15min)

### Cooldown (v6.7):
- m5 > -5% → cooldown triggered
- YOUNG (age < 15min): 45s, chg1 trigger +3%
- OLD: 30s, chg1 trigger +1%
- chg1 must be > +2% from baseline
- 2 consecutive rechecks in verify
- deterioration >3% = reject
- price: 3 consec drops >3% = reject

### Exit Plan (v6.7):
- TP1 (+50%): HOLD, 40% trailing
- TP2 (+100%): Sell 40%, 35% trail
- TP3 (+200%): Sell 30%, 35% trail
- TP4 (+300%): Sell 20%, 35% trail
- TP5 (+1000%): Sell 10%, 30% trail
- Stop: -20%

## Format for Chris (15-min update):

```
📊 15-MINUTE UPDATE | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL (+XX.XX%)
📈 Record: XW/XL | WR: XX%
🔒 Open: X positions (max 9)

📋 OPEN POSITIONS:
• TOKEN | entry $XX,XXX | current +XX%

📋 RECENT CLOSES:
• TOKEN | WIN/LOSS | +X.XXXX SOL

🧠 WHAT I'M LEARNING:
- Pattern insight
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

## Whale Database
- 16 whales analyzed
- Avg WR: 55.4% | Avg hold: 118h
- Strategy: Quality over quantity, hold for 2-5x wins

## Chris Market Insights
- 1:1 mcap/vol ratio in first 5min = early momentum signal (good entry point)
- Usually evolves to 1:3 mcap/vol ratio as pump develops = hold longer confirmation
- Sweet spot: $3.5K-$12K mcap range for early entries (v6.7 lowered from $8.5K)

## Integrity Check
```
cd /root/Dex-trading-bot && python3 integrity_monitor.py
```