#!/usr/bin/env node
/**
 * Smart Money Tracker - High-Conviction Signal Filter
 * Processes gmgn-cli smartmoney output and applies strict filters
 */

const fs = require('fs');

// Current time: 2026-05-16 07:22 UTC
const CURRENT_TIME = 1778917320; // Unix timestamp for 2026-05-16 07:22 UTC

// Tier1 wallets (must follow)
const TIER1_WALLETS = new Set([
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

// Tier2 wallets (monitor)
const TIER2_WALLETS = new Set([
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
]);

// Read JSON from stdin
let data;
try {
  const input = fs.readFileSync(0, 'utf-8');
  data = JSON.parse(input);
} catch (e) {
  console.error('Error parsing JSON:', e.message);
  process.exit(1);
}

if (!data.list || !Array.isArray(data.list)) {
  console.error('No list array found in data');
  process.exit(1);
}

// Filter to BUY trades only
const buys = data.list.filter(t => t.side === 'buy');

// Group by token address
const tokenGroups = {};
for (const trade of buys) {
  const addr = trade.base_address;
  if (!tokenGroups[addr]) {
    tokenGroups[addr] = [];
  }
  tokenGroups[addr].push(trade);
}

// Track stats
let totalBuys = buys.length;
let skippedOld = 0;
let skippedLowVolume = 0;
let skippedVolumeCollapsed = 0;
let skippedDumping = 0;
let skippedDistribution = 0;
let skippedLowHolders = 0;
let skippedBot = 0;
let highConvictionSignals = [];

// Process each unique token
for (const [tokenAddr, trades] of Object.entries(tokenGroups)) {
  // We need token info - but the track data doesn't have all fields
  // For now, we'll flag tokens that need further investigation
  // and note which ones we can assess from track data alone
  
  const token = trades[0].base_token;
  const symbol = token.symbol;
  
  // Check if any tier1 wallet is buying
  const tier1Buyers = trades.filter(t => TIER1_WALLETS.has(t.maker));
  const tier2Buyers = trades.filter(t => TIER2_WALLETS.has(t.maker));
  const isTier1 = tier1Buyers.length > 0;
  const isTier2 = tier2Buyers.length > 0;
  
  // Cluster signal
  const uniqueWallets = new Set(trades.map(t => t.maker)).size;
  const isCluster = uniqueWallets >= 2;
  
  // Large buys
  const largeBuys = trades.filter(t => t.amount_usd >= 500);
  const hasLargeBuy = largeBuys.length > 0;
  
  // Full position opens (for smartmoney: is_open_or_close = 0 means position opened)
  const fullOpens = trades.filter(t => t.is_open_or_close === 0);
  const hasFullOpen = fullOpens.length > 0;
  
  // Total buy amount
  const totalBuyAmount = trades.reduce((sum, t) => sum + t.amount_usd, 0);
  
  // Time range
  const timestamps = trades.map(t => t.timestamp);
  const oldest = Math.min(...timestamps);
  const newest = Math.max(...timestamps);
  const timeSpan = newest - oldest;
  
  // We can't fully filter without token info, but we can identify candidates
  // Flag for manual review with available data
  
  const signal = {
    token: symbol,
    address: tokenAddr,
    trades: trades.length,
    uniqueWallets: uniqueWallets,
    tier1Buyers: tier1Buyers.length,
    tier2Buyers: tier2Buyers.length,
    totalAmount: totalBuyAmount,
    largestBuy: Math.max(...trades.map(t => t.amount_usd)),
    hasFullOpen: hasFullOpen,
    isCluster: isCluster,
    timeSpan: timeSpan,
    launchpad: token.launchpad,
    needsTokenInfo: true
  };
  
  highConvictionSignals.push(signal);
}

// Sort by conviction (tier1 first, then amount, then cluster)
highConvictionSignals.sort((a, b) => {
  if (a.tier1Buyers !== b.tier1Buyers) return b.tier1Buyers - a.tier1Buyers;
  if (a.isCluster !== b.isCluster) return b.isCluster ? 1 : -1;
  return b.totalAmount - a.totalAmount;
});

// Output report
console.log(`🔥 SMART MONEY TRACKER — ${new Date(CURRENT_TIME * 1000).toUTCString()}`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`📊 Total smart money buys in last 100 trades: ${totalBuys}`);
console.log(`🎯 Unique tokens being bought: ${Object.keys(tokenGroups).length}`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n`);

// Show top signals
let reported = 0;
for (const signal of highConvictionSignals.slice(0, 10)) {
  const tier1Tag = signal.tier1Buyers > 0 ? '⭐TIER1' : (signal.tier2Buyers > 0 ? '🔍TIER2' : '');
  const clusterTag = signal.isCluster ? '⚡CLUSTER' : '';
  const fullOpenTag = signal.hasFullOpen ? '🔒FULL' : '';
  
  console.log(`🔥 ${signal.token} ${tier1Tag} ${clusterTag} ${fullOpenTag}`);
  console.log(`   📍 ${signal.address}`);
  console.log(`   💰 Total: $${signal.totalAmount.toFixed(2)} | Largest: $${signal.largestBuy.toFixed(2)}`);
  console.log(`   👥 Wallets: ${signal.uniqueWallets} | Trades: ${signal.trades}`);
  if (signal.tier1Buyers > 0) console.log(`   ⭐ Tier1 Buyers: ${signal.tier1Buyers}`);
  if (signal.tier2Buyers > 0) console.log(`   🔍 Tier2 Buyers: ${signal.tier2Buyers}`);
  console.log(`   ⏱️ Time span: ${signal.timeSpan}s | Launchpad: ${signal.launchpad || 'N/A'}`);
  console.log(`   🔗 DexScreener: https://dexscreener.com/solana/${signal.address}`);
  console.log(`   💵 Buy: /buy ${signal.address} 0.1\n`);
  reported++;
}

console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
console.log(`⚠️  NOTE: Full filtering requires token info (age, volume, holders, bot rate)`);
console.log(`   Run: gmgn-cli token info --chain sol --address <TOKEN> --raw`);
console.log(`   for each candidate to apply strict filters.`);
console.log(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
