#!/usr/bin/env node
/**
 * Smart Money Quality Signal Filter
 * Fetches smart money trades, filters tokens, reports only quality signals
 */

const { execSync } = require('child_process');

// ─── CONFIG ───────────────────────────────────────────────────────
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

const TIER_NAMES = {
  '6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3': 'Cowboy🔶BNB',
  '65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE': '+$5K 62.7% WR',
  '3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f': '+$6.4K 56.7% WR',
  'H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V': '+$27K consistent',
  '8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4': 'Stigman +$8.3K',
  '7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5': '+$4.9K 67.7% WR',
  'MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN': '+$2.9K 69.9% WR',
  'FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS': '+$4.5K 43% WR',
  'tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir': '+$3.7K 42% WR',
  '1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C': '+$4.6K 43% WR',
  'Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX': '+$3.7K 70% WR',
  'BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT': '+$1.7K 66% WR',
};

// ─── FILTERS ──────────────────────────────────────────────────────
const MAX_AGE_HOURS = 6;
const MIN_VOLUME_5M = 2000;
const MIN_HOLDERS = 100;
const MIN_PRICE_VS_ATH = 0.50;
const MAX_BOT_RATE = 0.40;

// ─── HELPERS ──────────────────────────────────────────────────────
function run(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf8', timeout: 15000 });
  } catch (e) {
    return null;
  }
}

function nowSec() {
  return Math.floor(Date.now() / 1000);
}

function fmtTime(ts) {
  const d = new Date(ts * 1000);
  return d.toISOString().replace('T', ' ').slice(0, 19) + ' UTC';
}

function short(addr) {
  return addr.slice(0, 4) + '…' + addr.slice(-4);
}

function getTier(maker) {
  if (TIER1.has(maker)) return 'T1';
  if (TIER2.has(maker)) return 'T2';
  return null;
}

function getWalletLabel(maker) {
  const tier = getTier(maker);
  const name = TIER_NAMES[maker] || '';
  if (tier === 'T1') return `🔥T1 ${name}`;
  if (tier === 'T2') return `⚡T2 ${name}`;
  return `📊 ${short(maker)}`;
}

// ─── FETCH SMART MONEY TRADES ─────────────────────────────────────
function fetchSmartMoney() {
  const raw = run('gmgn-cli track smartmoney --chain sol --limit 100 --raw 2>&1');
  if (!raw) return [];
  try {
    const data = JSON.parse(raw);
    return data.list || [];
  } catch {
    return [];
  }
}

