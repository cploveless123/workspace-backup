#!/usr/bin/env node
/**
 * Smart Money Tracker - Quality Filtered
 * Filters smart money buys through strict quality criteria
 */

const { execSync } = require('child_process');

// Current time from system
const CURRENT_TIME = Math.floor(Date.now() / 1000);

// Tier wallets
const TIER1 = [
  '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3', // Cowboy🔶BNB
  '65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE',
  '3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f',
  'H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V',
  '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4', // Stigman
  '7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5',
  'MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN',
  'FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS',
  'tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir',
  '1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C',
  'Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX',
  'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT',
];

const TIER2 = [
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw',
];

const ALL_WATCHED = [...TIER1, ...TIER2];

// Filters
const FILTERS = {
  maxAgeHours: 6,
  minVolume5m: 2000,
  minHolders: 100,
  minPriceVsATH: 0.50, // 50%
  maxBotRate: 0.40,     // 40%
};

async function fetchTokenInfo(address) {
  try {
    const result = execSync(
      `gmgn-cli token info --chain sol --address ${address} --raw`,
      { encoding: 'utf8', timeout: 15000 }
    );
    return JSON.parse(result.trim());
  } catch (e) {
    return null;
  }
}

function getWalletTier(address) {
  if (TIER1.includes(address)) return 'TIER1';
  if (TIER2.includes(address)) return 'TIER2';
  return 'OTHER';
}

function formatTime(ts) {
  const d = new Date(ts * 1000);
  return d.toISOString().slice(11, 16) + ' UTC';
}

function formatAge(minutes) {
  if (minutes < 60) return `${Math.round(minutes)}m`;
  const h = Math.floor(minutes / 60);
  const m = Math.round(minutes % 60);
  return `${h}h${m}m`;
}

