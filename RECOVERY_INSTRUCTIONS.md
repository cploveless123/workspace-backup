# EMERGENCY RECOVERY INSTRUCTIONS
## If Wilson Goes Down

---

## 🚨 QUICK STATUS CHECK

```bash
# Check if systems are running
ps aux | grep -E "whale_momentum|position_monitor|alert_sender|auto_scanner" | grep -v grep | wc -l

# Expected output: 4 (all running)
```

---

## 🔧 RESTART ALL SYSTEMS

```bash
cd /root/Dex-trading-bot

# Kill any stale processes
pkill -9 -f whale_momentum 2>/dev/null
pkill -9 -f position_monitor 2>/dev/null
pkill -9 -f alert_sender 2>/dev/null
pkill -9 -f auto_scanner 2>/dev/null

# Start fresh
nohup python3 -u whale_momentum_scanner.py > whale_momentum.log 2>&1 &
nohup python3 -u position_monitor.py > position_monitor.log 2>&1 &
nohup python3 -u alert_sender.py > alert_sender.log 2>&1 &
nohup python3 -u auto_scanner.py > auto_scanner.log 2>&1 &

# Verify
sleep 5
ps aux | grep -E "whale_momentum|position_monitor|alert_sender|auto_scanner" | grep -v grep | wc -l
# Should show: 4
```

---

## 🔍 DIAGNOSE ISSUES

### Check logs:
```bash
tail -20 /root/Dex-trading-bot/whale_momentum.log
tail -20 /root/Dex-trading-bot/auto_scanner.log
tail -20 /root/Dex-trading-bot/position_monitor.log
tail -20 /root/Dex-trading-bot/alert_sender.log
```

### Check Python processes:
```bash
ps aux | grep python | grep -v grep
```

### Test scanner manually:
```bash
cd /root/Dex-trading-bot
python3 -c "from alert_sender import get_status; print(get_status())"
python3 integrity_monitor.py
```

---

## 📊 CHECK WALLET STATUS

```bash
cd /root/Dex-trading-bot
python3 -c "from alert_sender import get_status; print(get_status())"
```

This shows: balance, record (W/L), open positions

---

## 🔄 SIM RESET (Fresh Start)

If you need to reset the simulation:

```bash
cd /root/Dex-trading-bot

# 1. Close all open positions
python3 << 'EOF'
import json
from datetime import datetime
with open('trades/sim_trades.jsonl') as f:
    lines = f.readlines()
new_lines = []
for line in lines:
    t = json.loads(line)
    if not t.get('closed_at'):
        t['status'] = 'closed'
        t['closed_at'] = datetime.utcnow().isoformat()
        t['exit_reason'] = 'SIM_RESET'
        t['pnl_sol'] = 0.0
    new_lines.append(json.dumps(t))
with open('trades/sim_trades.jsonl', 'w') as f:
    f.write('\n'.join(new_lines) + '\n')
print("All positions closed")
EOF

# 2. Reset timestamp
NOW=$(date +%Y-%m-%dT%H:%M:%S.000000)
sed -i "s/SIM_RESET_TIMESTAMP = '.*'/SIM_RESET_TIMESTAMP = '$NOW'/" trading_constants.py

# 3. Verify
python3 -c "from alert_sender import get_status; print(get_status())"
```

---

## 🛠️ COMMON FIXES

### If scanner won't start:
```bash
cd /root/Dex-trading-bot
python3 -c "import py_compile; py_compile.compile('whale_momentum_scanner.py')"
# If error, check syntax
```

### If imports fail:
```bash
pip3 install requests
```

### If GMGN calls slow:
```bash
# GMGN can be slow - scanner is optimized to only call GMGN when DexScreener shows holders=0
# This is normal
```

---

## 📁 KEY FILES

| File | Purpose |
|------|---------|
| `/root/Dex-trading-bot/trading_constants.py` | All settings (mcap, TP%, etc.) |
| `/root/Dex-trading-bot/trades/sim_trades.jsonl` | Trade history |
| `/root/Dex-trading-bot/whale_momentum_scanner.py` | Main scanner |
| `/root/Dex-trading-bot/position_monitor.py` | TP/Stop monitor |
| `/root/Dex-trading-bot/alert_sender.py` | Telegram alerts |
| `/root/Dex-trading-bot/auto_scanner.py` | Backup scanner |
| `/root/Dex-trading-bot/integrity_monitor.py` | Tamper detection |

---

## 🔑 IMPORTANT CONSTANTS

```bash
cd /root/Dex-trading-bot
grep "MIN_MCAP\|MAX_MCAP\|TP1_PERCENT\|STOP_LOSS" trading_constants.py
```

Current v5.6 settings:
- Mcap: $4K - $75K
- Dip: 10% - 40%
- TP1: +35% HOLD
- Stop: -20%

---

## 🌐 GIT BACKUP

```bash
cd /root/Dex-trading-bot
git add -A && git commit -m "Recovery backup $(date)" && git push origin master

# Also backup workspace
cd /root/.openclaw/workspace
git add -A && git commit -m "Recovery backup $(date)" && git push origin master
```

---

## 📱 TELEGRAM ALERTS

Bot: @WilsonVultrBot
Token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg
Chat ID: 6402511249

Test alert:
```bash
cd /root/Dex-trading-bot
python3 -c "from alert_sender import send_alert; send_alert('TEST - Systems online', 'TEST')"
```

---

## 🚨 EMERGENCY STOP

To stop ALL trading immediately:
```bash
pkill -9 -f whale_momentum
pkill -9 -f position_monitor
pkill -9 -f alert_sender
pkill -9 -f auto_scanner
```

---

## 📞 CONTACT

If Wilson is down and you can't recover:
1. Check logs: `tail -50 /root/Dex-trading-bot/whale_momentum.log`
2. Check git status: `cd /root/Dex-trading-bot && git status`
3. Push any local changes: `git add -A && git commit -m "Local save" && git push`
4. Restart from "QUICK STATUS CHECK" section above

---

## ✅ VERIFICATION CHECKLIST

After recovery, verify:
- [ ] `ps aux | grep whale | grep -v grep | wc -l` = 4
- [ ] `python3 -c "from alert_sender import get_status; print(get_status())"` works
- [ ] `python3 integrity_monitor.py` returns "passed"
- [ ] Balance shows 1.0 SOL (after reset)
- [ ] Git push succeeds

---

_Last updated: 2026-04-12 01:53 UTC_
_Wilson Recovery Guide v1.0_