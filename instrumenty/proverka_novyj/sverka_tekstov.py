"""Сверка текстов: всё, что было на Тильде, должно дословно найтись в новом сайте.

Эталон - выгрузка текстов копии Тильды (_Архив/novyj_etalon/teksty.txt, строки
«T x,y размер: html» и «B ...: 'текст'»). Теги, пробелы и неразрывные пробелы
нормализуются, регистр не важен (на Тильде часть заголовков - капсом через CSS).
Отзывы, подвал и окно записи выгружены только с главной - ищутся во всех частях.

Запуск из папки osteopathlesnov:  python -X utf8 instrumenty/proverka_novyj/sverka_tekstov.py
"""
import html
import pathlib
import re

KOREN = pathlib.Path(__file__).resolve().parents[2]
ETALON = KOREN / "_Архив" / "novyj_etalon" / "teksty.txt"
NOVYJ = KOREN   # новый сайт - в корне репозитория


def norm(s):
    s = re.sub(r"<br\s*/?>|</?(p|li|h\d|div|span)\b[^>]*>", " ", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    stranicy, tek = {}, None
    for stroka in ETALON.read_text(encoding="utf-8").splitlines():
        m = re.match(r"#+ (\S+) \| title:", stroka)
        if m:
            tek = m.group(1); stranicy[tek] = []; continue
        m = re.match(r"\s+T [\d.,-]+ [\d.]+px: (.*)$", stroka) or re.match(r"\s+B [^:]*: '(.*)'(?: ->.*)?$", stroka)
        if m and tek:
            stranicy[tek].append(m.group(1))
    chasti = " ".join(norm(p.read_text(encoding="utf-8")) for p in (NOVYJ / "chasti").glob("*.html"))
    vsego = net = 0
    for imya, teksty in stranicy.items():
        f = NOVYJ / f"{imya}.html"
        if not f.exists():
            print(f"!! нет страницы {f.name}"); continue
        novyj = norm(f.read_text(encoding="utf-8")) + " " + chasti
        propali = []
        for t in teksty:
            n = norm(t)
            if not n or n in ("/",):
                continue
            vsego += 1
            if n not in novyj:
                propali.append(n)
        net += len(propali)
        print(f"{'ok' if not propali else '!!'} {imya}: строк {len(teksty)}, не найдено {len(propali)}")
        for p in propali:
            print("     -", p[:150])
    print(f"Итого строк {vsego}, не найдено {net}.")


if __name__ == "__main__":
    main()
