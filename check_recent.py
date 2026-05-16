#!/usr/bin/env python3
import json, datetime, sys

data = json.load(open('/tmp/smartmoney.json'))
txs = data.get('list', [])

now = datetime.datetime.now(datetime.timezone.utc).timestamp()

print('Recent smart money buys (last 30 min):')
print('='*60)

for tx in txs:
    if tx.get('side') == 'buy':
        ts = tx.get('timestamp', 0)
        age_min = (now - ts) / 60
        if age_min < 30:
            symbol = tx.get('base_token', {}).get('symbol', 'UNKNOWN')
            addr = tx.get('base_address', '')
            amount = tx.get('amount_usd', 0)
            maker = tx.get('maker', '')
            is_open = tx.get('is_open_or_close', 0)
            open_str = 'FULL' if is_open else 'PARTIAL'
            print(f'{age_min:.0f}m ago | {maker[:16]}... | BUY {symbol} ${amount:.2f} [{open_str}]')
            print(f'  Address: {addr}')
            print()

print()
print('All buys sorted by recency:')
print('='*60)

buys = [(tx, (now - tx.get('timestamp', 0))/60) for tx in txs if tx.get('side') == 'buy']
buys.sort(key=lambda x: x[1])

for tx, age in buys[:20]:
    symbol = tx.get('base_token', {}).get('symbol', 'UNKNOWN')
    addr = tx.get('base_address', '')
    amount = tx.get('amount_usd', 0)
    maker = tx.get('maker', '')
    is_open = tx.get('is_open_or_close', 0)
    open_str = 'FULL' if is_open else 'partial'
    print(f'{age:.0f}m | {symbol:12} | ${amount:8.2f} | {maker[:12]}... | {open_str}')
