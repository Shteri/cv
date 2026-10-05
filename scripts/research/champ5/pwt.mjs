import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const urls = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', locale:'he-IL', ignoreHTTPSErrors:true, viewport:{width:1366,height:900} });
for (const u of urls) {
  const p = await ctx.newPage();
  try {
    const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await p.waitForTimeout(+process.env.WAIT||6000);
    const t = await p.evaluate(() => document.body ? document.body.innerText : '');
    console.log('=== ', u, r && r.status(), p.url(), '\n', t.slice(0, +process.env.N||400));
    const fn = (process.env.OUT||'.')+'/pw_' + u.replace(/^https?:\/\//,'').replace(/[^a-z0-9]+/gi,'_').slice(0,90) + '.html';
    fs.writeFileSync(fn, await p.content());
  } catch (e) { console.log('ERR', u, e.message.slice(0,200)); }
  await p.close();
}
await b.close();
