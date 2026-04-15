# USER.md - About Your Human

_Learn about the person you're helping. Update this as you go._

- **Name:** Chris
- **What to call them:** Chris
- **Pronouns:** 
- **Timezone:** UTC
- **Notes:** Building a DEX trading bot on Solana

## Active Project: TP5 COMPOUND STRATEGY
- **PRIMARY OBJECTIVE:** Turn 1 SOL → 100 SOL via compound TP5 winners
- **Strategy:** Identify winners early, let them run to +1000%, compound the remaining 10%

## TP5 Exit Strategy (v7.4 - Current)
| Level | Trigger | Sell % | Trail |
|-------|---------|--------|-------|
| TP1 | +50% | **HOLD** | 40% from peak |
| TP2 | +100% | 40% | 30% from peak |
| TP3 | +200% | 30% | 30% from peak |
| TP4 | +300% | 20% | 30% from peak |
| TP5 | +1000% | **ALL** | 20% from peak |
| Stop | -30% | ALL | — |

**Key:** TP1 is HOLD only — let winners ride with 40% trailing stop.

## Key Trading Rules
- Max 5 open positions at a time
- Position size: 0.1 SOL per trade
- Stop loss: -25% default, -15% for large winners (TP4+)
- Max daily loss: 0.3 SOL (stop if hit)
- Only pump.fun / raydium / pumpswap exchanges
- Pair address must end in "pump" for pump.fun/pumpswap
- Fresh data only (GMGN primary, DexScreener backup)
- IRONCLAD rules always enforced

## Current Status (2026-04-15)
- Balance: 1.0 SOL (reset)
- Record: 0W/0L (reset)
- Open: 0 positions (reset)
- Scanner: v7.4 CLEAN running with 15s cycle

## Exchange Rules
✅ pump.fun → pair_address must end in "pump"
✅ pumpswap → pair_address must end in "pump"  
✅ raydium → launchpad check only
❌ meteora ❌ orinoco ❌ lifinity ❌ saber → REJECTED

## Cooldown System
- **PUMP PATH** (chg1 >= +20%): 45s→30s→15s→BUY
  - Uses chg1 NOT chg5
- Young (<15min) + h1>+5% + chg5>-5%: 45s→BUY if chg5>=+2%
- Older (>=15min) + h1>+5% + chg5>-5%: 45s→BUY if chg5>=+2%
- Base (30s): chg1 > chg5_prev + 3% → BUY
- chg1<-5%: 15s rechecks until mcap>+5% from low→15s verify→BUY

## Alert System
- Throttle alerts: once per event (not per cycle)
- Same alert dedup: 5 minutes
- API failure alerts when GMGN or DexScreener fails
- Buy/Sell notifications with clickable links

## Backup System
- 30-minute cron job auto-restarts systems if down
- Backs up Dex-trading-bot and workspace every 30 min
- Telegram status every 30 min confirming all systems running

_(What do they care about? What projects are they working on? What annoys them? What makes them laugh? Build this over time.)_

---

The more you know, the better you can help. But remember — you're learning about a person, not building a dossier. Respect the difference.