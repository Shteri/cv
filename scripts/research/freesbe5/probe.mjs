import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: true, proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', locale: 'he-IL', timezoneId: 'Asia/Jerusalem', viewport: {width:1366,height:850}, extraHTTPHeaders: {'Accept-Language':'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7'} });
await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); window.chrome = {runtime:{}}; Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3,4,5]}); Object.defineProperty(navigator,'languages',{get:()=>['he-IL','he','en-US','en']}); });
for (const u of urls) {
  const page = await ctx.newPage();
  let st='';
  try { const r = await page.goto(u, {waitUntil:'domcontentloaded', timeout:60000}); st = r ? r.status() : 'null'; } catch(e) { st='ERR '+e.message.slice(0,100); }
  await page.waitForTimeout(12000);
  try { await page.reload({waitUntil:'domcontentloaded', timeout:60000}); await page.waitForTimeout(5000);} catch(e){}
  const html = await page.content().catch(()=> '');
  const title = await page.title().catch(()=> '');
  const fn = u.replace(/[^a-z0-9]+/gi,'_').slice(0,80)+'.html';
  (await import('fs')).writeFileSync(fn, html);
  console.log(u, st, 'title=', title, 'len=', html.length, fn);
  await page.close();
}
await browser.close();
