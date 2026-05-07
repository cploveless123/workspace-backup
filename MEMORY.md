# MEMORY.md - Long-Term Memory

## V1 SYSTEM - THE ONLY ALLOWED TRADING SYSTEM
- Scanner: `scanner_v1.py` (v1.6 - WHALE + ESTABLISHED + SNIPER + PUMP paths)
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

## Current Strategy: TP5 COMPOUND (v1.6)
Active system: scanner_v1.py + monitor_v1.py

### Scanner v1.6 Entry Paths:
- WHALE PATH: whale ≥ 5 + h1 > +100% + vol > $15K
- ESTABLISHED PATH: age > 600s + h1 > +100%
- SNIPER PATH: snipers ≥ 1 + h1 > +100% + vol > $10K
- PUMP PATH: h1 > +50% + chg5 > +10% + chg1 > +5%

### Filters:
- DYING TOKEN: chg1 < -5% OR chg5 < 0% → REJECT
- FALLEN GIANT: mcap < 20% of ATH → REJECT

### Entry Settings:
- Mcap: $5K-$20K
- Holders: ≥15
- H1: >+50% (pump) or >+100% (whale/established/sniper)
- Max open: 9 positions
- Position size: 0.1 SOL

### Exit Plan (monitor_v1.py v1.1):
| Level | Trigger | Sell % | Trail |
|-------|---------|--------|-------|
| TP1 | +30% | HOLD | 40% from peak |
| TP2 | +100% | 40% | 35% from peak |
| TP3 | +200% | 30% | 30% from peak |
| TP4 | +300% | 20% | 30% from peak |
| TP5 | +1000% | ALL | 15% from peak |
| STOP | -40% | ALL | EXIT |
| TIME STOP | >15min + pnl<0% | ALL | EXIT |

### Current Status (2026-05-07)
- Scanner: v1.6 running (PID 1209829)
- Monitor: v1.1 running (PID 1473861)
- System Guard: running (PID 1503986)
- Old files: moved to archive/
