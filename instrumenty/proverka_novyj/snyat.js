// Снимает с Tilda-копии содержимое Zero-блоков (элементы, стили, координаты) и снимки блоков
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const fs = require('fs');
const OUT = process.argv[2];
const PAGES = (process.argv[3] || 'index,osteopatiya,iscelenie,distancionnayasessiya,perezagruzka,denezhnyy-potok,pererozhdenie').split(',');
const WIDTHS = (process.argv[4] || '1440,390').split(',').map(Number);
fs.mkdirSync(OUT, { recursive: true });
(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  for (const w of WIDTHS) {
    const ctx = await b.newContext({ viewport: { width: w, height: 900 } });
    const page = await ctx.newPage();
    for (const p of PAGES) {
      await page.goto(`http://127.0.0.1:8765/${p}.html`, { waitUntil: 'networkidle', timeout: 90000 });
      const h = await page.evaluate(() => document.body.scrollHeight);
      for (let y = 0; y < h + 1500; y += 400) { await page.mouse.wheel(0, 400); await page.waitForTimeout(100); }
      await page.waitForTimeout(1500);
      const data = await page.evaluate(() => {
        const cs = (el, keys) => { const s = getComputedStyle(el); const o = {}; for (const k of keys) o[k] = s[k]; return o; };
        const recs = [];
        for (const rec of document.querySelectorAll('#allrecords > .t-rec, #allrecords .t-rec')) {
          if (recs.find(r => r.id === rec.id)) continue;
          const rb = rec.getBoundingClientRect();
          const art = rec.querySelector('.t396__artboard');
          const r = { id: rec.id, type: rec.dataset.recordType, top: Math.round(rb.top + scrollY), h: Math.round(rb.height), display: getComputedStyle(rec).display };
          if (art) r.art = cs(art, ['backgroundColor', 'backgroundImage', 'height']);
          r.elems = [];
          for (const el of rec.querySelectorAll('.tn-elem')) {
            const b2 = el.getBoundingClientRect();
            const e = { id: el.dataset.elemId, t: el.dataset.elemType, x: Math.round(b2.left - rb.left), y: Math.round(b2.top - rb.top), w: Math.round(b2.width), h: Math.round(b2.height), vis: getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden' && b2.width > 0 };
            const atom = el.querySelector('.tn-atom') || el;
            if (e.t === 'text') { e.html = atom.innerHTML.trim(); e.s = cs(atom, ['fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'color', 'lineHeight', 'letterSpacing', 'textTransform', 'textAlign', 'opacity']); }
            else if (e.t === 'button') { e.text = atom.innerText.trim(); e.href = atom.getAttribute('href'); e.s = cs(atom, ['fontFamily', 'fontSize', 'fontWeight', 'color', 'backgroundColor', 'borderColor', 'borderWidth', 'borderRadius', 'letterSpacing', 'textTransform']); }
            else if (e.t === 'image') { const img = el.querySelector('img'); e.src = img && (img.currentSrc || img.src); e.href = el.querySelector('a') && el.querySelector('a').getAttribute('href'); e.s = cs(atom, ['opacity', 'borderRadius']); }
            else if (e.t === 'shape') { e.s = cs(atom, ['backgroundColor', 'backgroundImage', 'borderColor', 'borderWidth', 'borderStyle', 'borderRadius', 'opacity', 'boxShadow']); e.href = el.querySelector('a') && el.querySelector('a').getAttribute('href'); }
            else { e.html = el.innerHTML.slice(0, 400); }
            r.elems.push(e);
          }
          if (!art) r.html = rec.innerHTML.slice(0, 1500);
          recs.push(r);
        }
        return { title: document.title, desc: (document.querySelector('meta[name=description]') || {}).content, h: document.body.scrollHeight, recs };
      });
      fs.writeFileSync(`${OUT}/${p}_${w}.json`, JSON.stringify(data, null, 1));
      await page.evaluate(() => window.scrollTo(0, 0)); await page.waitForTimeout(500);
      await page.screenshot({ path: `${OUT}/${p}_${w}.png`, fullPage: true });
      console.log(p, w, 'высота', data.h, 'блоков', data.recs.length);
    }
    await ctx.close();
  }
  await b.close();
})().catch(e => { console.error('СБОЙ', e); process.exit(1); });
