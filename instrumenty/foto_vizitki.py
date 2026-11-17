# Готовит фото для визитки: выбранные снимки -> vizitka/foto/*.webp и *.jpg
# Запуск: python -X utf8 instrumenty/foto_vizitki.py
# После замены фото поднять версию ?v=... в адресах фото в vizitka.html (иначе браузеры держат старые)
from pathlib import Path
from PIL import Image

TG = Path(r"C:\Users\emill\Downloads\AyuGram Desktop")
KUDA = Path(__file__).resolve().parent.parent / "vizitka" / "foto"
ARHIV = KUDA / "_Архив"
VYBOR = {  # имя в репозитории -> исходник (выбор пользователя 17.11.2026)
    "portret": TG / "photo_7_2026-11-17_17-16-54.jpg",
    "meditaciya": ARHIV / "meditaciya_ishodnik_v2.png",   # прислано в чат
    "koster": TG / "photo_5_2026-11-17_17-16-54.jpg",   # 17.11 вариант 20-52-21 отклонён, вернули №5
}

KUDA.mkdir(parents=True, exist_ok=True)
for imya, src in VYBOR.items():
    im = Image.open(src).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(KUDA / f"{imya}.webp", "WEBP", quality=80, method=6)
    im.save(KUDA / f"{imya}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    print(f"{imya}: {im.size}, webp {(KUDA / f'{imya}.webp').stat().st_size // 1024} КБ, "
          f"jpg {(KUDA / f'{imya}.jpg').stat().st_size // 1024} КБ")
