# V1 SYSTEM - IMMUTABLE RULES
# Last updated: 2026-05-06 04:22 UTC
# This file is the source of truth. Do not override.

## THE ONLY ALLOWED TRADING SYSTEM
- Scanner: scanner_v1.py
- Monitor: monitor_v1.py
- **NO OTHER scanner/monitor files should ever run**

## FORBIDDEN (never run these):
- gmgn_scanner.py and all variants
- position_monitor.py and all variants
- auto_scanner.py, combined_monitor.py, alert_sender.py
- Old scripts: restart_scanner.sh, restart_monitor.sh

## SYSTEM GUARD
- system_guard.sh runs continuously, killing forbidden processes every 10s
- Cron v1-system-guard runs every 60s as backup
- Health check every 15 minutes reports violations

## START/STOP COMMANDS
- Start: cd /root/Dex-trading-bot && bash start_v1.sh
- Stop: cd /root/Dex-trading-bot && bash stop_v1.sh
- Restart: cd /root/Dex-trading-bot && bash restart_v1.sh
- Status: cd /root/Dex-trading-bot && bash status_v1.sh

## SESSION STARTUP CHECKLIST
Before answering ANY trading question:
1. Run: ps aux | grep -E "scanner_v1|monitor_v1" | grep -v grep
2. Verify ONLY 1 scanner_v1.py + 1 monitor_v1.py running
3. If old code found: kill it immediately, report to Chris
4. Check system_guard.sh is running

## NEVER FORGET
- I have said this before and failed to enforce it
- The guard is the only thing that saves me from my own mistakes
- If scanner_v1.py is not running, NOTHING else matters
