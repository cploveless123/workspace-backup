#!/usr/bin/env python3
"""Filter smart money buys and fetch token info for high-conviction signals."""
import json, subprocess, sys, time
from collections import defaultdict

TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3","65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f","H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4","7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN","FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir","1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX","BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT",
}
TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY","43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz","9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go","DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw",
}
ALL_TRACKED = TIER1 | TIER2

now = 1778940000  # ~2026-05-16 13:56 UTC

data = json.load(sys.stdin)
txns = data.get("list", [])

# Extract unique BUYs from tracked wallets (dedup by token+wallet)
unique_buys = []
seen = set()
for tx in txns:
    if tx.get("side") != "buy":
        continue
    maker = tx.get("maker", "")
    if maker not in ALL_TRACKED:
        continue
    token = tx.get("base_address", "")
    key = (maker, token)
    if key in seen:
        continue
    seen.add(key)
    unique_buys.append(tx)

print(f"Found {len(unique_buys)} unique tracked-wallet buys\n")

# Cluster detection
wallet_counts = defaultdict(int)
for tx in unique_buys:
    wallet_counts[tx["base_address"]] += 1

# Process each buy
passed = []
failed_counts = {"too_old":0,"low_vol":0,"vol_collapsed":0,"dumping":0,"distribution":0,"low_holders":0,"high_bot":0}

for tx in unique_buys:
    token_addr = tx["base_address"]
    symbol = tx.get("base_token", {}).get("symbol", "???")
    wallet = tx["maker"]
    amount_usd = tx.get("amount_usd", 0)
    is_open = tx.get("is_open_or_close", 0)
    
    # Fetch token info
    try:
        out = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", token_addr, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        info = json.loads(out.stdout) if out.returncode == 0 else {}
    except Exception as e:
        print(f"  SKIP {symbol}: API error ({e})")
        continue
    
    if not info:
        print(f"  SKIP {symbol}: no token data")
        continue
    
    # Extract fields (handle nested dicts from GMGN)
    ts = info.get("creation_timestamp", 0)
    if isinstance(ts, dict):
        ts = ts.get("value", 0)
    age_min = (now - ts) / 60 if ts else 999
    
    # Price data is nested under "price" key
    price_data = info.get("price", {})
    if not isinstance(price_data, dict):
        price_data = {}
    
    vol_5m = float(price_data.get("volume_5m", 0) or 0)
    vol_1h = float(price_data.get("volume_1h", 0) or 0)
    price = float(price_data.get("price", 0) or 0)
    high_1h = float(price_data.get("price_1h", 0) or price)
    buys_1h = int(price_data.get("buys_1h", 0) or 0)
    sells_1h = int(price_data.get("sells_1h", 0) or 0)
    
    holders = info.get("holder_count", 0)
    if isinstance(holders, dict):
        holders = holders.get("value", 0)
    bot_rate = info.get("bot_degen_rate", 0)
    if isinstance(bot_rate, dict):
        bot_rate = bot_rate.get("value", 0)
    mcap = info.get("market_cap", 0)
    if isinstance(mcap, dict):
        mcap = mcap.get("value", 0)
    if not mcap:
        # Calculate from price * supply
        supply = float(info.get("circulating_supply", 0) or 0)
        mcap = price * supply
    
    # Calculations
    vol_trend = (vol_5m / (vol_1h / 12)) if vol_1h > 0 else 0
    buy_ratio = (buys_1h / (buys_1h + sells_1h)) if (buys_1h + sells_1h) > 0 else 0
    price_vs_high = (price / high_1h * 100) if high_1h > 0 else 0
    
    # Apply filters
    reasons = []
    if age_min > 30:
        reasons.append("too_old")
    if vol_5m < 5000:
        reasons.append("low_vol")
    if vol_trend < 0.20:
        reasons.append("vol_collapsed")
    if price_vs_high < 70:
        reasons.append("dumping")
    if buy_ratio < 0.6:
        reasons.append("distribution")
    if holders < 100:
        reasons.append("low_holders")
    if bot_rate > 40:
        reasons.append("high_bot")
    
    if reasons:
        for r in reasons:
            failed_counts[r] += 1
        print(f"  SKIP {symbol}: {', '.join(reasons)}")
        continue
    
    # PASSED all filters
    cluster = wallet_counts.get(token_addr, 0) >= 2
    large = amount_usd >= 500
    fresh_highvol = age_min < 15 and vol_5m > 10000
    
    passed.append({
        "wallet": wallet,
        "symbol": symbol,
        "amount": amount_usd,
        "mcap": mcap,
        "age": age_min,
        "vol_5m": vol_5m,
        "vol_trend": vol_trend,
        "price_vs_high": price_vs_high,
        "buy_ratio": buy_ratio,
        "holders": holders,
        "bot_rate": bot_rate,
        "cluster": cluster,
        "large": large,
        "full": is_open == 1,
        "fresh_highvol": fresh_highvol,
        "token": token_addr,
    })
    print(f"  PASS {symbol}: age={age_min:.1f}m vol5m=${vol_5m:.0f} trend={vol_trend:.1%} ratio={buy_ratio:.1%} holders={holders} bot={bot_rate:.0f}%")

# Output report
print(f"\n{'='*60}")
print(f"HIGH-CONVICTION SIGNALS: {len(passed)} of {len(unique_buys)} buys passed all filters")
print(f"{'='*60}\n")

for p in passed:
    wname = p["wallet"][:8] + "..." + p["wallet"][-4:]
    full_tag = "[FULL]" if p["full"] else "[PARTIAL]"
    print(f"🔥 HIGH-CONVICTION SIGNAL ({len(passed)} of {len(unique_buys)} filters passed)")
    print(f"[13:56 UTC] {wname} — BUY {p['symbol']} ${p['amount']:.2f} {full_tag}")
    print(f"📍 {p['token']}")
    print(f"💰 MCAP: ${p['mcap']:,.0f} | Price: ${p.get('price',0):.10f} | vs 1h High: {p['price_vs_high']:.0f}%")
    print(f"⏱️ Age: {p['age']:.1f} min | Vol 5m: ${p['vol_5m']:,.0f} | Vol Trend: {p['vol_trend']:.0%}")
    print(f"📊 Buy Ratio: {p['buy_ratio']:.0%} | Holders: {p['holders']:,} | Bot Rate: {p['bot_rate']:.0f}%")
    print(f"🔗 DexScreener: https://dexscreener.com/solana/{p['token']}")
    print(f"💵 Buy: /buy {p['token']} 0.1")
    print(f"\n⚡ CONVICTION INDICATORS:")
    print(f"• Multiple wallets: {'YES' if p['cluster'] else 'NO'}")
    print(f"• Large amount: {'YES' if p['large'] else 'NO'}")
    print(f"• Full position: {'YES' if p['full'] else 'NO'}")
    print(f"• Fresh + high volume: {'YES' if p['fresh_highvol'] else 'NO'}")
    print()

print(f"📊 FILTERED OUT: {len(unique_buys)-len(passed)} low-conviction buys skipped")
print(f"• Too old: {failed_counts['too_old']}")
print(f"• Low volume: {failed_counts['low_vol']}")
print(f"• Volume collapsed: {failed_counts['vol_collapsed']}")
print(f"• Dumping: {failed_counts['dumping']}")
print(f"• Distribution: {failed_counts['distribution']}")
print(f"• Low holders: {failed_counts['low_holders']}")
print(f"• High bot rate: {failed_counts['high_bot']}")
