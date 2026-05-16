#!/usr/bin/env python3
"""
Smart Money Tracker - Filter and analyze smart money buys
"""
import json
import sys
from datetime import datetime

# Current time: 2026-05-16 02:22 UTC
current_time = 1778898120

# Tier 1 wallets (must follow)
TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3": "Cowboy🔶BNB",
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE": None,
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f": None,
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V": None,
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4": "Stigman",
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5": None,
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN": None,
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS": None,
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir": None,
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C": None,
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX": None,
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT": None,
}

# Tier 2 wallets (monitor)
TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": None,
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": None,
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": None,
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": None,
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": None,
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": None,
}

# Read the data
with open('/tmp/smartmoney_raw.json', 'r') as f:
    data = json.load(f)

transactions = data.get("list", [])

# Extract unique BUY transactions from tracked wallets
buy_txs = []
seen = set()

for tx in transactions:
    if tx.get("side") != "buy":
        continue
    
    maker = tx.get("maker", "")
    token_addr = tx.get("base_address", "")
    
    if maker not in TIER1 and maker not in TIER2:
        continue
    
    key = f"{maker}:{token_addr}"
    if key in seen:
        continue
    seen.add(key)
    
    buy_txs.append(tx)

print(f"Found {len(buy_txs)} unique BUY transactions from tracked wallets\n")

for tx in buy_txs:
    maker = tx.get("maker", "")
    token_addr = tx.get("base_address", "")
    symbol = tx.get("base_token", {}).get("symbol", "UNKNOWN")
    amount_usd = tx.get("amount_usd", 0)
    is_open = tx.get("is_open_or_close", 0)
    
    tier = "TIER1" if maker in TIER1 else "TIER2"
    name = TIER1.get(maker) or TIER2.get(maker) or maker[:8]
    
    print(f"{tier} | {name} | {symbol} | ${amount_usd:.2f} | {'FULL' if is_open else 'PARTIAL'} | {token_addr}")
