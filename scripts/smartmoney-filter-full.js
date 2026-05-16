#!/usr/bin/env node
/**
 * Smart Money Tracker - Full Filtered Report
 * Applies strict filters to token data
 */

const CURRENT_TIME = 1778917320;

// Token data from gmgn-cli
const tokens = [
  {
    symbol: "BALLSACKDORKL",
    address: "4LEydtM5terKDQJeUgx5mPB6NYR5maE9hnGnasekpump",
    creation_timestamp: 1778656850,
    volume_5m: 525660.64507628,
    volume_1h: 2278226.57977235,
    price_1h_high: 0.0016095527,
    current_price: 0.00092164749,
    buys_1h: 11659,
    sells_1h: 9869,
    holders: 1734,
    bot_degen_rate: 0.5301,
    tier1_buyers: 16,
    total_buy_amount: 6228.42,
    is_cluster: true,
    has_full_open: true
  },
  {
    symbol: "RoyalPop",
    address: "8TbnsLM72WoHKmVyDqRqEkEuNRGFgA4zbRXQYv6Gpump",
    creation_timestamp: 1778455497,
    volume_5m: 19183.72457516,
    volume_1h: 407190.27718208,
    price_1h_high: 0.0027011222,
    current_price: 0.0015577875,
    buys_1h: 1836,
    sells_1h: 1613,
    holders: 3621,
    bot_degen_rate: 0.3194,
    tier1_buyers: 1,
    total_buy_amount: 310.34,
    is_cluster: true,
    has_full_open: true
  },
  {
    symbol: "DIRECTOR",
    address: "Do6N8m8ssowyAvXs2tkGKkJ8vaNC8H5oRkMdr9shpump",
    creation_timestamp: 1763482998,
    volume_5m: 2663.69022504,
    volume_1h: 52881.065655974,
    price_1h_high: 0.00052906048,
    current_price: 0.00042469191,
    buys_1h: 333,
    sells_1h: 199,
    holders: 3012,
    bot_degen_rate: 0.1564,
    tier1_buyers: 0,
    total_buy_amount: 431.77,
    is_cluster: false,
    has_full_open: true
  },
  {
    symbol: "FOUSEY",
    address: "H9eYmmdqfkPDr8hPb4CadNcSccU1mCf2xYaSmT6tpump",
    creation_timestamp: 1758067461,
    volume_5m: 0,
    volume_1h: 297.95913523,
    price_1h_high: 0.0000017563112,
    current_price: 0.0000022318962,
    buys_1h: 2,
    sells_1h: 0,
    holders: 38,
    bot_degen_rate: 0.1839,
    tier1_buyers: 0,
    total_buy_amount: 297.96,
    is_cluster: false,
    has_full_open: true
  },
  {
    symbol: "JOE",
    address: "EjvsudvUcxrZwCWARwdS9BmEPisvZLjmnkdegeRbpump",
    creation_timestamp: 1778790109,
    volume_5m: 40.25256817,
    volume_1h: 810.092694479,
    price_1h_high: 0.000022944703,
    current_price: 0.000016011501,
    buys_1h: 11,
    sells_1h: 18,
    holders: 520,
    bot_degen_rate: 0.2692,
    tier1_buyers: 0,
    total_buy_amount: 129.00,
    is_cluster: false,
    has_full_open: true
  }
];

// STRICT FILTERS
const FILTERS = {
  MAX_AGE_MINUTES: 30,
  MIN_VOLUME_5M: 5000,
  MIN_VOLUME_TREND_PCT: 20,
  MIN_PRICE_VS_1H_HIGH_PCT: 70,
  MIN_BUY_RATIO: 0.6,
  MIN_HOLDERS: 100,
  MAX_BOT_RATE: 0.40
};

