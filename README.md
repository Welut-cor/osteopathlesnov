# osteopathlesnov.ru - сайт без Тильды

Сайт https://osteopathlesnov.ru, свёрстанный заново на чистом HTML/CSS/JS: без кода Тильды и без библиотек, правится в любом редакторе. Тексты, фото и порядок блоков взяты с сайта на Тильде дословно.

- На GitHub Pages: https://welut-cor.github.io/osteopathlesnov/
- Резервная копия исходного сайта на Тильде: папка `tilda/`, на Pages - https://welut-cor.github.io/osteopathlesnov/tilda/
- **Права:** содержимое сайта принадлежит владельцу, все права защищены. Подробно - [LICENSE](LICENSE) и [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Скрипты в `instrumenty/` - MIT.
- Домен osteopathlesnov.ru пока ведёт на Тильду. Поэтому на всех страницах стоит `<meta name="robots" content="noindex, nofollow">` (над ней комментарий), а `canonical` ведёт на osteopathlesnov.ru: поисковики не считают Pages дублем настоящего сайта.

## Что где лежит

- `*.html` в корне - страницы: `index`, `osteopatiya`, `iscelenie`, `distancionnayasessiya`, `perezagruzka`, `denezhnyy-potok`, `pererozhdenie`. Ещё `vizitka.html` - визитка, о ней ниже.
- `css/sajt.css` - один стиль на все страницы. Цвета и размеры шрифтов заданы переменными в `:root` в начале файла. Без медиазапроса - стиль для телефона, `@media (min-width:640px)` - для планшета, `(min-width:960px)` - для ПК.
- `js/sajt.js` - поведение страниц:
  - печатающееся слово в шапке;
  - окно «Запись на услуги»;
  - карусель отзывов;
  - запуск видео;
  - анимации от прокрутки.

  Без JS сайт тоже работает.
- `chasti/` - общие части: `shapka`, `otzyvy`, `podval`, `okno`.
- `img`, `fonts`, `video` - сжатые картинки, шрифт Noah и видеоотзыв. Их однажды собрал `instrumenty/novyj_resursy.py` из копии Тильды.
- Форм на сайте нет, контакты - ссылки t.me и wa.me. Яндекс.Метрики нет.

## Как править

- Текст, цену, пункт списка - прямо в нужной странице `<страница>.html`.
- Шапку, отзывы, подвал с контактами, окно записи - в файле из `chasti/`, затем `python -X utf8 instrumenty/chasti.py` вставит часть во все страницы. В странице эти части стоят между метками `<!-- chast:имя -->` и `<!-- /chast:имя -->`. Правка между метками прямо в странице пропадёт при следующем запуске.
- Новый отзыв - ещё один `<article class="otzyv karta">` в `chasti/otzyvy.html`, по образцу соседних.
- Кнопка «Записаться» - это `<a href="#svyaz" data-zapis>`: она открывает окно записи.
- Проверка после правок:
  1. Поднять локальный сервер в папке репозитория: `python -m http.server 8765 --bind 127.0.0.1`.
  2. Снять страницы: `node instrumenty/proverka_novyj/proverka_novyj.js` (можно передать страницы и ширины через запятую). Снимки ложатся в `_Архив/novyj_snimki`; скрипт пишет об ошибках JS и о горизонтальной прокрутке.
  3. Проверить поведение (окно записи, карусель, видео, анимации): `node instrumenty/proverka_novyj/dvizhenie.js`.
  4. Сверить тексты с Тильдой: `python -X utf8 instrumenty/proverka_novyj/sverka_tekstov.py`.

**При переносе домена сюда** убрать из всех страниц строку `<meta name="robots" content="noindex, nofollow">`. Вместе с переносом решить вопрос Метрики, баннера cookie и политики (черновики лежат в `_razbor/`, папка вне git) и проверить право использовать шрифт Noah вне Тильды (см. THIRD_PARTY_NOTICES.md).

## Визитка

- Исходник - `vizitka.html` (своя вёрстка, без движка Тильды), текст - `vizitka/tekst.md`, фото - `vizitka/foto` (пересборка `instrumenty/foto_vizitki.py`). Шрифт и значок она берёт из копии Тильды: `tilda/assets/tilda/...`.
- На Тильде это страница https://osteopathlesnov.ru/vizitka (pageid 395736909): один блок T123 «HTML-код», шапка и подвал сайта отключены в настройках страницы. Там же скрытый блок-галерея GL01 - через него загружены фото, не удалять.
- После правки `vizitka.html`: `python -X utf8 instrumenty/vizitka_tilda.py` → `vizitka/tilda_t123.html`, его содержимое целиком вставить в блок T123 и опубликовать страницу. Новые фото сначала загрузить на Тильду и вписать их адреса в `FOTO` в скрипте.

## Копия Тильды (`tilda/`)

Статическая резервная копия сайта на Тильде (проект 10426977, тариф Personal, официального экспорта нет). Снята 17.11.2026, до 18.11 лежала в корне.

- Страницы - `tilda/*.html`, ссылки между ними относительные: открывается и с диска, и с Pages.
- Все файлы с `static.tildacdn.com` и плагин `cdn.postnikovmd.com` лежат в `tilda/assets/` (папки `tilda`, `tilda-neo`, `postnikov`). Имена папок специально без `tildacdn`: иначе lazyload Тильды подменяет пути на свой CDN.
- Режим зеркала: `canonical` ведёт на osteopathlesnov.ru, стоит `noindex, nofollow`, счётчик Метрики вырезан (`ZERKALO = True` в `instrumenty/sborka.py`). Наружу ходит только статистика Тильды (безвредна, падает так же, как на оригинале).
- Там же `tilda/404.html` и исходные `_original_robots.txt`, `_original_sitemap.xml` с Тильды.

**Пересъёмка после правок на Тильде.** Скриптам в `instrumenty/` нужны Python 3 с Pillow и Edge + playwright-core из `Clode projects\.claude\mcp\playwright`:

1. `python -X utf8 -I obzor.py <папка_сырое>` - скачать HTML страниц (список страниц внутри скрипта; новые страницы добавить туда же и в `zahvat.js`, `sborka.py`).
2. `node zahvat.js <папка_захват>` - открыть страницы в Edge и записать всё, что они догружают.
3. `python -X utf8 -I sborka.py <папка_сырое> <папка_захват> <папка_сайта>` - скачать файлы и переписать ссылки. Готовую папку положить на место `tilda/`.
4. Проверка: поднять `python -m http.server 8766 -d <папка_сайта>`, затем `node proverka.js <папка_снимков>` (порт внутри скрипта) и `python sravnit.py <папка_снимков>` - попиксельное сравнение с оригиналом.

Новый сайт пересъёмка не меняет: правки текста на Тильде нужно перенести в `*.html` в корне руками.
