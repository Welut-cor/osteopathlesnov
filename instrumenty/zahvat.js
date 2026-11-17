// Открывает страницы сайта в Edge, прокручивает, сохраняет все загруженные внешние файлы
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const fs = require('fs'), path = require('path');
const OUT = process.argv[2];
const PAGES = ['/', '/osteopatiya', '/iscelenie', '/distancionnayasessiya', '/perezagruzka', '/denezhnyy-potok', '/pererozhdenie'];
const SKIP = /mc\.yandex|yandex\.ru\/metrika|tildastat|stat\.tildacdn|tildacdn\.com\/api|google-analytics|googletagmanager/;
const spisok = {};
(async () => {
  const browser = await chromium.launch({ channel: 'msedge', headless: true });
  for (const vp of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    const ctx = await browser.newContext({ viewport: vp, userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36 Edg/130.0' });
    const page = await ctx.newPage();
    page.on('response', async (r) => {
      const u = r.url();
      if (!/^https?:/.test(u) || SKIP.test(u) || u.includes('osteopathlesnov.ru')) return;
      if (r.status() !== 200) { spisok[u] = spisok[u] || ('статус ' + r.status()); return; }
      try {
        const body = await r.body();
        const p = new URL(u);
        let rel = path.join(p.hostname, decodeURIComponent(p.pathname));
        if (rel.endsWith(path.sep)) rel += 'index';
        const file = path.join(OUT, rel);
        fs.mkdirSync(path.dirname(file), { recursive: true });
        fs.writeFileSync(file, body);
        spisok[u] = rel.split(path.sep).join('/');
      } catch (e) { spisok[u] = 'ошибка ' + e.message; }
    });
    for (const p of PAGES) {
      await page.goto('https://osteopathlesnov.ru' + p, { waitUntil: 'networkidle', timeout: 90000 });
      const h = await page.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h + 2000; y += 400) { await page.mouse.wheel(0, 400); await page.waitForTimeout(150); }
      await page.waitForTimeout(2500);
      console.log(vp.width, p, 'готово, файлов всего:', Object.keys(spisok).length);
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, '_spisok.json'), JSON.stringify(spisok, null, 1));
})().catch(e => { console.error('СБОЙ', e); process.exit(1); });
