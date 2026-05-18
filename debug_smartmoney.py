import json, sys

data = json.load(sys.stdin)
txs = data.get('list', [])
print(f'Total transactions: {len(txs)}')

# Count buys vs sells
buys = [t for t in txs if t.get('side') == 'buy']
sells = [t for t in txs if t.get('side') == 'sell']
print(f'Buys: {len(buys)}, Sells: {len(sells)}')

# Show unique makers
makers = set()
for t in txs:
    makers.add(t.get('maker', ''))
print(f'Unique makers: {len(makers)}')
print('Makers:', makers)

# Check if any tier wallets are present
TIER1 = ['6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3','65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE','3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f','H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V','8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4','7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5','MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN','FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS','tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir','1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C','Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX','BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT']
TIER2 = ['CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY','43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x','3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz','9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U','FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go','DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw']

tier1_found = [m for m in makers if m in TIER1]
tier2_found = [m for m in makers if m in TIER2]
print(f'TIER1 wallets found: {tier1_found}')
print(f'TIER2 wallets found: {tier2_found}')

# Show all buy transactions with maker info
print('\n--- ALL BUY TRANSACTIONS ---')
for t in buys[:10]:
    maker = t.get('maker', '')
    symbol = t.get('base_token', {}).get('symbol', 'UNKNOWN')
    amt = t.get('amount_usd', 0)
    tags = t.get('maker_info', {}).get('tags', [])
    print(f'  {maker[:20]}... | {symbol} | ${amt:.2f} | tags: {tags}')
