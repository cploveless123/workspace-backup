const data = JSON.parse(require('fs').readFileSync('sm.json', 'utf8'));
const tier1 = ['6EDaVsS6enYgJ81tmhEkiKFcb4HuzPUVFZeom6PHUqN3','65kmABTfVidnwPzs5bfeyptpM2ewkkNewnJK6QwUSKXE','3jSHyFJjkWnz73niuzRnjsxSEA6MV3kwKu4ZAFEXGN6f','H2KAvWycyqeHhqkMC1f83Pwju3B2MztLYdXVpNMcDs2V','8fsKLLtvKNanL4ginCaiRS6UfeemY11rSf8U8fN1dJw4','7BWy2mtHNdnWLMZejk5E5sfDDSQfXsjzjy9jPzeDyYk5','MeskxyRYaBhYERcNP2zLVTqFVR43TMX4MihyH7AU4XN','FdwVhbBQhY9rwF5yaZwVH2SK6jhtxj67idgVrrGgAmKS','tCPHCKBKPmVvDCPiv3JmTeXXc7ivPpTRfvPZuzTodir','1aC2FgH1tujX87Bv9yMVbda2sPiRDNCsjMJoJjw3n6C','Ab2iXBkhRwmRtsw7G3PRmY56nerSFYrwR9fi9mcDGZkX','BkqxrgpoWQPc5gx7q225rmoNYoCEdojbarb6Z4iZYhVT'];
const tier2 = ['CNDXkovjrP5otMJor1hwSpKWpmY1Qq4vgjBAtQS3Z2TY','43QmFc2QPPGyMrSNuPnhvfs8BFW1XVZYFdbwURtWoo9x','3wccdTM5Ty6ZZC8rpc2GrKUHEScHZmr3iTKjRA6sH2rz','9cxLzxjrTeodcbaEU3KCNGE1a4yFZEcdJ7uEXN378S4U','FhaYN5TDH6JGdkAU1q3vvVeWa7Snbz4dAk53g2XMv9go','DphoNsGZMZ1KVDvLitJREiroFeTePL3YogsDKyP28Ztw'];
const allTracked = [...tier1, ...tier2];
const buys = data.list.filter(t => t.side === 'buy' && allTracked.includes(t.maker));
const uniqueTokens = [...new Set(buys.map(t => t.base_address))];
console.log(JSON.stringify({count: buys.length, tokens: uniqueTokens, buys: buys.map(b => ({addr: b.base_address, sym: b.base_token.symbol, maker: b.maker, usd: b.amount_usd, ts: b.timestamp, is_open: b.is_open_or_close}))}));
