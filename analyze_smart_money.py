import json
import subprocess
import sys

# Read the smart money data from stdin
data = json.load(sys.stdin)

# Get current time from system or use a reasonable default
import time
current_time = int(time.time())

# Extract unique BUY transactions (filter out sells, WSOL, cbBTC)
unique_buys = {}
for tx in data.get("list", []):
    if tx["side"] != "buy":
        continue
    addr = tx["base_address"]
    # Skip non-meme tokens
    if addr in ["So11111111111111111111111111111111111111112", "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij"]:
        continue
    # Keep the most recent buy per token
    if addr not in unique_buys or tx["timestamp"] > unique_buys[addr]["timestamp"]:
        unique_buys[addr] = tx

# Tier wallets for reference
TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3": "Cowboy🔶BNB",
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE": "+$5K, 62.7% WR",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f": "+$6.4K, 56.7% WR",
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V": "+$27K, consistent",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4": "Stigman, +$8.3K, 44% WR",
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5": "+$4.9K, 67.7% WR",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN": "+$2.9K, 69.9% WR",
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS": "+$4.5K, 43% WR",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir": "+$3.7K, 42% WR",
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C": "+$4.6K, 43% WR",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX": "+$3.7K, 70% WR",
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT": "+$1.7K, 66% WR",
}

TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": "+$847, 44.6% WR",
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": "+$114",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": "+$5.7K, 47.7% WR",
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": "+$4.4K, 53.1% WR",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": "+$2K, 35.5% WR",
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": "+$3.9K, 39.1% WR",
}

print(f"📊 SMART MONEY SCAN — {len(unique_buys)} unique buy tokens found")
print("="*60)

# Count buys per token for cluster detection
token_buyers = {}
for tx in data.get("list", []):
    if tx["side"] != "buy":
        continue
    addr = tx["base_address"]
    if addr not in token_buyers:
        token_buyers[addr] = set()
    token_buyers[addr].add(tx["maker"])

# Fetch token info for each
results = []
skip_counts = {"too_old": 0, "low_volume": 0, "volume_collapsed": 0, "dumping": 0, "distribution": 0, "low_holders": 0, "high_bot": 0}

