#!/usr/bin/env python3
"""
Smart Money Tracker - Filtered Analysis
Fetches token info for each buy and applies strict filters
"""

import json, sys, subprocess, time
from collections import defaultdict
from datetime import datetime

TIER1_WALLETS = {
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

TIER2_WALLETS = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": "T2",
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": "T2",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": "T2",
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": "T2",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": "T2",
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": "T2",
}

def get_token_info(address):
    """Fetch token info from GMGN"""
    try:
        result = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", address, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        return data.get("data", data)
    except Exception as e:
        print(f"  ERROR fetching {address}: {e}", file=sys.stderr)
        return None

def analyze_token(token_data, buy_tx):
    """Apply strict filters and return analysis"""
    if not token_data:
        return None, "NO_DATA"
    
    # Extract fields
    now = time.time()
    creation_ts = token_data.get("creation_timestamp", 0)
    age_min = (now - creation_ts) / 60 if creation_ts else 999
    
    volume_5m = token_data.get("volume_5m", 0)
    volume_1h = token_data.get("volume_1h", 0)
    volume_trend = (volume_5m / (volume_1h / 12)) if volume_1h > 0 else 0
    
    price = token_data.get("price", 0)
    price_1h_high = token_data.get("price_1h_high", 0)
    price_vs_high = (price / price_1h_high * 100) if price_1h_high > 0 else 0
    
    buys_1h = token_data.get("buys_1h", 0)
    sells_1h = token_data.get("sells_1h", 0)
    buy_ratio = buys_1h / (buys_1h + sells_1h) if (buys_1h + sells_1h) > 0 else 0
    
    holders = token_data.get("holder_count", token_data.get("holders", 0))
    bot_rate = token_data.get("bot_degen_rate", token_data.get("bot_rate", 0))
    
    mcap = token_data.get("market_cap", 0)
    symbol = token_data.get("symbol", buy_tx.get("base_token", {}).get("symbol", "?"))
    
    # Apply filters
    fails = []
    if age_min > 30: fails.append("TOO_OLD")
    if volume_5m < 5000: fails.append("LOW_VOLUME")
    if volume_trend < 0.20: fails.append("VOLUME_COLLAPSED")
    if price_vs_high < 70: fails.append("DUMPING")
    if buy_ratio < 0.6: fails.append("DISTRIBUTION")
    if holders < 100: fails.append("LOW_HOLDERS")
    if bot_rate > 40: fails.append("HIGH_BOT")
    
    analysis = {
        "symbol": symbol,
        "address": buy_tx["base_address"],
        "age_min": age_min,
        "volume_5m": volume_5m,
        "volume_1h": volume_1h,
        "volume_trend": volume_trend,
        "price": price,
        "price_1h_high": price_1h_high,
        "price_vs_high": price_vs_high,
        "buy_ratio": buy_ratio,
        "holders": holders,
        "bot_rate": bot_rate,
        "mcap": mcap,
        "fails": fails,
        "passed": len(fails) == 0,
    }
    
    return analysis, None

