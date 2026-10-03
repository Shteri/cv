import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [url, out] = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const p = await b.newPage({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' });
let st = null;
try { const r = await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); st = r && r.status(); await p.waitForTimeout(6000); } catch (e) { console.error('ERR', e.message); }
const txt = await p.evaluate(() => document.body ? document.body.innerText : '');
const links = await p.evaluate(() => [...document.querySelectorAll('a')].map(a => a.href + ' | ' + a.innerText.trim().slice(0, 80)));
const fs = await import('node:fs');
fs.writeFileSync(out, `STATUS ${st}\nURL ${p.url()}\n` + txt + '\n\n==LINKS==\n' + links.join('\n'));
console.log('status', st, 'len', txt.length);
await b.close();
