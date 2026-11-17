// Какие элементы вылезают за правый край: node vylez.js страница ширина
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
(async () => {
  const [s, w] = process.argv.slice(2);
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await (await b.newContext({ viewport: { width: +w, height: 844 } })).newPage();
  await page.goto(`http://127.0.0.1:8765/novyj/${s}.html`, { waitUntil: 'networkidle' });
  const r = await page.evaluate(() => {
    const vw = document.documentElement.clientWidth, out = [];
    document.querySelectorAll('body *').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.right <= vw + 1 || !r.width) return;
      let p = el.parentElement;
      while (p && p !== document.body) { if (getComputedStyle(p).overflowX !== 'visible') return; p = p.parentElement; }
      out.push(el.tagName.toLowerCase() + '.' + [...el.classList].join('.') + ' право=' + Math.round(r.right) + ' y=' + Math.round(r.top + scrollY));
    });
    return out;
  });
  console.log(r.join('\n') || 'ничего не вылезает');
  await b.close();
})();
