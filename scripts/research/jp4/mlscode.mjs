import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const slugs=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1300,height:1800}});
const p=await ctx.newPage();
for (const s of slugs){ const [slug,pg]=s.split('@');
 await p.goto(`https://www.manua.ls/${slug}/manual?p=${pg||100}`,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(4000);
 const el=await p.$('.viewer-page.active') || await p.$('#viewer');
 const txt=el? (await el.innerText()).replace(/\s+/g,' '):'NOEL';
 const codes=[...new Set((txt.replace(/\s/g,'').match(/[0-9３１２]{2}[TＴ][A-Z0-9Ａ-Ｚ０-９]{4,6}/g)||[]))];
 console.log(slug,pg||100,codes.join(','),'|',txt.slice(0,150));
}
await b.close();
