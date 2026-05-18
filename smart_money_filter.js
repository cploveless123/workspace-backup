const fs = require('fs');
const { execSync } = require('child_process');

const data = require('./smartmoney_raw.json');
const now = Math.floor(Date.now() / 1000);

// Tier wallets
const tier1Wallets = [
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
];

const tier2Wallets = [
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
];

// Filter buys only (exclude WSOL)
const buys = data.list.filter(t => t.side === 'buy' && t.base_token.symbol !== 'WSOL');

// Group by token
const tokenMap = {};
for (const t of buys) {
  const addr = t.base_address;
  if (!tokenMap[addr]) {
    tokenMap[addr] = {
      symbol: t.base_token.symbol,
      address: addr,
      trades: [],
      wallets: new Set(),
      totalAmount: 0,
      isTier1: false,
      isTier2: false
    };
  }
  tokenMap[addr].trades.push(t);
  tokenMap[addr].wallets.add(t.maker);
  tokenMap[addr].totalAmount += t.amount_usd;
  if (tier1Wallets.includes(t.maker)) tokenMap[addr].isTier1 = true;
  if (tier2Wallets.includes(t.maker)) tokenMap[addr].isTier2 = true;
}

// Get unique token addresses for token info fetching
const tokens = Object.values(tokenMap);
console.log(`Found ${buys.length} buys across ${tokens.length} unique tokens`);
console.log('Fetching token info for each...\n');

const results = [];
const skipped = { tooOld: 0, lowVolume: 0, volumeCollapsed: 0, dumping: 0, distribution: 0, lowHolders: 0, highBot: 0 };

for (const token of tokens) {
  try {
    const cmd = `gmgn-cli token info --chain sol --address ${token.address} --raw 2>/dev/null`;
    const output = execSync(cmd, { encoding: 'utf8', timeout: 15000 });
    const info = JSON.parse(output);
    
    // Extract fields
    const tokenData = info.token || info;
    const createTime = tokenData.token_create_time || tokenData.create_time || 0;
    const ageMinutes = createTime ? (now - createTime) / 60 : 9999;
    
    const volume5m = tokenData.volume_5m || tokenData.vol_5m || 0;
    const volume1h = tokenData.volume_1h || tokenData.vol_1h || 0;
    const volumeTrend = volume1h > 0 ? (volume5m / (volume1h / 12)) * 100 : 0;
    
    const price1hHigh = tokenData.price_1h_high || tokenData.high_1h || tokenData.price || 0;
    const currentPrice = tokenData.price || tokenData.price_usd || 0;
    const priceVsHigh = price1hHigh > 0 ? (currentPrice / price1hHigh) * 100 : 100;
    
    const buys1h = tokenData.buys_1h || tokenData.buy_count_1h || 0;
    const sells1h = tokenData.sells_1h || tokenData.sell_count_1h || 0;
    const buyRatio = (buys1h + sells1h) > 0 ? buys1h / (buys1h + sells1h) : 0;
    
    const holders = tokenData.holders || tokenData.holder_count || 0;
    const botRate = tokenData.bot_degen_rate || tokenData.bot_rate || 0;
    const mcap = tokenData.market_cap || tokenData.mcap || 0;
    
    // Apply filters
    const filters = {
      age: ageMinutes < 30,
      volume: volume5m > 5000,
      trend: volumeTrend > 20,
      price: priceVsHigh > 70,
      ratio: buyRatio > 0.6,
      holders: holders > 100,
      bot: botRate < 40
    };
    
    const passed = Object.values(filters).filter(v => v).length;
    const allPass = Object.values(filters).every(v => v);
    
    if (!allPass) {
      if (!filters.age) skipped.tooOld++;
      if (!filters.volume) skipped.lowVolume++;
      if (!filters.trend) skipped.volumeCollapsed++;
      if (!filters.price) skipped.dumping++;
      if (!filters.ratio) skipped.distribution++;
      if (!filters.holders) skipped.lowHolders++;
      if (!filters.bot) skipped.highBot++;
      continue;
    }
    
    // Check cluster signal
    const clusterWallets = Array.from(token.wallets);
    const isCluster = clusterWallets.length >= 2;
    const largeAmount = token.totalAmount >= 500;
    const fullPosition = token.trades.some(t => t.is_open_or_close === 1);
    const freshHighVol = ageMinutes < 15 && volume5m > 10000;
    
    results.push({
      symbol: token.symbol,
      address: token.address,
      trades: token.trades,
      wallets: clusterWallets,
      totalAmount: token.totalAmount,
      age: ageMinutes,
      volume5m,
      volumeTrend,
      priceVsHigh,
      buyRatio,
      holders,
      botRate,
      mcap,
      isCluster,
      largeAmount,
      fullPosition,
      freshHighVol,
      isTier1: token.isTier1,
      isTier2: token.isTier2
    });
    
  } catch (e) {
    console.error(`Error fetching ${token.symbol}: ${e.message}`);
  }
}

