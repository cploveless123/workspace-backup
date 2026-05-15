#!/usr/bin/env node
/**
 * Smart Money Tracker - Filtered Report
 * Fetches smart money buys, then filters tokens by quality criteria.
 */

const { execSync } = require('child_process');

// ─── Config ──────────────────────────────────────────────────────────
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
  'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT',
]);

const TIER2 = new Set([
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw',
]);

const CURRENT_TIME = Math.floor(Date.now() / 1000); // Unix timestamp
const MAX_AGE_SECONDS = 6 * 60 * 60; // 6 hours
const MIN_VOLUME_5M = 2000;
const MIN_HOLDERS = 100;
const MIN_PRICE_VS_ATH = 0.5; // 50%
const MAX_BOT_RATE = 0.40; // 40%

// ─── Helpers ─────────────────────────────────────────────────────────
function run(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
  } catch (e) {
    return e.stdout || e.message || '';
  }
}

function getWalletTier(addr) {
  if (TIER1.has(addr)) return 'TIER1';
  if (TIER2.has(addr)) return 'TIER2';
  return null;
}

function getWalletLabel(addr) {
  const labels = {
    '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3': 'Cowboy🔶BNB',
    '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4': 'Stigman',
  };
  return labels[addr] || addr.slice(0, 6) + '...' + addr.slice(-4);
}

function formatAge(seconds) {
  const mins = Math.floor(seconds / 60);
  if (mins < 60) return `${mins}m`;
  const hrs = Math.floor(mins / 60);
  const rem = mins % 60;
  return `${hrs}h ${rem}m`;
}

function formatUSD(n) {
  if (n >= 1000) return '$' + (n / 1000).toFixed(1) + 'K';
  return '$' + n.toFixed(0);
}

// ─── Fetch Smart Money ─────────────────────────────────────────────
console.log('📡 Fetching smart money activity...\n');
const raw = run('gmgn-cli track smartmoney --chain sol --limit 100 --raw');
let data;
try {
  data = JSON.parse(raw);
} catch (e) {
  console.error('❌ Failed to parse smart money data:', e.message);
  process.exit(1);
}

const trades = data.list || [];

// Filter to BUYs only
const buys = trades.filter(t => t.side === 'buy');

// Deduplicate by (wallet, token) — keep latest
const seen = new Map();
for (const t of buys) {
  const key = `${t.maker}_${t.base_address}`;
  if (!seen.has(key) || t.timestamp > seen.get(key).timestamp) {
    seen.set(key, t);
  }
}
const uniqueBuys = Array.from(seen.values());

// Sort by timestamp desc
uniqueBuys.sort((a, b) => b.timestamp - a.timestamp);

console.log(`🔍 Found ${buys.length} raw buys → ${uniqueBuys.length} unique (wallet+token)\n`);

// ─── Process Each Buy ────────────────────────────────────────────────
const passed = [];
const skipped = { age: 0, volume: 0, holders: 0, price: 0, bot: 0, other: 0 };

