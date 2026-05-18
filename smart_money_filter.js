#!/usr/bin/env node
const { execSync } = require('child_process');

const currentTime = 1779124930; // From the data timestamp

// Tracked wallets
const TIER1 = [
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

const TIER2 = [
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
];

const allTracked = [...TIER1, ...TIER2];

// Parse the raw data from stdin
let rawData = '';
process.stdin.on('data', chunk => rawData += chunk);
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(rawData);
    const transactions = data.list || [];
    
    // Extract unique BUY transactions from tracked wallets
    const buys = [];
    const seenTokens = new Set();
    
    for (const tx of transactions) {
      if (tx.side !== 'buy') continue;
      if (tx.base_token?.symbol === 'SOL' || tx.base_token?.symbol === 'WSOL') continue;
      
      const isTracked = allTracked.includes(tx.maker);
      const tier = TIER1.includes(tx.maker) ? 'TIER1' : (TIER2.includes(tx.maker) ? 'TIER2' : 'OTHER');
      
      buys.push({
        wallet: tx.maker,
        tier,
        isTracked,
        symbol: tx.base_token?.symbol || 'Unknown',
        address: tx.base_address,
        amount_usd: tx.amount_usd,
        is_full: tx.is_open_or_close === 1,
        timestamp: tx.timestamp,
        tags: tx.maker_info?.tags || []
      });
      
      seenTokens.add(tx.base_address);
    }
    
    console.log(`Found ${buys.length} buys from ${seenTokens.size} unique tokens`);
    console.log('');
    
    // Group by token to find cluster signals
    const tokenBuys = {};
    for (const buy of buys) {
      if (!tokenBuys[buy.address]) {
        tokenBuys[buy.address] = [];
      }
      tokenBuys[buy.address].push(buy);
    }
    
    // Fetch token info for each unique token
    const tokenInfo = {};
    for (const address of seenTokens) {
      try {
        const result = execSync(`gmgn-cli token info --chain sol --address ${address} --raw 2>&1`, { timeout: 15000 });
        const info = JSON.parse(result.toString());
        tokenInfo[address] = info;
      } catch (e) {
        console.error(`Failed to fetch ${address}: ${e.message}`);
      }
    }
    
    // Apply filters
    const passed = [];
    const failed = [];
    const failReasons = { tooOld: 0, lowVolume: 0, volumeCollapsed: 0, dumping: 0, distribution: 0, lowHolders: 0, highBot: 0 };
    
    for (const [address, buysList] of Object.entries(tokenBuys)) {
      const info = tokenInfo[address];
      if (!info) {
        failed.push({ address, reason: 'No data', buys: buysList });
        continue;
      }
      
      const token = info;
      const price = info.price || {};
      const stat = info.stat || {};
      
      // Extract metrics from flat structure
      const creationTime = token.creation_timestamp || token.open_timestamp || 0;
      const ageMinutes = creationTime ? (currentTime - creationTime) / 60 : 999;
      
      const volume5m = parseFloat(price.volume_5m || 0);
      const volume1h = parseFloat(price.volume_1h || 0);
      const volumeTrend = volume1h > 0 ? (volume5m / (volume1h / 12)) * 100 : 0;
      
      const price1hHigh = parseFloat(token.ath_price || price.price_1h || 0);
      const currentPrice = parseFloat(price.price || 0);
      const priceVsHigh = price1hHigh > 0 ? (currentPrice / price1hHigh) * 100 : 100;
      
      const buys1h = price.buys_1h || 0;
      const sells1h = price.sells_1h || 0;
      const buyRatio = (buys1h + sells1h) > 0 ? buys1h / (buys1h + sells1h) : 0;
      
      const holders = token.holder_count || stat.holder_count || 0;
      const botRate = parseFloat(stat.bot_degen_rate || 0) * 100;
      
      const mcap = token.migration_market_cap || 0;
      
      // Apply filters
      let failReason = null;
      
      if (ageMinutes > 30) { failReason = 'Too old'; failReasons.tooOld++; }
      else if (volume5m < 5000) { failReason = 'Low volume'; failReasons.lowVolume++; }
      else if (volumeTrend < 20) { failReason = 'Volume collapsed'; failReasons.volumeCollapsed++; }
      else if (priceVsHigh < 70) { failReason = 'Dumping'; failReasons.dumping++; }
      else if (buyRatio < 0.6) { failReason = 'Distribution'; failReasons.distribution++; }
      else if (holders < 100) { failReason = 'Low holders'; failReasons.lowHolders++; }
      else if (botRate > 40) { failReason = 'High bot rate'; failReasons.highBot++; }
      
      const isCluster = buysList.length > 1;
      const hasLargeBuy = buysList.some(b => b.amount_usd >= 500);
      const hasFullPosition = buysList.some(b => b.is_full);
      const isFreshHighVolume = ageMinutes < 15 && volume5m > 10000;
      
      if (!failReason) {
        passed.push({
          address,
          symbol: buysList[0].symbol,
          buys: buysList,
          ageMinutes,
          volume5m,
          volumeTrend,
          priceVsHigh,
          buyRatio,
          holders,
          botRate,
          mcap,
          isCluster,
          hasLargeBuy,
          hasFullPosition,
          isFreshHighVolume
        });
      } else {
        failed.push({ address, reason: failReason, buys: buysList, ageMinutes, volume5m, buyRatio, holders, botRate });
      }
    }
    
    // Report
    console.log('=== HIGH-CONVICTION SIGNALS ===\n');
    
    if (passed.length === 0) {
      console.log('❌ NO tokens passed all filters\n');
    } else {
      for (const p of passed) {
        const totalBuy = p.buys.reduce((sum, b) => sum + b.amount_usd, 0);
        const wallets = p.buys.map(b => `${b.wallet.slice(0, 8)}...${b.wallet.slice(-4)}${b.tier === 'TIER1' ? '⭐' : ''}`).join(', ');
        
        console.log(`🔥 HIGH-CONVICTION SIGNAL (${p.buys.length} wallet${p.buys.length > 1 ? 's' : ''} buying)`);
        console.log(`${new Date(currentTime * 1000).toISOString()} — ${wallets}`);
        console.log(`💰 ${p.symbol} — BUY $${totalBuy.toFixed(2)} [${p.hasFullPosition ? 'FULL' : 'PARTIAL'}]`);
        console.log(`📍 ${p.address}`);
        console.log(`💰 MCAP: $${(p.mcap / 1000).toFixed(1)}K | Price: $${currentPrice?.toExponential?.(3) || 'N/A'} | vs 1h High: ${p.priceVsHigh.toFixed(1)}%`);
        console.log(`⏱️ Age: ${p.ageMinutes.toFixed(1)} min | Vol 5m: $${p.volume5m.toFixed(0)} | Vol Trend: ${p.volumeTrend.toFixed(1)}%`);
        console.log(`📊 Buy Ratio: ${(p.buyRatio * 100).toFixed(1)}% | Holders: ${p.holders} | Bot Rate: ${p.botRate.toFixed(1)}%`);
        console.log(`🔗 DexScreener: https://dexscreener.com/solana/${p.address}`);
        console.log(`💵 Buy: /buy ${p.address} 0.1`);
        console.log('');
        console.log('⚡ CONVICTION INDICATORS:');
        console.log(`• Multiple wallets: ${p.isCluster ? 'YES ✅' : 'NO'}`);
        console.log(`• Large amount: ${p.hasLargeBuy ? 'YES ✅' : 'NO'}`);
        console.log(`• Full position: ${p.hasFullPosition ? 'YES ✅' : 'NO'}`);
        console.log(`• Fresh + high volume: ${p.isFreshHighVolume ? 'YES ✅' : 'NO'}`);
        console.log('');
      }
    }
    
    console.log('=== FILTERED OUT ===');
    console.log(`📊 FILTERED OUT: ${failed.length} low-conviction buys skipped`);
    console.log(`• Too old: ${failReasons.tooOld}`);
    console.log(`• Low volume: ${failReasons.lowVolume}`);
    console.log(`• Volume collapsed: ${failReasons.volumeCollapsed}`);
    console.log(`• Dumping: ${failReasons.dumping}`);
    console.log(`• Distribution: ${failReasons.distribution}`);
    console.log(`• Low holders: ${failReasons.lowHolders}`);
    console.log(`• High bot rate: ${failReasons.highBot}`);
    
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
});
