import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const plates = process.argv.slice(2);
const doOffer = process.env.OFFER === '1';
const b = await chromium.launch({ headless:false, executablePath: '/opt/pw-browsers/chromium', proxy: { server: process.env.HTTPS_PROXY }, args: ['--ignore-certificate-errors'] });
const ctx = await b.newContext({ locale:'he-IL', userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36' });
const pg = await ctx.newPage();
pg.on('response', async r => { if (r.url().includes('/services/api')) { try { console.log('API', r.status(), (await r.text()).slice(0,4000)); } catch(e){} } });
for (const plate of plates) {
  await pg.goto('https://updates.mct.co.il/services/', { waitUntil: 'networkidle', timeout: 60000 });
  await pg.waitForTimeout(3000);
  await pg.fill('[name=car_no]', plate);
  await pg.click('#submit');
  await pg.waitForTimeout(6000);
  const det = await pg.evaluate(()=>[document.querySelector('#car_details')?.innerText, [...document.querySelectorAll('select option')].map(o=>o.value+':'+o.textContent)]);
  console.log('PLATE', plate, JSON.stringify(det));
  if (doOffer) {
    const opts = det[1];
    for (let i=0;i<opts.length;i++) {
      await pg.selectOption('select', String(i)).catch(()=>{});
      await pg.waitForTimeout(2500);
      await pg.click('#request_price').catch(e=>console.log('no btn'));
      await pg.waitForTimeout(5000);
      const fin = await pg.evaluate(()=>[document.querySelector('.service-title')?.innerText, document.querySelector('.service-desc')?.innerText, document.querySelector('#price_')?.innerText]);
      console.log('OFFER', i, JSON.stringify(fin));
      await pg.click('#back').catch(()=>{}); await pg.waitForTimeout(3000);
    }
  }
}
await b.close();
