════════════════════════════════════════════════════════════════
  WILSON TRADING SYSTEM — v7.9 WINNING FILTER+
  Last Updated: 2026-04-25 01:45 UTC
════════════════════════════════════════════════════════════════

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENTRY STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PUMP PATH: h1 > 100% AND chg5 >= 2% AND chg1 > -20%
  → 30s → 15s → 15s → BUY
  → Min age: 120 seconds

PREFILTERS (all must pass):
  • Mcap: $7,000 - $30,000
  • Holders: ≥20
  • H1: 100% - 700%
  • Ratio (chg1/chg5): ≥ 0.40 (non-pump only)
  • BS ratio: ≥1.5 (<15min) / ≥1.3 (>=15min)
  • Exchange: raydium, pump, pumpswap
  • Pump/pumpswap pair_address must end in "pump"

EXCHANGES:
  • ALLOWED: ['raydium', 'pump', 'pumpswap']
  • Pump/pumpswap pair_address must end in "pump"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXIT STRATEGY (TP5 Progressive Selling)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ┌──────┬──────────┬─────────────────┬────────────────────────┐
  │ Level│ Trigger  │ Sell %           │ Trail Stop             │
  ├──────┼──────────┼─────────────────┼────────────────────────┤
  │ TP1  │ +50%     │ HOLD (0%)        │ 12% from peak          │
  │ TP2  │ +100%    │ Sell 20%         │ 12% from peak          │
  │ TP3  │ +200%    │ Sell 15%         │ 12% from peak          │
  │ TP4  │ +300%    │ Sell 10%         │ 12% from peak          │
  │ TP5  │ +1000%   │ Sell ALL (100%)  │ EXIT                   │
  │ STOP │ -35%     │ Sell ALL (100%)  │ EXIT                   │
  └──────┴──────────┴─────────────────┴────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY CONSTANTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSITION_SIZE = 0.1 SOL
MAX_OPEN_POSITIONS = 5
MIN_MCAP = $7,000
MAX_MCAP = $30,000
MIN_HOLDERS = 20
H1_MOMENTUM_MIN = 100%
H1_MOMENTUM_MAX = 700%
MIN_CHG5_FOR_BUY = 5.0%
PUMP_ENTRY_CHG5 = 2.0%
PUMP_CHG1_THRESHOLD = 10.0%
PUMP_MIN_AGE = 120 sec
PUMP_WAIT_1 = 30s | PUMP_WAIT_2 = 15s | PUMP_VERIFY = 15s

BS_RATIO_NEW = 1.5 (<15min)
BS_RATIO_OLD = 1.3 (>=15min)

FALLEN_GIANT_H1 = 700 + mcap < $25K → REJECT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IRONCLAD RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PERM_BLACKLIST: Any token bought = NEVER buy again
2. Max 5 open positions
3. Position size: 0.1 SOL
4. Exchange: only raydium / pump / pumpswap
5. Fresh data only (GMGN primary, DexScreener backup)
6. Alert dedup: 300 seconds

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SYSTEM INFO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bot: /root/Dex-trading-bot/
Git: https://github.com/cploveless123/Dex-trading-bot.git
Telegram: @WilsonVultrBot (token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg)
Chat ID: 6402511249

Scanner: v7.7 OPTIMAL EXIT
