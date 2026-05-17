#!/bin/bash
# smart_money_filter.sh - Filter smart money buys with strict criteria
# Usage: cat smartmoney_raw.json | ./smart_money_filter.sh

# Current timestamp (2026-05-17 13:29 UTC = 1779024540)
CURRENT_TIME=1779024540

# Tier1 wallets (must follow)
TIER1_WALLETS=(
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3"
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE"
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f"
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V"
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4"
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5"
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN"
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS"
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir"
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C"
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX"
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT"
)

# Tier2 wallets (monitor)
TIER2_WALLETS=(
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY"
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x"
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz"
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U"
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go"
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw"
)

# Check if wallet is in tier1
is_tier1() {
    local wallet="$1"
    for w in "${TIER1_WALLETS[@]}"; do
        if [[ "$w" == "$wallet" ]]; then
            return 0
        fi
    done
    return 1
}

# Check if wallet is in tier2
is_tier2() {
    local wallet="$1"
    for w in "${TIER2_WALLETS[@]}"; do
        if [[ "$w" == "$wallet" ]]; then
            return 0
        fi
    done
    return 1
}

# Parse JSON and filter buys
python3 -c "
import json, sys

data = json.load(sys.stdin)
items = data.get('list', [])

# Current time
CURRENT_TIME = 1779024540

# Tier wallets
TIER1 = set([
    '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3',
    '65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE',
    '3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f',
    'H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V',
    '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4',
    '7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5',
    'MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN',
    'FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS',
    'tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir',
    '1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C',
    'Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX',
    'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT'
])

TIER2 = set([
    'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
    '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
    '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
    '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
    'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
    'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
])

# Filter only BUY trades from tracked wallets
buy_trades = []
for item in items:
    if item.get('side') == 'buy':
        maker = item.get('maker', '')
        if maker in TIER1 or maker in TIER2:
            buy_trades.append(item)

# Group by token to detect cluster signals
from collections import defaultdict
token_buys = defaultdict(list)
for trade in buy_trades:
    token_buys[trade['base_address']].append(trade)

# Output buy trades with metadata
output = {
    'buy_trades': buy_trades,
    'token_clusters': {},
    'stats': {
        'total_buys': len(buy_trades),
        'tier1_buys': sum(1 for t in buy_trades if t['maker'] in TIER1),
        'tier2_buys': sum(1 for t in buy_trades if t['maker'] in TIER2),
        'unique_tokens': len(token_buys)
    }
}

for token, trades in token_buys.items():
    makers = set(t['maker'] for t in trades)
    total_usd = sum(t.get('amount_usd', 0) for t in trades)
    output['token_clusters'][token] = {
        'count': len(trades),
        'unique_wallets': len(makers),
        'total_usd': total_usd,
        'trades': trades
    }

print(json.dumps(output, indent=2))
" 2>/dev/null || echo '{"error": "python3 not available"}'
