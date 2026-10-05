import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [u,out]=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
await p.goto(u,{timeout:60000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
await p.waitForTimeout(4000);
const fs=await import('node:fs'); fs.writeFileSync(out, await p.content()); console.log(await p.title());
await b.close();
