// usage: node infetch.mjs <home> <path1> <path2> ...  (paths relative to home origin); saves 200 responses into out/
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [home, ...paths] = process.argv.slice(2);
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: process.env.HEADFUL ? false : true, proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled'] });
const ctx = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', locale: 'he-IL', timezoneId: 'Asia/Jerusalem', viewport: {width:1366,height:850} });
await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', {get: () => undefined}); });
const page = await ctx.newPage();
let ok=false;
for (let a=0;a<4 && !ok;a++){
  try { await page.goto(home, {waitUntil:'domcontentloaded', timeout:60000}); } catch(e) {}
  await page.waitForTimeout(10000);
  const len=(await page.content()).length; console.log('home attempt',a,len); ok = len>20000;
}
if(!ok){ console.log('home blocked'); await browser.close(); process.exit(0); }
fs.mkdirSync('out',{recursive:true});
for (const p of paths) {
  const r = await page.evaluate(async (p) => { try { const res = await fetch(p, {credentials:'include'}); const b = new Uint8Array(await res.arrayBuffer()); let s=''; for (let i=0;i<b.length;i++) s+=String.fromCharCode(b[i]); return {st:res.status, ct:res.headers.get('content-type'), b64: btoa(s)}; } catch(e) { return {st:'ERR '+e.message}; } }, p);
  const buf = r.b64 ? Buffer.from(r.b64,'base64') : Buffer.alloc(0);
  const head = buf.slice(0,5).toString();
  console.log(r.st, buf.length, r.ct, head==='%PDF-'?'PDF':'', p);
  if (r.st===200 && buf.length>2000) fs.writeFileSync('out/'+p.replace(/[^a-z0-9.]+/gi,'_').slice(-120), buf);
  await page.waitForTimeout(1500);
}
await browser.close();
