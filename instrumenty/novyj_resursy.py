# Однократный перенос картинок, шрифтов и видео из копии Тильды в новый сайт (novyj/).
# Запуск из корня репозитория: python -X utf8 instrumenty/novyj_resursy.py
# Уже существующие файлы не перезаписывает.
import shutil
from pathlib import Path
from PIL import Image

KOREN = Path(__file__).resolve().parent.parent
T = KOREN / "assets" / "tilda"
N = KOREN / "novyj"

KOPII = {  # откуда (в assets/tilda) -> куда (в novyj)
    "tild6331-6431-4964-b762-656531303764/Noah-Regular.woff": "fonts/Noah-Regular.woff",
    "tild3561-3135-4133-b439-326138376164/Noah-Bold.woff": "fonts/Noah-Bold.woff",
    "tild3834-3634-4236-b931-626438653537/Ellipse_4.svg": "img/fon/pyatno.svg",
    "tild3139-3837-4930-a236-623162313233/Rectangle_17.svg": "img/fon/shapka.svg",
    "tild3135-6535-4431-b131-333931616464/Frame_47.svg": "img/fon/glaz.svg",
    "tild3232-6264-4164-b331-346166643935/Frame_48.svg": "img/fon/zvezda.svg",
    "tild6332-3437-4137-a365-393736616534/Frame_52.svg": "img/fon/krug-tochka.svg",
    "tild3636-3732-4338-a334-306434623536/Frame_53.svg": "img/fon/krug.svg",
    "tild3337-6638-4330-b635-333931396463/Frame_54.svg": "img/fon/krug-4.svg",
    "tild6132-3238-4866-b235-303532313465/Frame_17.svg": "img/ikonki/ustalost.svg",
    "tild3036-6533-4739-b835-313435663234/Frame_38.svg": "img/ikonki/napryazhenie.svg",
    "tild3831-3837-4830-b433-303761353761/Frame_40.svg": "img/ikonki/trevoga.svg",
    "tild6561-3836-4835-b733-366332306134/Frame_37.svg": "img/ikonki/ne-v-tele.svg",
    "tild3239-6164-4038-b732-346662336361/Frame_39.svg": "img/ikonki/dengi.svg",
    "tild6230-3765-4761-a363-313064663632/Frame_36.svg": "img/ikonki/bol.svg",
    "tila3339-6431-4962-a536-306330326466/otzyv_anastasiya_ava.jpg": "img/otzyvy/anastasiya.jpg",
    "tila3633-6365-4232-a265-303134333332/otzyv_anastasiya_obl.jpg": "img/otzyvy/anastasiya-oblozhka.jpg",
    "vide6235-6334-4363-a361-646130353461/otzyv_anastasiya.mp4": "video/otzyv-anastasiya.mp4",
}

# (откуда, куда, ширина, формат, качество)
SZHAT = [
    ("tild3533-6239-4736-b162-323532393562/Frame_55_1.png", "img/portret.jpg", 600, "JPEG", 84),
    ("tila6661-3431-4639-b937-323765353135/aleksandr_glavnaya_f.jpg", "img/aleksandr.jpg", 900, "JPEG", 82),
    ("tild3164-6466-4364-a138-396333343962/photo_2026-06-08_041.jpeg", "img/otzyvy/yuliya.jpg", 160, "JPEG", 85),
    ("tild3039-3164-4134-b132-303937363165/Frame_50.png", "img/rakovina-telo.webp", 560, "WEBP", 82),
    ("tild6262-3339-4135-b237-643134613334/Frame_51.png", "img/rakovina-sostoyanie.webp", 560, "WEBP", 82),
]

for otk, kuda in KOPII.items():
    k = N / kuda
    if k.exists():
        continue
    k.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(T / otk, k)
    print("скопирован", kuda)

for otk, kuda, w, fmt, q in SZHAT:
    k = N / kuda
    if k.exists():
        continue
    k.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(T / otk)
    im = im.convert("RGBA" if fmt == "WEBP" else "RGB")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    if fmt == "JPEG":
        im.save(k, "JPEG", quality=q, optimize=True, progressive=True)
    else:
        im.save(k, "WEBP", quality=q, method=6)
    print("сжат", kuda, im.size, k.stat().st_size // 1024, "КБ")

fav = N / "img" / "favicon-32.png"
if not fav.exists():
    shutil.copyfile(KOREN / "favicon" / "favicon-32.png", fav)
    print("скопирован img/favicon-32.png")
