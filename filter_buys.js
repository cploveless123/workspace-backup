const fs = require('fs');

const raw = fs.readFileSync('/dev/stdin', 'utf8');
const data = JSON.parse(raw);
const now = 1778914380;

const tier1 = [
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

const tier2 = [
  'CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY',
  '43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x',
  '3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz',
  '9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U',
  'FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go',
  'DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'
];

const tracked = new Set([...tier1, ...tier2]);

const buys = [];
const seen = new Set();

for (const tx of data.list) {
  if (tx.side !== 'buy') continue;
  if (!tracked.has(tx.maker)) continue;
  
  const key = tx.maker + ':' + tx.base_address;
  if (seen.has(key)) continue;
  seen.add(key);
  
  const walletName = tx.maker_info.twitter_name || tx.maker_info.name || tx.maker.slice(0, 8);
  const tier = tier1.includes(tx.maker) ? 'T1' : 'T2';
  
  buys.push({
    wallet: tx.maker,
    walletName,
    tier,
    token: tx.base_token.symbol,
    address: tx.base_address,
    amount: tx.amount_usd,
    isFull: tx.is_open_or_close === 1,
    timestamp: tx.timestamp,
    launchpad: tx.base_token.launchpad
  });
}

buys.sort((a, b) => b.timestamp - a.timestamp);
console.log(JSON.stringify(buys, null, 2));
