import sys, os, glob
from PIL import Image, ImageChops
D = sys.argv[1]
for k in sorted(glob.glob(os.path.join(D, 'kopiya_*.png'))):
    o = k.replace('kopiya_', 'original_')
    a, b = Image.open(k).convert('RGB'), Image.open(o).convert('RGB')
    h = min(a.height, b.height)
    a, b = a.crop((0, 0, a.width, h)), b.crop((0, 0, b.width, h))
    diff = ImageChops.difference(a, b).convert('L').point(lambda v: 255 if v > 40 else 0)
    bad = sum(diff.histogram()[255:]) / (a.width * h) * 100
    rows = [y for y in range(0, h, 50) if diff.crop((0, y, a.width, y + 50)).getbbox()]
    print(f"{os.path.basename(k)[7:-4]:30} высота {Image.open(k).height}/{Image.open(o).height}  отличий {bad:.2f}%  полосы по Y: {rows[:12]}")
