// usage: node sess.mjs <home> <url1> <url2> ... ; saves pages/files
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [home, ...urls] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', locale: 'he-IL', timezoneId: 'Asia/Jerusalem', viewport: {width:1366,height:850}, acceptDownloads:true, extraHTTPHeaders: {'Accept-Language':'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'} });
await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); window.chrome = {runtime:{}}; Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]}); Object.defineProperty(navigator,'languages',{get:()=>['he-IL','he','en-US','en']}); });
const page = await ctx.newPage();
try { await page.goto(home, {waitUntil:'domcontentloaded', timeout:60000}); } catch(e) { console.log('home err', e.message.slice(0,80)); }
await page.waitForTimeout(12000);
try { await page.reload({waitUntil:'domcontentloaded', timeout:60000}); } catch(e) {}
await page.waitForTimeout(4000);
console.log('home title', await page.title(), (await page.content()).length);
fs.mkdirSync('out', {recursive:true});
for (const u of urls) {
  const fn = 'out/' + u.replace(/^https?:\/\//,'').replace(/[^a-z0-9.]+/gi,'_').slice(-120);
  try {
    const r = await ctx.request.get(u, {timeout:60000, headers: {'Referer': home}});
    const b = await r.body();
    fs.writeFileSync(fn, b);
    console.log(r.status(), b.length, r.headers()['content-type'], u, '->', fn);
  } catch(e) { console.log('ERR', u, e.message.slice(0,100)); }
}
await browser.close();