// ─── FETCH TOKEN INFO ─────────────────────────────────────────────
function fetchTokenInfo(address) {
  const raw = run(`gmgn-cli token info --chain sol --address ${address} --raw 2>&1`);
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

// ─── APPLY FILTERS ────────────────────────────────────────────────
function applyFilters(tokenInfo, trade) {
  const fails = [];
  const now = nowSec();

  // 1. Age < 6 hours
  const creationTs = tokenInfo.creation_timestamp || 0;
  const ageHours = creationTs ? (now - creationTs) / 3600 : 999;
  if (ageHours > MAX_AGE_HOURS) fails.push(`age ${ageHours.toFixed(1)}h > 6h`);

  // 2. Volume 5m > $2,000
  const vol5m = tokenInfo.volume_5m || 0;
  if (vol5m < MIN_VOLUME_5M) fails.push(`vol5m $${vol5m.toFixed(0)} < $2K`);

  // 3. Holders > 100
  const holders = tokenInfo.holder_count || tokenInfo.stat?.holder_count || 0;
  if (holders < MIN_HOLDERS) fails.push(`holders ${holders} < 100`);

  // 4. Price > 50% of ATH
  const price = tokenInfo.price || 0;
  const ath = tokenInfo.ath_price || 0;
  const priceVsAth = ath > 0 ? price / ath : 0;
  if (priceVsAth < MIN_PRICE_VS_ATH) fails.push(`price ${(priceVsAth * 100).toFixed(0)}% ATH < 50%`);

  // 5. Bot rate < 40%
  const botRate = tokenInfo.stat?.bot_degen_rate || 0;
  if (botRate > MAX_BOT_RATE) fails.push(`bot ${(botRate * 100).toFixed(0)}% > 40%`);

  return { passes: fails.length === 0, fails, ageHours, vol5m, holders, priceVsAth, botRate, price, ath };
}

// ─── MAIN ─────────────────────────────────────────────────────────
function main() {
  console.log(`\n🔍 Smart Money Quality Filter — ${fmtTime(nowSec())}\n`);

  const trades = fetchSmartMoney();
  const buys = trades.filter(t => t.side === 'buy');

  console.log(`📊 Total smart money trades: ${trades.length} | Buys: ${buys.length}\n`);

  // Deduplicate by token+wallet to avoid duplicate analysis
  const seen = new Set();
  const uniqueBuys = [];
  for (const t of buys) {
    const key = `${t.maker}_${t.base_address}`;
    if (!seen.has(key)) {
      seen.add(key);
      uniqueBuys.push(t);
    }
  }

  const qualitySignals = [];
  const skipped = { age: 0, volume: 0, holders: 0, ath: 0, bot: 0, total: 0 };
  const processedTokens = new Set();
  const tokenCache = {};

  for (const trade of uniqueBuys) {
    const tokenAddr = trade.base_address;
    const wallet = trade.maker;
    const tier = getTier(wallet);

    // Skip WSOL
    if (tokenAddr === 'So11111111111111111111111111111111111111112') continue;

  // Only process each token once (first buy wins for token info)
    let tokenInfo;
    if (!processedTokens.has(tokenAddr)) {
      tokenInfo = fetchTokenInfo(tokenAddr);
      processedTokens.add(tokenAddr);
    } else {
      // Re-use previous result for this token
      tokenInfo = tokenCache[tokenAddr];
    }
    if (!tokenInfo) {
      skipped.total++;
      continue;
    }
    // Cache for reuse
    tokenCache[tokenAddr] = tokenInfo;

    if (!tokenInfo) {
      skipped.total++;
      continue;
    }

    const result = applyFilters(tokenInfo, trade);

    if (!result.passes) {
      skipped.total++;
      if (result.fails.some(f => f.includes('age'))) skipped.age++;
      if (result.fails.some(f => f.includes('vol5m'))) skipped.volume++;
      if (result.fails.some(f => f.includes('holders'))) skipped.holders++;
      if (result.fails.some(f => f.includes('ATH'))) skipped.ath++;
      if (result.fails.some(f => f.includes('bot'))) skipped.bot++;
      continue;
    }

    // Calculate MCAP
    const mcap = (tokenInfo.price || 0) * (tokenInfo.circulating_supply || tokenInfo.total_supply || 0);
    const symbol = trade.base_token?.symbol || tokenInfo.symbol || '???';

    qualitySignals.push({
      wallet,
      walletLabel: getWalletLabel(wallet),
      tier,
      token: symbol,
      address: tokenAddr,
      amount: trade.amount_usd || 0,
      mcap,
      ageMin: Math.round(result.ageHours * 60),
      vol5m: result.vol5m,
      holders: result.holders,
      botRate: result.botRate,
      priceVsAth: result.priceVsAth,
      price: result.price,
      timestamp: trade.timestamp,
      isOpenOrClose: trade.is_open_or_close,
    });
  }

  // ─── REPORT QUALITY SIGNALS ─────────────────────────────────────
  if (qualitySignals.length === 0) {
    console.log('❌ NO QUALITY SIGNALS FOUND\n');
  } else {
    console.log(`🔥 QUALITY SIGNALS: ${qualitySignals.length} PASSED ALL FILTERS\n`);
    console.log('═'.repeat(60));

    for (const s of qualitySignals) {
      const time = fmtTime(s.timestamp);
      const positionType = s.isOpenOrClose === 1 ? 'FULL' : 'PARTIAL';
      const tierEmoji = s.tier === 'T1' ? '🔥' : s.tier === 'T2' ? '⚡' : '📊';

      console.log(`\n${tierEmoji} [${time}] ${s.walletLabel}`);
      console.log(`   BUY $${s.amount.toFixed(2)} ${s.token} [${positionType}]`);
      console.log(`   📍 ${s.address}`);
      console.log(`   💰 MCAP: $${(s.mcap / 1000).toFixed(1)}K | Price: $${s.price.toExponential(2)} | vs ATH: ${(s.priceVsAth * 100).toFixed(0)}%`);
      console.log(`   ⏱️ Age: ${s.ageMin} min | Vol 5m: $${s.vol5m.toFixed(0)} | Holders: ${s.holders}`);
      console.log(`   🤖 Bot Rate: ${(s.botRate * 100).toFixed(0)}%`);
      console.log(`   🔗 DexScreener: https://dexscreener.com/solana/${s.address}`);
      console.log(`   💵 Buy: /buy ${s.address} 0.1`);
    }
    console.log('\n' + '═'.repeat(60));
  }

  // ─── FILTER SUMMARY ─────────────────────────────────────────────
  console.log(`\n📊 FILTERED OUT: ${skipped.total} junk buys skipped`);
  if (skipped.age > 0) console.log(`   • Age > 6h: ${skipped.age}`);
  if (skipped.volume > 0) console.log(`   • Vol 5m < $2K: ${skipped.volume}`);
  if (skipped.holders > 0) console.log(`   • Holders < 100: ${skipped.holders}`);
  if (skipped.ath > 0) console.log(`   • Price < 50% ATH: ${skipped.ath}`);
  if (skipped.bot > 0) console.log(`   • Bot rate > 40%: ${skipped.bot}`);

  console.log('\n✅ Done.\n');
}

main();
