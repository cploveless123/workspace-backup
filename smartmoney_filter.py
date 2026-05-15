#!/usr/bin/env python3
"""
Smart Money Filtered Signal Generator
Parses gmgn-cli smartmoney output, fetches token info from DexScreener backup, applies quality filters.
"""
import json, sys, subprocess, time, os, urllib.request
from datetime import datetime

CURRENT_TIME = 1778872020  # Friday May 15 2026 ~19:07 UTC
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

def get_token_info_gmgn(addr):
    try:
        r = subprocess.run(
            ["gmgn-cli", "token", "info", "--chain", "sol", "--address", addr, "--raw"],
            capture_output=True, text=True, timeout=30
        )
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)
    except Exception as e:
        return None

def get_token_info_dexscreener(addr):
    """Fallback to DexScreener API for token info"""
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{addr}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        pairs = data.get("pairs", [])
        if not pairs:
            return None
        
        # Get best pair (highest liquidity)
        best = max(pairs, key=lambda p: float(p.get("liquidity", {}).get("usd", 0) or 0))
        
        # Build compatible structure
        vol5m = best.get("volume", {}).get("m5", 0)
        if not vol5m and best.get("volume"):
            # Try to estimate from h1
            vol1h = best.get("volume", {}).get("h1", 0)
            vol5m = vol1h / 12 if vol1h else 0
        
        price = float(best.get("priceUsd", 0) or 0)
        ath = float(best.get("priceUsd", 0) or 0)  # DexScreener doesn't have ATH, use current as proxy
        
        return {
            "token": {
                "token_create_time": 0,  # Unknown from DexScreener
                "holder_count": 0,  # Unknown
                "bot_degen_rate": 0,  # Unknown
            },
            "pair": {
                "volume_5m": vol5m,
                "price": price,
                "ath_price": ath,
                "market_cap": best.get("marketCap", 0) or best.get("fdv", 0) or 0,
                "liquidity": best.get("liquidity", {}).get("usd", 0),
            }
        }
    except Exception as e:
        return None

def get_token_info(addr):
    """Try GMGN first, fallback to DexScreener"""
    info = get_token_info_gmgn(addr)
    if info:
        return info, "GMGN"
    info = get_token_info_dexscreener(addr)
    if info:
        return info, "DEXSCREENER"
    return None, None

def format_time(ts):
    dt = datetime.utcfromtimestamp(ts)
    return dt.strftime("%H:%M:%S UTC")

