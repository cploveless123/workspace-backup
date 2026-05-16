#!/usr/bin/env python3
"""
Smart Money Tracker - Filter & Report
Processes GMGN smart money data, fetches token info, applies strict filters.
"""

import json, sys, subprocess, time
from collections import defaultdict

TIER1 = {
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3", "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f", "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4", "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN", "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir", "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX", "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT"
}
TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY", "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz", "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go", "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw"
}

tracked = TIER1 | TIER2

def fetch_token_info(address):
    try:
        r = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", address, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)
    except Exception:
        return None

def format_report(passes, skip_counts, cluster_map):
    lines = []
    lines.append("🔥 SMART MONEY HIGH-CONVICTION REPORT")
    lines.append(f"📅 {time.strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")
    
    if not passes:
        lines.append("❌ NO HIGH-CONVICTION SIGNALS FOUND")
        lines.append("All tracked buys failed strict filters.")
    else:
        for p in passes:
            t = p['token']
            w = p['wallet']
            lines.append(f"{'='*50}")
            lines.append(f"🔥 HIGH-CONVICTION SIGNAL ({p['filters_passed']}/7 filters passed)")
            lines.append(f"[{p['time']}] {w['name']} — BUY {t['symbol']} ${p['amount_usd']:.2f} [{'FULL' if p['is_full'] else 'PARTIAL'}]")
            lines.append(f"📍 {t['address']}")
            lines.append(f"💰 MCAP: ${p['mcap']:,.0f} | Price: ${p['price']:.6f} | vs 1h High: {p['price_vs_high']:.1f}%")
            lines.append(f"⏱️ Age: {p['age_min']:.1f} min | Vol 5m: ${p['vol_5m']:,.0f} | Vol Trend: {p['vol_trend']:.1f}%")
            lines.append(f"📊 Buy Ratio: {p['buy_ratio']:.1%} | Holders: {p['holders']} | Bot Rate: {p['bot_rate']:.1f}%")
            lines.append(f"🔗 DexScreener: https://dexscreener.com/solana/{t['address']}")
            lines.append(f"💵 Buy: /buy {t['address']} 0.1")
            lines.append("")
            lines.append("⚡ CONVICTION INDICATORS:")
            lines.append(f"• Multiple wallets: {'YES' if p['cluster'] else 'NO'}")
            lines.append(f"• Large amount: {'YES' if p['large_amount'] else 'NO'}")
            lines.append(f"• Full position: {'YES' if p['is_full'] else 'NO'}")
            lines.append(f"• Fresh + high volume: {'YES' if p['fresh_highvol'] else 'NO'}")
            lines.append("")
    
    lines.append(f"📊 FILTERED OUT: {sum(skip_counts.values())} low-conviction buys skipped")
    if skip_counts.get('too_old', 0): lines.append(f"• Too old (>30min): {skip_counts['too_old']}")
    if skip_counts.get('low_volume', 0): lines.append(f"• Low volume (<$5K 5m): {skip_counts['low_volume']}")
    if skip_counts.get('vol_collapsed', 0): lines.append(f"• Volume collapsed: {skip_counts['vol_collapsed']}")
    if skip_counts.get('dumping', 0): lines.append(f"• Dumping (<70% of 1h high): {skip_counts['dumping']}")
    if skip_counts.get('distribution', 0): lines.append(f"• Distribution (buy ratio <60%): {skip_counts['distribution']}")
    if skip_counts.get('low_holders', 0): lines.append(f"• Low holders (<100): {skip_counts['low_holders']}")
    if skip_counts.get('high_bot', 0): lines.append(f"• High bot rate (>40%): {skip_counts['high_bot']}")
    if skip_counts.get('fetch_fail', 0): lines.append(f"• Token fetch failed: {skip_counts['fetch_fail']}")
    if skip_counts.get('not_tracked', 0): lines.append(f"• Wallet not in tracked list: {skip_counts['not_tracked']}")
    if skip_counts.get('sell_not_buy', 0): lines.append(f"• Sell transactions (not buys): {skip_counts['sell_not_buy']}")
    
    return "\n".join(lines)

