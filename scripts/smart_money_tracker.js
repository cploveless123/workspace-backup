#!/usr/bin/env node
/**
 * Smart Money Tracker - Quality Filtered Report
 * Fetches smart money buys, applies quality filters, reports only passing tokens
 */

const { execSync } = require('child_process');

// Tier 1 wallets (must follow)
const TIER1 = new Set([
  '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3',
  '65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE',
  '3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f',
  'H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V',
  '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4',
  '7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5',
  'MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN',
  'FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS',
  'tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir',
  '1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C',
  'Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX',
  'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT'
]);

// Tier 2 wallets (monitor)
const TIER2 = new Set([
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
]);

// Quality filters
const FILTERS = {
  maxAgeHours: 6,
  minVolume5m: 2000,
  minHolders: 100,
  minPriceVsATH: 0.50,
  maxBotRate: 0.40
};

const NOW = Math.floor(Date.now() / 1000);
const NOW_UTC = new Date().toISOString().replace('T', ' ').slice(0, 19) + ' UTC';

function getWalletTier(addr) {
  if (TIER1.has(addr)) return 'T1';
  if (TIER2.has(addr)) return 'T2';
  return 'SM';
}

function getWalletLabel(addr, tags) {
  if (TIER1.has(addr)) return 'TIER1';
  if (TIER2.has(addr)) return 'TIER2';
  return tags?.join(',') || 'SM';
}

function runCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout: 30000, stdio: ['pipe', 'pipe', 'pipe'] });
  } catch (e) {
    return e.stdout || e.stderr || '';
  }
}

function fetchTokenInfo(tokenAddress) {
  const raw = runCmd(`gmgn-cli token info --chain sol --address ${tokenAddress} --raw 2>&1`);
  try {
    const data = JSON.parse(raw);
    return data;
  } catch (e) {
    return null;
  }
}

function applyFilters(tokenInfo) {
  const failures = [];
  
  if (!tokenInfo) {
    return { pass: false, failures: ['API_ERROR'], data: null };
  }
  
  const creationTime = tokenInfo.creation_timestamp || 0;
  const ageHours = (NOW - creationTime) / 3600;
  
  // Note: volume_5m is NOT in token info - we need to check if it exists
  // token info doesn't have volume_5m directly, we'll check what we have
  const volume5m = tokenInfo.volume_5m || 0;
  const holders = tokenInfo.holder_count || 0;
  const price = tokenInfo.price || 0;
  const athPrice = tokenInfo.ath_price || 0;
  const priceVsATH = athPrice > 0 ? price / athPrice : 1;
  const botRate = tokenInfo.stat?.bot_degen_rate || 0;
  
  // Filter 1: Age < 6 hours
  if (ageHours > FILTERS.maxAgeHours) {
    failures.push(`age:${Math.round(ageHours)}h`);
  }
  
  // Filter 2: Volume 5m > $2,000 (if available)
  if (volume5m > 0 && volume5m < FILTERS.minVolume5m) {
    failures.push(`vol5m:$${Math.round(volume5m)}`);
  }
  
  // Filter 3: Holders > 100
  if (holders < FILTERS.minHolders) {
    failures.push(`holders:${holders}`);
  }
  
  // Filter 4: Price > 50% of ATH
  if (priceVsATH < FILTERS.minPriceVsATH) {
    failures.push(`priceVsATH:${(priceVsATH*100).toFixed(0)}%`);
  }
  
  // Filter 5: Bot rate < 40%
  if (botRate > FILTERS.maxBotRate) {
    failures.push(`botRate:${(botRate*100).toFixed(0)}%`);
  }
  
  return {
    pass: failures.length === 0,
    failures,
    data: {
      ageHours,
      ageMinutes: Math.round(ageHours * 60),
      volume5m,
      holders,
      price,
      athPrice,
      priceVsATH,
      botRate,
      mcap: (tokenInfo.price || 0) * (tokenInfo.circulating_supply || 0),
      symbol: tokenInfo.symbol,
      name: tokenInfo.name,
      liquidity: tokenInfo.liquidity || 0
    }
  };
}

