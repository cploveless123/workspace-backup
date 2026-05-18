import json, sys
from collections import defaultdict

data = json.load(sys.stdin)
txs = data.get('list', [])

TIER1 = {
    '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3': 'Cowboy🔶BNB',
    '65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE': 'T1',
    '3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f': 'T1',
    'H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V': 'T1',
    '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4': 'Stigman',
    '7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5': 'T1',
    'MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN': 'T1',
    'FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS': 'T1',
    'tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir': 'T1',
    '1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C': 'T1',
    'Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX': 'T1',
    'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT': 'T1',
}
TIER2 = {
    'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY': 'T2',
    '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x': 'T2',
    '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz': 'T2',
    '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U': 'T2',
    'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go': 'T2',
    'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw': 'T2',
}

seen = set()
buys = []
for tx in txs:
    if tx.get('side') != 'buy':
        continue
    maker = tx.get('maker', '')
    token_addr = tx.get('base_address', '')
    symbol = tx.get('base_token', {}).get('symbol', 'UNKNOWN')
    
    tier = None
    wallet_name = None
    if maker in TIER1:
        tier = 'TIER1'
        wallet_name = TIER1[maker]
    elif maker in TIER2:
        tier = 'TIER2'
        wallet_name = TIER2[maker]
    
    if not tier:
        continue
    
    key = f'{maker}:{token_addr}'
    if key in seen:
        continue
    seen.add(key)
    
    if symbol in ['WSOL', 'USDC', 'USDT']:
        continue
    
    buys.append({
        'maker': maker,
        'wallet_name': wallet_name,
        'tier': tier,
        'token': symbol,
        'address': token_addr,
        'amount_usd': tx.get('amount_usd', 0),
        'is_open_or_close': tx.get('is_open_or_close', 0),
        'timestamp': tx.get('timestamp', 0),
    })

print(f'Found {len(buys)} unique tracked buys')
for b in buys:
    print(f"  {b['wallet_name']} ({b['tier']}) | {b['token']} | ${b['amount_usd']:.2f} | Full={b['is_open_or_close']}")
