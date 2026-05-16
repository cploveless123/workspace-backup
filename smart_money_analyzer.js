#!/usr/bin/env node
/**
 * Smart Money Tracker - Direct Analysis
 * Fetches token info for unique BUY transactions from tracked wallets
 */

const { execSync } = require('child_process');

const CURRENT_TIME = Math.floor(Date.now() / 1000);

// Tracked wallets
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

const TIER2 = new Set([
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
]);

const ALL_TRACKED = new Set([...TIER1, ...TIER2]);

// Read JSON from stdin
let data = '';
process.stdin.on('data', chunk => data += chunk);
process.stdin.on('end', async () => {
  try {
    const parsed = JSON.parse(data);
    const txs = parsed.list || [];

    // Get only BUY transactions from tracked wallets, most recent first
    const buys = txs
      .filter(tx => tx.side === 'buy' && ALL_TRACKED.has(tx.maker))
      .sort((a, b) => b.timestamp - a.timestamp);

    // Deduplicate by token address (keep most recent)
    const tokenMap = new Map();
    for (const tx of buys) {
      if (!tokenMap.has(tx.base_address)) {
        tokenMap.set(tx.base_address, tx);
      }
    }

    const uniqueBuys = Array.from(tokenMap.values());
    console.log(`📊 Found ${uniqueBuys.length} unique recent buy transactions from tracked wallets\n`);

    const results = {
      passed: [],
      skipped: { tooOld: 0, lowVolume: 0, volumeCollapsed: 0, dumping: 0, distribution: 0, lowHolders: 0, highBotRate: 0, other: 0 }
    };

    for (const tx of uniqueBuys) {
      const tokenAddr = tx.base_address;
      const symbol = tx.base_token?.symbol || 'UNKNOWN';
      const wallet = tx.maker;
      const amount = tx.amount_usd || 0;
      const isFull = tx.is_open_or_close === 1;
      const tier = TIER1.has(wallet) ? 'TIER1' : 'TIER2';
      const walletName = tx.maker_info?.twitter_name || wallet.substring(0, 8) + '...';
      
      console.log(`🔍 Checking ${symbol} from ${walletName} (${tier}) - $${amount.toFixed(2)}`);

      try {
        const cmd = `gmgn-cli token info --chain sol --address ${tokenAddr} --raw`;
        const output = execSync(cmd, { encoding: 'utf8', timeout: 15000 });
        const info = JSON.parse(output);

        // Extract metrics from correct paths based on actual API response
        const creationTime = info.creation_timestamp || info.dev?.ath_token_info?.creation_timestamp || 0;
        const ageMinutes = creationTime > 0 ? (CURRENT_TIME - creationTime) / 60 : 999;
        
        const price = info.price || {};
        const volume5m = parseFloat(price.volume_5m || 0);
        const volume1h = parseFloat(price.volume_1h || 0);
        const volumeTrend = volume1h > 0 ? (volume5m / (volume1h / 12)) * 100 : 0;
        
        const price1hHigh = info.ath_price || parseFloat(price.price_1h || 0);
        const currentPrice = parseFloat(price.price || 0);
        const priceVsHigh = price1hHigh > 0 ? (currentPrice / price1hHigh) * 100 : 100;
        
        const buys1h = price.buys_1h || 0;
        const sells1h = price.sells_1h || 0;
        const buyRatio = (buys1h + sells1h) > 0 ? buys1h / (buys1h + sells1h) : 0;
        
        const holders = info.holder_count || info.stat?.holder_count || 0;
        const botRate = parseFloat(info.stat?.bot_degen_rate || 0) * 100;
        const mcap = info.migration_market_cap || 0;

        // Apply strict filters
        const filters = {
          age: ageMinutes < 30,
          volume: volume5m >= 5000,
          volumeTrend: volumeTrend >= 20,
          price: priceVsHigh >= 70,
          buyRatio: buyRatio >= 0.6,
          holders: holders >= 100,
          botRate: botRate < 40
        };

        const passCount = Object.values(filters).filter(v => v).length;
        const failReasons = [];
        if (!filters.age) failReasons.push(`tooOld(${ageMinutes.toFixed(1)}min)`);
        if (!filters.volume) failReasons.push(`lowVolume($${volume5m.toFixed(0)})`);
        if (!filters.volumeTrend) failReasons.push(`volCollapsed(${volumeTrend.toFixed(1)}%)`);
        if (!filters.price) failReasons.push(`dumping(${priceVsHigh.toFixed(1)}%)`);
        if (!filters.buyRatio) failReasons.push(`distribution(${(buyRatio*100).toFixed(1)}%)`);
        if (!filters.holders) failReasons.push(`lowHolders(${holders})`);
        if (!filters.botRate) failReasons.push(`highBot(${botRate.toFixed(1)}%)`);

        if (passCount === 7) {
          // Check cluster signal
          const clusterWallets = buys.filter(b => b.base_address === tokenAddr).map(b => b.maker);
          const uniqueCluster = [...new Set(clusterWallets)];
          const isCluster = uniqueCluster.length >= 2;

          results.passed.push({
            wallet, walletName, tier, symbol, tokenAddr, amount, isFull, mcap,
            currentPrice, ageMinutes, volume5m, volumeTrend, priceVsHigh,
            buyRatio, holders, botRate, isCluster, clusterCount: uniqueCluster.length,
            isLarge: amount >= 500, isFreshHighVol: ageMinutes < 15 && volume5m > 10000
          });
          console.log(`  ✅ HIGH-CONVICTION SIGNAL - All 7 filters passed!\n`);
        } else {
          const primaryReason = failReasons[0]?.split('(')[0] || 'other';
          if (results.skipped[primaryReason] !== undefined) {
            results.skipped[primaryReason]++;
          } else {
            results.skipped.other++;
          }
          console.log(`  ❌ FAILED (${passCount}/7): ${failReasons.join(', ')}\n`);
        }
      } catch (e) {
        console.log(`  ⚠️ Error: ${e.message}\n`);
        results.skipped.other++;
      }
    }

    // Generate report
    console.log('='.repeat(60));
    console.log('🔥 SMART MONEY HIGH-CONVICTION SIGNAL REPORT');
    console.log('='.repeat(60));
    console.log(`Time: ${new Date(CURRENT_TIME * 1000).toISOString()}`);
    console.log(`Checked: ${uniqueBuys.length} unique buys from tracked wallets`);
    console.log(`Signals: ${results.passed.length} | Filtered: ${Object.values(results.skipped).reduce((a,b)=>a+b,0)}`);
    console.log('');

    if (results.passed.length > 0) {
      for (const r of results.passed) {
        const timeStr = new Date(CURRENT_TIME * 1000).toISOString().replace('T',' ').substring(0,19);
        console.log(`🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)`);
        console.log(`[${timeStr}] ${r.walletName} (${r.tier}) — BUY $${r.amount.toFixed(2)} ${r.symbol} [${r.isFull?'FULL':'PARTIAL'}]`);
        console.log(`📍 ${r.tokenAddr}`);
        console.log(`💰 MCAP: $${r.mcap.toLocaleString()} | Price: $${r.currentPrice.toExponential(3)} | vs 1h High: ${r.priceVsHigh.toFixed(1)}%`);
        console.log(`⏱️ Age: ${r.ageMinutes.toFixed(1)} min | Vol 5m: $${r.volume5m.toLocaleString()} | Vol Trend: ${r.volumeTrend.toFixed(1)}%`);
        console.log(`📊 Buy Ratio: ${(r.buyRatio*100).toFixed(1)}% | Holders: ${r.holders} | Bot Rate: ${r.botRate.toFixed(1)}%`);
        console.log(`🔗 DexScreener: https://dexscreener.com/solana/${r.tokenAddr}`);
        console.log(`💵 Buy: /buy ${r.tokenAddr} 0.1`);
        console.log('');
        console.log('⚡ CONVICTION INDICATORS:');
        console.log(`• Multiple wallets: ${r.isCluster ? 'YES ('+r.clusterCount+')' : 'NO'}`);
        console.log(`• Large amount (>$500): ${r.isLarge ? 'YES' : 'NO'}`);
        console.log(`• Full position open: ${r.isFull ? 'YES' : 'NO'}`);
        console.log(`• Fresh + high volume: ${r.isFreshHighVol ? 'YES' : 'NO'}`);
        console.log('—'.repeat(40));
      }
    } else {
      console.log('🚫 No high-conviction signals found this cycle.');
      console.log('All tracked wallet buys failed one or more strict filters.');
    }

    console.log('\n📊 FILTERED OUT SUMMARY:');
    console.log(`• Too old (>30min): ${results.skipped.tooOld}`);
    console.log(`• Low volume (<$5K 5m): ${results.skipped.lowVolume}`);
    console.log(`• Volume collapsed (<20% of 1h): ${results.skipped.volumeCollapsed}`);
    console.log(`• Dumping (<70% of 1h high): ${results.skipped.dumping}`);
    console.log(`• Distribution (buy ratio <60%): ${results.skipped.distribution}`);
    console.log(`• Low holders (<100): ${results.skipped.lowHolders}`);
    console.log(`• High bot rate (>40%): ${results.skipped.highBotRate}`);
    console.log(`• Other/errors: ${results.skipped.other}`);

  } catch (e) {
    console.error('Fatal error:', e.message);
    process.exit(1);
  }
});
