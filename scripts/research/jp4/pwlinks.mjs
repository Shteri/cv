import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1400,height:1000}});
const p=await ctx.newPage();
for (const u of urls){
await p.goto(u,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
await p.waitForTimeout(6000);
for (let i=0;i<8;i++){ await p.mouse.wheel(0,3000); await p.waitForTimeout(700); }
const r=await p.evaluate(()=>[...document.querySelectorAll('a')].map(a=>[a.textContent.trim().replace(/\s+/g,' '),a.href]));
console.log('==',u,await p.title()); const s=new Set(); for(const x of r){ if(s.has(x[1]))continue; s.add(x[1]); if(/document\/(view|read)\/\d+/.test(x[1])) console.log(x[0].slice(0,100),'|',x[1]); }
}
await b.close();
