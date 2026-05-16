const fs = require('fs');

// Current time: 2026-05-15 23:38 UTC
const now = 1778888280; // approximate timestamp for 2026-05-15 23:38 UTC
const sixHoursAgo = now - (6 * 60 * 60);

// Token data from GMGN
const tokens = {
  "ANGcQTF2SWNCDJZTYuTz7JUxBZw9HWtxCB5vYHeapump": {
    symbol: "Gait",
    creation_timestamp: 1778882915,
    volume_5m: 14957.84,
    holder_count: 335,
    price: 0.000030727849,
    ath_price: 0.000047041889,
    bot_degen_rate: 0.524,
    mcap: 0 // will calculate
  },
  "Q8GkpPPQodLmBx2rinbMuBYR1HaJ41fTqLpPRrkpump": {
    symbol: "50/50",
    creation_timestamp: 1778887733,
    volume_5m: 31.11,
    holder_count: 17,
    price: 0.0000026021774,
    ath_price: 0.000026272066,
    bot_degen_rate: 0.0023,
    mcap: 0
  },
  "4Y5HhBEa2Mmbx3P6S1ttLGzSYCfgykMdmutFHXsNpump": {
    symbol: "BABYWOJAK",
    creation_timestamp: 1778879070,
    volume_5m: 16717.95,
    holder_count: 930,
    price: 0.00014767618,
    ath_price: 0.00024248858,
    bot_degen_rate: 0.1277,
    mcap: 0
  },
  "AuH1cjbBQhneaY2yDAXPEsbAu8sMkWPm36vMfpdpDhVz": {
    symbol: "Ebola",
    creation_timestamp: 1716002360,
    volume_5m: 151.74,
    holder_count: 175,
    price: 0.000006639757,
    ath_price: 0.00005732824,
    bot_degen_rate: 0.2716,
    mcap: 0
  }
};

// Calculate market caps
tokens["ANGcQTF2SWNCDJZTYuTz7JUxBZw9HWtxCB5vYHeapump"].mcap = tokens["ANGcQTF2SWNCDJZTYuTz7JUxBZw9HWtxCB5vYHeapump"].price * 1000000000;
tokens["Q8GkpPPQodLmBx2rinbMuBYR1HaJ41fTqLpPRrkpump"].mcap = tokens["Q8GkpPPQodLmBx2rinbMuBYR1HaJ41fTqLpPRrkpump"].price * 999965894;
tokens["4Y5HhBEa2Mmbx3P6S1ttLGzSYCfgykMdmutFHXsNpump"].mcap = tokens["4Y5HhBEa2Mmbx3P6S1ttLGzSYCfgykMdmutFHXsNpump"].price * 990626195;
tokens["AuH1cjbBQhneaY2yDAXPEsbAu8sMkWPm36vMfpdpDhVz"].mcap = tokens["AuH1cjbBQhneaY2yDAXPEsbAu8sMkWPm36vMfpdpDhVz"].price * 999974644;

// Buy data
const buys = [
  {
    maker: "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4",
    tier: "TIER1",
    token: "ANGcQTF2SWNCDJZTYuTz7JUxBZw9HWtxCB5vYHeapump",
    symbol: "Gait",
    amount_usd: 215.98,
    timestamp: 1778888015,
    wallet_name: "Stigman"
  },
  {
    maker: "8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4",
    tier: "TIER1",
    token: "Q8GkpPPQodLmBx2rinbMuBYR1HaJ41fTqLpPRrkpump",
    symbol: "50/50",
    amount_usd: 83.09,
    timestamp: 1778887897,
    wallet_name: "Stigman"
  },
  {
    maker: "43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x",
    tier: "TIER2",
    token: "4Y5HhBEa2Mmbx3P6S1ttLGzSYCfgykMdmutFHXsNpump",
    symbol: "BABYWOJAK",
    amount_usd: 55.43,
    timestamp: 1778887887,
    wallet_name: "43QmFc2Q"
  },
  {
    maker: "3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz",
    tier: "TIER2",
    token: "AuH1cjbBQhneaY2yDAXPEsbAu8sMkWPm36vMfpdpDhVz",
    symbol: "Ebola",
    amount_usd: 132.17,
    timestamp: 1778887852,
    wallet_name: "3wccdTM5"
  }
];

// Apply filters
const results = [];
const skipped = [];

for (const buy of buys) {
  const token = tokens[buy.token];
  const age_minutes = Math.floor((now - token.creation_timestamp) / 60);
  const age_hours = age_minutes / 60;
  const vs_ath = (token.price / token.ath_price * 100).toFixed(1);
  
  const filters = {
    age: { value: age_hours, pass: age_hours < 6, reason: age_hours < 6 ? null : `Age ${age_hours.toFixed(1)}h > 6h` },
    volume: { value: token.volume_5m, pass: token.volume_5m > 2000, reason: token.volume_5m > 2000 ? null : `Vol 5m $${token.volume_5m.toFixed(0)} < $2K` },
    holders: { value: token.holder_count, pass: token.holder_count > 100, reason: token.holder_count > 100 ? null : `Holders ${token.holder_count} < 100` },
    price_vs_ath: { value: vs_ath, pass: parseFloat(vs_ath) > 50, reason: parseFloat(vs_ath) > 50 ? null : `Price ${vs_ath}% ATH < 50%` },
    bot_rate: { value: token.bot_degen_rate, pass: token.bot_degen_rate < 0.40, reason: token.bot_degen_rate < 0.40 ? null : `Bot rate ${(token.bot_degen_rate*100).toFixed(1)}% > 40%` }
  };
  
  const passed = Object.values(filters).filter(f => f.pass).length;
  const total = Object.values(filters).length;
  const all_pass = passed === total;
  
  const result = {
    ...buy,
    age_minutes,
    age_hours: age_hours.toFixed(1),
    volume_5m: token.volume_5m,
    holders: token.holder_count,
    bot_rate: (token.bot_degen_rate * 100).toFixed(1),
    vs_ath,
    mcap: token.mcap.toFixed(2),
    filters,
    passed,
    total,
    all_pass
  };
  
  if (all_pass) {
    results.push(result);
  } else {
    const failed = Object.values(filters).filter(f => !f.pass).map(f => f.reason).join(', ');
    skipped.push({ ...result, fail_reason: failed });
  }
}

console.log(JSON.stringify({ passed: results, skipped }, null, 2));
