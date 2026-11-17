# Убирает белый фон вокруг иконки: заливка фона от краёв, сглаженный край без белой каймы, квадрат.
# Запуск: python -X utf8 -I prozrachnyj_fon.py <вход.png> <выход.png>
import sys
from collections import deque
from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGBA')
w, h = im.size
px = im.load()

def white(c, t=235):
    return min(c[:3]) >= t

# 1. фон - белые пиксели, связанные с краем картинки
bg = [[False] * h for _ in range(w)]
q = deque((x, y) for x in range(w) for y in (0, h - 1)) + deque((x, y) for y in range(h) for x in (0, w - 1))
while q:
    x, y = q.popleft()
    if bg[x][y] or not white(px[x, y]):
        continue
    bg[x][y] = True
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not bg[nx][ny]:
            q.append((nx, ny))

def near_bg(x, y, r):
    return any(bg[i][j] for i in range(max(0, x - r), min(w, x + r + 1)) for j in range(max(0, y - r), min(h, y + r + 1)))

# опорные цвета круга - самые частые не белые
from collections import Counter
cnt = Counter(px[x, y][:3] for x in range(w) for y in range(h) if not white(px[x, y], 200))
palette = [c for c, _ in cnt.most_common(2)]

out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
op = out.load()
for x in range(w):
    for y in range(h):
        c = px[x, y]
        if bg[x][y]:
            continue
        if near_bg(x, y, 2):
            # край: пиксель = цвет круга, смешанный с белым -> вычислить прозрачность
            best = None
            for p in palette:
                k = max(range(3), key=lambda i: 255 - p[i])  # самый «небелый» канал цвета
                a = max(0.0, min(1.0, (255 - c[k]) / max(1, 255 - p[k])))
                err = sum((a * p[i] + (1 - a) * 255 - c[i]) ** 2 for i in range(3))
                if best is None or err < best[0]:
                    best = (err, p, a)
            _, base, a = best
            op[x, y] = (*base, round(a * 255)) if a < 0.98 else c
        else:
            op[x, y] = c

# 2. квадрат по рамке круга
bbox = out.getbbox()
cw, ch = bbox[2] - bbox[0], bbox[3] - bbox[1]
side = max(cw, ch)
sq = Image.new('RGBA', (side, side), (0, 0, 0, 0))
sq.paste(out.crop(bbox), ((side - cw) // 2, (side - ch) // 2))
sq.save(dst, optimize=True)
print('было', im.size, '-> стало', sq.size, '| рамка круга', bbox, '| цвета круга', palette)
