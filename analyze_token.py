#!/usr/bin/env python3
import json, sys, datetime

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
        # 1. Age < 30 min
        if age_min < 30:
            result['filters_passed'] += 1
            result['checks']['age'] = True
        else:
            result['checks']['age'] = False
            
        # 2. Volume 5m > $5K
        if vol_5m > 5000:
            result['filters_passed'] += 1
            result['checks']['volume_5m'] = True
        else:
            result['checks']['volume_5m'] = False
            
        # 3. Volume trend > 20%
        if vol_trend > 0.20:
            result['filters_passed'] += 1
            result['checks']['vol_trend'] = True
        else:
            result['checks']['vol_trend'] = False
            
        # 4. Price vs 1h high > 70%
        if price_vs_high > 70:
            result['filters_passed'] += 1
            result['checks']['price_vs_high'] = True
        else:
            result['checks']['price_vs_high'] = False
            
        # 5. Buy ratio > 0.6
        if buy_ratio > 0.6:
            result['filters_passed'] += 1
            result['checks']['buy_ratio'] = True
        else:
            result['checks']['buy_ratio'] = False
            
        # 6. Holders > 100
        if holders > 100:
            result['filters_passed'] += 1
            result['checks']['holders'] = True
        else:
            result['checks']['holders'] = False
            
        # 7. Bot rate < 40%
        if bot_rate < 40:
            result['filters_passed'] += 1
            result['checks']['bot_rate'] = True
        else:
            result['checks']['bot_rate'] = False
        
        result['high_conviction'] = result['filters_passed'] == result['filters_total']
        
        return result
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            token_json = f.read()
    else:
        token_json = sys.stdin.read()
    
    result = analyze_token(token_json)
    print(json.dumps(result, indent=2))
