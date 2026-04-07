import json

# Read trades
trades = []
try:
    with open('/root/Dex-trading-bot/trades/sim_trades.jsonl', 'r') as f:
        for line in f:
            if line.strip():
                trades.append(json.loads(line))
except:
    pass

# Wallet balance
wallet = json.load(open('/root/Dex-trading-bot/sim_wallet.json'))

# Format report
report = 'LAST 5 TRADES REPORT\n'
report += '================\n\n'

if not trades:
    report += 'No trades in current session.\n'
else:
    for t in trades[-5:]:
        report += 'Token: ' + t.get('token', 'UNKNOWN') + '\n'
        report += 'Entry MC: $' + str(t.get('entry_mcap', 'N/A')) + '\n'
        report += 'Exit MC: $' + str(t.get('exit_mcap', 'N/A')) + '\n'
        pnl = t.get('pnl_sol', 0)
        pct = t.get('net_pct', 0) * 100
        report += 'P&L: +%.4f SOL (+%.1f%%)\n' % (pnl, pct)
        report += 'Exit: ' + t.get('exit_reason', 'N/A') + '\n'
        ca = t.get('token_address', '')
        if ca:
            report += 'DexScreener: https://dexscreener.com/solana/' + ca + '\n'
            report += 'DexTools: https://www.dextools.io/solana/token/' + ca + '\n'
            report += 'PumpFun: https://pump.fun/' + ca + '\n'
        report += '\n'

report += 'Wallet: %.2f SOL, %.2f ETH, %.2f BASE\n' % (
    wallet['balances']['solana'],
    wallet['balances']['ethereum'],
    wallet['balances']['base']
)
report += 'Positions: %d\n' % len(wallet.get('positions', []))

print(report)