# EMERGENCY RECOVERY GUIDE — Vultr Console

**If Wilson goes silent or you can't trade, follow this guide step by step.**

---

## WHAT IS THIS?

This guide helps you recover the trading bot (Wilson) if:
- You stop getting heartbeat updates
- The bot stops responding
- You can't reach Wilson via Telegram
- Exec/commands are all failing

---

## STEP 1: ACCESS VULTR CONSOLE

1. **Log into Vultr** → https://my.vultr.com
2. **Find your server** (the VPS running Wilson)
3. **Click on it** → go to "Console" tab
4. A black/green screen will appear — this is your server's terminal

**You are now inside your server. Everything below happens HERE.**

---

## STEP 2: CHECK IF BOT IS RUNNING

Type this command and press Enter:

```
ps aux | grep python
```

**What you should see:**
- 2 lines with "gmgn_scanner.py" and "position_monitor.py"
- Both should show as running (not "defunct" or "zombie")

**If you see NOTHING or only 1 process → Bot crashed → Go to STEP 3**

**If you see 2+ processes → Bot is running → Try STEP 5 first**

---

## STEP 3: KILL EVERYTHING (Clean Slate)

If the bot crashed or is messed up, first kill all Python processes:

```
killall -9 python
```

Press Enter. Wait 3 seconds.

---

## STEP 4: RESTART THE BOT

After killing, start the bot fresh:

```
cd /root/Dex-trading-bot
nohup /root/Dex-trading-bot/venv/bin/python -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
nohup /root/Dex-trading-bot/venv/bin/python -u position_monitor.py >> position_monitor.log 2>&1 &
```

Press Enter. You should see a new prompt appear immediately.

---

## STEP 5: VERIFY IT'S WORKING

Run this to confirm both are running:

```
ps aux | grep gmgn
```

**You should see:**
- Line with "gmgn_scanner.py"
- Line with "position_monitor.py"

**Count the lines → should be EXACTLY 2**

If more than 2 lines, you have duplicate processes (BAD → go to STEP 3 and restart).

---

## STEP 6: CHECK LOGS

To see recent activity:

```
tail -10 /root/Dex-trading-bot/gmgn_scanner.log
```

You should see recent timestamps showing it's scanning.

---

## STEP 7: CHECK BALANCE

```
cat /root/Dex-trading-bot/sim_wallet.json
```

Look for: `"balance": X.XXXXX`

This is your current SOL balance.

---

## STEP 8: TEST TELEGRAM ALERTS

Tell Wilson (via Telegram) to send a test alert. If he responds, he's alive.

If no response for 5+ minutes → Go to STEP 9.

---

## STEP 9: RESTART OPENCLAW (If Wilson is silent but bot is running)

If the bot is running (you see processes) but Wilson doesn't respond to Telegram:

```
kill -9 $(pgrep -f openclaw-gateway)
```

Wait 5 seconds, it should auto-restart.

---

## STEP 10: IF NOTHING WORKS — FULL REBOOT

**Last resort. This restarts the entire server:**

In Vultr dashboard:
1. Go to your server
2. Click "Server Reset"
3. Confirm the reset

**WAIT 2-3 MINUTES** for server to come back online.

Then repeat from STEP 1.

---

## QUICK REFERENCE — COPY-PASTE COMMANDS

When you're in the console, copy these exactly:

```
# Check processes
ps aux | grep python

# Kill everything
killall -9 python

# Start bot
cd /root/Dex-trading-bot && nohup /root/Dex-trading-bot/venv/bin/python -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 & nohup /root/Dex-trading-bot/venv/bin/python -u position_monitor.py >> position_monitor.log 2>&1 &

# Verify 2 processes
ps aux | grep gmgn | grep -v grep | wc -l

# Check balance
cat /root/Dex-trading-bot/sim_wallet.json

# View recent trades
tail -5 /root/Dex-trading-bot/trades/sim_trades.jsonl

# View scanner log
tail -10 /root/Dex-trading-bot/gmgn_scanner.log
```

---

## WHAT IS WILSON?

Wilson is the AI assistant (OpenClaw agent) that:
- Monitors the bot
- Sends you Telegram alerts
- Calculates stats
- Makes trading decisions

The **bot** (gmgn_scanner + position_monitor) does the actual trading.
**Wilson** talks to you about it.

Both need to be running for everything to work.

---

## COMMON PROBLEMS

**Problem: "command not found"**
→ You typed something wrong. Retype exactly as shown.

**Problem: "Permission denied"**
→ You need to be root. Type: `sudo su` first, then re-enter command.

**Problem: Server won't respond at all**
→ Server is down. Use Vultr dashboard to hard reboot.

**Problem: Bot running but no Telegram alerts**
→ Wilson (OpenClaw) is down but bot is alive. Restart OpenClaw:
```
kill -9 $(pgrep -f openclaw-gateway)
```

**Problem: Too many python processes (more than 2)**
→ Duplicate bot instances running. This causes bugs.
→ Fix: `killall -9 python` then restart from STEP 4.

---

## WHAT EACH FILE DOES

| File | Purpose |
|------|---------|
| `gmgn_scanner.py` | Scans for tokens, makes buy decisions |
| `position_monitor.py` | Watches open positions, handles exits |
| `sim_trades.jsonl` | History of ALL trades (never delete) |
| `sim_wallet.json` | Your SOL balance (source of truth) |
| `.perm_blacklist.json` | Tokens we never buy again |

---

## RECOVERY FLOW (SUMMARY)

```
Are you getting heartbeat updates?
  YES → Everything OK. Nothing to do.
  NO  → Is bot running?
          YES → Restart OpenClaw (STEP 9)
          NO  → Kill + Restart (STEP 3 → STEP 4 → STEP 5)
                Still broken? → FULL REBOOT (STEP 10)
```

---

**Write this down or bookmark this page. You'll need it.**