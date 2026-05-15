#!/usr/bin/env python3
"""
Smart Money Tracker - Filtered Signal Generator
Run: python3 /root/.openclaw/workspace/scripts/smart_money_tracker.py

Fetches smart money trades from GMGN, filters for tracked wallet buys,
applies quality filters, and reports only passing signals.
"""
import json
import subprocess
import sys
import time

# === CONFIGURATION ===
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

TIER2 = {
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY": None,
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x": None,
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz": None,
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U": None,
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go": None,
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw": None,
}

# === FILTERS ===
FILTER_AGE_HOURS = 6
FILTER_VOLUME_5M = 2000
FILTER_HOLDERS = 100
FILTER_ATH_PCT = 50
FILTER_BOT_RATE = 0.40  # API returns decimal (0.4815 = 48.15%)

ALL_TIERS = {**TIER1, **TIER2}

def safe_float(v):
    if not v: return 0.0
    if isinstance(v, (int, float)): return float(v)
    if isinstance(v, str): return float(v)
    return 0.0

def fetch_smartmoney():
    """Fetch smart money trades from GMGN."""
    cmd = "gmgn-cli track smartmoney --chain sol --limit 100 --raw"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"ERROR fetching smart money: {result.stderr}", file=sys.stderr)
        return None
    return json.loads(result.stdout.strip())

def fetch_token_info(address):
    """Fetch token info from GMGN."""
    cmd = f"gmgn-cli token info --chain sol --address {address} --raw"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout.strip())

def extract_buys(trades_data):
    """Extract unique BUYs from tracked wallets."""
    trades = trades_data.get('list', [])
    buys = []
    seen_tokens = set()
    
    for t in trades:
        if t.get('side') != 'buy':
            continue
        maker = t.get('maker', '')
        if maker not in ALL_TIERS:
            continue
        token = t.get('base_address', '')
        if token in seen_tokens:
            continue
        seen_tokens.add(token)
        buys.append({
            'maker': maker,
            'token': token,
            'symbol': t.get('base_token', {}).get('symbol', '?'),
            'amount_usd': t.get('amount_usd', 0),
            'is_open_or_close': t.get('is_open_or_close', 0),
            'timestamp': t.get('timestamp', 0),
        })
    return buys

def apply_filters(token_info, now):
    """Apply quality filters to token info."""
    info = token_info or {}
    token = info.get('token', info)
    
    # 1. Age
    create_time = token.get('creation_timestamp', 0)
    age_sec = now - create_time if create_time else 999999
    age_min = age_sec / 60
    age_ok = age_sec < FILTER_AGE_HOURS * 3600
    
    # 2. Volume 5m
    vol_5m = token.get('volume_5m', 0)
    if not vol_5m and 'price' in info and isinstance(info['price'], dict):
        vol_5m = info['price'].get('volume_5m', 0)
    if not vol_5m and 'price' in token and isinstance(token['price'], dict):
        vol_5m = token['price'].get('volume_5m', 0)
    vol_5m = safe_float(vol_5m)
    vol_ok = vol_5m >= FILTER_VOLUME_5M
    
    # 3. Holders
    holders = token.get('holder_count', 0)
    if not holders and 'stat' in info:
        holders = info['stat'].get('holder_count', 0)
    holders_ok = holders >= FILTER_HOLDERS
    
    # 4. Price vs ATH
    price = token.get('price', 0)
    ath = token.get('ath_price', 0)
    if (not price or isinstance(price, dict)) and 'price' in info and isinstance(info['price'], dict):
        price = info['price'].get('price', 0)
    if (not price or isinstance(price, dict)) and 'price' in token and isinstance(token['price'], dict):
        price = token['price'].get('price', 0)
    price = safe_float(price)
    ath = safe_float(ath)
    ath_pct = (price / ath * 100) if ath and price else 100
    ath_ok = ath_pct >= FILTER_ATH_PCT
    
    # 5. Bot rate
    bot_rate = token.get('bot_degen_rate', 0)
    if not bot_rate and 'stat' in info:
        bot_rate = info['stat'].get('bot_degen_rate', 0)
    bot_rate = safe_float(bot_rate)
    bot_ok = bot_rate < FILTER_BOT_RATE
    
    filters_passed = sum([age_ok, vol_ok, holders_ok, ath_ok, bot_ok])
    
    return {
        'age_ok': age_ok, 'age_min': age_min, 'age_sec': age_sec,
        'vol_ok': vol_ok, 'vol_5m': vol_5m,
        'holders_ok': holders_ok, 'holders': holders,
        'ath_ok': ath_ok, 'ath_pct': ath_pct,
        'bot_ok': bot_ok, 'bot_rate': bot_rate,
        'passed': filters_passed,
    }

