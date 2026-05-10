# Heartbeat Checklist - Run every 15 minutes

## Check Systems
1. `ps aux | grep -E "scanner_v1|monitor_v1" | grep -v grep | wc -l` (should be 2)
2. Check scanner status: `cd /root/Dex-trading-bot && /root/Dex-trading-bot/venv/bin/python -c "from scanner_v1 import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"`
3. Check scanner log: `tail -20 /root/Dex-trading-bot/scanner_v1.log`
4. Check monitor log: `tail -20 /root/Dex-trading-bot/monitor_v1.log`
5. Check trades: `tail -3 /root/Dex-trading-bot/trades/sim_trades.jsonl`
6. **Read actual wallet balance from `sim_wallet.json`** — the bot writes it there after every sell. Format: `cat /root/Dex-trading-bot/sim_wallet.json`

## Primary Objective: Trade to 100 SOL via compound TP5 winners

## Current Strategy: TP5 COMPOUND v1.8

### Entry Paths (priority order):
1. **SMART_DEGEN**: Smart Degen > 0 + H1 200-500% + MCAP $10K-$20K
2. **PROVEN**: Age > 600s + H1 200-500% + MCAP $10K-$20K + (KOL $200+ OR Snipers)
3. **KOL**: KOL Vol >= $200 + H1 > 30% + MCAP $5K-$50K
4. **WHALE**: Whale >= 3 + H1 > 75% + Vol > $10K
5. **SNIPER_HEAVY**: Snipers >= 2 + H1 > 50% + chg1 > 5% + Vol > $10K
6. **PHOENIX**: MCAP $3K-$8K + chg5 20-50% + chg1 < 20% + Vol > $5K
7. **DIP**: MCAP $8K-$20K + H1 > 100% + dipped -5% to -15% + recovering

### Key Data Points:
- Overall WR: 36.4% (5,790 trades)
- Overall PnL: -66.74 SOL
- Best filter: SMART_DEGEN + MCAP $10-20K + H1 200-500% = 53.1% WR
- KOL volume $200+ = 54.5% WR (changed from $50 on 2026-05-10)
- Age > 600s = 56.9% WR
- STOP losses = 93% of all losses

### CRITICAL RULES:
- NEVER change code without Chris's explicit approval
- ALWAYS follow SAFE_CHANGES.md
- Backup first, test after, report before deploying
- Verify before speaking - check logs, code, data
- Show exact commands and outputs
- Double check all calculations
- No assumptions, no shortcuts, no lies

## Format for Chris (15-min update):

```
📊 15-MIN UPDATE | HH:MM UTC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance: X.XXXX SOL | 📈 XW/XL | 🔒 X open

📋 SCANNER STATUS:
• SMART_DEGEN: X | PROVEN: X | KOL: X | WHALE: X | SNIPER_HEAVY: X
• Rejected: X | DexScreener Fails: X | GMGN fails: X/X/X

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
pkill -f scanner_v1 2>/dev/null; pkill -f monitor_v1 2>/dev/null
cd /root/Dex-trading-bot && rm -f scanner_v1.log
(stdbuf -oL -eL /root/Dex-trading-bot/venv/bin/python -u scanner_v1.py 2>&1 | tee scanner_v1.log) &
(stdbuf -oL -eL /root/Dex-trading-bot/venv/bin/python -u monitor_v1.py 2>&1 | tee monitor_v1.log) &
echo "Restarted"
```

## Git push (hourly):
```bash
cd /root/Dex-trading-bot && git add -A && git commit -m "Update $(date)" && git push origin master
cd /root/.openclaw/workspace && git add -A && git commit -m "Update $(date)" && git push origin master
```
