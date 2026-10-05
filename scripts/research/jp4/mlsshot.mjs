import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [slug,out,...pages]=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1300,height:1800}, deviceScaleFactor:1.5});
const p=await ctx.newPage();
for (const pg of pages){
 await p.goto(`https://www.manua.ls/${slug}/manual?p=${pg}`,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(4500);
 const el=await p.$('.viewer-page.active') || await p.$('#viewer');
 const txt=el? (await el.innerText()).replace(/\s+/g,' '):'NOEL';
 console.log('=== page',pg,txt.slice(0,+process.env.N||300));
 if(el && process.env.SHOT) await el.screenshot({path:`${out}_${pg}.png`});
}
await b.close();
