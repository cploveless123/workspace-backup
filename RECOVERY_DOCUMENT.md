════════════════════════════════════════════════════════════════
  WILSON TRADING SYSTEM — COMPLETE RECOVERY DOCUMENT
  Last Updated: 2026-04-19 02:21 UTC
════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. SYSTEM OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Trading Bot: Solana DEX sniper (pump.fun / pumpswap / raydium)
Primary Goal: Turn 1 SOL → 100 SOL via compound TP5 winners
Mode: LIVE TRADING (real money at risk)
Location: /root/Dex-trading-bot/
Git: https://github.com/cploveless123/Dex-trading-bot

Backup Workspace: /root/.openclaw/workspace/
Git: https://github.com/cploveless123/workspace-backup.git

Telegram Bot: @WilsonVultrBot
Telegram Token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg
Chat ID: 6402511249 (Chris)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. TRADING STRATEGY — BABA PLAN (Current)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ENTRY: Pump Path
  • h1 > +100% AND chg5 >= +10% AND chg1 > -20%
  • All pre-filters must pass first

PRE-FILTERS:
  • Mcap: $8,000 – $30,000
  • Holders: ≥15
  • Volume 24h: >$5,000
  • BS ratio: <80%
  • H1: ≤600% (above = rejected "too parabolic")
  • Exchange: pump.fun / pumpswap / raydium only
  • Min age: 210 seconds before pump path can trigger
  • ATH distance: must be within 55% below ATH

PUMP PATH STAGES:
  1. PUMP_WAIT_1 (30s): verify h1>100 + chg5>=10 + chg1>-20 → advance
  2. PUMP_WAIT_2 (15s): verify same conditions → advance
  3. PUMP_VERIFY (15s): verify same conditions → BUY 0.1 SOL
  4. On any fail: enter RECOVERY

RECOVERY:
  • 600 seconds (10 minutes) after failing pump checks
  • Token is re-evaluated after recovery period
  • Keeps cycling through pump stages until it buys or is blacklisted

EXIT PLAN:
  ┌──────┬──────────┬─────────┬────────────────┐
  │ TP   │ Trigger  │ Sell %  │ Trail Stop     │
  ├──────┼──────────┼─────────┼────────────────┤
  │ TP1  │ +50%     │ HOLD    │ 40% from peak  │
  │ TP2  │ +100%    │ 30%     │ 35% from peak  │
  │ TP3  │ +200%    │ 35%     │ 35% from peak  │
  │ TP4  │ +300%    │ 25%     │ 35% from peak  │
  │ TP5  │ +1000%   │ ALL     │ 20% from peak  │
  │ STOP │ -35%     │ ALL     │ EXIT           │
  └──────┴──────────┴─────────┴────────────────┘
  • TP1 is HOLD only — let winners ride with 40% trailing stop

IRONCLAD RULES:
  1. PERM_BLACKLIST: Never re-buy a token that was bought
  2. Max 5 open positions at once
  3. Position size: 0.1 SOL per trade
  4. Fresh data only (GMGN primary, DexScreener backup)
  5. Stop loss: -35% (tighter than before)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. SCANNER SETUP — gmgn_scanner.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SOURCES (cycling every 15s):
  1. GMGN trending (50 tokens)
  2. GMGN trenches (50 tokens)
  3. GMGN trenches (50 tokens)
  4. DexScreener pump.fun new pairs (20 tokens)

gmgn-cli LOCATION (CRITICAL FIX):
  • Binary: /opt/node22/bin/gmgn-cli
  • Symlink: /usr/local/bin/gmgn-cli → /opt/node22/bin/gmgn-cli
  • Access via: /opt/node22/bin/gmgn-cli OR /usr/local/bin/gmgn-cli
  • RUN WITH: node /opt/node22/lib/node_modules/gmgn-cli/dist/index.js (fallback)

SCANNER START COMMAND:
  cd /root/Dex-trading-bot && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &

SCANNER LOG:
  /root/Dex-trading-bot/gmgn_scanner.log

PUMP PATH CODE LOCATION (line ~567):
  pump_triggered = (h1 > 100 and chg5 >= 10.0 and chg1 > -20.0)

TO UPDATE PUMP PATH PARAMETERS:
  Edit these constants in gmgn_scanner.py:
  • PUMP_ENTRY_CHG5 = 10.0
  • PUMP_WAIT_1 = 30
  • PUMP_WAIT_2 = 15
  • PUMP_VERIFY_DELAY = 15
  • RECOVERY_WAIT = 600

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. POSITION MONITOR — position_monitor.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PURPOSE: Track open positions, execute TP levels, trail stops, stop loss

START COMMAND:
  cd /root/Dex-trading-bot && python3 -u position_monitor.py >> position_monitor.log 2>&1 &

LOG:
  /root/Dex-trading-bot/position_monitor.log

