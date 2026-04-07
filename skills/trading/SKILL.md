# Trading Skill - Wilson

## Purpose
Autonomous crypto trading on Solana with focus on:
- Riding whale moves (GMGN smart money)
- Early entry on low-mcap tokens
- Verified data only (no stale signals)

## Data Sources
- **GMGN.ai**: @gmgn Telegram channel for pump signals
- **DexScreener**: Real-time pair data
- **21 Whale Wallets**: Tracked for accumulation patterns
- **Pump.fun**: Token launches

## Trading Rules

### Entry Filters (ALL must pass)
1. **Age**: <12 hours old
2. **Liquidity**: >$5,000
3. **Volume 24h**: >$5,000
4. **Market Cap**: >$5,000 (VERIFIED on-chain)
5. **Holders**: >10
6. **Social**: Checkmarks (Twitter/Telegram/Website)
7. **Audit**: NoMint + Blacklist checks pass
8. **MCap Match**: Signal vs live API <20% discrepancy

### Whale Filters
- Net buy 1h: High = conviction
- Top holders <10%: Lower rug risk
- Dev action: Burn/lock = good sign

### Position Rules
- Max 5 open positions
- Max 0.1 SOL per trade (sim)
- Slippage: 20-50% for volatile

### Exit Rules
- +20%: Sell 75%
- +100%: Full exit
- -20%: Stop loss

## Verify Before Buy (CRITICAL)
1. Check signal timestamp (must be today)
2. Verify address format (base58, 43-44 chars)
3. Query DexScreener API for real-time mcap
4. Compare mcap to signal mcap (>20% diff = reject)
5. Check rugged.tw / rugcheck.xyz for safety

## Sources
- GMGN Telegram: @gmgn (ID: 7346593982)
- Bot: @WilsonVultrBot (token: 8767746012:AAEAUg-yCC8uZ-U2y-VBiuKS7qGm58XYQeg)
- Chat: 6402511249
