#!/usr/bin/env python3
"""Busca, revisa e baixa as fotos que faltam no guia.

Fontes: Unsplash (candidatas escolhidas à mão em photos_todo.json),
Openverse (Flickr e outras coleções CC, sem Wikimedia) e iNaturalist
(observações com licença CC). Nada de Wikipedia/Wikimedia: os links
quebram e o guia embute as imagens de qualquer forma.

  python3 src/fetch_photos.py status          # o que falta
  python3 src/fetch_photos.py search [slot…]  # baixa miniaturas candidatas
                                              # e gera src/img/_candidatos/index.html
  python3 src/fetch_photos.py pick SLOT N     # baixa a candidata N em alta
                                              # e grava o crédito em photos.json
  python3 src/fetch_photos.py auto            # escolhe a 1ª candidata de cada slot
                                              # (use só depois de revisar a folha)

Depois: python3 src/build.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request

SRC = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(SRC, 'img')
CAND = os.path.join(IMG, '_candidatos')
TODO = os.path.join(SRC, 'photos_todo.json')
PHOTOS = os.path.join(SRC, 'photos.json')
UA = {'User-Agent': 'vinte-litros-de-mundo/2 (guia pessoal de aquarismo)'}
LIC_NAMES = {'by': 'CC BY', 'by-sa': 'CC BY-SA', 'by-nc': 'CC BY-NC', 'by-nc-sa': 'CC BY-NC-SA',
             'by-nd': 'CC BY-ND', 'by-nc-nd': 'CC BY-NC-ND', 'cc0': 'CC0', 'pdm': 'Domínio público (PDM)'}


def load(path, default):
    return json.load(open(path, encoding='utf-8')) if os.path.exists(path) else default


def save(path, data):
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data if binary else json.loads(data)


def missing_slots():
    slots = set()
    for root, _, files in os.walk(SRC):
        for f in files:
            if f.endswith('.html') and 'pages' in root:
                for m in re.findall(r'src="(img/[^"]+\.jpg)"', open(os.path.join(root, f), encoding='utf-8').read()):
                    if not os.path.exists(os.path.join(SRC, m)):
                        slots.add(m[4:-4])
    return sorted(slots)


def openverse(q, n=14):
    params = {'q': q, 'page_size': n, 'mature': 'false',
              'excluded_source': 'wikimedia,wikimedia_audio'}
    url = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode(params)
    time.sleep(3)  # limite de requisições anônimas
    out = []
    for r in get(url).get('results', []):
        if 'wikimedia' in (r.get('source') or '') or 'wiki' in (r.get('foreign_landing_url') or ''):
            continue
        if 'nd' in (r.get('license') or '').split('-'):
            continue  # sem obras derivadas: o guia recorta as fotos
        lic = LIC_NAMES.get(r.get('license', ''), r.get('license', '').upper())
        out.append(dict(source=(r.get('source') or '').capitalize(), author=r.get('creator') or 'autor desconhecido',
                        license=f"{lic} {r.get('license_version') or ''}".strip(), page=r.get('foreign_landing_url'),
                        thumb=r.get('thumbnail') or r.get('url'), full=r.get('url'), title=r.get('title'),
                        w=r.get('width') or 0, h=r.get('height') or 0))
    return out


def inaturalist(taxon, n=8):
    params = {'taxon_name': taxon, 'photos': 'true', 'quality_grade': 'research', 'per_page': n,
              'order_by': 'votes', 'photo_license': 'cc-by,cc-by-nc,cc-by-sa,cc-by-nc-sa,cc0'}
    url = 'https://api.inaturalist.org/v1/observations?' + urllib.parse.urlencode(params)
    time.sleep(1)
    out = []
    for o in get(url).get('results', []):
        for p in o.get('photos', [])[:1]:
            lic = (p.get('license_code') or '').replace('cc-', '')
            if 'nd' in lic.split('-'):
                continue
            out.append(dict(source='iNaturalist', author=(o.get('user') or {}).get('login', 'autor desconhecido'),
                            license=f"{LIC_NAMES.get(lic, lic.upper())} 4.0" if lic != 'cc0' else 'CC0',
                            page=o.get('uri'), thumb=p['url'].replace('square', 'medium'),
                            full=p['url'].replace('square', 'large'), title=o.get('species_guess'), w=1024, h=0))
    return out


def upgrade(url):
    """Flickr: tenta o tamanho de 1024 px quando a URL aponta para 500 px."""
    m = re.match(r'(https://live\.staticflickr\.com/\d+/\d+_[0-9a-f]+)(\.jpg)$', url or '')
    return [m.group(1) + '_b.jpg', url] if m else [url]


def search(slots):
    todo = load(TODO, {})
    for slot in slots:
        spec = todo.setdefault(slot, {})
        cands = list(spec.get('candidates', []))
        for q in spec.get('openverse', []):
            try:
                cands += openverse(q)
            except Exception as e:
                print(f'  openverse falhou para {q!r}: {e}')
        for t in spec.get('inaturalist', []):
            try:
                cands += inaturalist(t)
            except Exception as e:
                print(f'  inaturalist falhou para {t!r}: {e}')
        seen, uniq = set(), []
        for c in cands:
            if c.get('full') and c['full'] not in seen:
                seen.add(c['full']); uniq.append(c)
        spec['found'] = uniq
        d = os.path.join(CAND, slot)
        os.makedirs(d, exist_ok=True)
        for i, c in enumerate(uniq):
            path = os.path.join(d, f'{i:02d}.jpg')
            if not os.path.exists(path):
                try:
                    open(path, 'wb').write(get(c.get('thumb') or c['full'], binary=True))
                except Exception as e:
                    print(f'  miniatura falhou {slot} #{i}: {e}')
        montage(slot, uniq)
        print(f'{slot}: {len(uniq)} candidatas')
    save(TODO, todo)
    sheet(todo)


def montage(slot, cands):
    """Folha PNG numerada, para revisar as candidatas de um lugar."""
    from PIL import Image, ImageDraw
    d = os.path.join(CAND, slot)
    W, H, cols = 300, 200, 5
    rows = max(1, (len(cands) + cols - 1) // cols)
    sheet_im = Image.new('RGB', (W * cols, (H + 34) * rows), 'white')
    dr = ImageDraw.Draw(sheet_im)
    for i, c in enumerate(cands):
        x, y = (i % cols) * W, (i // cols) * (H + 34)
        try:
            im = Image.open(os.path.join(d, f'{i:02d}.jpg')).convert('RGB')
            im.thumbnail((W - 6, H - 6))
            sheet_im.paste(im, (x + 3, y + 3))
        except Exception:
            dr.rectangle([x + 3, y + 3, x + W - 3, y + H - 3], outline='red')
        lic = c.get('license', '')
        dr.text((x + 4, y + H + 2), f"#{i} {c.get('w') or '?'}px {lic} {c['source']}", fill='black')
        dr.text((x + 4, y + H + 16), (c.get('title') or '')[:46], fill='#555')
    sheet_im.save(os.path.join(d, 'sheet.png'))


def sheet(todo):
    rows = []
    for slot, spec in sorted(todo.items()):
        cells = ''.join(
            f'<figure><img src="{slot}/{i:02d}.jpg"><figcaption><b>{i}</b> {c.get("title") or ""}<br>'
            f'{c["author"]} / {c["source"]}, {c["license"]}</figcaption></figure>'
            for i, c in enumerate(spec.get('found', [])))
        rows.append(f'<section><h2>{slot}</h2><p>{spec.get("nota", "")}</p><div class="g">{cells}</div></section>')
    html = ('<meta charset="utf-8"><style>body{font:13px sans-serif;margin:20px} .g{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}'
            'img{width:100%;aspect-ratio:8/5;object-fit:cover;background:#ddd} figure{margin:0} h2{margin:24px 0 6px}</style>'
            '<h1>Candidatas — escolha com: python3 src/fetch_photos.py pick SLOT N</h1>' + ''.join(rows))
    os.makedirs(CAND, exist_ok=True)
    open(os.path.join(CAND, 'index.html'), 'w', encoding='utf-8').write(html)
    print('folha de revisão:', os.path.join(CAND, 'index.html'))


def pick(slot, n, src=None):
    """Baixa a candidata N da lista de SRC (padrão: o próprio lugar) para SLOT."""
    todo = load(TODO, {})
    c = todo[src or slot]['found'][int(n)]
    dest = os.path.join(IMG, slot + '.jpg')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    data = None
    for u in upgrade(c['full']):
        try:
            data = get(u, binary=True)
            break
        except Exception as e:
            print(f'  {u}: {e}')
    open(dest, 'wb').write(data)
    photos = load(PHOTOS, {})
    photos[f'img/{slot}.jpg'] = dict(author=c['author'], source=c['source'], license=c['license'], page=c.get('page') or '')
    save(PHOTOS, photos)
    print(f'{slot} <- #{n} {c["author"]} / {c["source"]}')


def manual(slot, url, author, source, license, page, crop=None, pad=None):
    """Grava uma foto escolhida à mão; crop = 'x0,y0,x1,y1' em frações da imagem."""
    import io
    from PIL import Image
    data = None
    for u in upgrade(url):
        try:
            data = get(u, binary=True)
            break
        except Exception as e:
            print(f'  {u}: {e}')
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if crop:
        x0, y0, x1, y1 = [float(v) for v in crop.split(',')]
        W, H = im.size
        im = im.crop((int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H)))
    if pad:  # completa até a proporção pedida com a cor do canto (fundos lisos)
        a, b = [float(v) for v in pad.split(':')]
        W, H = im.size
        tw, th = (max(W, int(H * a / b)), max(H, int(W * b / a)))
        canvas = Image.new('RGB', (tw, th), im.getpixel((2, 2)))
        canvas.paste(im, ((tw - W) // 2, (th - H) // 2))
        im = canvas
    dest = os.path.join(IMG, slot + '.jpg')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    im.save(dest, 'JPEG', quality=90)
    photos = load(PHOTOS, {})
    photos[f'img/{slot}.jpg'] = dict(author=author, source=source, license=license, page=page)
    save(PHOTOS, photos)
    print(f'{slot} <- {author} / {source} {im.size[0]}x{im.size[1]}')


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    if cmd == 'status':
        ms = missing_slots()
        print(f'{len(ms)} fotos faltando:'); [print(' ', s) for s in ms]
    elif cmd == 'search':
        search(sys.argv[2:] or missing_slots())
    elif cmd == 'pick':
        pick(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    elif cmd == 'manual':
        manual(*sys.argv[2:])
    elif cmd == 'auto':
        todo = load(TODO, {})
        for s in missing_slots():
            if todo.get(s, {}).get('found'):
                pick(s, 0)
    else:
        print(__doc__)


if __name__ == '__main__':
    main()
