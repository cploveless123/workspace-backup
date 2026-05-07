import json
from collections import Counter, defaultdict
import statistics

reasons = Counter()
paths = Counter()
path_reasons = defaultdict(Counter)
mcap_by_reason = defaultdict(list)
h1_by_reason = defaultdict(list)
holders_by_reason = defaultdict(list)

with open('/root/Dex-trading-bot/trades/rejections.jsonl') as f:
    for line in f:
        try:
            r = json.loads(line.strip())
            reason = r.get('reason','UNKNOWN')
            path = r.get('entry_path','UNKNOWN')
            reasons[reason] += 1
            paths[path] += 1
            path_reasons[path][reason] += 1
            mcap = r.get('mcap',0)
            h1 = r.get('h1',0)
            holders = r.get('holders',0)
            if mcap > 0: mcap_by_reason[reason].append(mcap)
            if h1 != 0: h1_by_reason[reason].append(h1)
            if holders > 0: holders_by_reason[reason].append(holders)
        except:
            pass

print('=== REJECTION REASONS ===')
for reason, count in reasons.most_common():
    pct = count/sum(reasons.values())*100
    print(f'{reason}: {count} ({pct:.1f}%)')

print('\n=== ENTRY PATHS ===')
for path, count in paths.most_common():
    pct = count/sum(paths.values())*100
    print(f'{path}: {count} ({pct:.1f}%)')

print('\n=== PATH vs REASON BREAKDOWN ===')
for path in ['PUMP','SURGE','WHALE','ESTABLISHED','SNIPER','UNKNOWN','BASE']:
    if path not in path_reasons: continue
    print(f'\n{path}:')
    for reason, count in path_reasons[path].most_common():
        print(f'  {reason}: {count}')

print('\n=== MEDIAN METRICS BY REASON ===')
for reason in ['MIN_MCAP','MAX_MCAP','MIN_HOLDERS','MIN_VOLUME','MIN_H1','COOLDOWN','MAX_POSITIONS','TIME_BLOCKED','API_ERROR','UNKNOWN']:
    if reason not in mcap_by_reason and reason not in h1_by_reason: continue
    print(f'\n{reason}:')
    if mcap_by_reason[reason]:
        vals = mcap_by_reason[reason]
        print(f'  mcap: median=${statistics.median(vals):,.0f}  mean=${statistics.mean(vals):,.0f}  min=${min(vals):,.0f}  max=${max(vals):,.0f}')
    if h1_by_reason[reason]:
        vals = h1_by_reason[reason]
        print(f'  h1:   median={statistics.median(vals):.1f}%  mean={statistics.mean(vals):.1f}%  min={min(vals):.1f}%  max={max(vals):.1f}%')
    if holders_by_reason[reason]:
        vals = holders_by_reason[reason]
        print(f'  holders: median={statistics.median(vals):.0f}  mean={statistics.mean(vals):.0f}  min={min(vals)}  max={max(vals)}')
