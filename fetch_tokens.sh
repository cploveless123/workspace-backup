#!/bin/bash
# Fetch token info for tracked wallet buys

tokens=(
  "ANGcQTF2SWNCDJZTYuTz7JUxBZw9HWtxCB5vYHeapump"
  "Q8GkpPPQodLmBx2rinbMuBYR1HaJ41fTqLpPRrkpump"
  "4Y5HhBEa2Mmbx3P6S1ttLGzSYCfgykMdmutFHXsNpump"
  "AuH1cjbBQhneaY2yDAXPEsbAu8sMkWPm36vMfpdpDhVz"
)

for token in "${tokens[@]}"; do
  echo "=== TOKEN: $token ==="
  npx gmgn-cli token info --chain sol --address "$token" --raw 2>/dev/null
  echo ""
  sleep 2
done