def main():
    data = json.load(sys.stdin)
    trades = data.get("list", [])
    
    # Filter to BUY trades only, dedup by token+wallet (keep most recent)
    buys = {}
    for t in trades:
        if t.get("side") != "buy":
            continue
        key = (t["maker"], t["base_address"])
        if key not in buys or t["timestamp"] > buys[key]["timestamp"]:
            buys[key] = t
    
    buy_list = sorted(buys.values(), key=lambda x: x["timestamp"], reverse=True)
    
    passed = []
    skipped = []
    
    for t in buy_list:
        maker = t["maker"]
        addr = t["base_address"]
        sym = t.get("base_token", {}).get("symbol", "???")
        amt = t.get("amount_usd", 0)
        ts = t["timestamp"]
        
        tier = "TIER1" if maker in TIER1 else ("TIER2" if maker in TIER2 else "OTHER")
        
        print(f"\n{'='*60}")
        print(f"[{format_time(ts)}] {tier} {maker[:8]}... BUY {sym} ${amt:.2f}")
        print(f"  Token: {addr}")
        
        info, source = get_token_info(addr)
        if not info:
            skipped.append((t, "API_FAIL", "Could not fetch token info from GMGN or DexScreener"))
            print(f"  ❌ SKIP: API failure (both GMGN and DexScreener)")
            continue
        
        print(f"  Source: {source}")
        
        # Extract fields
        token = info.get("token", {})
        pair = info.get("pair", {})
        
        create_ts = token.get("token_create_time", 0)
        age_sec = CURRENT_TIME - create_ts if create_ts else 0
        age_min = age_sec / 60 if age_sec else 0
        
        vol_5m = pair.get("volume_5m", 0)
        holders = token.get("holder_count", 0)
        price = pair.get("price", 0)
        ath = token.get("ath_price", 0) or pair.get("ath_price", 0)
        bot_rate = token.get("bot_degen_rate", 0)
        mcap = pair.get("market_cap", 0)
        
        # Price vs ATH
        price_vs_ath = (price / ath * 100) if ath and ath > 0 else 100  # Assume 100% if no ATH data
        
        print(f"  Age: {age_min:.0f}min | Vol5m: ${vol_5m:.0f} | Holders: {holders}")
        print(f"  Price: ${price:.10f} | ATH: ${ath:.10f} | vs ATH: {price_vs_ath:.1f}%")
        print(f"  Bot Rate: {bot_rate}% | MCAP: ${mcap:.0f}")
        
        # Apply filters — skip unknowns gracefully
        reasons = []
        if age_min > 360 and create_ts > 0:  # > 6 hours (only if we know age)
            reasons.append(f"AGE({age_min:.0f}m>360)")
        if vol_5m < 2000:
            reasons.append(f"VOL(${vol_5m:.0f}<2K)")
        if holders < 100 and holders > 0:  # Only if we know holders
            reasons.append(f"HOLDERS({holders}<100)")
        if price_vs_ath < 50 and ath > 0:
            reasons.append(f"ATH({price_vs_ath:.1f}%<50%)")
        if bot_rate > 40 and bot_rate > 0:
            reasons.append(f"BOT({bot_rate}%>40%)")
        
        if reasons:
            skip_reason = " | ".join(reasons)
            skipped.append((t, skip_reason, info, source))
            print(f"  ❌ SKIP: {skip_reason}")
        else:
            # If from DexScreener, note that some data is estimated
            if source == "DEXSCREENER":
                print(f"  ⚠️  DexScreener fallback — age/holders/bot rate unknown, assuming OK")
            passed.append((t, info, tier, source))
            print(f"  ✅ PASS — QUALITY SIGNAL")
    
    # Final report
    print(f"\n{'='*60}")
    print(f"📊 SMART MONEY FILTERED REPORT")
    print(f"{'='*60}")
    print(f"Total buys checked: {len(buy_list)}")
    print(f"Quality signals (passed): {len(passed)}")
    print(f"Filtered out (skipped): {len(skipped)}")
    print(f"\n")
    
    if passed:
        print(f"🔥 QUALITY SIGNALS — {len(passed)} PASSED")
        print(f"-" * 60)
        for t, info, tier, source in passed:
            maker = t["maker"]
            addr = t["base_address"]
            sym = t.get("base_token", {}).get("symbol", "???")
            amt = t.get("amount_usd", 0)
            ts = t["timestamp"]
            
            token = info.get("token", {})
            pair = info.get("pair", {})
            create_ts = token.get("token_create_time", 0)
            age_min = (CURRENT_TIME - create_ts) / 60 if create_ts else 0
            vol_5m = pair.get("volume_5m", 0)
            holders = token.get("holder_count", 0)
            price = pair.get("price", 0)
            ath = token.get("ath_price", 0) or pair.get("ath_price", 0)
            bot_rate = token.get("bot_degen_rate", 0)
            mcap = pair.get("market_cap", 0)
            price_vs_ath = (price / ath * 100) if ath and ath > 0 else 100
            
            warning = ""
            if source == "DEXSCREENER":
                warning = "\n⚠️ Data from DexScreener (age/holders/bots unknown)"
            
            print(f"\n🔥 {tier} SIGNAL{warning}")
            print(f"[{format_time(ts)}] {maker[:16]}... — BUY {sym} ${amt:.2f}")
            print(f"📍 {addr}")
            print(f"💰 MCAP: ${mcap:.0f} | Price: ${price:.10f} | vs ATH: {price_vs_ath:.1f}%")
            print(f"⏱️ Age: {age_min:.0f} min | Vol 5m: ${vol_5m:.0f} | Holders: {holders}")
            print(f"🤖 Bot Rate: {bot_rate}%")
            print(f"🔗 DexScreener: https://dexscreener.com/solana/{addr}")
            print(f"💵 Buy: /buy {addr} 0.1")
    
    if skipped:
        print(f"\n\n📊 FILTERED OUT: {len(skipped)} junk buys skipped")
        print(f"-" * 60)
        # Group by reason
        reason_counts = {}
        for item in skipped:
            reason = item[1]
            for r in reason.split(" | "):
                reason_counts[r] = reason_counts.get(r, 0) + 1
        for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1]):
            print(f"  {reason}: {count}")
    
    print(f"\n{'='*60}")
    print(f"Report complete — {len(passed)} quality / {len(skipped)} filtered")

if __name__ == "__main__":
    main()