async function main() {
  // Fetch smart money activity
  console.log('📡 Fetching smart money activity...\n');
  
  let trades;
  try {
    const result = execSync(
      'gmgn-cli track smartmoney --chain sol --limit 100 --raw',
      { encoding: 'utf8', timeout: 30000 }
    );
    trades = JSON.parse(result.trim()).list;
  } catch (e) {
    console.error('❌ Failed to fetch smart money:', e.message);
    process.exit(1);
  }

  // Filter to buys only from watched wallets
  const buys = trades.filter(t => 
    t.side === 'buy' && 
    ALL_WATCHED.includes(t.maker) &&
    t.base_address !== 'So11111111111111111111111111111111111111112' // Skip WSOL
  );

  console.log(`🔍 Found ${buys.length} buys from tracked wallets (out of ${trades.length} total trades)\n`);

  // Deduplicate by token address (keep most recent per token)
  const tokenMap = new Map();
  for (const buy of buys) {
    if (!tokenMap.has(buy.base_address) || tokenMap.get(buy.base_address).timestamp < buy.timestamp) {
      tokenMap.set(buy.base_address, buy);
    }
  }

  const uniqueBuys = Array.from(tokenMap.values());
  console.log(`📊 ${uniqueBuys.length} unique tokens to analyze\n`);

  const passed = [];
  const failed = [];

  // Process each unique buy
  for (let i = 0; i < uniqueBuys.length; i++) {
    const buy = uniqueBuys[i];
    const tokenAddr = buy.base_address;
    const symbol = buy.base_token?.symbol || 'UNKNOWN';
    
    console.log(`[${i+1}/${uniqueBuys.length}] Analyzing ${symbol}...`);
    
    const info = await fetchTokenInfo(tokenAddr);
    if (!info) {
      console.log(`  ❌ Failed to fetch token info`);
      failed.push({ buy, reason: 'API_ERROR', symbol });
      continue;
    }

    // Extract fields - handle nested price object
    const creationTs = info.creation_timestamp || 0;
    const ageMinutes = (CURRENT_TIME - creationTs) / 60;
    const ageHours = ageMinutes / 60;
    
    // Volume 5m - check multiple possible field locations
    const volume5m = info.volume_5m || info.stat?.volume_5m || info.pool?.volume_5m || info.volume?.['5m'] || info.price?.volume_5m || 0;
    
    const holders = info.holder_count || info.stat?.holder_count || 0;
    
    // Price can be nested in price object or top-level
    const price = info.price?.price || info.price || 0;
    const athPrice = info.ath_price || 0;
    const priceVsATH = athPrice > 0 ? parseFloat(price) / athPrice : 1;
    
    const botRate = info.stat?.bot_degen_rate || info.bot_degen_rate || 0;
    
    const circulatingSupply = info.circulating_supply || info.total_supply || 0;
    const mcap = parseFloat(price) * parseFloat(circulatingSupply || 0);

    // Apply filters
    const checks = {
      age: { pass: ageHours < FILTERS.maxAgeHours, value: ageHours, label: 'Age < 6h' },
      volume: { pass: volume5m > FILTERS.minVolume5m, value: volume5m, label: 'Vol 5m > $2K' },
      holders: { pass: holders > FILTERS.minHolders, value: holders, label: 'Holders > 100' },
      priceATH: { pass: priceVsATH > FILTERS.minPriceVsATH, value: priceVsATH, label: 'Price > 50% ATH' },
      botRate: { pass: botRate < FILTERS.maxBotRate, value: botRate, label: 'Bot rate < 40%' },
    };

    const passCount = Object.values(checks).filter(c => c.pass).length;
    const totalChecks = Object.keys(checks).length;

    if (passCount === totalChecks) {
      // ALL PASSED
      passed.push({
        buy,
        info,
        checks,
        ageMinutes,
        mcap,
        symbol,
        passCount,
        totalChecks,
      });
      console.log(`  ✅ ALL FILTERS PASSED (${passCount}/${totalChecks})`);
    } else {
      // Some failed
      const failReasons = Object.values(checks)
        .filter(c => !c.pass)
        .map(c => c.label)
        .join(', ');
      failed.push({ buy, reason: failReasons, symbol, checks });
      console.log(`  ❌ Failed (${passCount}/${totalChecks}): ${failReasons}`);
      console.log(`     Age: ${formatAge(ageMinutes)} | Holders: ${holders} | Price: $${parseFloat(price).toExponential(3)} | ATH: $${athPrice.toExponential(3)} | vsATH: ${(priceVsATH*100).toFixed(1)}% | Vol5m: $${parseFloat(volume5m).toFixed(0)} | Bot: ${(botRate*100).toFixed(1)}%`);
    }
  }

  // Report
  console.log('\n' + '='.repeat(60));
  console.log('📋 QUALITY SIGNALS REPORT');
  console.log('='.repeat(60));

  if (passed.length === 0) {
    console.log('\n🚫 No tokens passed all filters.\n');
  } else {
    console.log(`\n🔥 ${passed.length} QUALITY SIGNAL(S) FOUND\n`);
    
    for (const p of passed) {
      const { buy, info, checks, ageMinutes, mcap, symbol } = p;
      const tier = getWalletTier(buy.maker);
      const walletName = buy.maker_info?.name || buy.maker.slice(0, 8) + '...';
      const isFull = buy.is_open_or_close === 1 ? 'FULL' : 'PARTIAL';
      
      console.log(`🔥 QUALITY SIGNAL (${p.passCount} of ${p.totalChecks} filters passed)`);
      console.log(`[${formatTime(buy.timestamp)}] ${walletName} (${tier}) — BUY ${symbol} $${buy.amount_usd?.toFixed(2) || 'N/A'} [${isFull}]`);
      console.log(`📍 ${buy.base_address}`);
      console.log(`💰 MCAP: $${(mcap / 1000).toFixed(1)}K | Price: $${parseFloat(info.price?.price || info.price || 0).toExponential(3)} | vs ATH: ${(checks.priceATH.value * 100).toFixed(0)}%`);
      console.log(`⏱️ Age: ${formatAge(ageMinutes)} | Vol 5m: $${checks.volume.value.toFixed(0)} | Holders: ${checks.holders.value}`);
      console.log(`🤖 Bot Rate: ${(checks.botRate.value * 100).toFixed(1)}%`);
      console.log(`🔗 DexScreener: https://dexscreener.com/solana/${buy.base_address}`);
      console.log(`💵 Buy: /buy ${buy.base_address} 0.1`);
      console.log('');
    }
  }

  // Filtered out summary
  console.log('─'.repeat(60));
  console.log(`📊 FILTERED OUT: ${failed.length} junk buys skipped`);
  
  const failBreakdown = {};
  for (const f of failed) {
    const reasons = f.reason.split(', ');
    for (const r of reasons) {
      failBreakdown[r] = (failBreakdown[r] || 0) + 1;
    }
  }
  
  for (const [reason, count] of Object.entries(failBreakdown)) {
    console.log(`   • ${reason}: ${count}`);
  }
  
  console.log('\n' + '='.repeat(60));
}

main().catch(console.error);