// Sort by conviction
results.sort((a, b) => {
  const scoreA = (a.isCluster ? 4 : 0) + (a.largeAmount ? 2 : 0) + (a.fullPosition ? 2 : 0) + (a.freshHighVol ? 2 : 0) + (a.isTier1 ? 3 : 0);
  const scoreB = (b.isCluster ? 4 : 0) + (b.largeAmount ? 2 : 0) + (b.fullPosition ? 2 : 0) + (b.freshHighVol ? 2 : 0) + (b.isTier1 ? 3 : 0);
  return scoreB - scoreA;
});

// Output report
console.log('\n═══════════════════════════════════════════');
console.log('🔥 HIGH-CONVICTION SMART MONEY SIGNALS');
console.log('═══════════════════════════════════════════\n');

for (const r of results) {
  const walletNames = r.wallets.map(w => {
    const trade = r.trades.find(t => t.maker === w);
    const name = trade?.maker_info?.name || w.slice(0, 8) + '...';
    const tier = tier1Wallets.includes(w) ? ' [T1]' : tier2Wallets.includes(w) ? ' [T2]' : '';
    return name + tier;
  }).join(', ');
  
  const positionType = r.fullPosition ? 'FULL' : 'PARTIAL';
  const mainTrade = r.trades[0];
  
  console.log(`🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)`);
  console.log(`[${new Date(mainTrade.timestamp * 1000).toISOString().slice(11,16)}] ${walletNames} — BUY $${r.totalAmount.toFixed(2)} ${r.symbol} [${positionType}]`);
  console.log(`📍 ${r.address}`);
  console.log(`💰 MCAP: $${(r.mcap/1000).toFixed(1)}K | Price: $${mainTrade.price_usd.toExponential(2)} | vs 1h High: ${r.priceVsHigh.toFixed(1)}%`);
  console.log(`⏱️ Age: ${r.age.toFixed(1)} min | Vol 5m: $${r.volume5m.toFixed(0)} | Vol Trend: ${r.volumeTrend.toFixed(1)}%`);
  console.log(`📊 Buy Ratio: ${(r.buyRatio*100).toFixed(1)}% | Holders: ${r.holders} | Bot Rate: ${r.botRate.toFixed(1)}%`);
  console.log(`🔗 DexScreener: https://dexscreener.com/solana/${r.address}`);
  console.log(`💵 Buy: /buy ${r.address} 0.1`);
  console.log(`\n⚡ CONVICTION INDICATORS:`);
  console.log(`• Multiple wallets: ${r.isCluster ? 'YES ✅' : 'NO'}`);
  console.log(`• Large amount: ${r.largeAmount ? 'YES ✅' : 'NO'}`);
  console.log(`• Full position: ${r.fullPosition ? 'YES ✅' : 'NO'}`);
  console.log(`• Fresh + high volume: ${r.freshHighVol ? 'YES ✅' : 'NO'}`);
  console.log(`• Tier wallet: ${r.isTier1 ? 'T1 ✅' : r.isTier2 ? 'T2' : 'NO'}`);
  console.log(`───────────────────────────────────────────\n`);
}

const totalSkipped = Object.values(skipped).reduce((a,b) => a+b, 0);
console.log(`📊 FILTERED OUT: ${totalSkipped} low-conviction buys skipped`);
console.log(`• Too old (>30min): ${skipped.tooOld}`);
console.log(`• Low volume (<$5K 5m): ${skipped.lowVolume}`);
console.log(`• Volume collapsed (<20% of 1h avg): ${skipped.volumeCollapsed}`);
console.log(`• Dumping (<70% of 1h high): ${skipped.dumping}`);
console.log(`• Distribution (buy ratio <60%): ${skipped.distribution}`);
console.log(`• Low holders (<100): ${skipped.lowHolders}`);
console.log(`• High bot rate (>40%): ${skipped.highBot}`);
console.log(`\n✅ ${results.length} HIGH-CONVICTION signals passed all filters`);
