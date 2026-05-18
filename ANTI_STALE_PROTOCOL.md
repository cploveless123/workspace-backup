# ANTI-STALE DATA PROTOCOL
# Created: 2026-05-18 01:56 UTC
# Purpose: Ensure I never report stale or incorrect data

## THE RULE
**Before answering ANY trading question:**
1. Run `ps aux | grep -E "scanner_v1|monitor_v1" | grep -v grep | wc -l`
2. Run `tail -20 scanner_v1.log`
3. Run `tail -20 monitor_v1.log`
4. Run `tail -5 trades/sim_trades.jsonl`
5. Run `cat sim_wallet.json` (or actual balance source)
6. Only THEN answer

## NEVER SAY
- "I think..."
- "From memory..."
- "Last time I checked..."
- "Probably..."

## ALWAYS SAY
- "Here's what the system shows right now..."
- "Live data at [timestamp]: ..."
- "Verified [X] seconds ago: ..."

## CONSEQUENCES
- Wrong information = lost trust
- Stale data = bad decisions
- Assumptions = broken systems

## REMINDER SYSTEM
- Cron job: Every 4 hours
- Message: "REMINDER: Never report on stale data..."
- Job ID: f0021da3-974b-494e-adcb-e3f0ed52d046

## IF IN DOUBT
- Say "Let me check live data first"
- Run the verification commands
- Report only what you verified

---
This is a binding protocol. Follow it or be silent.
