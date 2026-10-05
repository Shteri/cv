import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await b.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36', locale:'he-IL', ignoreHTTPSErrors:true });
for (const u of urls) {
  const p = await ctx.newPage();
  try {
    const r = await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await p.waitForTimeout(8000);
    const t = await p.evaluate(() => document.body ? document.body.innerText : '');
    console.log('=== ', u, r && r.status(), p.url(), '\n', t.slice(0, 200));
    const fn = 'pw_' + u.replace(/[^a-z0-9]+/gi,'_').slice(0,80) + '.html';
    (await import('fs')).writeFileSync(fn, await p.content());
  } catch (e) { console.log('ERR', u, e.message); }
  await p.close();
}
await b.close();
