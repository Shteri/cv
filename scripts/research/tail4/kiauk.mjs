import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const b=await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx=await b.newContext({userAgent:"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"});
const p=await ctx.newPage();
const reqs=[];
p.on('response', r=>{const u=r.url(); if(/json|manual|pdf|api/i.test(u) && !/\.(png|jpg|svg|css|woff)/.test(u)) reqs.push(r.status()+' '+u);});
await p.goto(process.argv[2],{timeout:90000,waitUntil:'networkidle'}).catch(e=>console.log('ERR',e.message));
await p.waitForTimeout(3000);
for (const t of (process.argv.slice(3))) { const el=await p.$(`text=${t}`); if(el){await el.click().catch(()=>{}); await p.waitForTimeout(3000);} else console.log('no',t); }
console.log("URL",p.url()); const body=await p.evaluate(()=>document.body.innerText); console.log(body.slice(0,3000));
const links=await p.evaluate(()=>[...document.querySelectorAll('a')].map(a=>a.textContent.trim().replace(/\s+/g,' ').slice(0,60)+' | '+a.href).filter(x=>/pdf|manual/i.test(x)));
console.log(links.join('\n')); console.log('--- reqs'); console.log([...new Set(reqs)].join('\n'));
await b.close();
