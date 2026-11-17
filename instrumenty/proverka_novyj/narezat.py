# Режет полный снимок страницы на куски для просмотра: narezat.py снимок.png высота_куска [ширина_вывода] [y0] [y1]
import sys
from pathlib import Path
from PIL import Image

src = Path(sys.argv[1]); step = int(sys.argv[2]); out_w = int(sys.argv[3]) if len(sys.argv) > 3 else 0
img = Image.open(src)
y0 = int(sys.argv[4]) if len(sys.argv) > 4 else 0
y1 = int(sys.argv[5]) if len(sys.argv) > 5 else img.height
papka = src.parent / (src.stem + "_kuski"); papka.mkdir(exist_ok=True)
i = 0
for y in range(y0, y1, step):
    k = img.crop((0, y, img.width, min(y + step, y1)))
    if out_w and k.width != out_w:
        k = k.resize((out_w, round(k.height * out_w / k.width)), Image.LANCZOS)
    p = papka / f"{y:05d}.png"; k.save(p); i += 1
    print(p)
