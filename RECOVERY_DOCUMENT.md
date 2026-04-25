════════════════════════════════════════════════════════════════
  WILSON TRADING SYSTEM — COMPLETE RECOVERY DOCUMENT
  Last Updated: 2026-04-25 00:57 UTC
  Version: v7.9 WINNING FILTER+ (deployed 2026-04-24 22:25)
  Updated: BS_RATIO (0.1/0.5), TRAIL (15%), STOP (-25%)
════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 1: SYSTEM OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SYSTEM PURPOSE: Turn 1 SOL → 100 SOL via compound TP5 winners
MODE: LIVE TRADING (real money at risk)
PRIMARY BOT: /root/Dex-trading-bot/
WORKSPACE: /root/.openclaw/workspace/

GIT REPOS:
  • Bot:       https://github.com/cploveless123/Dex-trading-bot.git
  • Workspace: https://github.com/cploveless123/workspace-backup.git

TELEGRAM:
  • Bot username: @WilsonVultrBot
  • Bot token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg
  • Chat ID: 6402511249 (Chris)
  • Always use HTML mode for Telegram messages (Markdown fails with emoji)

CRITICAL ARCHITECTURE (2026-04-24):
  gmgn_scanner.py imports ALL constants from trading_constants.py
  → SINGLE SOURCE OF TRUTH → no parameter drift

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 2: CURRENT VERSIONS & DEPLOYMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCANNER: v7.7 OPTIMAL EXIT (gmgn_scanner.py)
  • GMGN_SCANNER_VERSION = "v7.7 OPTIMAL EXIT"
  • ALL constants imported from trading_constants.py
  • No local duplicates — param drift eliminated

POSITION MONITOR: position_monitor.py
  • Uses TP1-TP5 from trading_constants.py
  • TP5 Progressive Selling Strategy

SIGNAL SCORER: signal_scorer.py
  • USE_SCORE_GATE = False (disabled)
  • Computes winner-metric score for every buy (logging only)

SMART MONEY TRACKER: smart_money_tracker.py v1.0
  • Polls GMGN API for smart money trades every 60s
  • Config: smart_money_config.json, smart_money_wallets.json

FILES TO RESTORE AFTER REBOOT:
  /root/Dex-trading-bot/.perm_blacklist.json    (permanent blacklist - 3080+ tokens)
  /root/Dex-trading-bot/.stop_loss_cooldown     (stop loss cooldown state)
  /root/Dex-trading-bot/smart_money_cache.json  (smart money cache)
  /root/Dex-trading-bot/trades/sim_trades.jsonl (trade history)
  /root/Dex-trading-bot/sim_wallet.json         (balance state)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: TRADING CONSTANTS (Single Source of Truth)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LOCATION: /root/Dex-trading-bot/trading_constants.py
STATUS: ✅ All constants in this file — gmgn_scanner.py imports from here

# CORE TRADING
  POSITION_SIZE = 0.1          SOL per trade
  MAX_OPEN_POSITIONS = 5       max concurrent positions
  MAX_DAILY_LOSS = 9999        disabled (no daily loss limit)

# ENTRY FILTERS
  MIN_MCAP = 7000              minimum market cap USD
  MAX_MCAP = 30000             maximum market cap USD
  MIN_HOLDERS = 20             minimum holder count
  MIN_VOLUME = 5000            minimum 24h volume USD
  MIN_CHG5_FOR_BUY = 2.0       minimum 5m change % for buy signal
  H1_MOMENTUM_MIN = 100.0      minimum 1h change % (momentum requirement)
  H1_MOMENTUM_MAX = 99999.0    NO CEILING - let any momentum through

# PUMP PATH
  PUMP_CHG1_THRESHOLD = 5.001  chg1 must exceed this for pump path trigger
  PUMP_ENTRY_CHG5 = 10.0        chg5 must exceed this for pump entry
  PUMP_MIN_AGE = 210           min age (sec) before buying via pump path (3.5 min)

# FALLEN GIANT FILTER
  FALLEN_GIANT_H1 = 700         if h1 > this AND mcap < threshold → reject
  FALLEN_GIANT_MCAP = 25000
  H1_INSTABILITY_MULTIPLIER = 3 if h1 changes by >3x → reject

# BUY/SELL RATIO (updated 2026-04-25)
  BS_RATIO_NEW = 0.1           required for tokens < 15 min old
  BS_RATIO_OLD = 0.5           required for tokens >= 15 min old
  BS_PUMP_FUN_OK = True        skip BS check for pump.fun tokens

