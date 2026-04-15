# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep | wc -l` (should be 2)
2. Check scanner status: `cd /root/Dex-trading-bot && /root/Dex-trading-bot/venv/bin/python -c "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"`
3. Check scanner log: `tail -20 /root/Dex-trading-bot/gmgn_scanner.log`
4. Check trades: `tail -3 trades/sim_trades.jsonl`

## Primary Objective: Trade to 100 SOL via compound TP5 winners

## Current Strategy: TP5 COMPOUND

### Entry Criteria:
- Mcap: $6K-$55K
- Holders: ≥15
- H1: ≥+5% (momentum)
- chg5: ≥+2% (base entry) OR ≥+20% (pump path)
- Exchange: pump.fun (pair ends "pump") / raydium / pumpswap

### TP5 Exit Plan (v7.4 - Current):
| Level | Trigger | Sell % | Stop |
|-------|---------|--------|------|
| TP1 | +50% | HOLD | -30% trailing 40% |
| TP2 | +100% | 40% | -30% trailing 30% |
| TP3 | +200% | 30% | -30% trailing 30% |
| TP4 | +300% | 20% | -30% trailing 30% |
| TP5 | +1000% | ALL | EXIT |
| Stop | -30% | ALL | EXIT |

### Cooldown System (CORRECTED):
- **PUMP PATH** (chg1 >= +20%): 45s→30s→15s→BUY (uses chg1 NOT chg5)
- **YOUNG** (<15min) + h1>+5% + chg1>-5%: 45s cooldown → BUY if chg1 > chg1_prev + 3%
- **OLDER** (>=15min) + h1>+5% + chg1>-5%: 45s cooldown → BUY if chg1 >= +2%
- **BASE** (30s): chg1 > chg1_prev + 3% → BUY
- **Recovery** (chg1<-5%): 15s rechecks until mcap>+5% from low → 15s verify → BUY

### IRONCLAD Rules:
- PERM_BLACKLIST: never buy again
- Max 5 open positions
- 0.1 SOL per trade
- Fresh data only (GMGN primary, DexScreener backup)
- Alert dedup: 5 min

## Format for Chris (15-min update):

```
📊 15-MIN UPDATE | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL | 📈 XW/XL | 🔒 X open

📋 SCANNER STATUS:
• Cooldown: X | Blacklist: X | Rejected: X
• DexScreener Fails: X | GMGN fails: X/X/X

📋 OPEN POSITIONS:
• TOKEN | entry $XX,XXX | current +XX%

📋 RECENT CLOSES:
• TOKEN | WIN/LOSS | +X.XXXX SOL

🎯 PROGRESS TO 100 SOL:
• Current: X.XX SOL
• Target: 100 SOL
• Progress: X.X%
```

## If systems down:
```bash
pkill -f gmgn_scanner 2>/dev/null; pkill -f position_monitor 2>/dev/null
cd /root/Dex-trading-bot && rm -f gmgn_scanner.log
(stdbuf -oL -eL /root/Dex-trading-bot/venv/bin/python -u gmgn_scanner.py 2>&1 | tee gmgn_scanner.log) &
(stdbuf -oL -eL /root/Dex-trading-bot/venv/bin/python -u position_monitor.py 2>&1 | tee position_monitor.log) &
echo "Restarted"
```

## Git push (hourly):
```bash
cd /root/Dex-trading-bot && git add -A && git commit -m "Update $(date)" && git push origin master
cd /root/.openclaw/workspace && git add -A && git commit -m "Update $(date)" && git push origin master
```