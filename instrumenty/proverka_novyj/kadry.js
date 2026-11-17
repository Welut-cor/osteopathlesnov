// Кадры окна при прокрутке: node kadry.js url ширина высота_окна y0 y1 шаг папка [клик_селектор]
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const fs = require('fs');
const [url, w, vh, y0, y1, step, out, klik] = process.argv.slice(2);
(async () => {
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  const page = await (await b.newContext({ viewport: { width: +w, height: +vh } })).newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  // доехать до y0 колесом
  let cur = 0;
  while (cur < +y0) { const d = Math.min(300, +y0 - cur); await page.mouse.wheel(0, d); cur += d; await page.waitForTimeout(60); }
  await page.waitForTimeout(1200);
  if (klik) { await page.click(klik); await page.waitForTimeout(1200); }
  let i = 0;
  for (let y = +y0; y <= +y1; y += +step) {
    if (y > +y0) { let d = +step; while (d > 0) { const s = Math.min(150, d); await page.mouse.wheel(0, s); d -= s; await page.waitForTimeout(60); } await page.waitForTimeout(900); }
    const sy = await page.evaluate(() => Math.round(scrollY));
    await page.screenshot({ path: `${out}/${String(i++).padStart(2, '0')}_${sy}.png` });
  }
  await b.close();
})();
