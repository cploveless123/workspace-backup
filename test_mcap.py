entry_price = 9.99766e-06
entry_mcap = 15904
current_price = 1.568e-05  # +56.9% gain

# Proportional mcap (what we use for TP display)
tp_mcap = int(entry_mcap * (current_price / entry_price))
print(f'TP mcap: ${tp_mcap:,} (should be > entry ${entry_mcap:,})')

# Verify it's above entry
assert tp_mcap > entry_mcap, 'TP mcap should be above entry!'
print('✓ Test passed')
