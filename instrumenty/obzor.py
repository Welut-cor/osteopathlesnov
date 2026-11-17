import re, urllib.request, collections, os, sys
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read()
pages = ['/', '/osteopatiya', '/iscelenie', '/distancionnayasessiya', '/perezagruzka', '/denezhnyy-potok', '/pererozhdenie']
seen = set(pages); queue = list(pages)
hosts = collections.Counter(); exts = collections.Counter()
while queue:
    p = queue.pop(0)
    html = get('https://osteopathlesnov.ru' + p).decode('utf-8')
    name = 'index' if p == '/' else p.strip('/')
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(html)
    for m in re.finditer(r'href="(/[a-z0-9\-_/]*)(?:[#?][^"]*)?"', html):
        q = m.group(1)
        if q not in seen and not re.search(r'\.\w{2,4}$', q):
            seen.add(q); queue.append(q)
    for m in re.finditer(r'https?://([a-z0-9.\-]+)(/[^"\'\s)<>]*)?', html):
        hosts[m.group(1)] += 1
        e = os.path.splitext((m.group(2) or '').split('?')[0])[1]
        exts[e] += 1
    print(p, len(html), 'форм:', html.count('t-form '), 'zero:', html.count('t396'))
print('страницы:', sorted(seen))
print('хосты:', hosts.most_common(25))
print('расширения:', exts.most_common(20))