function applyFilters(token) {
  const results = {
    passed: [],
    failed: []
  };

  // 1. Age < 30 minutes
  const ageMinutes = (CURRENT_TIME - token.creation_timestamp) / 60;
  if (ageMinutes < FILTERS.MAX_AGE_MINUTES) {
    results.passed.push(`✅ Age: ${ageMinutes.toFixed(1)} min (< 30)`);
  } else {
    results.failed.push(`❌ Age: ${ageMinutes.toFixed(1)} min (> 30)`);
  }

  // 2. Volume 5m > $5,000
  if (token.volume_5m > FILTERS.MIN_VOLUME_5M) {
    results.passed.push(`✅ Vol 5m: $${token.volume_5m.toFixed(0)} (> $5K)`);
  } else {
    results.failed.push(`❌ Vol 5m: $${token.volume_5m.toFixed(0)} (< $5K)`);
  }

  // 3. Volume trend > 20% of 1h average
  const volume_1h_avg = token.volume_1h / 12;
  const volumeTrend = (token.volume_5m / volume_1h_avg) * 100;
  if (volumeTrend > FILTERS.MIN_VOLUME_TREND_PCT) {
    results.passed.push(`✅ Vol Trend: ${volumeTrend.toFixed(1)}% (> 20%)`);
  } else {
    results.failed.push(`❌ Vol Trend: ${volumeTrend.toFixed(1)}% (< 20%)`);
  }

  // 4. Price vs 1h high > 70%
  const priceVsHigh = (token.current_price / token.price_1h_high) * 100;
  if (priceVsHigh > FILTERS.MIN_PRICE_VS_1H_HIGH_PCT) {
    results.passed.push(`✅ Price vs 1h High: ${priceVsHigh.toFixed(1)}% (> 70%)`);
  } else {
    results.failed.push(`❌ Price vs 1h High: ${priceVsHigh.toFixed(1)}% (< 70%)`);
  }

  // 5. Buy/Sell ratio > 0.6
  const totalTrades = token.buys_1h + token.sells_1h;
  const buyRatio = totalTrades > 0 ? token.buys_1h / totalTrades : 0;
  if (buyRatio > FILTERS.MIN_BUY_RATIO) {
    results.passed.push(`✅ Buy Ratio: ${(buyRatio * 100).toFixed(1)}% (> 60%)`);
  } else {
    results.failed.push(`❌ Buy Ratio: ${(buyRatio * 100).toFixed(1)}% (< 60%)`);
  }

  // 6. Holders > 100
  if (token.holders > FILTERS.MIN_HOLDERS) {
    results.passed.push(`✅ Holders: ${token.holders} (> 100)`);
  } else {
    results.failed.push(`❌ Holders: ${token.holders} (< 100)`);
  }

  // 7. Bot rate < 40%
  if (token.bot_degen_rate < FILTERS.MAX_BOT_RATE) {
    results.passed.push(`✅ Bot Rate: ${(token.bot_degen_rate * 100).toFixed(1)}% (< 40%)`);
  } else {
    results.failed.push(`❌ Bot Rate: ${(token.bot_degen_rate * 100).toFixed(1)}% (> 40%)`);
  }

  return {
    ...results,
    allPassed: results.failed.length === 0,
    passCount: results.passed.length,
    failCount: results.failed.length
  };
}