# DIP FILTER
  MIN_DIP_PCT = 5              minimum dip % from ATH
  MAX_DIP_PCT = 45             maximum dip % from ATH (don't buy dumps)

# TIMING COOLDOWNS
  YOUNG_AGE_THRESHOLD = 180    tokens younger than this use young cooldown
  YOUNG_COOLDOWN = 30          young path cooldown (<15min + chg5>+50%)
  OLDER_COOLDOWN = 30          older path cooldown (>15min + h1>+25% + chg5>-10%)
  BASE_WAIT = 15               base path wait (15s verify chg1 > chg1_prev + 3%)
  CHG1_RECHECK_INTERVAL = 6   recovery recheck interval
  CHG1_VERIFY_DELAY = 6        recovery verify before buy
  RECOVERY_WAIT = 6            recovery wait interval

# PUMP PATH TIMING
  PUMP_WAIT_1 = 45             first pump confirmation wait (45s)
  PUMP_WAIT_2 = 10            second pump confirmation wait (10s)
  PUMP_VERIFY_DELAY = 10      final pump verification wait (10s)

# TP5 EXIT PLAN (v7.7 Optimal Exit - updated 2026-04-25)
  TP1_PCT = 50,  TP1_TRAIL = 15,  TP1_SELL_PCT = 0      (HOLD at TP1)
  TP2_PCT = 100, TP2_TRAIL = 15,  TP2_SELL_PCT = 0.20    (sell 20%)
  TP3_PCT = 200, TP3_TRAIL = 15,  TP3_SELL_PCT = 0.15    (sell 15%)
  TP4_PCT = 300, TP4_TRAIL = 15,  TP4_SELL_PCT = 0.10    (sell 10%)
  TP5_PCT = 1000, TP5_TRAIL = 15, TP5_SELL_PCT = 1.0     (sell ALL)
  STOP_LOSS_PCT = 25           exit all at -25%

# EXCHANGES
  ALLOWED_EXCHANGES = ['raydium', 'pump', 'pumpswap']
  PUMP_EXCHANGES = ['pump', 'pumpswap']  pair address must end in "pump"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 4: ENTRY STRATEGY (Pump Path + Cooldowns)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUMP PATH TRIGGERS WHEN:
  • h1 > H1_MOMENTUM_MIN (100%) AND
  • chg5 >= PUMP_ENTRY_CHG5 (10%) AND
  • chg1 > -20% (not crashed)

PUMP PATH STAGES:
  1. PUMP_WAIT_1 (45s): verify h1>100 + chg5>=10 + chg1>-20 → advance
  2. PUMP_WAIT_2 (10s): verify same conditions → advance
  3. PUMP_VERIFY (10s): verify same conditions → BUY 0.1 SOL
  4. On any fail → enter CHG1_RECHECK or RECOVERY_WAIT

CHG1 RECOVERY (chg1 < -5% during pump wait):
  • STATE_CHG1_RECHECK: 6s rechecks until mcap > +5% from lowest observed
  • STATE_CHG1_VERIFY: 6s verify → BUY

RECOVERY (chg5 dropped - recovery monitoring):
  • STATE_RECOVERY_WAIT: 6s rechecks
  • Recovery target: lowest_chg5 + CHG5_RECOVERY_CHECK (5%)
  • Must exceed recovery target AND MIN_CHG5_FOR_BUY (2%)
  • Then → BASE_WAIT 30s → verify → BUY

BASE PATH (normal entry):
  • h1 > 100% + chg5 > 2% + chg1 > chg1_prev + 3%
  • 15s verify → BUY

COOLDOWN PATHS (non-pump entries):
  • CHG1 < -5% → CHG1_RECHECK (6s) → CHG1_VERIFY (6s) → BUY
  • h1>+25% + chg5>-10% → COOLDOWN_WAIT (30s) → BASE_WAIT (30s) → verify chg1 > chg1_prev+10% → BUY
  • YOUNG (<3min) + h1>+100% + chg5>-5% → YOUNG_COOLDOWN (30s) → verify chg1 > chg1_prev+10% → BUY
  • OLDER (>=3min) + h1>+100% + chg5>-5% → OLDER_COOLDOWN (30s) → verify chg1 > chg1_prev+10% → BUY

PUMP MIN AGE: 210 seconds (3.5 min) - all paths must wait this before buying

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 5: EXIT STRATEGY (TP5 Progressive Selling)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌──────┬──────────┬─────────────────┬────────────────────────┐
  │ Level│ Trigger  │ Sell %           │ Trail Stop             │
  ├──────┼──────────┼─────────────────┼────────────────────────┤
  │ TP1  │ +50%     │ HOLD (0%)        │ 15% from peak          │
  │ TP2  │ +100%    │ Sell 20%         │ 15% from peak          │
  │ TP3  │ +200%    │ Sell 15%         │ 15% from peak          │
  │ TP4  │ +300%    │ Sell 10%         │ 15% from peak          │
  │ TP5  │ +1000%   │ Sell ALL (100%)  │ EXIT                   │
  │ STOP │ -25%     │ Sell ALL (100%)  │ EXIT                   │
  └──────┴──────────┴─────────────────┴────────────────────────┘

KEY RULE: TP1 is HOLD only — let winners ride with 15% trailing stop.
Only start selling at TP2 (+100%).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 6: IRONCLAD RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PERM_BLACKLIST: Any token ever bought = NEVER buy again
2. Max 5 open positions at once
3. Position size: 0.1 SOL per trade
4. Never re-buy (PERM_BLACKLIST checked before every buy)
5. Exchange: only pump.fun / raydium / pumpswap
   - pump.fun pair address must end in "pump"
   - pumpswap pair address must end in "pump"
   - raydium: launchpad check only
6. Fresh data only (no stale) — GMGN primary, DexScreener backup
7. Alert dedup: 300 seconds (5 min) — same alert only once per 5 minutes
8. DexScreener fails > 5/hour → stop calls for 1 hour
9. Both GMGN + DexScreener throttled → STOP ALL BUYS until fixed
10. Throttle alert: once per event (not per cycle)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 7: GMGN CLI SETUP & COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GMGN-CLI LOCATION:
  Binary: /opt/node22/bin/gmgn-cli
  Symlink: /usr/local/bin/gmgn-cli → /opt/node22/bin/gmgn-cli
  Fallback: node /opt/node22/lib/node_modules/gmgn-cli/dist/index.js

USEFUL GMGN COMMANDS:
  # Check trending
  /usr/local/bin/gmgn-cli market trending --chain sol --interval 5m --limit 3

  # Token info
  /usr/local/bin/gmgn-cli token info --chain sol --address <ADDRESS>

  # Smart money
  /usr/local/bin/gmgn-cli smartmoney positions --chain sol

  # New pairs
  /usr/local/bin/gmgn-cli market newpairs --chain sol --interval 5m --limit 5

  # Trenches
  /usr/local/bin/gmgn-cli market trenches --chain sol --interval 1h --limit 5

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 8: START / STOP / RESTART COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCANNER (gmgn_scanner.py):
  START: cd /root/Dex-trading-bot && nohup /root/Dex-trading-bot/venv/bin/python -u gmgn_scanner.py > gmgn_scanner.log 2>&1 &
  STOP:  pkill -f gmgn_scanner
  CHECK: ps aux | grep gmgn_scanner | grep -v grep

POSITION MONITOR (position_monitor.py):
  START: cd /root/Dex-trading-bot && nohup /root/Dex-trading-bot/venv/bin/python -u position_monitor.py > position_monitor.log 2>&1 &
  STOP:  pkill -f position_monitor
  CHECK: ps aux | grep position_monitor | grep -v grep

BOTH RUNNING (confirm 2 processes):
  ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep | wc -l
  (should return 2)

LOGS:
  /root/Dex-trading-bot/gmgn_scanner.log
  /root/Dex-trading-bot/position_monitor.log

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 9: STATUS CHECK COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCANNER STATUS (JSON):
  cd /root/Dex-trading-bot && /root/Dex-trading-bot/venv/bin/python -c \
    "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"

OPEN POSITIONS:
  grep "BUY" /root/Dex-trading-bot/trades/sim_trades.jsonl | python3 -c \
    "import json,sys; [print(json.loads(l).get('token_name'), json.loads(l).get('status','open')) for l in sys.stdin if l.strip()]"

BALANCE:
  cat /root/Dex-trading-bot/sim_wallet.json

RECENT TRADES (last 5):
  tail -5 /root/Dex-trading-bot/trades/sim_trades.jsonl

RECORD (wins/losses):
  grep -c "BUY" trades/sim_trades.jsonl && grep -c "SELL" trades/sim_trades.jsonl

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 10: CRON JOBS (Scheduled Tasks)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ACTIVE CRON JOBS:
  1. hourly-bot-backup (ID: 649e19f9)
     • Every :30 (30 * * * * *)
     • Backs up Dex-trading-bot to GitHub

  2. auto-backup (ID: 3d16c86d)
     • Every 30 min (everyMs: 1800000)
     • Backs up bot + workspace

  3. scan-report-30min (ID: cb0115d8)
     • Every 30 min (everyMs: 1800000)
     • Sends scanner status to Telegram

  4. hourly-health-check (ID: d5a59055)
     • Every :15 (15 * * * * *)
     • Checks systems and alerts if down

  5. wallet-monitor (ID: e6239808)
     • Every 5 min (everyMs: 300000)
     • Monitors wallet balance

DISABLED:
  • git-backup (ID: 13ed03a1) - DISABLED

CHECK CRON STATUS:
  openclaw cron list

MANUAL TRIGGER:
  openclaw cron run <job-id>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 11: GIT BACKUP COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MANUAL BACKUP - BOT:
  cd /root/Dex-trading-bot && git add -A && git commit -m "$(date)" && git push origin master

MANUAL BACKUP - WORKSPACE:
  cd /root/.openclaw/workspace && git add -A && git commit -m "$(date)" && git push origin master

BOTH AT ONCE:
  cd /root/Dex-trading-bot && git add -A && git commit -m "$(date)" && git push origin master && cd /root/.openclaw/workspace && git add -A && git commit -m "$(date)" && git push origin master

CLONE REPOS ON NEW MACHINE:
  git clone https://github.com/cploveless123/Dex-trading-bot.git
  git clone https://github.com/cploveless123/workspace-backup.git

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 12: TELEGRAM ALERTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BOT: @WilsonVultrBot
TOKEN: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg
CHAT_ID: 6402511249

ALWAYS USE HTML MODE (Markdown fails with emoji → HTTP 400)
  parse_mode="HTML" in sendMessage payload

ALERT DEDUP: 300 seconds (5 minutes)

GMGN ALERTS:
  • GMGN throttled → immediate Telegram alert
  • DexScreener throttled → immediate Telegram alert
  • Both down → 🚨 STOP ALL BUYS + Telegram alert

BUY/SELL ALERTS:
  • Include entry mcap and exit mcap
  • PnL with green/red emoji
  • Clickable DexScreener + pump.fun links
  • Plain URLs (Telegram auto-detects)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 13: OPENCLAWS (AI AGENT) CONFIGURATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AGENT NAME: Wilson
PERSONA: Sharp, practical, results-driven AI assistant
EMOJI: 🤖

WORKSPACE: /root/.openclaw/workspace/
GIT: https://github.com/cploveless123/workspace-backup.git

OPENCLAW CLI:
  openclaw gateway status
  openclaw gateway start
  openclaw gateway stop
  openclaw gateway restart
  openclaw help

CONFIG LOCATION: /opt/node22/lib/node_modules/openclaw/
CRON JOBS: /root/.openclaw/cron/jobs.json

KEY SKILLS: healthcheck, weather, tmux, skill-creator

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 14: RECOVERY STEPS AFTER REBOOT / Fresh Machine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Clone repos
  git clone https://github.com/cploveless123/Dex-trading-bot.git /root/Dex-trading-bot
  git clone https://github.com/cploveless123/workspace-backup.git /root/.openclaw/workspace

STEP 2: Setup Python environment
  cd /root/Dex-trading-bot
  python3 -m venv venv
  ./venv/bin/pip install -r requirements.txt

STEP 3: Verify gmgn-cli
  /usr/local/bin/gmgn-cli --version
  ln -sf /opt/node22/bin/gmgn-cli /usr/local/bin/gmgn-cli 2>/dev/null || true

STEP 4: Start scanner
  cd /root/Dex-trading-bot
  nohup ./venv/bin/python -u gmgn_scanner.py > gmgn_scanner.log 2>&1 &

STEP 5: Start position monitor
  nohup ./venv/bin/python -u position_monitor.py > position_monitor.log 2>&1 &

STEP 6: Verify processes (should return 2)
  ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep | wc -l

STEP 7: Verify scanner status
  ./venv/bin/python -c "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"

STEP 8: Verify Telegram
  curl "https://api.telegram.org/bot8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg/sendMessage?chat_id=6402511249&text=Bot restarted successfully"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 15: PERFORMANCE METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RESET: 2026-04-24 (after v7.0/v7.1 failures - 155 trades, 17.6% WR, -2.9 SOL closed PnL)

v7.9 WINNING FILTER+ (deployed 2026-04-24 22:25 UTC):
  Entry filters: h1>=100 + mcap>=$7K + ratio>=0.40 + holders>=20
  Exit: TP2 sell 20%, TP3 sell 15%, TP4 sell 10%, TP5 sell ALL
  Trail: 15% for all TP levels | Stop: -25%

KEY IMPROVEMENTS FROM v7.0/v7.1:
  • Fallen Giants: h1>500%+mcap<$20K → REJECTED
  • H1 ceiling removed (was 200%, now 99999%)
  • Ratio filter: chg1/chg5 >= 0.40 (momentum acceleration)
  • Smart money tracking v1.0 integrated (deployed 2026-04-24 23:39)

STRATEGY: Identify winners early via pump path, let them run to +1000%, compound remaining

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 16: FILE STRUCTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/root/Dex-trading-bot/
├── gmgn_scanner.py          # Main scanner (v7.7) - imports all from trading_constants.py
├── position_monitor.py      # Exit strategy monitor
├── alert_sender.py          # Telegram alerts
├── signal_scorer.py         # Winner-metric scoring (disabled)
├── smart_money_tracker.py   # Smart money tracking v1.0
├── smart_money_config.json  # Smart money config
├── smart_money_wallets.json # Wallets to track
├── smart_money_cache.json   # Cache of smart money activity
├── trading_constants.py      # ✅ SINGLE SOURCE OF TRUTH for all constants
├── gmgn_scanner.log         # Scanner output log
├── position_monitor.log     # Monitor output log
├── .perm_blacklist.json     # Permanent token blacklist (CRITICAL)
├── .stop_loss_cooldown      # Stop loss cooldown state
├── trades/
│   ├── sim_trades.jsonl     # Trade history (CRITICAL)
│   ├── sim_wallet.json      # Balance state
│   ├── scan_log.jsonl       # Scan results
│   ├── score_log.jsonl      # Signal scores
│   └── archive_*.jsonl      # Old trade archives
└── venv/                    # Python virtual environment

/root/.openclaw/workspace/
├── AGENTS.md | SOUL.md | USER.md | MEMORY.md
├── HEARTBEAT.md | IDENTITY.md | TOOLS.md
├── RECOVERY_DOCUMENT.md     # This document
├── RECOVERY_INSTRUCTIONS.md
└── VULTR_RECOVERY_GUIDE.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 17: QUICK REFERENCE COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Check running processes
ps aux | grep -E "gmgn_scanner|position_monitor" | grep -v grep

# Check scanner log
tail -20 /root/Dex-trading-bot/gmgn_scanner.log

# Check position monitor log
tail -20 /root/Dex-trading-bot/position_monitor.log

# Check balance
cat /root/Dex-trading-bot/sim_wallet.json

# Check scanner status
cd /root/Dex-trading-bot && ./venv/bin/python -c "from gmgn_scanner import get_scanner_status; import json; print(json.dumps(get_scanner_status(), indent=2))"

# Test gmgn-cli
/usr/local/bin/gmgn-cli market trending --chain sol --interval 5m --limit 3

# Restart scanner
pkill -f gmgn_scanner; sleep 1; cd /root/Dex-trading-bot && nohup ./venv/bin/python -u gmgn_scanner.py > gmgn_scanner.log 2>&1 &

# Restart position monitor
pkill -f position_monitor; sleep 1; cd /root/Dex-trading-bot && nohup ./venv/bin/python -u position_monitor.py > position_monitor.log 2>&1 &

# Manual git backup
cd /root/Dex-trading-bot && git add -A && git commit -m "$(date)" && git push origin master
cd /root/.openclaw/workspace && git add -A && git commit -m "$(date)" && git push origin master

# Check cron jobs
openclaw cron list

# Test Telegram
curl "https://api.telegram.org/bot8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg/sendMessage?chat_id=6402511249&text=Test"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 18: CRITICAL CONSTANTS (Print This)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUMP PATH:     h1>100% + chg5>=10% + chg1>-20% → 45s→10s→10s→BUY
ENTRY FILTERS: mcap $7K-$30K | holders ≥20 | h1 100-99999%
BS_RATIO:      NEW=0.1 (<15min) | OLD=0.5 (>=15min)

TP EXIT PLAN:
  TP1 (+50%):  HOLD      | Trail 15%
  TP2 (+100%): Sell 20%  | Trail 15%
  TP3 (+200%): Sell 15%  | Trail 15%
  TP4 (+300%): Sell 10%  | Trail 15%
  TP5 (+1000%): Sell ALL | EXIT
  STOP:        -25%      | EXIT

POSITION SIZE: 0.1 SOL | MAX OPEN: 5
BLACKLIST:     PERM blacklist = NEVER buy again
PUMP MIN AGE:  210 seconds (3.5 min)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
END OF RECOVERY DOCUMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━