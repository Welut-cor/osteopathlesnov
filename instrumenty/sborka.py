# Собирает автономную копию сайта: скачивает внешние файлы и переписывает ссылки на локальные
import re, os, sys, json, urllib.request, urllib.parse, posixpath

SYROE, ZAHVAT, SITE = sys.argv[1], sys.argv[2], sys.argv[3]
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36'}
PAGES = {'index': '/', 'osteopatiya': '/osteopatiya', 'iscelenie': '/iscelenie',
         'distancionnayasessiya': '/distancionnayasessiya', 'perezagruzka': '/perezagruzka',
         'denezhnyy-potok': '/denezhnyy-potok', 'pererozhdenie': '/pererozhdenie'}
URL_RE = re.compile(r'https?://(?:static|neo|ws)\.tildacdn\.com/[^"\'\s)<>\\]+|https?://cdn\.postnikovmd\.com/[^"\'\s)<>\\]+')

import gzip, base64
def get(u):
    data = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
    if data[:2] == b'\x1f\x8b':  # CDN отдаёт часть файлов сжатыми без запроса
        data = gzip.decompress(data)
    return data

def inline_vars(t):
    # url() в CSS-переменных Chrome считает от файла стилей - встраиваем как data:
    def repl(m):
        lp = m.group(2)
        f = os.path.join(SITE, *lp.split('/'))
        if not os.path.exists(f) or os.path.getsize(f) > 30000:
            return m.group(0)
        mime = 'image/svg+xml' if lp.endswith('.svg') else 'image/png' if lp.endswith('.png') else 'image/jpeg'
        return m.group(1) + "url('data:" + mime + ';base64,' + base64.b64encode(open(f, 'rb').read()).decode() + "')"
    return re.sub(r'(--[\w-]+\s*:\s*)url\(\s*[\'"]?(assets/[^\'")]+)[\'"]?\s*\)', repl, t)

def local_path(u):
    p = urllib.parse.urlsplit(u)
    path = posixpath.normpath(urllib.parse.unquote(p.path))
    if path in ('', '/', '.'):
        return None
    # имена папок без "tildacdn": иначе lazyload Тильды подменяет путь на свой CDN
    folder = {'static.tildacdn.com': 'tilda', 'neo.tildacdn.com': 'tilda-neo', 'ws.tildacdn.com': 'tilda-ws',
              'cdn.postnikovmd.com': 'postnikov'}.get(p.hostname, p.hostname)
    return 'assets/' + folder + path

done, fail = {}, {}
def fetch(u, depth=0):
    u = u.rstrip('.,;')
    key = u.split('?')[0]
    if key in done or key in fail:
        return done.get(key)
    lp = local_path(key)
    if not lp or not re.search(r'\.[a-z0-9]{2,5}$', lp, re.I):
        fail[key] = 'не файл'; return None
    try:
        data = get(key)
    except Exception as e:
        try: data = get(u)
        except Exception as e2:
            fail[key] = str(e2); return None
    full = os.path.join(SITE, *lp.split('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    done[key] = lp
    if lp.endswith('.css') and depth < 3:
        css = data.decode('utf-8', 'replace')
        def repl(m):
            ref = m.group(2)
            if ref.startswith('data:') or ref.startswith('#'):
                return m.group(0)
            absu = urllib.parse.urljoin(key, ref)
            sub = fetch(absu, depth + 1)
            if not sub:
                return m.group(0)
            return 'url(' + m.group(1) + posixpath.relpath(sub, posixpath.dirname(lp)) + m.group(1) + ')'
        css = re.sub(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)', repl, css)
        data = css.encode('utf-8')
    open(full, 'wb').write(data)
    return lp

# 1. адреса из страниц и из захвата браузером
texts = {n: open(os.path.join(SYROE, n + '.html'), encoding='utf-8').read() for n in PAGES}
urls = set()
for t in texts.values():
    urls.update(URL_RE.findall(t))
for u in json.load(open(os.path.join(ZAHVAT, '_spisok.json'), encoding='utf-8')):
    if 'optim.tildacdn' not in u:
        urls.add(u)
for u in sorted(urls):
    fetch(u)

# 2. адреса внутри скачанных JS (картинки, модули Postnikov)
for key, lp in list(done.items()):
    if lp.endswith('.js'):
        js = open(os.path.join(SITE, *lp.split('/')), encoding='utf-8', errors='replace').read()
        for u in URL_RE.findall(js):
            fetch(u)

def rewrite(text):
    # длинные адреса первыми, чтобы не задеть префиксы
    found = sorted(set(URL_RE.findall(text)), key=len, reverse=True)
    for u in found:
        lp = done.get(u.rstrip('.,;').split('?')[0])
        if lp:
            text = text.replace(u, lp)
    return text

# 3. базовый адрес модулей Postnikov -> локальный
for key, lp in done.items():
    if lp.endswith('.js'):
        f = os.path.join(SITE, *lp.split('/'))
        js = open(f, encoding='utf-8', errors='replace').read()
        new = rewrite(js)
        if new != js:
            open(f, 'w', encoding='utf-8').write(new)

# 4. страницы: ссылки между страницами -> файлы .html
def fix_links(t):
    def repl(m):
        path, tail = m.group(1), m.group(2) or ''
        name = 'index' if path in ('/', '') else path.strip('/')
        if name in PAGES:
            return 'href="' + name + '.html' + tail + '"'
        return m.group(0)
    t = re.sub(r'href="(?:https?://osteopathlesnov\.ru)?(/[a-z0-9\-]*)([#?][^"]*)?"', repl, t)
    return t

for n, t in texts.items():
    t = inline_vars(fix_links(rewrite(t)))
    open(os.path.join(SITE, n + '.html'), 'w', encoding='utf-8').write(t)

# 5. служебные файлы сайта
for f in ('robots.txt', 'sitemap.xml'):
    try: open(os.path.join(SITE, '_original_' + f), 'wb').write(get('https://osteopathlesnov.ru/' + f))
    except Exception as e: fail[f] = str(e)

print('скачано файлов:', len(done))
print('не скачано:', len([k for k, v in fail.items() if v != 'не файл']))
for k, v in fail.items():
    if v != 'не файл': print('  ', k, '->', v[:100])
left = {}
for n in PAGES:
    t = open(os.path.join(SITE, n + '.html'), encoding='utf-8').read()
    for u in URL_RE.findall(t): left[u] = left.get(u, 0) + 1
print('осталось внешних адресов tildacdn/postnikov в страницах:', len(left))
for u in list(left)[:15]: print('  ', u)
