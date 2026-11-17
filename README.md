# osteopathlesnov.ru — копия сайта с Tilda

Статическая резервная копия https://osteopathlesnov.ru (проект Tilda 10426977, тариф Personal, официального экспорта нет). Снята 17.11.2026.

- Копия на GitHub Pages: https://welut-cor.github.io/osteopathlesnov/
- **Права:** содержимое сайта принадлежит владельцу, все права защищены. Код Tilda - Tilda Publishing. Подробно - [LICENSE](LICENSE) и [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Скрипты в `instrumenty/` - MIT.
- **Режим зеркала:** у каждой страницы `canonical` ведёт на osteopathlesnov.ru и стоит `<meta name="robots" content="noindex, nofollow">`, чтобы поисковики не считали копию дублем настоящего сайта. Если домен переедет на эту копию - убрать `noindex` (в `instrumenty/sborka.py` поставить `ZERKALO = False` и пересобрать).

- Страницы — `*.html` в корне, ссылки между ними относительные: открывается и с диска, и с GitHub Pages (в том числе на поддомене `user.github.io/repo/`).
- Все файлы с `static.tildacdn.com` и плагин `cdn.postnikovmd.com` лежат в `assets/` (папки `tilda`, `tilda-neo`, `postnikov`). Имена папок специально без `tildacdn`: иначе lazyload Тильды подменяет пути на свой CDN.
- Наружу ходит только Яндекс.Метрика (оставлена намеренно) и статистика Тильды (безвредна, падает так же, как на оригинале).
- Форм на сайте нет, контакты — ссылки t.me и wa.me.

## Визитка

- Исходник - `vizitka.html` (своя вёрстка, без движка Тильды), текст - `vizitka/tekst.md`, фото - `vizitka/foto` (пересборка `instrumenty/foto_vizitki.py`).
- На Тильде это страница https://osteopathlesnov.ru/vizitka (pageid 395736909): один блок T123 «HTML-код», шапка и подвал сайта отключены в настройках страницы. Там же скрытый блок-галерея GL01 - через него загружены фото, не удалять.
- После правки `vizitka.html`: `python -X utf8 instrumenty/vizitka_tilda.py` → `vizitka/tilda_t123.html`, его содержимое целиком вставить в блок T123 и опубликовать страницу. Новые фото сначала загрузить на Тильду и вписать их адреса в `FOTO` в скрипте.
- `sborka.py` визитку не трогает: её нет в списке `PAGES`.

## Обновить копию после правок на Тильде

Скрипты в `instrumenty/` (нужны Python 3 с Pillow и Edge + playwright-core из `Clode projects\.claude\mcp\playwright`):

1. `python -X utf8 -I obzor.py <папка_сырое>` — скачать HTML страниц (список страниц внутри скрипта; новые страницы добавить туда же и в `zahvat.js`, `sborka.py`).
2. `node zahvat.js <папка_захват>` — открыть страницы в Edge и записать всё, что они догружают.
3. `python -X utf8 -I sborka.py <папка_сырое> <папка_захват> <папка_сайта>` — скачать файлы и переписать ссылки.
4. Проверка: поднять `python -m http.server 8766 -d <папка_сайта>`, затем `node proverka.js <папка_снимков>` (порт внутри скрипта) и `python sravnit.py <папка_снимков>` — попиксельное сравнение с оригиналом.
