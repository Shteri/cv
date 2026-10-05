import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls = process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
for (const u of urls){
  const r=await p.goto(u,{timeout:60000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
  await p.waitForTimeout(3000);
  const links = await p.evaluate(()=>[...document.querySelectorAll('a[href*="/manual/"]')].map(a=>a.href+' | '+a.innerText.trim().replace(/\s+/g,' ')).filter((v,i,s)=>s.indexOf(v)===i));
  console.log('##',u,r&&r.status()); console.log(links.slice(0,60).join('\n'));
}
await b.close();