KEY FILES:
  • Trades: /root/Dex-trading-bot/trades/sim_trades.jsonl
  • Wallet: /root/Dex-trading-bot/sim_wallet.json
  • Perm blacklist: /root/Dex-trading-bot/.perm_blacklist.json
  • Stop loss cooldown: /root/Dex-trading-bot/.stop_loss_cooldown
  • Position peak cache: /root/Dex-trading-bot/.position_peak_cache.json

TP EXIT PARAMETERS (in trading_constants.py):
  TP1_PCT = 50, TP1_TRAIL = 40, TP1_SELL_PCT = 0
  TP2_PCT = 100, TP2_TRAIL = 35, TP2_SELL_PCT = 0.30
  TP3_PCT = 200, TP3_TRAIL = 35, TP3_SELL_PCT = 0.35
  TP4_PCT = 300, TP4_TRAIL = 35, TP4_SELL_PCT = 0.25
  TP5_PCT = 1000, TP5_TRAIL = 20, TP5_SELL_PCT = 1.0
  STOP_LOSS_PCT = 35

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. TRADING DATA FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE FILES:
  /root/Dex-trading-bot/trades/sim_trades.jsonl
    → Live trade log (BUY/SELL records)
  /root/Dex-trading-bot/sim_wallet.json
    → Current balance (JSON: {"balance": X.XX, "last_updated": "..."})
  /root/Dex-trading-bot/.perm_blacklist.json
    → Tokens we bought (NEVER buy again)
  /root/Dex-trading-bot/.stop_loss_cooldown.json
    → Tokens on 30-min stop loss cooldown

ARCHIVE FILES (old trade logs):
  /root/Dex-trading-bot/trades/archive_*.jsonl
    → Older archived trades

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. ALERT SYSTEM — Telegram
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bot: @WilsonVultrBot
Token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg
Chat ID: 6402511249

Alert Format Rules:
  • Telegram uses HTML mode (NOT Markdown)
  • Entry/Exit mcap on all sells
  • PnL with green/red emoji
  • Clickable links (plain URLs)
  • No signal alerts — only BUY/SELL executed
  • Alert dedup: 5 minutes between same alerts

Alert Types:
  • BUY executed (entry price, mcap, token name)
  • SELL executed (exit price, mcap, PnL, reason)
  • TP hit (which TP level)
  • STOP_LOSS hit
  • GMGN throttled
  • DexScreener throttled
  • API failures

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. VPS RECOVERY — Vultr Console
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACCESS: https://my.vultr.com → Select Server → Server Console

IF SERVER IS FROZEN/HUNG:
  1. Vultr control panel → Server → Stop → wait 10s → Start
  2. Wait for boot → console shows root@vultr:~#

IF gmgn-cli NOT FOUND:
  1. Check if symlink exists: ls -la /usr/local/bin/gmgn-cli
  2. If broken: ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli
  3. Verify: /usr/local/bin/gmgn-cli market trending --chain sol --interval 5m --limit 1

IF SCANNER DIES WITH "NO SUCH FILE":
  → gmgn-cli symlink is broken → fix symlink (see above)
  → Then restart scanner

FULL RESTART SEQUENCE:
  # Fix gmgn-cli symlink
  ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli
  
  # Restart scanner (if not running)
  cd /root/Dex-trading-bot && pkill -f gmgn_scanner
  cd /root/Dex-trading-bot && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &
  
  # Restart position monitor
  cd /root/Dex-trading-bot && pkill -f position_monitor
  cd /root/Dex-trading-bot && python3 -u position_monitor.py >> position_monitor.log 2>&1 &

CHECK STATUS:
  ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep
  tail -10 /root/Dex-trading-bot/gmgn_scanner.log
  tail -10 /root/Dex-trading-bot/position_monitor.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. BACKUP SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GIT REPOS:
  Dex-trading-bot: https://github.com/cploveless123/Dex-trading-bot
  Workspace: https://github.com/cploveless123/workspace-backup.git

HOURLY BACKUP (cron job ID: 16429a40-b0b6-470e-8c3e-8c154b57862a):
  Runs at :30 every hour UTC
  Backs up: workspace files (*.md, skills/), cron jobs, system skills
  Also backs up Dex-trading-bot via separate hourly cron

MANUAL BACKUP:
  cd /root/Dex-trading-bot && git add -A && git commit -m "Update $(date)" && git push origin master
  cd /root/.openclaw/workspace && git add -A && git commit -m "Update $(date)" && git push origin master

BACKUP STATUS:
  Last checked: working as of 01:54 UTC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. MEMORY / CONTEXT FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Location: /root/.openclaw/workspace/

Key Files:
  MEMORY.md
    → Long-term memory (loaded in main session only)
    → Contains: trading bot setup, system status, key lessons
  
  HEARTBEAT.md
    → 15-minute heartbeat checklist
    → System checks, scanner status, open positions
    → Recovery commands if systems down
  
  memory/2026-04-19.md
    → Daily memory log (created 2026-04-19)
    → Contains: system issues, scanner config, positions
  
  USER.md
    → Chris's profile, trading rules, TP5 strategy
  
  SOUL.md / AGENTS.md / TOOLS.md
    → System configuration and agent behavior

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. CRON JOBS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hourly Backup (workspace):
  Job ID: 16429a40-b0b6-470e-8c3e-8c154b57862a
  Schedule: :30 every hour UTC
  Action: git add/commit/push workspace files