def generate_report(passed, failed, now):
    """Generate formatted report."""
    lines = []
    lines.append(f"🔥 SMART MONEY TRACKER - {time.strftime('%H:%M UTC', time.gmtime(now))}")
    lines.append('')
    
    if passed:
        lines.append(f'✅ QUALITY SIGNALS: {len(passed)} of {len(passed)+len(failed)} passed all filters')
        lines.append('')
        for b in passed:
            maker = b['maker']
            name = ALL_TIERS.get(maker)
            f = b['filters']
            info = b['info']
            token = info.get('token', info)
            
            price_val = safe_float(token.get('price', 0))
            supply = safe_float(token.get('total_supply', 0))
            mcap = price_val * supply
            
            price_str = token.get('price', 0)
            if not price_str or isinstance(price_str, dict):
                if 'price' in info and isinstance(info['price'], dict):
                    price_str = info['price'].get('price', 0)
            price_str = str(price_str) if price_str else '0'
            
            full_partial = '[FULL]' if b['is_open_or_close'] else '[PARTIAL]'
            wallet_label = name if name else maker[:8] + '...'
            
            lines.append(f'🔥 QUALITY SIGNAL ({f["passed"]} of 5 filters passed)')
            lines.append(f"[{time.strftime('%H:%M', time.gmtime(b['timestamp']))}] {wallet_label} — BUY {b['symbol']} ${b['amount_usd']:.2f} {full_partial}")
            lines.append(f"📍 {b['token']}")
            lines.append(f"💰 MCAP: ${mcap:,.0f} | Price: ${price_str} | vs ATH: {f['ath_pct']:.1f}%")
            lines.append(f"⏱️ Age: {f['age_min']:.0f} min | Vol 5m: ${f['vol_5m']:,.0f} | Holders: {f['holders']}")
            lines.append(f"🤖 Bot Rate: {f['bot_rate']*100:.1f}%")
            lines.append(f"🔗 DexScreener: https://dexscreener.com/solana/{b['token']}")
            lines.append(f"💵 Buy: /buy {b['token']} 0.1")
            lines.append('')
    else:
        lines.append('❌ NO QUALITY SIGNALS - All buys failed filters')
        lines.append('')
    
    lines.append(f'📊 FILTERED OUT: {len(failed)} junk buys skipped')
    for b in failed:
        f = b['filters']
        reasons = []
        if not f['age_ok']: reasons.append('age')
        if not f['vol_ok']: reasons.append('volume')
        if not f['holders_ok']: reasons.append('holders')
        if not f['ath_ok']: reasons.append('dumped')
        if not f['bot_ok']: reasons.append('bots')
        tier = 'T1' if b['maker'] in TIER1 else 'T2'
        lines.append(f"  • {b['symbol']} ({tier}): {', '.join(reasons)}")
    
    return '\n'.join(lines)

def main():
    now = int(time.time())
    
    # Fetch smart money trades
    data = fetch_smartmoney()
    if not data:
        print("❌ Failed to fetch smart money data")
        return 1
    
    # Extract tier wallet buys
    buys = extract_buys(data)
    print(f"Found {len(buys)} unique BUYs from tracked wallets")
    
    # Fetch token info and apply filters
    passed = []
    failed = []
    
    for b in buys:
        info = fetch_token_info(b['token'])
        if not info:
            print(f"  SKIP {b['symbol']}: Failed to fetch token info")
            continue
        b['info'] = info
        
        filters = apply_filters(info, now)
        b['filters'] = filters
        
        if filters['passed'] == 5:
            passed.append(b)
        else:
            failed.append(b)
    
    # Generate and print report
    report = generate_report(passed, failed, now)
    print(report)
    
    # Save results
    with open('/tmp/smartmoney_filtered.json', 'w') as f:
        json.dump({'passed': passed, 'failed': failed, 'now': now}, f, indent=2, default=str)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
