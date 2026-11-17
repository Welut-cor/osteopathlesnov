# Сторонние компоненты

Что лежит в `assets/` и кому принадлежит. Данные взяты из заголовков самих файлов; где заголовка нет - это помечено.

| Файлы | Владелец | Условия |
|---|---|---|
| `assets/tilda/js/*`, `assets/tilda/css/*`, `assets/tilda/ws/*`, `assets/tilda/lib/*`, `assets/tilda-neo/*` | Tilda Publishing | Пользовательское соглашение Tilda. Код платформы, не открытый |
| regenerator-runtime внутри `tilda-animation-2.0.min.js` и `tilda-animation-sbs-1.0.min.js` | Facebook, Inc. | MIT (указано в заголовке файла) |
| `assets/postnikov/tilda@1.6/mods.min.js`, `swiper.min.js` | Maksim Postnikov, 2026 | MIT, https://postnikovmd.com/mods/license (указано в заголовке файла) |
| `assets/postnikov/tilda@1.6/swiper-core.min.js`, `swiper-core.min.css` | библиотека Swiper в сборке Postnikov | заголовка с лицензией в файле нет; библиотека Swiper распространяется по MIT |
| `assets/tilda/fonts/tildasans/*` (TildaSans) | Tilda Publishing | шрифт платформы, условия Tilda |
| `assets/tilda/fonts/georgia/*` (Georgia) | Microsoft | коммерческий шрифт, раздаётся Tilda для сайтов на платформе |
| `assets/tilda/tild*/Noah-*.woff` (Noah) | правообладатель шрифта | шрифт загружен владельцем сайта в Tilda; права на веб-использование - у владельца сайта |
| остальные `assets/tilda/tild*/*` (фото, иконки, картинки) | владелец сайта | все права защищены, см. `LICENSE` |

Если сайт будет переезжать с Tilda на собственный хостинг, нужно отдельно проверить право использовать код Tilda и шрифты Georgia и Noah вне платформы.
