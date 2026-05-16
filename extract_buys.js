const fs = require('fs');

const data = JSON.parse(fs.readFileSync(0, 'utf8'));
const now = Math.floor(Date.now() / 1000);
const sixHoursAgo = now - (6 * 60 * 60);

// Tracked wallets
const tier1 = new Set([
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

const tier2 = new Set([
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
]);

// Extract unique buys from tracked wallets
const seen = new Set();
const buys = [];

for (const tx of data.list) {
  if (tx.side !== 'buy') continue;
  const maker = tx.maker;
  if (!tier1.has(maker) && !tier2.has(maker)) continue;
  
  const key = `${maker}-${tx.base_address}`;
  if (seen.has(key)) continue;
  seen.add(key);
  
  const tier = tier1.has(maker) ? 'TIER1' : 'TIER2';
  buys.push({
    maker,
    tier,
    token: tx.base_address,
    symbol: tx.base_token.symbol,
    amount_usd: tx.amount_usd,
    timestamp: tx.timestamp
  });
}

console.log(JSON.stringify(buys, null, 2));
