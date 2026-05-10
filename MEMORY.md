# MEMORY.md - Long-Term Memory

## V1 SYSTEM - THE ONLY ALLOWED TRADING SYSTEM
- Scanner: `scanner_v1.py` (v1.8 - WHALE + SNIPER_HEAVY + KOL + PHOENIX + DIP + SMART_DEGEN + PROVEN paths)
- Monitor: `monitor_v1.py` (v1.1 - TP1-5 + TIME STOP)
- **NO OTHER scanner/monitor files should ever run**

### Commands:
- Start: `cd /root/Dex-trading-bot && bash start_v1.sh`
- Stop: `cd /root/Dex-trading-bot && bash stop_v1.sh`
- Restart: `cd /root/Dex-trading-bot && bash restart_v1.sh`
- Status: `cd /root/Dex-trading-bot && bash status_v1.sh`

### FORBIDDEN (never run these - all moved to archive/):
- `gmgn_scanner.py` and ALL variants → archive/old_scanners/
- `position_monitor.py` and ALL variants → archive/old_monitors/
- `auto_scanner.py`, `combined_monitor.py`, `alert_sender.py` → archive/
- Old scripts: `restart_scanner.sh`, `restart_monitor.sh`

### System Guard:
- system_guard.sh running (PID checked every 10s)
- Kills any non-v1 scanner/monitor processes
- Health check every 15 minutes
- Strategy review every 4 hours

## Trading Bot Setup
- Location: `/root/Dex-trading-bot/`
- Git remote: https://github.com/cploveless123/Dex-trading-bot.git
- Workspace backup: https://github.com/cploveless123/workspace-backup.git
- Telegram alerts via @WilsonVultrBot (token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg)
- Chat ID: 6402511249 (Chris - "please grow good weed")

## APRIL 16 BABA STRATEGY - RESTORED 2026-04-25 19:08 UTC
Chris confirmed 75% WR during 06:00-10:00 UTC. I BROKE it after VPN switch. RESTORED.

### Buy Strategy (THE WINNING SETTINGS):
| Setting | April 16 | Broke To |
|--------|----------|----------|
| MIN_MCAP | $8,000 | $7,000 |
| MAX_MCAP | $20,000 | $30,000 |
| H1_MOMENTUM_MIN | 25% | 100% ← TOO HIGH! |
| H1_MOMENTUM_MAX | 200% | 600% | Scanner uses 600% (not 200%) |
| PUMP_MIN_AGE | 120s | 240s ← TOO LONG! |
| MIN_CHG5_FOR_BUY | 2% | 5% ← TOO RESTRICTIVE |
| PUMP_CHG1_THRESHOLD | 10% | 5% |

### Exit Plan (April 16):
| Level | Trigger | Sell % | Trail |
|-------|---------|--------|-------|
| TP1 | +50% | HOLD | 40% |
| TP2 | +100% | 35% | 30% |
| TP3 | +200% | 35% | 30% |
| TP4 | +300% | 20% | 30% |
| TP5 | +1000% | 10% | 15% |
| STOP | -25% | ALL | — |

### DO NOT CHANGE THESE SETTINGS

## Current Strategy: TP5 COMPOUND (v1.8)
Active system: scanner_v1.py + monitor_v1.py

### Scanner v1.8 Entry Paths (in priority order):
1. **SMART_DEGEN PATH**: Smart Degen > 0 + H1 200-500% + MCAP $10K-$20K + Age 90-3600s
   - Data: 192 trades, 53.1% WR, +3.80 SOL
2. **PROVEN PATH**: Age > 600s + H1 200-500% + MCAP $10K-$20K + (KOL Vol $200+ OR Snipers >= 1)
   - Data: Expected 60-65% WR (combined from profitable subsets)
3. **KOL PATH**: KOL Vol >= $200 + H1 > 30% + MCAP $5K-$50K + Age 90-3600s
   - Data: 54.5% WR at $200+ vol (changed from $50 on 2026-05-10 15:42 UTC)
4. **WHALE PATH**: Whale >= 3 + H1 > 75% + Vol > $10K
   - Data: 54.9% WR, +0.69 SOL
5. **SNIPER_HEAVY PATH**: Snipers >= 2 + H1 > 50% + chg1 > 5% + Vol > $10K
   - Data: 42.6% WR, +1.63 SOL
6. **PHOENIX PATH**: MCAP $3K-$8K + chg5 20-50% + chg1 < 20% + Vol > $5K + vol/mcap > 0.3
   - Dead token revival
7. **DIP PATH**: MCAP $8K-$20K + H1 > 100% + dipped -5% to -15% from ATH + chg1 recovering + Vol > $5K
   - Second chance entry

### DISABLED PATHS:
- PUMP path (was 34.7% WR, -36.18 SOL)
- UNKNOWN path (was 36.5% WR, -31.13 SOL)
- Signal score filtering (BACKWARD - filters OUT winners)

### Exit Plan (monitor_v1.py v1.1):
| Level | Trigger | Sell % | Trail |
|-------|---------|--------|-------|
| TP1 | +30% | HOLD | 45% from peak |
| TP2 | +100% | 40% | 45% from peak |
| TP3 | +200% | 30% | 40% from peak |
| TP4 | +300% | 20% | 35% from peak |
| TP5 | +1000% | HOLD | 25% from peak |
| STOP | -45% | ALL | EXIT |
| TIME STOP | >15min + pnl<0% | ALL | EXIT |

### Key Data from 5,790 Trades:
- Overall WR: 36.4%
- Overall PnL: -66.74 SOL
- Stop losses: 93% of all losses
- Winners are 25% OLDER than losers (194s vs 156s)
- Winners have 88% MORE snipers (2.2 vs 1.2)
- Winners have 10% LOWER chg1 (78.6% vs 87.4%) - cooler entry

### Filters:
- DYING TOKEN: chg1 < -5% OR chg5 < 0% → REJECT
- FALLEN GIANT: mcap < 20% of ATH → REJECT

### Entry Settings:
- Mcap: $3K-$20K (varies by path)
- Holders: ≥15
- Age: 90-3600s
- Position size: 0.1 SOL
- Max open: 9 positions

### IRONCLAD Rules:
- PERM_BLACKLIST: never buy again
- Fresh data only (GMGN primary, DexScreener backup)
- Alert dedup: 5 min

## Current Status (2026-05-10 16:25 UTC)
- Scanner: v1.8 running (PID 3217632)
- Monitor: v1.1 running (PID 1946476)
- Balance: -13.39 SOL
- Open: 1 position (LifeLog, -30% PnL)
- KOL volume filter: $200+ (active since 15:42 UTC)
- New paths: SMART_DEGEN + PROVEN (added 16:10 UTC)

## Git Commit History:
- 2026-05-10 16:25: Scanner v1.8 - Add SMART_DEGEN + PROVEN paths, KOL vol $200+ filter

## CRITICAL REMINDERS:
- NEVER make code changes without Chris's explicit approval
- ALWAYS follow SAFE_CHANGES.md exactly
- Backup first, test after, report before deploying
- Verify before speaking - check logs, code, data
- Show work with exact commands and outputs
- Double check all calculations and formulas
- No assumptions, no shortcuts, no lies
