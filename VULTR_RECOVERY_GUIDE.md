# VULTR CONSOLE RECOVERY GUIDE

## Accessing Vultr Console

1. Go to **https://my.vultr.com**
2. Click **Servers** → select your VPS
3. Click **Server Console** (or "View Console")
4. A new window opens with terminal access

If console is **blank/black** → Server is hung:
→ Click **Server** → **Stop** → wait 10 seconds → **Start**
→ Wait 2-3 minutes for boot → console shows `root@vultr:~#`

---

## SCENARIO 1: Server was completely stopped/restarted

After Vultr boot completes, paste this ALL at once:

```
ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli && cd /root/Dex-trading-bot && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 & && python3 -u position_monitor.py >> position_monitor.log 2>&1 &
```

Verify with:
```
ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep
```

---

## SCENARIO 2: Server is running but scanner is dead (no signals, scan errors)

**Step 1:** Fix gmgn-cli path
```
ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli
```

**Step 2:** Restart scanner
```
cd /root/Dex-trading-bot && pkill -f gmgn_scanner && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
```

**Step 3:** Verify
```
tail -5 /root/Dex-trading-bot/gmgn_scanner.log
```

---

## SCENARIO 3: Scanner works but position monitor is broken (wrong balance, "no price" errors)

**Step 1:** Restart position monitor
```
cd /root/Dex-trading-bot && pkill -f position_monitor && python3 -u position_monitor.py >> position_monitor.log 2>&1 &
```

**Step 2:** Verify
```
tail -5 /root/Dex-trading-bot/position_monitor.log
```

---

## SCENARIO 4: Balance is completely wrong (negative, way too high, etc.)

**Step 1:** Reset wallet and trades
```
echo '{"balance": 1.0, "last_updated": "2026-04-19T00:00:00+00:00"}' > /root/Dex-trading-bot/sim_wallet.json && mv /root/Dex-trading-bot/trades/sim_trades.jsonl /root/Dex-trading-bot/trades/archive_sim_$(date +%Y%m%d_%H%M%S).jsonl && touch /root/Dex-trading-bot/trades/sim_trades.jsonl
```

**Step 2:** Restart position monitor
```
cd /root/Dex-trading-bot && pkill -f position_monitor && python3 -u position_monitor.py >> position_monitor.log 2>&1 &
```

Note: This archives ALL trade history and resets to 1.0 SOL balance. The perm_blacklist stays intact (those tokens are still banned).

---

## SCENARIO 5: Getting constant "Scan error: No such file" or "gmgn-cli not found"

Fix the symlink:
```
ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli
```

Then restart scanner:
```
cd /root/Dex-trading-bot && pkill -f gmgn_scanner && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
```

Test gmgn-cli works:
```
/usr/local/bin/gmgn-cli market trending --chain sol --interval 5m --limit 1
```

---

## SCENARIO 6: Getting throttle alerts and buys were stopped

The system has a circuit breaker — when BOTH GMGN throttled AND DexScreener failing, it stops buys.

Wait 5-10 minutes. The scanner will automatically resume when APIs recover.

To check current status:
```
cd /root/Dex-trading-bot && /root/Dex-trading-bot/venv/bin/python -c "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"
```

If `buys_stopped: false` → system resumed automatically.

---

## SCENARIO 7: Everything is running but you want to restart cleanly

```
cd /root/Dex-trading-bot && pkill -f gmgn_scanner && pkill -f position_monitor && sleep 2 && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 & && python3 -u position_monitor.py >> position_monitor.log 2>&1 &
```

---

## CHECK STATUS (run any time)

**Check what's running:**
```
ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep
```

**Check scanner log:**
```
tail -10 /root/Dex-trading-bot/gmgn_scanner.log
```

**Check position monitor log:**
```
tail -10 /root/Dex-trading-bot/position_monitor.log
```

**Check balance:**
```
cat /root/Dex-trading-bot/sim_wallet.json
```

**Check open positions:**
```
grep "BUY" /root/Dex-trading-bot/trades/sim_trades.jsonl | python3 -c "import json,sys; [print(json.loads(l).get('token_name'), json.loads(l).get('status','open')) for l in sys.stdin if l.strip()]"
```

---

## MANUAL BACKUP (if worried about losing changes)

```
cd /root/Dex-trading-bot && git add -A && git commit -m "$(date)" && git push origin master
cd /root/.openclaw/workspace && git add -A && git commit -m "$(date)" && git push origin master
```

---

## WHAT EACH THING DOES

| Command | What it does |
|---------|-------------|
| `ln -sf` | Creates symlink so scanner can find gmgn-cli |
| `pkill -f gmgn_scanner` | Kills old scanner process |
| `python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &` | Starts scanner in background, logs to file |
| `python3 -u position_monitor.py >> position_monitor.log 2>&1 &` | Starts position monitor in background |
| `ps aux \| grep` | Shows running processes |
| `tail -10` | Shows last 10 lines of log file |
| `sim_wallet.json` | Holds current balance |
| `sim_trades.jsonl` | Holds all trade records |

---

## COMMON ERRORS AND FIXES

| Error | Fix |
|-------|-----|
| `No such file: 'gmgn-cli'` | `ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli` |
| `Scan error: [Errno 2]` | Same as above — gmgn-cli path broken |
| `local variable 'closed_pnl' referenced before assignment` | Restart position monitor |
| Balance showing negative | Reset balance (Scenario 4) |
| Scanner not finding anything | Check scanner log for errors |
| Position monitor shows "No price" | Restart position monitor |

---

## RECOVERY FLOWchart

```
Is server responding?
├── YES → Go to Vultr console
│   ├── Scanner dead? → Scenario 2
│   ├── Position monitor dead? → Scenario 3
│   ├── Balance wrong? → Scenario 4
│   ├── gmgn-cli error? → Scenario 5
│   └── Everything fine? → All good!
└── NO (blank/frozen) → Hard reset via Vultr control panel → Scenario 1
```