for addr, tx in unique_buys.items():
    symbol = tx["base_token"]["symbol"]
    wallet = tx["maker"]
    
    # Check wallet tier
    tier = "TIER1" if wallet in TIER1 else ("TIER2" if wallet in TIER2 else "OTHER")
    wallet_label = TIER1.get(wallet) or TIER2.get(wallet) or ""
    
    # Fetch token info
    try:
        result = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", addr, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        token_data = json.loads(result.stdout) if result.stdout else {}
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
        continue
    
    if not token_data:
        continue
    
    # Extract data - handle nested structures properly
    creation_time = token_data.get("creation_timestamp", 0)
    if isinstance(creation_time, dict):
        creation_time = creation_time.get("value", 0)
    age_min = (current_time - creation_time) / 60 if creation_time else 999
    
    # Price data is nested under "price" key
    price_data = token_data.get("price", {})
    if not price_data:
        price_data = token_data  # fallback
    
    vol_5m = float(price_data.get("volume_5m", 0)) if price_data else 0
    if isinstance(vol_5m, dict):
        vol_5m = float(vol_5m.get("value", 0))
    vol_1h = float(price_data.get("volume_1h", 0)) if price_data else 0
    if isinstance(vol_1h, dict):
        vol_1h = float(vol_1h.get("value", 0))
    vol_trend = (vol_5m / (vol_1h / 12)) * 100 if vol_1h > 0 else 0
    
    price = float(price_data.get("price", 0)) if price_data else 0
    if isinstance(price, dict):
        price = float(price.get("value", 0))
    # Get 1h high from price history - use price_1h as proxy if no high_1h
    high_1h = float(price_data.get("price_1h", price)) if price_data else price
    if isinstance(high_1h, dict):
        high_1h = float(high_1h.get("value", price))
    # If price_1h is lower than current, current might be the high
    if high_1h < price:
        high_1h = price
    price_vs_high = (price / high_1h) * 100 if high_1h > 0 else 100
    
    buys_1h = int(price_data.get("buys_1h", 0)) if price_data else 0
    if isinstance(buys_1h, dict):
        buys_1h = int(buys_1h.get("value", 0))
    sells_1h = int(price_data.get("sells_1h", 0)) if price_data else 0
    if isinstance(sells_1h, dict):
        sells_1h = int(sells_1h.get("value", 0))
    buy_ratio = buys_1h / (buys_1h + sells_1h) if (buys_1h + sells_1h) > 0 else 0
    
    # Holder count from top level or stat
    holders = token_data.get("holder_count", 0)
    if isinstance(holders, dict):
        holders = holders.get("value", 0)
    if not holders:
        stat = token_data.get("stat", {})
        holders = stat.get("holder_count", 0) if stat else 0
    
    # Bot rate from stat
    bot_rate = 0
    stat = token_data.get("stat", {})
    if stat:
        bot_rate = float(stat.get("bot_degen_rate", 0)) if isinstance(stat.get("bot_degen_rate"), (int, float, str)) else 0
    
    mcap = token_data.get("market_cap", 0)
    if isinstance(mcap, dict):
        mcap = mcap.get("value", 0)
    if not mcap:
        # Calculate from price * supply
        supply = token_data.get("total_supply", "0")
        try:
            supply_num = float(supply)
            mcap = price * supply_num
        except:
            mcap = 0
    
    # Apply filters
    filters_passed = 0
    filters_total = 7
    
    # 1. Age < 30 min
    if age_min < 30:
        filters_passed += 1
    else:
        skip_counts["too_old"] += 1
        
    # 2. Volume 5m > $5K
    if vol_5m > 5000:
        filters_passed += 1
    else:
        skip_counts["low_volume"] += 1
        
    # 3. Volume trend > 20%
    if vol_trend > 20:
        filters_passed += 1
    else:
        skip_counts["volume_collapsed"] += 1
        
    # 4. Price vs 1h high > 70%
    if price_vs_high > 70:
        filters_passed += 1
    else:
        skip_counts["dumping"] += 1
        
    # 5. Buy ratio > 0.6
    if buy_ratio > 0.6:
        filters_passed += 1
    else:
        skip_counts["distribution"] += 1
        
    # 6. Holders > 100
    if holders > 100:
        filters_passed += 1
    else:
        skip_counts["low_holders"] += 1
        
    # 7. Bot rate < 40%
    if bot_rate < 40:
        filters_passed += 1
    else:
        skip_counts["high_bot"] += 1
    
    # Check conviction indicators
    num_buyers = len(token_buyers.get(addr, set()))
    cluster = num_buyers >= 2
    large_amount = tx["amount_usd"] >= 500
    full_position = tx["is_open_or_close"] == 1
    fresh_high_vol = age_min < 15 and vol_5m > 5000
    
    result = {
        "pass": filters_passed == filters_total,
        "filters_passed": filters_passed,
        "symbol": symbol,
        "address": addr,
        "wallet": wallet,
        "wallet_label": wallet_label,
        "tier": tier,
        "amount_usd": tx["amount_usd"],
        "mcap": mcap,
        "price": price,
        "age_min": age_min,
        "vol_5m": vol_5m,
        "vol_trend": vol_trend,
        "price_vs_high": price_vs_high,
        "buy_ratio": buy_ratio,
        "holders": holders,
        "bot_rate": bot_rate,
        "cluster": cluster,
        "large_amount": large_amount,
        "full_position": full_position,
        "fresh_high_vol": fresh_high_vol,
        "num_buyers": num_buyers,
        "is_open_or_close": tx["is_open_or_close"],
    }
    results.append(result)

# Sort: passed first, then by amount
results.sort(key=lambda x: (-x["pass"], -x["amount_usd"]))

