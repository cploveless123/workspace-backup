#!/usr/bin/env python3
import json, subprocess, sys, os
from collections import defaultdict

# Current time: 2026-05-18 22:24 UTC 
CURRENT_TIME = 1779143040

# Tier wallets
TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3": "Cowboy🔶BNB",
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE": "T1",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f": "T1",
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V": "T1",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4": "Stigman",
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5": "T1",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN": "T1",
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS": "T1",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir": "T1",
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C": "T1",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX": "T1",
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT": "T1",
}
TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": "T2",
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": "T2",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": "T2",
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": "T2",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": "T2",
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": "T2",
}

# Read the JSON data from stdin
raw = sys.stdin.read()
data = json.loads(raw)
transactions = data.get("list", [])

# Extract unique BUY transactions from tracked wallets
seen_tokens = set()
buys = []
for tx in transactions:
    if tx.get("side") != "buy":
        continue
    maker = tx.get("maker", "")
    token_addr = tx.get("base_address", "")
    symbol = tx.get("base_token", {}).get("symbol", "UNKNOWN")
    
    # Skip non-tracked wallets
    tier = None
    wallet_name = None
    if maker in TIER1:
        tier = "TIER1"
        wallet_name = TIER1[maker]
    elif maker in TIER2:
        tier = "TIER2"
        wallet_name = TIER2[maker]
    
    if not tier:
        continue
    
    # Skip duplicates (same token from same wallet)
    key = f"{maker}:{token_addr}"
    if key in seen_tokens:
        continue
    seen_tokens.add(key)
    
    # Skip WSOL, USDC
    if symbol in ["WSOL", "USDC", "USDT"]:
        continue
    
    buys.append({
        "maker": maker,
        "wallet_name": wallet_name,
        "tier": tier,
        "token": symbol,
        "address": token_addr,
        "amount_usd": tx.get("amount_usd", 0),
        "is_open_or_close": tx.get("is_open_or_close", 0),
        "timestamp": tx.get("timestamp", 0),
        "tags": tx.get("maker_info", {}).get("tags", []),
    })

print(f"Found {len(buys)} unique BUY transactions from tracked wallets", file=sys.stderr)
print(f"Tokens to analyze: {[b['token'] for b in buys]}", file=sys.stderr)

# Now fetch token info for each
results = []
for buy in buys:
    addr = buy["address"]
    symbol = buy["token"]
    print(f"\n--- Fetching {symbol} ({addr}) ---", file=sys.stderr)
    
    try:
        cmd = f"gmgn-cli token info --chain sol --address {addr} --raw"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}", file=sys.stderr)
            continue
        
        token_data = json.loads(result.stdout)
        
        # Extract key metrics
        token_info = token_data.get("data", {})
        if not token_info:
            token_info = token_data
        
        # Get creation time
        creation_time = token_info.get("creation_timestamp", 0)
        if not creation_time:
            # Try pair data
            pairs = token_info.get("pairs", [{}])
            if pairs:
                creation_time = pairs[0].get("creation_timestamp", 0)
        
        age_minutes = (CURRENT_TIME - creation_time) / 60 if creation_time else 9999
        
        # Volume data
        vol_5m = token_info.get("volume_5m", 0) or token_info.get("volume5m", 0) or 0
        vol_1h = token_info.get("volume_1h", 0) or token_info.get("volume1h", 0) or 0
        
        # Price data
        price = token_info.get("price", 0) or 0
        high_1h = token_info.get("high_1h", 0) or token_info.get("high1h", 0) or 0
        
        # Buy/sell data
        buys_1h = token_info.get("buys_1h", 0) or token_info.get("buy1h", 0) or 0
        sells_1h = token_info.get("sells_1h", 0) or token_info.get("sell1h", 0) or 0
        
        # Holders
        holders = token_info.get("holder_count", 0) or token_info.get("holders", 0) or 0
        
        # Bot rate
        bot_rate = token_info.get("bot_degen_rate", 0) or token_info.get("botRate", 0) or 0
        
        # Market cap
        mcap = token_info.get("market_cap", 0) or token_info.get("mcap", 0) or 0
        
        # Calculate metrics
        vol_1h_avg_per_5m = vol_1h / 12 if vol_1h else 0
        volume_trend = (vol_5m / vol_1h_avg_per_5m * 100) if vol_1h_avg_per_5m else 0
        
        total_tx_1h = buys_1h + sells_1h
        buy_ratio = (buys_1h / total_tx_1h) if total_tx_1h else 0
        
        price_vs_high = (price / high_1h * 100) if high_1h else 100
        
        result = {
            **buy,
            "age_minutes": age_minutes,
            "vol_5m": vol_5m,
            "vol_1h": vol_1h,
            "volume_trend": volume_trend,
            "price": price,
            "high_1h": high_1h,
            "price_vs_high": price_vs_high,
            "buys_1h": buys_1h,
            "sells_1h": sells_1h,
            "buy_ratio": buy_ratio,
            "holders": holders,
            "bot_rate": bot_rate,
            "mcap": mcap,
            "raw_data": token_info,
        }
        results.append(result)
        
        print(f"  Age: {age_minutes:.1f}m | Vol5m: ${vol_5m:.0f} | VolTrend: {volume_trend:.1f}% | PriceVsHigh: {price_vs_high:.1f}% | BuyRatio: {buy_ratio:.2f} | Holders: {holders} | Bot: {bot_rate:.1f}%", file=sys.stderr)
        
    except Exception as e:
        print(f"ERROR fetching {symbol}: {e}", file=sys.stderr)
        continue

