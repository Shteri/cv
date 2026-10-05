import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [u]=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
p.on('response', r=>{const x=r.url(); if(/manua\.ls/.test(x) && !/\.(js|css|woff2?|svg|png|ico)(\?|$)/.test(x)) console.log(r.status(), r.headers()['content-type'], x.slice(0,200));});
await p.goto(u,{timeout:90000,waitUntil:'domcontentloaded'});
await p.waitForTimeout(5000);
await b.close();