def main():
    data = json.load(sys.stdin)
    txs = data.get("list", [])
    
    # Deduplicate by tx hash, keep only buys from tracked wallets
    seen_tx = set()
    buys = []
    for tx in txs:
        tx_hash = tx.get("transaction_hash")
        if tx_hash in seen_tx:
            continue
        seen_tx.add(tx_hash)
        
        if tx.get("side") != "buy":
            continue
        
        maker = tx.get("maker", "")
        if maker not in tracked:
            continue
        
        buys.append(tx)
    
    # Group by token for cluster detection
    token_wallets = defaultdict(set)
    for tx in buys:
        token_wallets[tx["base_address"]].add(tx["maker"])
    
    passes = []
    skip_counts = defaultdict(int)
    
    for tx in buys:
        addr = tx["base_address"]
        maker = tx["maker"]
        amount_usd = tx.get("amount_usd", 0)
        is_full = tx.get("is_open_or_close", 0) == 1
        
        # Fetch token info
        info = fetch_token_info(addr)
        if not info:
            skip_counts['fetch_fail'] += 1
            continue
        
        # Extract fields
        try:
            token_data = info.get("data", info)
            if isinstance(token_data, list) and token_data:
                token_data = token_data[0]
            
            # Age
            creation_ts = token_data.get("creation_timestamp", 0)
            age_min = (time.time() - creation_ts) / 60 if creation_ts else 999
            
            # Volume - handle nested price object
            price_data = token_data.get("price", {})
            if isinstance(price_data, dict):
                vol_5m = float(price_data.get("volume_5m", 0))
                vol_1h = float(price_data.get("volume_1h", 0))
                buys_1h = int(price_data.get("buys_1h", 0))
                sells_1h = int(price_data.get("sells_1h", 0))
                price = float(price_data.get("price", 0))
                price_1h_high = float(price_data.get("price_1h", price))  # Use price_1h as proxy for 1h high
            else:
                vol_5m = float(token_data.get("volume_5m", 0))
                vol_1h = float(token_data.get("volume_1h", 0))
                buys_1h = int(token_data.get("buys_1h", 0))
                sells_1h = int(token_data.get("sells_1h", 0))
                price = float(token_data.get("price", 0))
                price_1h_high = float(token_data.get("price_1h_high", price))
            
            vol_trend = (vol_5m / (vol_1h / 12) * 100) if vol_1h else 0
            price_vs_high = (price / price_1h_high * 100) if price_1h_high else 100
            buy_ratio = buys_1h / (buys_1h + sells_1h) if (buys_1h + sells_1h) else 0.5
            
            # Holders - check multiple locations
            holders = int(token_data.get("holder_count", 0))
            if not holders:
                stat = token_data.get("stat", {})
                if isinstance(stat, dict):
                    holders = int(stat.get("holder_count", 0))
            
            # Bot rate
            bot_rate = float(token_data.get("bot_degen_rate", 0))
            if not bot_rate:
                stat = token_data.get("stat", {})
                if isinstance(stat, dict):
                    bot_rate = float(stat.get("bot_degen_rate", 0))
            
            # MCAP
            mcap = float(token_data.get("market_cap", 0))
            
            filters_passed = 0
            if age_min < 30: filters_passed += 1
            if vol_5m > 5000: filters_passed += 1
            if vol_trend > 20: filters_passed += 1
            if price_vs_high > 70: filters_passed += 1
            if buy_ratio > 0.6: filters_passed += 1
            if holders > 100: filters_passed += 1
            if bot_rate < 40: filters_passed += 1
            
            # Apply skip logic
            if age_min >= 30:
                skip_counts['too_old'] += 1
                continue
            if vol_5m < 5000:
                skip_counts['low_volume'] += 1
                continue
            if vol_trend <= 20:
                skip_counts['vol_collapsed'] += 1
                continue
            if price_vs_high <= 70:
                skip_counts['dumping'] += 1
                continue
            if buy_ratio <= 0.6:
                skip_counts['distribution'] += 1
                continue
            if holders < 100:
                skip_counts['low_holders'] += 1
                continue
            if bot_rate >= 40:
                skip_counts['high_bot'] += 1
                continue
            
            # High-conviction indicators
            cluster = len(token_wallets[addr]) > 1
            large_amount = amount_usd >= 500
            fresh_highvol = age_min < 15 and vol_5m > 10000
            
            wallet_name = "TIER1" if maker in TIER1 else "TIER2"
            
            passes.append({
                "time": time.strftime("%H:%M", time.gmtime(tx.get("timestamp", 0))),
                "wallet": {"name": wallet_name, "address": maker},
                "token": {"symbol": tx.get("base_token", {}).get("symbol", "???"), "address": addr},
                "amount_usd": amount_usd,
                "is_full": is_full,
                "mcap": mcap,
                "price": price,
                "price_vs_high": price_vs_high,
                "age_min": age_min,
                "vol_5m": vol_5m,
                "vol_trend": vol_trend,
                "buy_ratio": buy_ratio,
                "holders": holders,
                "bot_rate": bot_rate,
                "filters_passed": filters_passed,
                "cluster": cluster,
                "large_amount": large_amount,
                "fresh_highvol": fresh_highvol
            })
            
        except Exception as e:
            skip_counts['fetch_fail'] += 1
            continue
    
    report = format_report(passes, dict(skip_counts), token_wallets)
    print(report)

if __name__ == "__main__":
    main()
