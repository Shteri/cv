import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
for (const u of urls){
 await p.goto(u,{timeout:60000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(3000);
 const r=await p.evaluate(()=>({t:document.title, l:[...document.querySelectorAll('a')].map(a=>[a.textContent.trim().replace(/\s+/g,' '),a.getAttribute('href')]).filter(x=>/\/manual\/\d+/.test(x[1]||''))}));
 console.log('==',u,r.t); const seen=new Set(); for(const x of r.l){ if(seen.has(x[1]))continue; seen.add(x[1]); console.log('  ',x[0].slice(0,90),'|',x[1]);}
}
await b.close();
