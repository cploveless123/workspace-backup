#!/usr/bin/env python3
import json, sys, os, subprocess, datetime

TIER1_WALLETS = [
    "6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3",
    "65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE",
    "3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f",
    "H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V",
    "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4",
    "7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5",
    "MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN",
    "FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS",
    "tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir",
    "1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C",
    "Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX",
    "BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT",
]

TIER2_WALLETS = [
    "CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY",
    "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x",
    "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz",
    "9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U",
    "FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go",
    "DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw",
]

def get_wallet_tier(maker):
    if maker in TIER1_WALLETS:
        return "TIER1"
    elif maker in TIER2_WALLETS:
        return "TIER2"
    return "OTHER"

def analyze_token(token_json):
    try:
        data = json.loads(token_json)
        token = data.get('data', data)
        
        name = token.get('name', token.get('symbol', 'UNKNOWN'))
        address = token.get('address', '')
        
        # Price is nested in some responses
        price_raw = token.get('price', 0)
        if isinstance(price_raw, dict):
            price = float(price_raw.get('price', 0) or 0)
            price_1h_high = float(price_raw.get('price_1h', price) or price)
            buys_1h = int(price_raw.get('buys_1h', 0) or 0)
            sells_1h = int(price_raw.get('sells_1h', 0) or 0)
            vol_5m = float(price_raw.get('volume_5m', 0) or 0)
            vol_1h = float(price_raw.get('volume_1h', 0) or 0)
        else:
            price = float(price_raw or 0)
            price_1h_high = float(token.get('price_1h_high', token.get('high_1h', price)) or price)
            buys_1h = int(token.get('buy_1h', token.get('buys_1h', 0)) or 0)
            sells_1h = int(token.get('sell_1h', token.get('sells_1h', 0)) or 0)
            vol_5m = float(token.get('volume_5m', 0) or 0)
            vol_1h = float(token.get('volume_1h', 0) or 0)
        
        mcap = float(token.get('market_cap', 0) or 0)
        if mcap == 0 and price > 0:
            supply = float(token.get('total_supply', 0) or token.get('circulating_supply', 0) or 0)
            if supply > 0:
                mcap = price * supply
        
        liquidity = float(token.get('liquidity', 0) or 0)
        holders = int(token.get('holder_count', token.get('holders', 0)) or 0)
        
        # Bot rate
        bot_rate = float(token.get('bot_degen_rate', token.get('bot_rate', 0)) or 0)
        
        # Age
        creation_time = token.get('creation_timestamp', 0)
        if creation_time:
            age_min = (datetime.datetime.now(datetime.timezone.utc).timestamp() - creation_time) / 60
        else:
            age_min = 999
        
        # Calculations
        total_trades = buys_1h + sells_1h
        buy_ratio = buys_1h / total_trades if total_trades > 0 else 0
        vol_trend = (vol_5m / (vol_1h / 12)) if vol_1h > 0 else 0
        price_vs_high = (price / price_1h_high * 100) if price_1h_high > 0 else 0
        
        result = {
            'name': name,
            'address': address,
            'price': price,
            'mcap': mcap,
            'liquidity': liquidity,
            'age_min': age_min,
            'vol_5m': vol_5m,
            'vol_1h': vol_1h,
            'vol_trend': vol_trend,
            'buys_1h': buys_1h,
            'sells_1h': sells_1h,
            'buy_ratio': buy_ratio,
            'price_vs_high': price_vs_high,
            'holders': holders,
            'bot_rate': bot_rate,
            'filters_passed': 0,
            'filters_total': 7,
            'checks': {}
        }
        
        # Apply filters
        if age_min < 30:
            result['filters_passed'] += 1
            result['checks']['age'] = True
        else:
            result['checks']['age'] = False
            
        if vol_5m > 5000:
            result['filters_passed'] += 1
            result['checks']['volume_5m'] = True
        else:
            result['checks']['volume_5m'] = False
            
        if vol_trend > 0.20:
            result['filters_passed'] += 1
            result['checks']['vol_trend'] = True
        else:
            result['checks']['vol_trend'] = False
            
        if price_vs_high > 70:
            result['filters_passed'] += 1
            result['checks']['price_vs_high'] = True
        else:
            result['checks']['price_vs_high'] = False
            
        if buy_ratio > 0.6:
            result['filters_passed'] += 1
            result['checks']['buy_ratio'] = True
        else:
            result['checks']['buy_ratio'] = False
            
        if holders > 100:
            result['filters_passed'] += 1
            result['checks']['holders'] = True
        else:
            result['checks']['holders'] = False
            
        if bot_rate < 40:
            result['filters_passed'] += 1
            result['checks']['bot_rate'] = True
        else:
            result['checks']['bot_rate'] = False
        
        result['high_conviction'] = result['filters_passed'] == result['filters_total']
        
        return result
    except Exception as e:
        return {'error': str(e)}

