import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls = process.argv.slice(2);
const b = await chromium.launch({ headless: true, executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled','--headless=new'] });
const ctx = await b.newContext({ locale:'he-IL', timezoneId:'Asia/Jerusalem', viewport:{width:1366,height:900}, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', extraHTTPHeaders:{'Accept-Language':'he-IL,he;q=0.9,en;q=0.8'} });
await ctx.addInitScript(()=>{Object.defineProperty(navigator,'webdriver',{get:()=>undefined}); window.chrome={runtime:{}}; Object.defineProperty(navigator,'languages',{get:()=>['he-IL','he','en']}); Object.defineProperty(navigator,'plugins',{get:()=>[1,2,3]});});
const pg = await ctx.newPage();
for (const u of urls) {
  let st='';
  try { const r = await pg.goto(u, { waitUntil: 'domcontentloaded', timeout: 60000 }); st = r && r.status(); } catch(e) { st = 'ERR '+e.message.slice(0,80); }
  await pg.waitForTimeout(12000);
  const t = await pg.title().catch(()=> '');
  const body = (await pg.content().catch(()=>'')).length;
  console.log(u, st, JSON.stringify(t), body);
  const fn = 'pw_' + u.replace(/[^a-z0-9]/gi,'_').slice(0,80) + '.html';
  require_fs: { const fs = await import('fs'); fs.writeFileSync(fn, await pg.content().catch(()=> '')); }
}
await b.close();