def main():
    # Read smart money data from stdin
    data = json.load(sys.stdin)
    txs = data.get("list", [])
    
    # Filter buys only, exclude WSOL
    buys = [t for t in txs if t.get("side") == "buy"]
    buys = [t for t in buys if t.get("base_token", {}).get("symbol") != "WSOL"]
    
    print(f"📊 SMART MONEY TRACKER - {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Total buys analyzed: {len(buys)}\n")
    
    # Track stats
    skip_reasons = defaultdict(int)
    high_conviction = []
    
    # Group by token for cluster detection
    by_token = defaultdict(list)
    for b in buys:
        by_token[b["base_address"]].append(b)
    
    # Process each unique token once (fetch info once)
    for addr, token_buys in by_token.items():
        symbol = token_buys[0]["base_token"]["symbol"]
        print(f"🔍 Analyzing {symbol} ({addr[:20]}...)")
        
        # Fetch token info
        token_data = get_token_info(addr)
        
        # Analyze
        analysis, err = analyze_token(token_data, token_buys[0])
        if err:
            print(f"  ❌ ERROR: {err}")
            skip_reasons["FETCH_ERROR"] += len(token_buys)
            continue
        
        if analysis["passed"]:
            # Check for cluster signal
            unique_wallets = set(t["maker"] for t in token_buys)
            is_cluster = len(unique_wallets) >= 2
            
            # Check for large buys
            large_buys = [t for t in token_buys if t.get("amount_usd", 0) >= 500]
            has_large = len(large_buys) > 0
            
            # Check for full positions
            full_positions = [t for t in token_buys if t.get("is_open_or_close") == 1]
            has_full = len(full_positions) > 0
            
            # Check fresh + high volume
            is_fresh_high_vol = analysis["age_min"] < 15 and analysis["volume_5m"] > 10000
            
            analysis["cluster"] = is_cluster
            analysis["large_buy"] = has_large
            analysis["full_position"] = has_full
            analysis["fresh_high_vol"] = is_fresh_high_vol
            analysis["buy_count"] = len(token_buys)
            analysis["wallets"] = list(unique_wallets)
            analysis["total_usd"] = sum(t.get("amount_usd", 0) for t in token_buys)
            
            high_conviction.append(analysis)
            print(f"  ✅ HIGH-CONVICTION ({len(token_buys)} buys, {len(unique_wallets)} wallets)")
        else:
            for reason in analysis["fails"]:
                skip_reasons[reason] += len(token_buys)
            print(f"  ❌ FILTERED OUT: {', '.join(analysis['fails'])}")
    
    print(f"\n{'='*60}")
    print(f"🔥 HIGH-CONVICTION SIGNALS: {len(high_conviction)} tokens")
    print(f"{'='*60}\n")
    
    for h in high_conviction:
        print(f"🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)")
        wallets_str = ", ".join([w[:16]+"..." for w in h["wallets"]])
        print(f"[20:34 UTC] {wallets_str} — BUY {h['symbol']} ${h['total_usd']:.2f}")
        print(f"📍 {h['address']}")
        print(f"💰 MCAP: ${h['mcap']:,.0f} | Price: ${h['price']:.8f} | vs 1h High: {h['price_vs_high']:.0f}%")
        print(f"⏱️ Age: {h['age_min']:.1f} min | Vol 5m: ${h['volume_5m']:,.0f} | Vol Trend: {h['volume_trend']*100:.0f}%")
        print(f"📊 Buy Ratio: {h['buy_ratio']*100:.0f}% | Holders: {h['holders']} | Bot Rate: {h['bot_rate']:.1f}%")
        print(f"🔗 DexScreener: https://dexscreener.com/solana/{h['address']}")
        print(f"💵 Buy: /buy {h['address']} 0.1")
        print(f"\n⚡ CONVICTION INDICATORS:")
        print(f"• Multiple wallets: {'YES' if h['cluster'] else 'NO'} ({h['buy_count']} buys)")
        print(f"• Large amount: {'YES' if h['large_buy'] else 'NO'}")
        print(f"• Full position: {'YES' if h['full_position'] else 'NO'}")
        print(f"• Fresh + high volume: {'YES' if h['fresh_high_vol'] else 'NO'}")
        print(f"{'='*60}\n")
    
    # Summary of filtered out
    total_skipped = sum(skip_reasons.values())
    print(f"📊 FILTERED OUT: {total_skipped} low-conviction buys skipped")
    reason_names = {
        "TOO_OLD": "Too old",
        "LOW_VOLUME": "Low volume",
        "VOLUME_COLLAPSED": "Volume collapsed",
        "DUMPING": "Dumping",
        "DISTRIBUTION": "Distribution",
        "LOW_HOLDERS": "Low holders",
        "HIGH_BOT": "High bot rate",
        "FETCH_ERROR": "Fetch error",
    }
    for reason, count in skip_reasons.items():
        print(f"• {reason_names.get(reason, reason)}: {count}")

if __name__ == "__main__":
    main()
