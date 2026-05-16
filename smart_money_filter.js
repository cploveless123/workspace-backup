#!/usr/bin/env node
/**
 * Smart Money Tracker - Filter & Report
 * Processes gmgn-cli track smartmoney output, fetches token info, applies strict filters
 */

const { execSync } = require('child_process');

const CURRENT_TIME = 1778917063; // From the API response context

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

// Read the smart money data from stdin
let data = '';
process.stdin.on('data', chunk => data += chunk);
process.stdin.on('end', async () => {
  try {
    const parsed = JSON.parse(data);
    const txs = parsed.list || [];

    // Filter to only BUY transactions from tracked wallets
    const buys = txs.filter(tx => 
      tx.side === 'buy' && ALL_TRACKED.has(tx.maker)
    );

    // Deduplicate by token address (keep most recent per token)
    const tokenMap = new Map();
    for (const tx of buys) {
      const existing = tokenMap.get(tx.base_address);
      if (!existing || tx.timestamp > existing.timestamp) {
        tokenMap.set(tx.base_address, tx);
      }
    }

    const uniqueBuys = Array.from(tokenMap.values());
    console.log(`Found ${uniqueBuys.length} unique buy transactions from tracked wallets\n`);

    const results = {
      passed: [],
      skipped: {
        tooOld: 0,
        lowVolume: 0,
        volumeCollapsed: 0,
        dumping: 0,
        distribution: 0,
        lowHolders: 0,
        highBotRate: 0,
        other: 0
      }
    };

    for (const tx of uniqueBuys) {
      const tokenAddr = tx.base_address;
      const symbol = tx.base_token?.symbol || 'UNKNOWN';
      const wallet = tx.maker;
      const amount = tx.amount_usd || 0;
      const isFull = tx.is_open_or_close === 1;
      const tier = TIER1.has(wallet) ? 'TIER1' : 'TIER2';
      
      console.log(`Checking ${symbol} (${tokenAddr}) from ${wallet.substring(0,8)}... (${tier})`);

      try {
        // Fetch token info
        const cmd = `gmgn-cli token info --chain sol --address ${tokenAddr} --raw`;
        const output = execSync(cmd, { encoding: 'utf8', timeout: 15000 });
        const info = JSON.parse(output);

        const token = info.token || {};
        const pair = info.pair || {};
        const analysis = info.analysis || {};

        // Extract metrics
        const creationTime = token.creation_timestamp || 0;
        const ageMinutes = (CURRENT_TIME - creationTime) / 60;
        
        const volume5m = pair.volume_5m || 0;
        const volume1h = pair.volume_1h || 0;
        const volumeTrend = volume1h > 0 ? (volume5m / (volume1h / 12)) * 100 : 0;
        
        const price1hHigh = pair.price_1h_high || pair.price || 0;
        const currentPrice = pair.price || 0;
        const priceVsHigh = price1hHigh > 0 ? (currentPrice / price1hHigh) * 100 : 0;
        
        const buys1h = pair.buys_1h || 0;
        const sells1h = pair.sells_1h || 0;
        const buyRatio = (buys1h + sells1h) > 0 ? buys1h / (buys1h + sells1h) : 0;
        
        const holders = token.holders || pair.holders || 0;
        const botRate = analysis.bot_degen_rate || 0;
        const mcap = pair.market_cap || token.market_cap || 0;

        // Apply filters
        const filters = {
          age: ageMinutes < 30,
          volume: volume5m >= 5000,
          volumeTrend: volumeTrend >= 20,
          price: priceVsHigh >= 70,
          buyRatio: buyRatio >= 0.6,
          holders: holders >= 100,
          botRate: botRate < 40
        };

        const passed = Object.values(filters).every(v => v);
        const failReasons = [];
        if (!filters.age) failReasons.push('tooOld');
        if (!filters.volume) failReasons.push('lowVolume');
        if (!filters.volumeTrend) failReasons.push('volumeCollapsed');
        if (!filters.price) failReasons.push('dumping');
        if (!filters.buyRatio) failReasons.push('distribution');
        if (!filters.holders) failReasons.push('lowHolders');
        if (!filters.botRate) failReasons.push('highBotRate');

        if (passed) {
          // Check for cluster signal (multiple wallets buying same token)
          const clusterWallets = buys.filter(b => b.base_address === tokenAddr).map(b => b.maker);
          const uniqueClusterWallets = [...new Set(clusterWallets)];
          const isCluster = uniqueClusterWallets.length >= 2;
          const isLarge = amount >= 500;
          const isFreshHighVol = ageMinutes < 15 && volume5m > 10000;

          results.passed.push({
            wallet,
            walletShort: wallet.substring(0, 8),
            tier,
            symbol,
            tokenAddr,
            amount,
            isFull,
            mcap,
            ageMinutes,
            volume5m,
            volumeTrend,
            priceVsHigh,
            buyRatio,
            holders,
            botRate,
            isCluster,
            isLarge,
            isFreshHighVol,
            clusterCount: uniqueClusterWallets.length
          });
          console.log(`  ✅ PASSED all filters`);
        } else {
          const primaryReason = failReasons[0];
          results.skipped[primaryReason]++;
          console.log(`  ❌ FAILED: ${failReasons.join(', ')}`);
        }
      } catch (e) {
        console.log(`  ⚠️ Error fetching token info: ${e.message}`);
        results.skipped.other++;
      }
    }

    // Generate report
    console.log('\n' + '='.repeat(60));
    console.log('📊 SMART MONEY HIGH-CONVICTION SIGNAL REPORT');
    console.log('='.repeat(60));
    console.log(`Time: ${new Date(CURRENT_TIME * 1000).toISOString()}`);
    console.log(`Total unique buys checked: ${uniqueBuys.length}`);
    console.log(`High-conviction signals: ${results.passed.length}`);
    console.log(`Filtered out: ${Object.values(results.skipped).reduce((a,b) => a+b, 0)}`);
    console.log('');

    if (results.passed.length > 0) {
      for (const r of results.passed) {
        const timeStr = new Date(CURRENT_TIME * 1000).toISOString().replace('T', ' ').substring(0, 19);
        console.log(`🔥 HIGH-CONVICTION SIGNAL (7/7 filters passed)`);
        console.log(`[${timeStr}] ${r.walletShort}... (${r.tier}) — BUY ${r.symbol} $${r.amount.toFixed(2)} [${r.isFull ? 'FULL' : 'PARTIAL'}]`);
        console.log(`📍 ${r.tokenAddr}`);
        console.log(`💰 MCAP: $${r.mcap.toLocaleString()} | Price: $${(r.currentPrice || 0).toExponential(3)} | vs 1h High: ${r.priceVsHigh.toFixed(1)}%`);
        console.log(`⏱️ Age: ${r.ageMinutes.toFixed(1)} min | Vol 5m: $${r.volume5m.toLocaleString()} | Vol Trend: ${r.volumeTrend.toFixed(1)}%`);
        console.log(`📊 Buy Ratio: ${(r.buyRatio * 100).toFixed(1)}% | Holders: ${r.holders} | Bot Rate: ${r.botRate.toFixed(1)}%`);
        console.log(`🔗 DexScreener: https://dexscreener.com/solana/${r.tokenAddr}`);
        console.log(`💵 Buy: /buy ${r.tokenAddr} 0.1`);
        console.log('');
        console.log('⚡ CONVICTION INDICATORS:');
        console.log(`• Multiple wallets: ${r.isCluster ? 'YES (' + r.clusterCount + ')' : 'NO'}`);
        console.log(`• Large amount: ${r.isLarge ? 'YES' : 'NO'}`);
        console.log(`• Full position: ${r.isFull ? 'YES' : 'NO'}`);
        console.log(`• Fresh + high volume: ${r.isFreshHighVol ? 'YES' : 'NO'}`);
        console.log('—'.repeat(40));
      }
    } else {
      console.log('🚫 No high-conviction signals found this cycle.');
    }

    console.log('\n📊 FILTERED OUT SUMMARY:');
    console.log(`• Too old (>30min): ${results.skipped.tooOld}`);
    console.log(`• Low volume (<$5K): ${results.skipped.lowVolume}`);
    console.log(`• Volume collapsed: ${results.skipped.volumeCollapsed}`);
    console.log(`• Dumping (<70% of high): ${results.skipped.dumping}`);
    console.log(`• Distribution (buy ratio <60%): ${results.skipped.distribution}`);
    console.log(`• Low holders (<100): ${results.skipped.lowHolders}`);
    console.log(`• High bot rate (>40%): ${results.skipped.highBotRate}`);
    console.log(`• Other/errors: ${results.skipped.other}`);

  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
});