def fetch_token_info(address):
    """Fetch token info using gmgn-cli"""
    try:
        cmd = f"gmgn-cli token info --chain sol --address {address} --raw"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            return result.stdout
        return None
    except:
        return None

def main():
    # Read smart money data from stdin or file
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)
    
    txs = data.get('list', [])
    
    # Get unique buy transactions
    buy_txs = []
    seen = set()
    for tx in txs:
        if tx.get('side') == 'buy':
            addr = tx.get('base_address', '')
            if addr and addr not in seen:
                seen.add(addr)
                buy_txs.append(tx)
    
    print(f"📊 SMART MONEY TRACKER - {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Found {len(buy_txs)} unique buy tokens from smart money wallets\n")
    
    # Track results
    high_conviction = []
    filtered_out = {
        'too_old': 0,
        'low_volume': 0,
        'volume_collapsed': 0,
        'dumping': 0,
        'distribution': 0,
        'low_holders': 0,
        'high_bot': 0,
        'other': 0
    }
    
    # Analyze each token
    for tx in buy_txs[:15]:  # Limit to first 15 to avoid rate limits
        addr = tx.get('base_address', '')
        symbol = tx.get('base_token', {}).get('symbol', 'UNKNOWN')
        amount_usd = tx.get('amount_usd', 0)
        maker = tx.get('maker', '')
        is_open = tx.get('is_open_or_close', 0)
        
        # Skip WSOL
        if addr == 'So11111111111111111111111111111111111111112':
            continue
            
        print(f"🔍 Analyzing {symbol} ({addr[:8]}...)...", end=' ', flush=True)
        
        # Fetch token info
        token_json = fetch_token_info(addr)
        if not token_json:
            print("❌ API failed")
            continue
        
        # Save for debugging
        with open(f'/tmp/token_{addr[:8]}.json', 'w') as f:
            f.write(token_json)
        
        result = analyze_token(token_json)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        passed = result['filters_passed']
        total = result['filters_total']
        
        if result['high_conviction']:
            print(f"✅ ALL FILTERS PASSED")
            
            # Check for cluster signal
            cluster = sum(1 for t in buy_txs if t.get('base_address') == addr) > 1
            
            high_conviction.append({
                'tx': tx,
                'result': result,
                'cluster': cluster,
                'tier': get_wallet_tier(maker)
            })
        else:
            # Track why it failed
            checks = result['checks']
            if not checks.get('age', True):
                filtered_out['too_old'] += 1
                print(f"❌ Too old ({result['age_min']:.0f} min)")
            elif not checks.get('volume_5m', True):
                filtered_out['low_volume'] += 1
                print(f"❌ Low volume (${result['vol_5m']:.0f})")
            elif not checks.get('vol_trend', True):
                filtered_out['volume_collapsed'] += 1
                print(f"❌ Vol collapsed ({result['vol_trend']:.1%})")
            elif not checks.get('price_vs_high', True):
                filtered_out['dumping'] += 1
                print(f"❌ Dumping ({result['price_vs_high']:.1f}%)")
            elif not checks.get('buy_ratio', True):
                filtered_out['distribution'] += 1
                print(f"❌ Distribution ({result['buy_ratio']:.1%})")
            elif not checks.get('holders', True):
                filtered_out['low_holders'] += 1
                print(f"❌ Low holders ({result['holders']})")
            elif not checks.get('bot_rate', True):
                filtered_out['high_bot'] += 1
                print(f"❌ High bot ({result['bot_rate']:.1f}%)")
            else:
                filtered_out['other'] += 1
                print(f"❌ Failed {passed}/{total}")
    
    # Report high conviction signals
    print(f"\n{'='*60}")
    print(f"🔥 HIGH-CONVICTION SIGNALS: {len(high_conviction)}")
    print(f"{'='*60}\n")
    
    for signal in high_conviction:
        tx = signal['tx']
        result = signal['result']
        maker = tx.get('maker', '')
        tier = signal['tier']
        
        print(f"🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)")
        print(f"[{datetime.datetime.fromtimestamp(tx.get('timestamp', 0), tz=datetime.timezone.utc).strftime('%H:%M')}] {maker[:12]}... ({tier}) — BUY {result['name']} ${tx.get('amount_usd', 0):.2f} [{'FULL' if tx.get('is_open_or_close') else 'PARTIAL'}]")
        print(f"📍 {tx.get('base_address', '')}")
        print(f"💰 MCAP: ${result['mcap']:,.0f} | Price: ${result['price']:.10f} | vs 1h High: {result['price_vs_high']:.1f}%")
        print(f"⏱️ Age: {result['age_min']:.0f} min | Vol 5m: ${result['vol_5m']:,.0f} | Vol Trend: {result['vol_trend']:.1%}")
        print(f"📊 Buy Ratio: {result['buy_ratio']:.1%} | Holders: {result['holders']} | Bot Rate: {result['bot_rate']:.1f}%")
        print(f"🔗 DexScreener: https://dexscreener.com/solana/{tx.get('base_address', '')}")
        print(f"💵 Buy: /buy {tx.get('base_address', '')} 0.1")
        print()
        print("⚡ CONVICTION INDICATORS:")
        print(f"• Multiple wallets: {'YES' if signal['cluster'] else 'NO'}")
        print(f"• Large amount: {'YES' if tx.get('amount_usd', 0) > 500 else 'NO'}")
        print(f"• Full position: {'YES' if tx.get('is_open_or_close') else 'NO'}")
        print(f"• Fresh + high volume: {'YES' if result['age_min'] < 15 and result['vol_5m'] > 50000 else 'NO'}")
        print()
    
    # Report filtered out summary
    total_filtered = sum(filtered_out.values())
    print(f"📊 FILTERED OUT: {total_filtered} low-conviction buys skipped")
    if filtered_out['too_old']:
        print(f"• Too old: {filtered_out['too_old']}")
    if filtered_out['low_volume']:
        print(f"• Low volume: {filtered_out['low_volume']}")
    if filtered_out['volume_collapsed']:
        print(f"• Volume collapsed: {filtered_out['volume_collapsed']}")
    if filtered_out['dumping']:
        print(f"• Dumping: {filtered_out['dumping']}")
    if filtered_out['distribution']:
        print(f"• Distribution: {filtered_out['distribution']}")
    if filtered_out['low_holders']:
        print(f"• Low holders: {filtered_out['low_holders']}")
    if filtered_out['high_bot']:
        print(f"• High bot rate: {filtered_out['high_bot']}")
    
    print(f"\n{'='*60}")
    print(f"Summary: {len(high_conviction)} high-conviction / {total_filtered} filtered / {len(buy_txs)} total buys")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
