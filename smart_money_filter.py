#!/usr/bin/env python3
"""Smart Money Tracker - High-Conviction Signal Filter"""

import json
import subprocess
import sys
from collections import Counter, defaultdict

# Current time from cron job context
NOW = 1778901794

# TIER1 wallets
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

# TIER2 wallets
TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": None,
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": None,
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": None,
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": None,
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": None,
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": None,
}

def get_token_info(token_addr):
    """Fetch token info from GMGN API"""
    try:
        result = subprocess.run(
            ['gmgn-cli', 'token', 'info', '--chain', 'sol', '--address', token_addr, '--raw'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except Exception:
        return None

def analyze_trades(data):
    """Analyze smart money trades and filter for high-conviction signals"""
    trades = data.get('list', [])
    
    # Filter buys only
    buys = [t for t in trades if t.get('side') == 'buy']
    
    # Group by token for cluster detection
    token_wallets = defaultdict(set)
    for b in buys:
        token_wallets[b['base_address']].add(b['maker'])
    
    # Track results
    skip_reasons = Counter()
    passed = []
    
    for b in buys:
        wallet = b['maker']
        token_addr = b['base_address']
        amount_usd = b.get('amount_usd', 0)
        is_full = b.get('is_open_or_close', 0) == 1
        symbol = b.get('base_token', {}).get('symbol', 'UNKNOWN')
        
        # Check if tracked wallet
        is_tier1 = wallet in TIER1
        is_tier2 = wallet in TIER2
        if not is_tier1 and not is_tier2:
            skip_reasons['Untracked wallet'] += 1
            continue
        
        # Fetch token info
        token_data = get_token_info(token_addr)
        if not token_data:
            skip_reasons['API error'] += 1
            continue
        
        # Extract data
        token_info = token_data.get('data', token_data)
        price_data = token_info.get('price', {})
        stat_data = token_info.get('stat', {})
        
        # Age
        creation_ts = token_info.get('creation_timestamp', 0)
        age_min = (NOW - creation_ts) / 60 if creation_ts else 999
        
        # Volume
        vol_5m = float(price_data.get('volume_5m', 0) or 0)
        vol_1h = float(price_data.get('volume_1h', 0) or 0)
        vol_trend = (vol_5m / (vol_1h / 12)) * 100 if vol_1h else 0
        
        # Price vs high
        price = float(price_data.get('price', 0) or 0)
        high_1h = float(price_data.get('price_1h', 0) or 0)
        price_vs_high = (price / high_1h * 100) if high_1h else 0
        
        # Buy/sell ratio
        buys_1h = int(price_data.get('buys_1h', 0) or 0)
        sells_1h = int(price_data.get('sells_1h', 0) or 0)
        total_tx = buys_1h + sells_1h
        buy_ratio = (buys_1h / total_tx) if total_tx else 0
        
        # Holders
        holders = int(stat_data.get('holder_count', 0) or token_info.get('holder_count', 0) or 0)
        
        # Bot rate
        bot_rate = float(stat_data.get('bot_degen_rate', 0) or 0) * 100
        
        # Market cap
        mcap = float(token_info.get('market_cap', 0) or 0)
        
        # Apply STRICT filters
        if age_min >= 30:
            skip_reasons['Too old (>30min)'] += 1
            continue
        
        if vol_5m < 5000:
            skip_reasons['Low volume 5m (<$5K)'] += 1
            continue
        
        if vol_trend < 20:
            skip_reasons['Volume collapsed'] += 1
            continue
        
        if price_vs_high < 70:
            skip_reasons['Dumping (<70% of 1h high)'] += 1
            continue
        
        if buy_ratio < 0.6:
            skip_reasons['Distribution (buy ratio <0.6)'] += 1
            continue
        
        if holders < 100:
            skip_reasons['Low holders (<100)'] += 1
            continue
        
        if bot_rate >= 40:
            skip_reasons['High bot rate (>40%)'] += 1
            continue
        
        # Conviction indicators
        wallets_on_token = token_wallets.get(token_addr, set())
        is_cluster = len(wallets_on_token) >= 2
        is_large = amount_usd >= 500
        is_fresh_highvol = age_min < 15 and vol_5m > 10000
        
        wallet_label = TIER1.get(wallet) or TIER2.get(wallet) or wallet[:8]
        tier_label = "TIER1" if is_tier1 else "TIER2"
        
        passed.append({
            'wallet': wallet,
            'wallet_label': wallet_label,
            'tier': tier_label,
            'symbol': symbol,
            'amount_usd': amount_usd,
            'is_full': is_full,
            'token_addr': token_addr,
            'mcap': mcap,
            'price': price,
            'age_min': age_min,
            'vol_5m': vol_5m,
            'vol_trend': vol_trend,
            'price_vs_high': price_vs_high,
            'buy_ratio': buy_ratio,
            'holders': holders,
            'bot_rate': bot_rate,
            'is_cluster': is_cluster,
            'is_large': is_large,
            'is_fresh_highvol': is_fresh_highvol,
        })
    
    return passed, skip_reasons, len(buys)

def print_report(passed, skip_reasons, total_buys):
    """Print formatted report"""
    print("🔥 SMART MONEY TRACKER - HIGH-CONVICTION SIGNALS")
    print(f"📅 Time: 2026-05-16 03:22 UTC")
    print(f"📊 Total buys analyzed: {total_buys}")
    print(f"✅ High-conviction signals: {len(passed)}")
    print(f"❌ Filtered out: {total_buys - len(passed) - skip_reasons.get('Untracked wallet', 0) - skip_reasons.get('API error', 0)}")
    print()
    
    if passed:
        for p in passed:
            print(f"🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)")
            print(f"[{p['tier']}] {p['wallet_label']} — BUY {p['symbol']} ${p['amount_usd']:.2f} [{'FULL' if p['is_full'] else 'PARTIAL'}]")
            print(f"📍 {p['wallet']}")
            print(f"💰 MCAP: ${p['mcap']:,.0f} | Price: ${p['price']:.10f} | vs 1h High: {p['price_vs_high']:.1f}%")
            print(f"⏱️ Age: {p['age_min']:.1f} min | Vol 5m: ${p['vol_5m']:,.0f} | Vol Trend: {p['vol_trend']:.1f}%")
            print(f"📊 Buy Ratio: {p['buy_ratio']*100:.1f}% | Holders: {p['holders']:.0f} | Bot Rate: {p['bot_rate']:.1f}%")
            print(f"🔗 DexScreener: https://dexscreener.com/solana/{p['token_addr']}")
            print(f"💵 Buy: /buy {p['token_addr']} 0.1")
            print()
            print("⚡ CONVICTION INDICATORS:")
            print(f"• Multiple wallets: {'YES 🔥' if p['is_cluster'] else 'NO'}")
            print(f"• Large amount: {'YES 💰' if p['is_large'] else 'NO'}")
            print(f"• Full position: {'YES 🎯' if p['is_full'] else 'NO'}")
            print(f"• Fresh + high volume: {'YES ⚡' if p['is_fresh_highvol'] else 'NO'}")
            print("-" * 60)
            print()
    else:
        print("❌ NO HIGH-CONVICTION SIGNALS FOUND")
        print()
    
    print("📊 FILTERED OUT SUMMARY:")
    for reason, count in skip_reasons.most_common():
        print(f"• {reason}: {count}")

if __name__ == "__main__":
    # Read JSON from stdin
    data = json.load(sys.stdin)
    passed, skip_reasons, total_buys = analyze_trades(data)
    print_report(passed, skip_reasons, total_buys)
