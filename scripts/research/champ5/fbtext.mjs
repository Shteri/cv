import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const ids = process.argv.slice(2);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx = await b.newContext({ ignoreHTTPSErrors:true, locale:'he-IL', viewport:{width:1400,height:1000} });
for (const id of ids) {
  const p = await ctx.newPage();
  let base=null, qs=null;
  p.on('request', r => { const m=r.url().match(/^(https:\/\/[^?]+?)\/common\/pager\.json\?(.*)$/); if (m) { base=m[1]; qs=m[2]; } });
  try {
    await p.goto('https://online.flippingbook.com/view/'+id+'/', { waitUntil: 'domcontentloaded', timeout: 60000 });
    for (let i=0;i<30 && !base;i++) await p.waitForTimeout(1000);
    if (!base) { console.log(id,'no base'); await p.close(); continue; }
    const title = await p.title();
    const res = await p.evaluate(async ([base,qs]) => {
      const pg = await (await fetch(base+'/common/pager.json?'+qs)).json();
      const n = pg.pages ? Object.keys(pg.pages).length : (pg.pageCount||200);
      const out=[];
      for (let i=1;i<=Math.min(n||200,400);i++){
        const nn=String(i).padStart(4,'0');
        const r=await fetch(base+'/flash/search/search'+nn+'.xml?'+qs);
        if(!r.ok){ out.push('#'+i+' '+r.status); if(r.status==404||r.status==403) break; continue;}
        out.push('### PAGE '+i+'\n'+await r.text());
      }
      return {n, pgkeys:Object.keys(pg).join(','), out};
    }, [base,qs]);
    fs.writeFileSync('fb/'+id+'.txt', title+'\n'+res.out.join('\n'));
    console.log(id, title, res.n, res.pgkeys, res.out.length);
  } catch(e) { console.log('ERR',id,e.message.slice(0,200)); }
  await p.close();
}
await b.close();