for (const trade of uniqueBuys) {
  const tier = getWalletTier(trade.maker);
  if (!tier) continue; // Only track TIER1/TIER2 wallets

  const tokenAddr = trade.base_address;
  const symbol = trade.base_token?.symbol || '???';
  const amount = trade.amount_usd || 0;

  console.log(`🔎 Checking ${symbol} (${tokenAddr.slice(0, 8)}...) from ${getWalletLabel(trade.maker)}...`);

  // Fetch token info
  const tokenRaw = run(`gmgn-cli token info --chain sol --address ${tokenAddr} --raw`);
  let info;
  try {
    info = JSON.parse(tokenRaw);
  } catch (e) {
    console.log(`   ⚠️  Token info fetch failed, skipping`);
    skipped.other++;
    continue;
  }

  // Extract fields - check nested price object first, then top-level
  const priceObj = info.price || {};
  const tokenCreateTime = info.creation_timestamp || info.token_create_time || 0;
  const ageSeconds = tokenCreateTime ? CURRENT_TIME - tokenCreateTime : Infinity;
  const volume5m = priceObj.volume_5m || info.volume_5m || 0;
  const holders = info.stat?.holder_count || info.holder_count || 0;
  const price = parseFloat(priceObj.price || info.price || 0);
  const athPrice = info.ath_price || 0;
  const botRate = info.stat?.bot_degen_rate || info.bot_degen_rate || 0;
  const mcap = info.market_cap || info.market_cap_sol || info.migration_market_cap || 0;

  // Apply filters
  let failReason = null;
  if (ageSeconds > MAX_AGE_SECONDS) failReason = 'age';
  else if (volume5m < MIN_VOLUME_5M) failReason = 'volume';
  else if (holders < MIN_HOLDERS) failReason = 'holders';
  else if (athPrice > 0 && price / athPrice < MIN_PRICE_VS_ATH) failReason = 'price';
  else if (botRate > MAX_BOT_RATE) failReason = 'bot';

  if (failReason) {
    skipped[failReason]++;
    const reasonMap = {
      age: `Age ${formatAge(ageSeconds)} > 6h`,
      volume: `Vol 5m ${formatUSD(volume5m)} < $2K`,
      holders: `Holders ${holders} < 100`,
      price: `Price ${(price/athPrice*100).toFixed(0)}% ATH < 50%`,
      bot: `Bot rate ${(botRate*100).toFixed(0)}% > 40%`,
    };
    console.log(`   ❌ FILTER FAIL: ${reasonMap[failReason]} — SKIPPED`);
    continue;
  }

  // All filters passed!
  const priceVsAth = athPrice > 0 ? (price / athPrice * 100).toFixed(0) : 'N/A';
  passed.push({
    trade,
    info,
    tier,
    walletLabel: getWalletLabel(trade.maker),
    ageSeconds,
    volume5m,
    holders,
    botRate,
    priceVsAth,
    mcap,
  });

  console.log(`   ✅ ALL FILTERS PASSED!`);
}

// ─── Report ──────────────────────────────────────────────────────────
console.log('\n' + '='.repeat(60));
console.log(`🔥 SMART MONEY FILTERED REPORT`);
console.log(`📅 ${new Date().toUTCString()}`);
console.log('='.repeat(60) + '\n');

if (passed.length === 0) {
  console.log('❌ No quality signals found. All buys failed filters.\n');
} else {
  console.log(`✅ ${passed.length} QUALITY SIGNAL(S) FOUND:\n`);

  for (const p of passed) {
    const t = p.trade;
    const isFull = t.is_open_or_close === 1 ? 'FULL' : 'PARTIAL';
    const tierEmoji = p.tier === 'TIER1' ? '🔴' : '🟡';

    console.log(`${tierEmoji} QUALITY SIGNAL (5/5 filters passed)`);
    console.log(`[${new Date(t.timestamp * 1000).toISOString().slice(11, 19)} UTC] ${p.walletLabel} — BUY ${t.base_token?.symbol || '???'} ${formatUSD(t.amount_usd || 0)} [${isFull}]`);
    console.log(`📍 ${t.base_address}`);
    console.log(`💰 MCAP: ${formatUSD(p.mcap)} | Price: $${(t.price_usd || 0).toExponential(2)} | vs ATH: ${p.priceVsAth}%`);
    console.log(`⏱️ Age: ${formatAge(p.ageSeconds)} | Vol 5m: ${formatUSD(p.volume5m)} | Holders: ${p.holders}`);
    console.log(`🤖 Bot Rate: ${(p.botRate * 100).toFixed(1)}%`);
    console.log(`🔗 DexScreener: https://dexscreener.com/solana/${t.base_address}`);
    console.log(`💵 Buy: /buy ${t.base_address} 0.1`);
    console.log('');
  }
}

// Filter summary
const totalSkipped = Object.values(skipped).reduce((a, b) => a + b, 0);
console.log(`📊 FILTERED OUT: ${totalSkipped} junk buys skipped`);
if (skipped.age > 0) console.log(`   • Age > 6h: ${skipped.age}`);
if (skipped.volume > 0) console.log(`   • Volume 5m < $2K: ${skipped.volume}`);
if (skipped.holders > 0) console.log(`   • Holders < 100: ${skipped.holders}`);
if (skipped.price > 0) console.log(`   • Price < 50% ATH: ${skipped.price}`);
if (skipped.bot > 0) console.log(`   • Bot rate > 40%: ${skipped.bot}`);
if (skipped.other > 0) console.log(`   • Other/fetch errors: ${skipped.other}`);

console.log('\n' + '='.repeat(60));
console.log(`✨ Only ${passed.length} of ${uniqueBuys.length} unique buys passed all filters`);
console.log('='.repeat(60));
