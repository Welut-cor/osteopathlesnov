/* Сайт Александра Леснова - поведение страниц. Без библиотек.
   Без JS сайт тоже работает: кнопки «Записаться» ведут к блоку связи внизу,
   отзывы листаются пальцем, пункты «вы получите» стоят списком. */
(function () {
  'use strict';
  var html = document.documentElement;
  var tihoe = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (tihoe) html.classList.add('bez-dvizh');

  /* --- печатающееся слово в шапке: «Остеопат», «Энергопрактик», «Целитель» --- */
  document.querySelectorAll('[data-slova]').forEach(function (el) {
    var slova = el.getAttribute('data-slova').split('|');
    if (tihoe || slova.length < 2) return;
    var i = 0, n = slova[0].length, stiraem = true;
    function shag() {
      var slovo = slova[i];
      if (stiraem) {
        n--;
        if (n <= 0) { stiraem = false; i = (i + 1) % slova.length; n = 0; }
      } else {
        n++;
        if (n >= slova[i].length) { stiraem = true; el.textContent = slova[i]; return setTimeout(shag, 2000); }
      }
      el.textContent = slova[i].slice(0, Math.max(n, 0));
      setTimeout(shag, stiraem ? 60 : 110);
    }
    setTimeout(shag, 2000);
  });

  /* --- окно «Запись на услуги» --- */
  var okno = document.getElementById('zapis');
  if (okno && typeof okno.showModal === 'function') {
    document.addEventListener('click', function (e) {
      var a = e.target.closest('[data-zapis]');
      if (!a) return;
      e.preventDefault();
      okno.showModal();
    });
    okno.addEventListener('click', function (e) {     // нажатие мимо окна закрывает его
      var r = okno.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) okno.close();
    });
  }

  /* --- карусель отзывов --- */
  document.querySelectorAll('.otzyvy').forEach(function (blok) {
    var lenta = blok.querySelector('.karusel');
    if (!lenta) return;
    function shagKarty() {
      var k = lenta.children;
      return k.length > 1 ? k[1].offsetLeft - k[0].offsetLeft : lenta.clientWidth;
    }
    blok.querySelectorAll('[data-karusel]').forEach(function (kn) {
      kn.addEventListener('click', function () {
        var vpered = kn.getAttribute('data-karusel') === 'vpered';
        var konec = lenta.scrollWidth - lenta.clientWidth;
        var cel = lenta.scrollLeft + (vpered ? 1 : -1) * shagKarty();
        if (vpered && lenta.scrollLeft >= konec - 5) cel = 0;            // с последнего - на первый
        if (!vpered && lenta.scrollLeft <= 5) cel = konec;               // с первого - на последний
        lenta.scrollTo({ left: cel, behavior: tihoe ? 'auto' : 'smooth' });
      });
    });
  });

  /* --- видеоотзыв: запуск по нажатию --- */
  document.querySelectorAll('.otzyv__video').forEach(function (ramka) {
    var video = ramka.querySelector('video'), kn = ramka.querySelector('.otzyv__pusk');
    if (!video || !kn) return;
    kn.addEventListener('click', function () {
      ramka.classList.add('idet');
      video.controls = true;
      video.play();
    });
  });

  /* --- анимации от прокрутки: элементу с data-hod задаётся --p от 0 до 1 --- */
  var hod = [].slice.call(document.querySelectorAll('[data-hod]'));
  var poluchite = [].slice.call(document.querySelectorAll('.poluchite'));
  if (tihoe || (!hod.length && !poluchite.length)) return;

  function nastroitPoluchite() {
    poluchite.forEach(function (b) {
      var lenta = b.querySelector('.poluchite__lenta'), p = lenta.children;
      if (p.length < 2) return;
      var sdvig = p[p.length - 1].offsetLeft - p[0].offsetLeft;
      lenta.style.setProperty('--sdvig', sdvig + 'px');
    });
  }

  var zhdet = false;
  function obnovit() {
    zhdet = false;
    var vh = window.innerHeight;
    hod.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var p = (vh - r.top) / (vh * 0.9);          // 0 - верх блока у низа экрана, 1 - почти у верха
      el.style.setProperty('--p', Math.min(1, Math.max(0, p)).toFixed(3));
    });
    poluchite.forEach(function (b) {
      var r = b.getBoundingClientRect();
      var put = b.offsetHeight - vh;
      var p = Math.min(1, Math.max(0, -r.top / (put || 1)));
      b.style.setProperty('--p', p.toFixed(3));
      var p2 = b.querySelectorAll('.poluchite__lenta li');
      var akt = Math.round(p * (p2.length - 1));
      p2.forEach(function (li, k) { li.classList.toggle('akt', k === akt); });
    });
  }
  function zapros() { if (!zhdet) { zhdet = true; requestAnimationFrame(obnovit); } }
  nastroitPoluchite();
  obnovit();
  window.addEventListener('scroll', zapros, { passive: true });
  window.addEventListener('resize', function () { nastroitPoluchite(); zapros(); });
  window.addEventListener('load', function () { nastroitPoluchite(); zapros(); });
})();