// Process all tokens
console.log(`🔥 SMART MONEY HIGH-CONVICTION REPORT`);
console.log(`⏰ ${new Date(CURRENT_TIME * 1000).toUTCString()}`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

let highConvictionCount = 0;
let skippedCount = 0;
const skipReasons = {
  tooOld: 0,
  lowVolume: 0,
  volumeCollapsed: 0,
  dumping: 0,
  distribution: 0,
  lowHolders: 0,
  botRate: 0
};

for (const token of tokens) {
  const filterResults = applyFilters(token);
  
  if (filterResults.allPassed) {
    highConvictionCount++;
    
    // Calculate conviction indicators
    const isCluster = token.is_cluster;
    const isLargeBuy = token.total_buy_amount >= 500;
    const isFullOpen = token.has_full_open;
    const isFreshHighVol = (CURRENT_TIME - token.creation_timestamp) / 60 < 15 && token.volume_5m > 5000;
    
    console.log(`🔥🔥🔥 HIGH-CONVICTION SIGNAL (${filterResults.passCount}/7 PASSED)`);
    console.log(`[${new Date(CURRENT_TIME * 1000).toISOString().substr(11, 5)} UTC] ${token.tier1_buyers > 0 ? '⭐TIER1 ' : ''}BUY ${token.symbol} $${token.total_buy_amount.toFixed(2)}`);
    console.log(`📍 ${token.address}`);
    console.log(`💰 MCAP: N/A | Price: $${token.current_price.toFixed(10)} | vs 1h High: ${((token.current_price / token.price_1h_high) * 100).toFixed(1)}%`);
    console.log(`⏱️ Age: ${((CURRENT_TIME - token.creation_timestamp) / 60).toFixed(1)} min | Vol 5m: $${token.volume_5m.toFixed(0)} | Vol Trend: ${((token.volume_5m / (token.volume_1h / 12)) * 100).toFixed(1)}%`);
    console.log(`📊 Buy Ratio: ${((token.buys_1h / (token.buys_1h + token.sells_1h)) * 100).toFixed(1)}% | Holders: ${token.holders} | Bot Rate: ${(token.bot_degen_rate * 100).toFixed(1)}%`);
    console.log(`🔗 DexScreener: https://dexscreener.com/solana/${token.address}`);
    console.log(`💵 Buy: /buy ${token.address} 0.1\n`);
    
    console.log(`⚡ CONVICTION INDICATORS:`);
    console.log(`• Multiple wallets: ${isCluster ? '✅ YES' : '❌ NO'}`);
    console.log(`• Large amount: ${isLargeBuy ? '✅ YES' : '❌ NO'}`);
    console.log(`• Full position: ${isFullOpen ? '✅ YES' : '❌ NO'}`);
    console.log(`• Fresh + high volume: ${isFreshHighVol ? '✅ YES' : '❌ NO'}`);
    console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);
  } else {
    skippedCount++;
    
    // Track skip reasons
    const ageMinutes = (CURRENT_TIME - token.creation_timestamp) / 60;
    if (ageMinutes >= 30) skipReasons.tooOld++;
    if (token.volume_5m < 5000) skipReasons.lowVolume++;
    const volumeTrend = (token.volume_5m / (token.volume_1h / 12)) * 100;
    if (volumeTrend < 20) skipReasons.volumeCollapsed++;
    const priceVsHigh = (token.current_price / token.price_1h_high) * 100;
    if (priceVsHigh < 70) skipReasons.dumping++;
    const buyRatio = token.buys_1h / (token.buys_1h + token.sells_1h);
    if (buyRatio < 0.6) skipReasons.distribution++;
    if (token.holders < 100) skipReasons.lowHolders++;
    if (token.bot_degen_rate > 0.40) skipReasons.botRate++;
    
    console.log(`⏭️  SKIPPED: ${token.symbol} (${filterResults.passCount}/7 passed)`);
    for (const fail of filterResults.failed) {
      console.log(`   ${fail}`);
    }
    console.log(`   🔗 ${token.address}\n`);
  }
}

// Summary
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`📊 FILTER SUMMARY`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`🔥 High-Conviction Signals: ${highConvictionCount}`);
console.log(`⏭️  Filtered Out: ${skippedCount}`);
console.log(`\n📉 Skip Reasons:`);
console.log(`• Too old (>30 min): ${skipReasons.tooOld}`);
console.log(`• Low volume 5m (<$5K): ${skipReasons.lowVolume}`);
console.log(`• Volume collapsed (<20% of 1h avg): ${skipReasons.volumeCollapsed}`);
console.log(`• Dumping (<70% of 1h high): ${skipReasons.dumping}`);
console.log(`• Distribution (buy ratio <60%): ${skipReasons.distribution}`);
console.log(`• Low holders (<100): ${skipReasons.lowHolders}`);
console.log(`• Bot rate >40%: ${skipReasons.botRate}`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