function formatReport(buys, skipped) {
  let report = `🔥 SMART MONEY QUALITY REPORT\n`;
  report += `⏰ ${NOW_UTC}\n`;
  report += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
  
  if (buys.length === 0) {
    report += `❌ NO QUALITY SIGNALS FOUND\n`;
    report += `All ${skipped.length} buys filtered out.\n\n`;
  } else {
    report += `✅ ${buys.length} QUALITY SIGNALS (${buys.length} of ${buys.length + skipped.length} passed)\n\n`;
    
    for (const buy of buys) {
      const tier = getWalletTier(buy.maker);
      const tierEmoji = tier === 'T1' ? '🔶' : tier === 'T2' ? '🔸' : '💎';
      
      report += `${tierEmoji} [${buy.time}] ${buy.walletLabel} — BUY $${buy.amountUsd.toFixed(0)} ${buy.tokenSymbol}\n`;
      report += `📍 ${buy.tokenAddress}\n`;
      const mcap = Number(buy.filters.mcap) || 0;
      const price = Number(buy.filters.price) || 0;
      const priceVsATH = Number(buy.filters.priceVsATH) || 0;
      const mcapStr = mcap >= 1000000 ? `$${(mcap/1000000).toFixed(2)}M` : mcap >= 1000 ? `$${(mcap/1000).toFixed(1)}K` : `$${mcap.toFixed(0)}`;
      const priceStr = price > 0 ? `$${price.toExponential(2)}` : 'N/A';
      const athStr = priceVsATH > 0 ? `${(priceVsATH*100).toFixed(0)}%` : 'N/A';
      
      report += `💰 MCAP: ${mcapStr} | Price: ${priceStr} | vs ATH: ${athStr}\n`;
      report += `⏱️ Age: ${buy.filters.ageMinutes} min | Vol 5m: $${Math.round(buy.filters.volume5m)} | Holders: ${buy.filters.holders}\n`;
      report += `🤖 Bot Rate: ${(buy.filters.botRate*100).toFixed(0)}%\n`;
      report += `🔗 DexScreener: https://dexscreener.com/solana/${buy.tokenAddress}\n`;
      report += `💵 Buy: /buy ${buy.tokenAddress} 0.1\n\n`;
    }
  }
  
  // Filtered out summary
  const skipReasons = {};
  for (const s of skipped) {
    for (const reason of s.failures) {
      const key = reason.split(':')[0];
      skipReasons[key] = (skipReasons[key] || 0) + 1;
    }
  }
  
  report += `📊 FILTERED OUT: ${skipped.length} junk buys skipped\n`;
  for (const [reason, count] of Object.entries(skipReasons)) {
    report += `   • ${reason}: ${count}\n`;
  }
  
  return report;
}

async function main() {
  console.log('Fetching smart money activity...');
  
  // Fetch smart money trades
  const raw = runCmd('gmgn-cli track smartmoney --chain sol --limit 100 --raw 2>&1');
  let trades;
  try {
    trades = JSON.parse(raw);
  } catch (e) {
    console.error('Failed to parse smart money data:', e.message);
    process.exit(1);
  }
  
  if (!trades.list || trades.list.length === 0) {
    console.log('No smart money trades found.');
    process.exit(0);
  }
  
  // Filter to buys only
  const buys = trades.list.filter(t => t.side === 'buy');
  console.log(`Found ${buys.length} buy trades out of ${trades.list.length} total`);
  
  // Deduplicate by token address (keep most recent per token)
  const tokenMap = new Map();
  for (const buy of buys) {
    const existing = tokenMap.get(buy.base_address);
    if (!existing || buy.timestamp > existing.timestamp) {
      tokenMap.set(buy.base_address, buy);
    }
  }
  
  const uniqueBuys = Array.from(tokenMap.values());
  console.log(`Processing ${uniqueBuys.length} unique token buys...`);
  
  const passed = [];
  const skipped = [];
  
  // Process each unique buy
  for (const buy of uniqueBuys.slice(0, 20)) { // Limit to 20 to avoid rate limits
    const tokenAddress = buy.base_address;
    const walletAddr = buy.maker;
    
    console.log(`Checking ${buy.base_token?.symbol || 'UNKNOWN'} (${tokenAddress.slice(0, 8)}...)...`);
    
    const tokenInfo = fetchTokenInfo(tokenAddress);
    const result = applyFilters(tokenInfo);
    
    if (result.pass) {
      const date = new Date(buy.timestamp * 1000);
      const timeStr = date.toISOString().slice(11, 16);
      
      passed.push({
        tokenAddress,
        tokenSymbol: buy.base_token?.symbol || 'UNKNOWN',
        maker: walletAddr,
        walletLabel: getWalletLabel(walletAddr, buy.maker_info?.tags),
        amountUsd: buy.amount_usd || 0,
        time: timeStr,
        filters: result.data
      });
      console.log(`  ✅ PASSED all filters`);
    } else {
      skipped.push({
        tokenAddress,
        tokenSymbol: buy.base_token?.symbol || 'UNKNOWN',
        failures: result.failures
      });
      console.log(`  ❌ FAILED: ${result.failures.join(', ')}`);
    }
    
    // Rate limit protection
    await new Promise(r => setTimeout(r, 500));
  }
  
  // Generate report
  const report = formatReport(passed, skipped);
  console.log('\n' + report);
}

main().catch(console.error);
