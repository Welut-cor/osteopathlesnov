// Проверка novyj/: node proverka_novyj.js [страницы через запятую] [ширины через запятую]
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const fs = require('fs');
const OUT = __dirname + '/../../_Архив/novyj_snimki';   // снимки - вне git (_Архив в .gitignore)
const STR = (process.argv[2] || 'index,osteopatiya,iscelenie,distancionnayasessiya,perezagruzka,denezhnyy-potok,pererozhdenie').split(',');
const SHIR = (process.argv[3] || '390,768,1440').split(',').map(Number);
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const itog = [];
  for (const w of SHIR) {
    const ctx = await b.newContext({ viewport: { width: w, height: w < 700 ? 844 : 900 } });
    for (const s of STR) {
      const page = await ctx.newPage();
      const osh = [];
      page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') osh.push(m.type() + ': ' + m.text()); });
      page.on('pageerror', e => osh.push('pageerror: ' + e.message));
      page.on('requestfailed', r => osh.push('сбой запроса: ' + r.url()));
      page.on('response', r => { if (r.status() >= 400) osh.push(r.status() + ' ' + r.url()); });
      await page.goto(`http://127.0.0.1:8765/novyj/${s}.html`, { waitUntil: 'networkidle' });
      // проехать страницу, чтобы подгрузились ленивые картинки
      const h = await page.evaluate(() => document.documentElement.scrollHeight);
      for (let y = 0; y < h; y += 600) { await page.evaluate(y => scrollTo(0, y), y); await page.waitForTimeout(40); }
      await page.evaluate(() => scrollTo(0, 0));
      await page.waitForTimeout(500);
      const d = await page.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const sw = document.documentElement.scrollWidth;
        const vylez = [];
        if (sw > vw) document.querySelectorAll('body *').forEach(el => {
          const r = el.getBoundingClientRect();
          if (r.right > vw + 1 && r.width) {
            let p = el.parentElement, skryt = false;
            while (p && p !== document.body) { const o = getComputedStyle(p).overflowX; if (o !== 'visible') { skryt = true; break; } p = p.parentElement; }
            if (!skryt) vylez.push(el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' ' + Math.round(r.right));
          }
        });
        const imgs = [...document.images].filter(i => !i.complete || !i.naturalWidth).map(i => i.src);
        return { vw, sw, vylez: vylez.slice(0, 10), shrift: document.fonts.check('18px Noah'), bitye: imgs, vys: document.documentElement.scrollHeight };
      });
      await page.screenshot({ path: `${OUT}/${s}_${w}.png`, fullPage: true });
      itog.push({ s, w, ...d, osh });
      await page.close();
    }
    await ctx.close();
  }
  await b.close();
  for (const r of itog) {
    const plohо = r.sw > r.vw || r.osh.length || r.bitye.length || !r.shrift;
    console.log(`${plohо ? '!!' : 'ok'} ${r.s} ${r.w}: высота ${r.vys}, ширина ${r.sw}/${r.vw}, шрифт ${r.shrift}` +
      (r.vylez.length ? '\n   вылезают: ' + r.vylez.join(' | ') : '') +
      (r.bitye.length ? '\n   картинки: ' + r.bitye.join(' | ') : '') +
      (r.osh.length ? '\n   ошибки: ' + r.osh.join(' | ') : ''));
  }
})();