# Print HIGH-CONVICTION signals
high_conviction = [r for r in results if r["pass"]]
if high_conviction:
    print(f"\n🔥 HIGH-CONVICTION SIGNALS: {len(high_conviction)} tokens passed ALL filters\n")
    for r in high_conviction:
        print(f"🔥 HIGH-CONVICTION ({r['filters_passed']}/7 filters passed)")
        print(f"[{r['tier']}] {r['wallet'][:8]}...{r['wallet'][-8:]} — BUY {r['symbol']} ${r['amount_usd']:.2f} [{'FULL' if r['is_open_or_close'] else 'PARTIAL'}]")
        print(f"📍 {r['address']}")
        print(f"💰 MCAP: ${r['mcap']:,.0f} | Price: ${float(r.get('price', 0)):.10f} | vs 1h High: {r['price_vs_high']:.1f}%")
        print(f"⏱️ Age: {r['age_min']:.1f} min | Vol 5m: ${r['vol_5m']:,.0f} | Vol Trend: {r['vol_trend']:.1f}%")
        print(f"📊 Buy Ratio: {r['buy_ratio']*100:.1f}% | Holders: {r['holders']} | Bot Rate: {r['bot_rate']:.1f}%")
        print(f"🔗 DexScreener: https://dexscreener.com/solana/{r['address']}")
        print(f"💵 Buy: /buy {r['address']} 0.1")
        print(f"\n⚡ CONVICTION INDICATORS:")
        print(f"• Multiple wallets ({r['num_buyers']} buyers): {'YES' if r['cluster'] else 'NO'}")
        print(f"• Large amount: {'YES' if r['large_amount'] else 'NO'}")
        print(f"• Full position: {'YES' if r['full_position'] else 'NO'}")
        print(f"• Fresh + high volume: {'YES' if r['fresh_high_vol'] else 'NO'}")
        print("-"*50)
else:
    print("\n❌ NO HIGH-CONVICTION SIGNALS — All tokens failed at least one filter\n")
    # Show closest candidates
    close_candidates = [r for r in results if r["filters_passed"] >= 5]
    if close_candidates:
        print(f"📌 CLOSEST CANDIDATES ({len(close_candidates)} tokens with 5-6/7 filters passed):\n")
        for r in close_candidates:
            print(f"  ⚠️ {r['symbol']} | {r['filters_passed']}/7 passed | ${r['amount_usd']:.2f} | {r['age_min']:.1f}min | {r['tier']}")
            # Show which filters failed
            fails = []
            if r['age_min'] >= 30: fails.append("age")
            if r['vol_5m'] <= 5000: fails.append("volume_5m")
            if r['vol_trend'] <= 20: fails.append("vol_trend")
            if r['price_vs_high'] <= 70: fails.append("price_vs_high")
            if r['buy_ratio'] <= 0.6: fails.append("buy_ratio")
            if r['holders'] <= 100: fails.append("holders")
            if r['bot_rate'] >= 40: fails.append("bot_rate")
            print(f"     Failed: {', '.join(fails)}")
            print(f"     Vol 5m: ${r['vol_5m']:,.0f} | Buy Ratio: {r['buy_ratio']*100:.1f}% | Holders: {r['holders']} | Bot: {r['bot_rate']:.1f}%")
            print(f"     https://dexscreener.com/solana/{r['address']}")
            print()

# Print filtered out summary
total_skipped = len(results) - len(high_conviction)
print(f"\n📊 FILTERED OUT: {total_skipped} low-conviction buys skipped")
for reason, count in skip_counts.items():
    if count > 0:
        label = {"too_old": "Too old (>30min)", "low_volume": "Low volume (<$5K 5m)", 
                 "volume_collapsed": "Volume collapsed", "dumping": "Dumping (<70% of 1h high)",
                 "distribution": "Distribution (buy ratio <0.6)", "low_holders": "Low holders (<100)",
                 "high_bot": "High bot rate (>40%)"}[reason]
        print(f"• {label}: {count}")

# Print all tokens with their filter status for reference
print(f"\n📋 ALL TOKENS SCANNED:")
for r in results:
    status = "✅ PASS" if r["pass"] else f"❌ FAIL ({r['filters_passed']}/7)"
    print(f"  {status} | {r['symbol']} | ${r['amount_usd']:.2f} | {r['age_min']:.1f}min | {r['tier']}")