# Apply filters
PASSED = []
SKIPPED = defaultdict(int)
FILTER_REASONS = []

for r in results:
    reasons = []
    passed = True
    
    # Filter 1: Age < 30 min
    if r["age_minutes"] > 30:
        reasons.append("Too old")
        SKIPPED["too_old"] += 1
        passed = False
    
    # Filter 2: Volume 5m > $5,000
    if r["vol_5m"] < 5000:
        reasons.append("Low volume")
        SKIPPED["low_volume"] += 1
        passed = False
    
    # Filter 3: Volume trend > 20% of 1h average
    if r["volume_trend"] < 20:
        reasons.append("Volume collapsed")
        SKIPPED["volume_collapsed"] += 1
        passed = False
    
    # Filter 4: Price vs 1h high > 70%
    if r["price_vs_high"] < 70:
        reasons.append("Dumping")
        SKIPPED["dumping"] += 1
        passed = False
    
    # Filter 5: Buy/Sell ratio > 0.6
    if r["buy_ratio"] < 0.6:
        reasons.append("Distribution")
        SKIPPED["distribution"] += 1
        passed = False
    
    # Filter 6: Holders > 100
    if r["holders"] < 100:
        reasons.append("Low holders")
        SKIPPED["low_holders"] += 1
        passed = False
    
    # Filter 7: Bot rate < 40%
    if r["bot_rate"] > 40:
        reasons.append("High bot rate")
        SKIPPED["high_bot"] += 1
        passed = False
    
    if passed:
        PASSED.append(r)
    else:
        FILTER_REASONS.append({
            "token": r["token"],
            "reasons": reasons,
            "wallet": r["wallet_name"],
        })

# Check for cluster signals (multiple wallets buying same token)
token_wallets = defaultdict(list)
for r in results:
    token_wallets[r["address"]].append(r["maker"])

# Print report
print("\n" + "="*60)
print("SMART MONEY TRACKER REPORT")
print("="*60)
print(f"Time: 2026-05-18 22:24 UTC")
print(f"Total tracked buys analyzed: {len(results)}")
print(f"HIGH-CONVICTION signals: {len(PASSED)}")
print(f"Filtered out: {len(results) - len(PASSED)}")
print()

if PASSED:
    print("🔥 HIGH-CONVICTION SIGNALS:")
    print("-" * 60)
    for r in PASSED:
        # Check cluster
        wallets_for_token = token_wallets.get(r["address"], [])
        is_cluster = len(wallets_for_token) > 1
        
        # Check large amount
        is_large = r["amount_usd"] >= 500
        
        # Check full position
        is_full = r["is_open_or_close"] == 1
        
        # Check fresh + high volume
        is_fresh_highvol = r["age_minutes"] < 15 and r["vol_5m"] > 10000
        
        print(f"\n🔥 HIGH-CONVICTION SIGNAL (7 of 7 filters passed)")
        print(f"[{r['tier']}] {r['wallet_name']} — BUY {r['token']} ${r['amount_usd']:.2f} [{'FULL' if is_full else 'PARTIAL'}]")
        print(f"📍 {r['address']}")
        print(f"💰 MCAP: ${r['mcap']:,.0f} | Price: ${r['price']:.10f} | vs 1h High: {r['price_vs_high']:.1f}%")
        print(f"⏱️ Age: {r['age_minutes']:.1f} min | Vol 5m: ${r['vol_5m']:,.0f} | Vol Trend: {r['volume_trend']:.1f}%")
        print(f"📊 Buy Ratio: {r['buy_ratio']*100:.1f}% | Holders: {r['holders']:.0f} | Bot Rate: {r['bot_rate']:.1f}%")
        print(f"🔗 DexScreener: https://dexscreener.com/solana/{r['address']}")
        print(f"💵 Buy: /buy {r['address']} 0.1")
        print()
        print("⚡ CONVICTION INDICATORS:")
        print(f"• Multiple wallets: {'YES' if is_cluster else 'NO'} ({len(wallets_for_token)} wallets)")
        print(f"• Large amount: {'YES' if is_large else 'NO'}")
        print(f"• Full position: {'YES' if is_full else 'NO'}")
        print(f"• Fresh + high volume: {'YES' if is_fresh_highvol else 'NO'}")
        print("-" * 60)
else:
    print("❌ NO HIGH-CONVICTION SIGNALS FOUND")
    print()

print("\n📊 FILTERED OUT SUMMARY:")
print(f"• Total skipped: {len(results) - len(PASSED)}")
for reason, count in SKIPPED.items():
    print(f"• {reason}: {count}")

print("\n📋 DETAILED SKIP REASONS:")
for fr in FILTER_REASONS:
    print(f"  {fr['token']} ({fr['wallet']}): {', '.join(fr['reasons'])}")

# Save results
output = {
    "passed": PASSED,
    "skipped_count": dict(SKIPPED),
    "total_analyzed": len(results),
    "timestamp": CURRENT_TIME,
}
print(json.dumps(output, indent=2))