Hourly Backup (Dex-trading-bot):
  Schedule: :30 every hour UTC
  Action: git add/commit/push Dex-trading-bot

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. COMMON ISSUES AND FIXES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ISSUE: "Scan error: [Errno 2] No such file or directory: 'gmgn-cli'"
CAUSE: Scanner can't find gmgn-cli binary
FIX:
  1. ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli
  2. Restart scanner

ISSUE: "Monitor error: local variable 'closed_pnl' referenced before assignment"
CAUSE: Python scoping bug in position_monitor.py
FIX:
  1. Add "closed_pnl = total_pnl" in monitor_cycle() before use
  2. Restart position monitor

ISSUE: Scanner dies immediately on restart
CAUSE: Run without & to see actual error
FIX:
  cd /root/Dex-trading-bot && python3 -u gmgn_scanner.py
  (no &) → see error → fix → then run with &

ISSUE: Server frozen (console blank)
CAUSE: VPS is hung
FIX: Hard reset via Vultr control panel (Stop → Start)

ISSUE: Balance showing wrong (negative, too high)
CAUSE: sim_wallet.json corrupted
FIX:
  echo '{"balance": 1.0, "last_updated": "2026-04-19T00:00:00+00:00"}' > /root/Dex-trading-bot/sim_wallet.json
  mv trades file to archive, touch new empty one
  restart position monitor

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. QUICK REFERENCE COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check running processes
ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep

# Check scanner log
tail -20 /root/Dex-trading-bot/gmgn_scanner.log

# Check position monitor log
tail -20 /root/Dex-trading-bot/position_monitor.log

# Check balance
cat /root/Dex-trading-bot/sim_wallet.json

# Check open positions
grep "BUY" /root/Dex-trading-bot/trades/sim_trades.jsonl | python3 -c "import json,sys; [print(json.loads(l).get('token_name'), json.loads(l).get('status','open')) for l in sys.stdin if l.strip()]"

# Check closed trades
tail -10 /root/Dex-trading-bot/trades/sim_trades.jsonl

# Check scanner status
cd /root/Dex-trading-bot && /root/Dex-trading-bot/venv/bin/python -c "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"

# Test gmgn-cli
/usr/local/bin/gmgn-cli market trending --chain sol --interval 5m --limit 3

# Restart scanner
cd /root/Dex-trading-bot && pkill -f gmgn_scanner && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &

# Restart position monitor
cd /root/Dex-trading-bot && pkill -f position_monitor && python3 -u position_monitor.py >> position_monitor.log 2>&1 &

# Manual backup
cd /root/Dex-trading-bot && git add -A && git commit -m "$(date)" && git push origin master
cd /root/.openclaw/workspace && git add -A && git commit -m "$(date)" && git push origin master

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. PERFORMANCE TRACKING (Session 2026-04-19)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reset Time: ~02:08 UTC
Starting Balance: 1.0 SOL
Current Balance: ~0.74 SOL (as of 02:15 UTC)

Trades This Session:
  WINNERS:
    SEX: +0.062 SOL (TP2 hit, partial sell)
  LOSERS:
    guy: -0.081 SOL (STOP_LOSS)
    later: -0.068 SOL (STOP_LOSS)
    rETH: -0.044 SOL (STOP_LOSS)
    DOGEVAN: -0.038 SOL (STOP_LOSS)
    Dickhead: -0.042 SOL (STOP_LOSS)
    SEX: closed at small loss (trailing stop)

Record: 2W / 8L (20% WR)
Overall (all time): ~194W / 374L (34.1% WR), -5.98 SOL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
14. WHAT TO DO IF YOU WAKE UP AND NOTHING IS WORKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Check Vultr console
  → https://my.vultr.com → Server → Server Console
  → Is it frozen? → Stop/Start
  → Is it on? → Continue

Step 2: Fix gmgn-cli if missing
  ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli

Step 3: Start scanner
  cd /root/Dex-trading-bot && python3 -u gmgn_scanner.py >> gmgn_scanner.log 2>&1 &

Step 4: Start position monitor
  cd /root/Dex-trading-bot && python3 -u position_monitor.py >> position_monitor.log 2>&1 &

Step 5: Verify
  ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep
  tail -5 gmgn_scanner.log
  tail -5 position_monitor.log

Step 6: Check my Telegram for status
  → I'm Wilson, monitoring 24/7
  → If systems down, I'll alert

Step 7: Check memory file
  cat /root/.openclaw/workspace/memory/2026-04-19.md

Step 8: Check git for recent changes
  cd /root/Dex-trading-bot && git log --oneline -5
  cd /root/.openclaw/workspace && git log --oneline -5

Step 9: If nothing else works
  → Text me (Wilson) on Telegram
  → I'll walk you through it

════════════════════════════════════════════════════════════════
  END OF RECOVERY DOCUMENT
════════════════════════════════════════════════════════════════