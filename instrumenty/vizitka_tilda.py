# Собирает из vizitka.html код для HTML-блока T123 на Тильде (страница osteopathlesnov.ru/vizitka).
# Запуск: python -X utf8 instrumenty/vizitka_tilda.py  ->  vizitka/tilda_t123.html
# Содержимое файла целиком вставить в блок T123 страницы «Александр Леснов - энерготерапия» и опубликовать.
#
# Фото на Тильде лежат отдельно (загружены 17.11.2026 через скрытый блок-галерею GL01 на той же странице).
# Сменили фото в vizitka/foto - загрузить новое на Тильду и поменять адрес в FOTO.
import os, re, sys

KOREN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISHODNIK = os.path.join(KOREN, 'vizitka.html')
ITOG = os.path.join(KOREN, 'vizitka', 'tilda_t123.html')

FOTO = {
    'portret.jpg': 'https://static.tildacdn.com/tila3833-6663-4363-a563-316662613139/portret.jpg',
    'meditaciya.jpg': 'https://static.tildacdn.com/tila6135-3962-4831-b034-663738393766/meditaciya.jpg',
    'koster.jpg': 'https://static.tildacdn.com/tila3561-6531-4363-b266-356230653161/koster.jpg',
    'portret.webp': 'https://static.tildacdn.com/tila6131-6338-4137-a235-353861323366/portret.webp',
    'meditaciya.webp': 'https://static.tildacdn.com/tila6435-6130-4330-a165-643166656666/meditaciya.webp',
    'koster.webp': 'https://static.tildacdn.com/tila6337-3332-4131-b638-613236306530/koster.webp',
}

# поверх стилей Тильды: #allrecords a красит ссылки в оранжевый и снимает подчёркивание
POVERH = """
/* --- поверх стилей Тильды --- */
#vz{font:400 17px/1.5 'noah',Arial,sans-serif;color:var(--text);background:var(--paper)}
#allrecords #vz a{color:inherit}
#allrecords #vz footer a{text-decoration:underline}
#allrecords #vz .btn:hover,#allrecords #vz .btn:focus-visible{color:var(--paper)}
#vz h1,#vz h2,#vz h3{font-family:inherit;color:inherit}
/* tilda-grid обнуляет margin у p, блоки Тильды дают ul свои отступы - возвращаем браузерные,
   с весом простого тега, чтобы классы визитки (.card p и т.п.) по-прежнему были сильнее */
:where(#vz) p,:where(#vz) ul{margin:1em 0}
@media (min-width:860px){#vz{font-size:18px}}
/* баннер cookie (T972) на этой странице - шрифтом визитки, а не Arial/Georgia */
.t972 .t-name,.t972 .t-descr,.t972 .t-btnflex__text,.t972__toggle-txt{font-family:'noah',Arial,sans-serif!important}
"""

def main():
    t = open(ISHODNIK, encoding='utf-8').read()
    style = re.search(r'<style>(.*?)</style>', t, re.S).group(1)
    skript_tema = re.search(r'</style>\s*<script>(.*?)</script>\s*</head>', t, re.S).group(1)
    telo = re.search(r'<body>(.*)</body>', t, re.S).group(1)

    # meta theme-color / color-scheme на Тильде может не быть - создаём
    skript_tema = skript_tema.replace(
        "window.postavitTemu = function(t){",
        "var meta = function(n){ var m = document.querySelector('meta[name=\"' + n + '\"]');"
        " if (!m) { m = document.createElement('meta'); m.name = n; document.head.appendChild(m); } return m; };\n"
        "window.postavitTemu = function(t){", 1)
    skript_tema = skript_tema.replace("document.querySelector('meta[name=\"theme-color\"]')", "meta('theme-color')")
    skript_tema = skript_tema.replace("document.querySelector('meta[name=\"color-scheme\"]')", "meta('color-scheme')")
    if "querySelector('meta" in skript_tema.replace("document.querySelector('meta[name=\"' + n", ''):
        sys.exit('скрипт темы изменился - поправь замены meta')

    kod = '<link rel="preload" href="tilda/assets/tilda/tild6331-6431-4964-b762-656531303764/Noah-Regular.woff" as="font" type="font/woff" crossorigin>\n'
    kod += '<style>' + style.rstrip() + '\n' + POVERH + '</style>\n'
    kod += '<script>' + skript_tema + '</script>\n'
    kod += '<div id="vz">' + telo + '</div>\n'

    kod = kod.replace('tilda/assets/tilda/', 'https://static.tildacdn.com/')
    for imya, url in FOTO.items():
        kod = re.sub(r'vizitka/foto/' + re.escape(imya) + r'(\?v=[\w]+)?', url, kod)
    kod = kod.replace('href="index.html"', 'href="/"')

    ostalos = re.findall(r'(?:src|srcset|href)="(?!https?:|tel:|#|/")[^"]*"', kod)
    if ostalos:
        sys.exit('остались локальные адреса: ' + ', '.join(ostalos))
    open(ITOG, 'w', encoding='utf-8', newline='\n').write(kod)
    print('готово:', ITOG, len(kod), 'символов')

main()
