// Открывает копию и оригинал, пишет внешние запросы и ошибки, снимает страницы целиком
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const OUT = process.argv[2];
const PAGES = ['index', 'osteopatiya', 'iscelenie', 'distancionnayasessiya', 'perezagruzka', 'denezhnyy-potok', 'pererozhdenie'];
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  for (const vp of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    for (const src of ['kopiya', 'original']) {
      const ctx = await b.newContext({ viewport: vp });
      const page = await ctx.newPage();
      const vneshnie = new Set(), oshibki = [];
      page.on('request', r => { const u = r.url(); if (src === 'kopiya' && !u.startsWith('http://127.0.0.1') && !u.startsWith('data:')) vneshnie.add(u.split('?')[0]); });
      page.on('console', m => { if (m.type() === 'error') oshibki.push(m.text().slice(0, 160)); });
      page.on('pageerror', e => oshibki.push('JS: ' + e.message.slice(0, 160)));
      page.on('requestfailed', r => oshibki.push('не загрузилось: ' + r.url().slice(0, 140)));
      for (const p of (vp.width === 390 ? ['index', 'osteopatiya'] : PAGES)) {
        const url = src === 'kopiya' ? `http://127.0.0.1:8765/${p}.html` : `https://osteopathlesnov.ru/${p === 'index' ? '' : p}`;
        await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
        const h = await page.evaluate(() => document.body.scrollHeight);
        for (let y = 0; y < h + 1500; y += 400) { await page.mouse.wheel(0, 400); await page.waitForTimeout(120); }
        await page.waitForTimeout(2000);
        await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(800);
        await page.screenshot({ path: `${OUT}/${src}_${vp.width}_${p}.png`, fullPage: true });
        const vys = await page.evaluate(() => document.body.scrollHeight);
        console.log(src, vp.width, p, 'высота', vys);
      }
      if (src === 'kopiya') { console.log('  внешние запросы:', [...vneshnie].join('\n    ') || 'нет'); console.log('  ошибки:', oshibki.join('\n    ') || 'нет'); }
      await ctx.close();
    }
  }
  await b.close();
})().catch(e => { console.error('СБОЙ', e); process.exit(1); });
