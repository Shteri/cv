import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const [u,out,wait]=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless:true, proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors','--disable-blink-features=AutomationControlled','--headless=new'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", viewport:{width:1400,height:1000}, locale:'en-US'});
await ctx.addInitScript(()=>{Object.defineProperty(navigator,'webdriver',{get:()=>undefined});});
const p=await ctx.newPage();
await p.goto(u,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
for(let i=0;i<6;i++){ await p.waitForTimeout(5000); const t=await p.title(); if(!/moment/i.test(t)) break; }
fs.writeFileSync(out+'.html', await p.content());
fs.writeFileSync(out+'.txt', await p.evaluate(()=>document.body.innerText));
await p.screenshot({path:out+'.png'});
console.log(await p.title());
await b.close();
