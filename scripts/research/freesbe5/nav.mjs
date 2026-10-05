import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const urls = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', locale: 'he-IL', timezoneId: 'Asia/Jerusalem', viewport: {width:1366,height:850}, acceptDownloads:true, extraHTTPHeaders: {'Accept-Language':'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'} });
await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); window.chrome = {runtime:{}}; Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]}); Object.defineProperty(navigator,'languages',{get:()=>['he-IL','he','en-US','en']}); });
fs.mkdirSync('out', {recursive:true});
const page = await ctx.newPage();
for (const u of urls) {
  const fn = 'out/' + u.replace(/^https?:\/\//,'').replace(/[^a-z0-9.]+/gi,'_').slice(-120);
  let ok=false;
  for (let attempt=0; attempt<3 && !ok; attempt++) {
    try { await page.goto(u, {waitUntil:'domcontentloaded', timeout:60000}); } catch(e) { console.log('err', e.message.slice(0,80)); }
    await page.waitForTimeout(8000 + attempt*6000);
    const html = await page.content().catch(()=> '');
    if (html.length > 20000) { fs.writeFileSync(fn+'.html', html); console.log('OK', u, html.length, await page.title()); ok=true; }
    else console.log('blocked', attempt, u, html.length);
  }
}
await browser.close();
