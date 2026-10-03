import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [mid, out, ...pages] = process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1400,height:1100}, deviceScaleFactor:1.6});
const p=await ctx.newPage();
for (const pg of pages){
  await p.goto(`https://www.manualslib.com/manual/${mid}/x.html?page=${pg}`,{timeout:60000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
  await p.waitForTimeout(4000);
  const el=await p.$('.pdf') || await p.$('#pdfContainer') || await p.$('[id^=pdf]');
  const txt = await p.evaluate(()=>{const e=document.querySelector('.pdf'); return e? e.innerText : ''});
  console.log('=== page',pg,'\n',txt.slice(0,3000));
  if (el) await el.screenshot({path:`${out}_${pg}.png`}); else await p.screenshot({path:`${out}_${pg}.png`,fullPage:false});
}
await b.close();
