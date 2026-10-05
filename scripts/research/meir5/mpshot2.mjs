import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [,, slug, prefix, ...pages] = process.argv;
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx = await b.newContext({ viewport: { width: 1300, height: 1900 }, deviceScaleFactor: 2, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' });
const pg = await ctx.newPage();
for (const p of pages) {
  await pg.goto(`https://www.manualpdf.co.il/${slug}/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p=${p}`, { waitUntil: 'networkidle', timeout: 90000 }).catch(e=>console.log('goto',e.message));
  await pg.waitForTimeout(2500);
  await pg.keyboard.press('Escape').catch(()=>{});
  await pg.evaluate(()=>{ for (const e of [...document.querySelectorAll('body *')]) { const s=getComputedStyle(e); if ((s.position==='fixed'||s.position==='sticky') ) e.remove(); } document.body.style.filter='none'; for (const e of document.querySelectorAll('*')) { const s=getComputedStyle(e); if (s.filter && s.filter!=='none') e.style.filter='none'; } });
  await pg.waitForTimeout(500);
  const el = await pg.$('.viewer-page .pf') || await pg.$('.viewer-page');
  if (!el) { console.log('no el', p); continue; }
  await el.scrollIntoViewIfNeeded(); await pg.waitForTimeout(500);
  await el.screenshot({ path: `${prefix}-${p}.png` });
  console.log('ok', p);
}
await b.close();
