import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const [re,...ids]=process.argv.slice(2); const R=new RegExp(re,'i');
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
for (const id of ids){
 await p.goto(`https://www.manualslib.com/manual/${id}/x.html`,{timeout:60000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(2500);
 const r=await p.evaluate(()=>({t:document.title, l:[...document.querySelectorAll('a')].map(a=>[a.textContent.trim().replace(/\s+/g,' '),a.getAttribute('href')]).filter(x=>/page=/.test(x[1]||''))}));
 console.log('==',id,r.t); const seen=new Set(); for(const x of r.l){ if(!R.test(x[0])) continue; const k=x[0]+x[1]; if(seen.has(k))continue; seen.add(k); console.log('  ',x[0].slice(0,100),'|',x[1].replace(/.*page=/,'p'));}
}
await b.close();
