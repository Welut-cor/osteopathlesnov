# Готовит фото для визитки: выбранные снимки из Telegram -> vizitka/foto/*.webp и *.jpg
# Запуск: python -X utf8 instrumenty/foto_vizitki.py
from pathlib import Path
from PIL import Image

ISTOCHNIK = Path(r"C:\Users\emill\Downloads\AyuGram Desktop")
KUDA = Path(__file__).resolve().parent.parent / "vizitka" / "foto"
VYBOR = {  # номер снимка -> имя в репозитории
    7: "portret",      # 17.11 выбор пользователя (было 2)
    1: "meditaciya",
    5: "koster",       # 17.11 выбор пользователя (было 3)
}

KUDA.mkdir(parents=True, exist_ok=True)
for n, imya in VYBOR.items():
    src = ISTOCHNIK / f"photo_{n}_2026-11-17_17-16-54.jpg"
    im = Image.open(src).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    im.save(KUDA / f"{imya}.webp", "WEBP", quality=80, method=6)
    im.save(KUDA / f"{imya}.jpg", "JPEG", quality=82, optimize=True, progressive=True)
    print(f"{imya}: {im.size}, webp {(KUDA / f'{imya}.webp').stat().st_size // 1024} КБ, "
          f"jpg {(KUDA / f'{imya}.jpg').stat().st_size // 1024} КБ")
