import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [slug,...pages]=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1300,height:1800}});
const p=await ctx.newPage();
const seen=new Set();
p.on('response', r=>{const u=r.url(); if(/\/viewer\/.*\.(webp|png|jpg|svg)/.test(u) && !seen.has(u)){seen.add(u); console.log('IMG',u);}});
for (const pg of pages){
 await p.goto(`https://www.manua.ls/${slug}/manual?p=${pg}`,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(3500);
}
await b.close();
