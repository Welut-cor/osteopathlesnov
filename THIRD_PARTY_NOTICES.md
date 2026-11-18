# Сторонние компоненты

Что лежит в `tilda/assets/` (копия сайта на Tilda) и в `fonts/` (новый сайт) и кому принадлежит. Данные взяты из заголовков самих файлов; где заголовка нет - это помечено.

| Файлы | Владелец | Условия |
|---|---|---|
| `tilda/assets/tilda/js/*`, `tilda/assets/tilda/css/*`, `tilda/assets/tilda/ws/*`, `tilda/assets/tilda/lib/*`, `tilda/assets/tilda-neo/*` | Tilda Publishing | Пользовательское соглашение Tilda. Код платформы, не открытый |
| regenerator-runtime внутри `tilda-animation-2.0.min.js` и `tilda-animation-sbs-1.0.min.js` | Facebook, Inc. | MIT (указано в заголовке файла) |
| `tilda/assets/postnikov/tilda@1.6/mods.min.js`, `swiper.min.js` | Maksim Postnikov, 2026 | MIT, https://postnikovmd.com/mods/license (указано в заголовке файла) |
| `tilda/assets/postnikov/tilda@1.6/swiper-core.min.js`, `swiper-core.min.css` | библиотека Swiper в сборке Postnikov | заголовка с лицензией в файле нет; библиотека Swiper распространяется по MIT |
| `tilda/assets/tilda/fonts/tildasans/*` (TildaSans) | Tilda Publishing | шрифт платформы, условия Tilda |
| `tilda/assets/tilda/fonts/georgia/*` (Georgia) | Microsoft | коммерческий шрифт, раздаётся Tilda для сайтов на платформе |
| `tilda/assets/tilda/tild*/Noah-*.woff` (Noah) | правообладатель шрифта | шрифт загружен владельцем сайта в Tilda; права на веб-использование - у владельца сайта |
| `fonts/Noah-*.woff` (Noah, новый сайт) | правообладатель шрифта | тот же файл шрифта, что владелец сайта загрузил в Tilda; право использовать его вне Tilda нужно проверить до переноса домена |
| остальные `tilda/assets/tilda/tild*/*` (фото, иконки, картинки) | владелец сайта | все права защищены, см. `LICENSE` |

Если сайт будет переезжать с Tilda на собственный хостинг, нужно отдельно проверить право использовать код Tilda и шрифты Georgia и Noah вне платформы.
