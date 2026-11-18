// Проверка поведения нового сайта: окно записи, карусель, видео, «вы получите», стопка этапов.
// Нужен локальный сервер на 8765. Запуск из osteopathlesnov: node instrumenty/proverka_novyj/dvizhenie.js
const { chromium } = require('C:/Users/emill/Desktop/Clode projects/.claude/mcp/playwright/node_modules/playwright-core');
const OUT = __dirname + '/../../_Архив/novyj_snimki';
const URL = 'http://127.0.0.1:8765/';
const itog = [];
const ok = (uslovie, chto) => itog.push((uslovie ? 'ok ' : '!! ') + chto);

(async () => {
  const b = await chromium.launch({ channel: 'msedge', headless: true });
  for (const w of [390, 1440]) {
    const page = await (await b.newContext({ viewport: { width: w, height: w < 700 ? 844 : 900 } })).newPage();
    const osh = [];
    page.on('pageerror', e => osh.push(e.message));

    // окно записи
    await page.goto(URL + 'index.html', { waitUntil: 'networkidle' });
    await page.click('.geroj [data-zapis]');
    await page.waitForTimeout(300);
    ok(await page.evaluate(() => document.getElementById('zapis').open), `${w}: окно записи открылось`);
    await page.screenshot({ path: `${OUT}/d_okno_${w}.png` });
    await page.mouse.click(5, 5);
    await page.waitForTimeout(300);
    ok(!(await page.evaluate(() => document.getElementById('zapis').open)), `${w}: клик мимо окна закрыл его`);

    // карусель
    const sl0 = await page.evaluate(() => document.querySelector('.karusel').scrollLeft);
    await page.click('[data-karusel="vpered"]');
    await page.waitForTimeout(900);
    const sl1 = await page.evaluate(() => document.querySelector('.karusel').scrollLeft);
    ok(sl1 > sl0, `${w}: карусель вперёд (${sl0} → ${Math.round(sl1)})`);
    await page.click('[data-karusel="nazad"]');
    await page.waitForTimeout(900);
    ok(await page.evaluate(() => document.querySelector('.karusel').scrollLeft) < 5, `${w}: карусель назад`);

    // видео
    await page.click('.otzyv__pusk');
    await page.waitForTimeout(1500);
    const v = await page.evaluate(() => { const x = document.querySelector('.otzyv__video video'); return { paused: x.paused, t: x.currentTime, controls: x.controls }; });
    ok(!v.paused && v.t > 0 && v.controls, `${w}: видео играет (t=${v.t.toFixed(2)})`);

    // стопка этапов: карточки липнут друг над другом
    const y = await page.evaluate(() => document.querySelector('.etapy__spisok').getBoundingClientRect().top + scrollY);
    for (const sdvig of [0, 250, 450, 700]) {
      await page.evaluate(y => scrollTo(0, y), y + sdvig);
      await page.waitForTimeout(400);
      const tops = await page.evaluate(() => [...document.querySelectorAll('.etap')].map(e => Math.round(e.getBoundingClientRect().top)));
      itog.push(`   ${w}: этапы, прокрутка +${sdvig}: верх карточек ${tops.join(', ')}`);
      await page.screenshot({ path: `${OUT}/d_etapy_${w}_${sdvig}.png` });
    }

    // «вы получите» на странице услуги
    await page.goto(URL + 'osteopatiya.html', { waitUntil: 'networkidle' });
    const blok = await page.evaluate(() => { const b = document.querySelector('.poluchite'); return { y: b.getBoundingClientRect().top + scrollY, h: b.offsetHeight }; });
    const vh = await page.evaluate(() => innerHeight);
    for (const dolya of [0, 0.5, 1]) {
      await page.evaluate(y => scrollTo(0, y), blok.y + dolya * (blok.h - vh));
      await page.waitForTimeout(500);
      const s = await page.evaluate(() => {
        const b = document.querySelector('.poluchite');
        const li = [...b.querySelectorAll('.poluchite__lenta li')];
        const r = b.querySelector('.poluchite__krug').getBoundingClientRect();
        return { p: getComputedStyle(b).getPropertyValue('--p'), akt: li.findIndex(x => x.classList.contains('akt')),
                 x: li.map(x => Math.round(x.getBoundingClientRect().left)), krugTop: Math.round(r.top) };
      });
      ok(Math.abs(s.akt - dolya * 3) <= 0.5, `${w}: получите при ${dolya}: --p=${s.p.trim()}, активный пункт ${s.akt}, x пунктов ${s.x.join(',')}, круг сверху ${s.krugTop}`);
      await page.screenshot({ path: `${OUT}/d_poluchite_${w}_${dolya}.png` });
    }
    ok(!osh.length, `${w}: ошибок JS нет ${osh.join(' | ')}`);
    await page.context().close();
  }
  await b.close();
  console.log(itog.join('\n'));
})();
