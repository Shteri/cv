import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const urls=process.argv.slice(2);
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36", viewport:{width:1400,height:1000}});
const p=await ctx.newPage();
for (const u of urls){
 await p.goto(u,{timeout:90000,waitUntil:'domcontentloaded'}).catch(e=>console.log('ERR',e.message));
 await p.waitForTimeout(8000);
 for (let i=0;i<6;i++){ await p.mouse.wheel(0,2500); await p.waitForTimeout(600); }
 const html=await p.content();
 const s=new Set(html.match(/[^"'\s()]+\.pdf/gi)||[]);
 console.log('==',u); for(const x of s) console.log('  ',x);
 const opts=await p.evaluate(()=>[...document.querySelectorAll('option,button,a')].map(e=>e.textContent.trim()).filter(t=>/juke|x-trail|qashqai|micra/i.test(t)).slice(0,40));
 console.log('  OPTS',opts.join(' | '));
}
await b.close();
