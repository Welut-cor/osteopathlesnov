"""Вставляет общие части сайта из novyj/chasti/ во все страницы novyj/*.html.

Общая часть - файл novyj/chasti/<имя>.html. В странице для неё стоят метки:
    <!-- chast:<имя> -->
    ...сюда скрипт кладёт содержимое файла...
    <!-- /chast:<имя> -->
Всё, что между метками, скрипт заменяет. Править шапку, отзывы, подвал и окно
записи нужно в chasti/, а не в страницах: правка в странице пропадёт при
следующем запуске.

Запуск из папки osteopathlesnov:
    python instrumenty/chasti.py          - вставить и записать
    python instrumenty/chasti.py --suho   - только показать, какие страницы изменятся
"""
import pathlib
import re
import sys

KOREN = pathlib.Path(__file__).resolve().parent.parent / "novyj"
CHASTI = KOREN / "chasti"
METKA = re.compile(r"(<!-- chast:([\w-]+) -->)(.*?)(<!-- /chast:\2 -->)", re.S)


def main():
    suho = "--suho" in sys.argv
    chasti = {p.stem: p.read_text(encoding="utf-8").strip("\n") for p in CHASTI.glob("*.html")}
    if not chasti:
        sys.exit(f"Нет файлов в {CHASTI}")
    izmeneno, oshibki = 0, 0
    for stranica in sorted(KOREN.glob("*.html")):
        tekst = stranica.read_text(encoding="utf-8")
        nevedomye = []

        def zamena(m):
            imya = m.group(2)
            if imya not in chasti:
                nevedomye.append(imya)
                return m.group(0)
            return f"{m.group(1)}\n{chasti[imya]}\n{m.group(4)}"

        novyj = METKA.sub(zamena, tekst)
        for imya in nevedomye:
            print(f"  ! {stranica.name}: нет файла chasti/{imya}.html")
            oshibki += 1
        if novyj != tekst:
            izmeneno += 1
            print(("  изменится: " if suho else "  обновлена: ") + stranica.name)
            if not suho:
                stranica.write_text(novyj, encoding="utf-8", newline="\n")
    print(f"Страниц {'к изменению' if suho else 'обновлено'}: {izmeneno}. Частей: {', '.join(sorted(chasti))}.")
    if oshibki:
        sys.exit(1)


if __name__ == "__main__":
    main()
