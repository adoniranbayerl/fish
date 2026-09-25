#!/usr/bin/env python3
"""Monta os volumes a partir de src/ e gera HTML autocontido + PDF.

Uso:  python3 src/build.py            (os dois volumes, HTML + PDF)
      python3 src/build.py guia       (só o guia)
      python3 src/build.py diario --no-pdf

Cada volume é: <vol>/head.html + páginas em <vol>/pages/*.html (ordem
alfabética) + <vol>/tail.html. O script numera as páginas, alterna
recto/verso, resolve {{pg:id}} e embute fontes e imagens em base64.
Imagens ausentes viram um quadro "foto pendente" (rode fetch_photos.py).
"""
import base64, io, os, re, subprocess, sys

from PIL import Image

SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
VOLUMES = {
    'guia': 'vinte-litros-de-mundo',
    'diario': 'diario-2027',
}
MAX_PX = 2000          # lado maior; ~240 dpi numa página A4 inteira
JPEG_Q = 80

_cache = {}


def img_data_uri(rel):
    path = os.path.join(SRC, rel)
    if rel in _cache:
        return _cache[rel]
    if not os.path.exists(path):
        name = os.path.basename(rel)
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500">'
               '<rect width="800" height="500" fill="#E1E8E1"/>'
               '<rect x="12" y="12" width="776" height="476" fill="none" stroke="#76827C" stroke-width="3" stroke-dasharray="14 10"/>'
               '<text x="400" y="240" text-anchor="middle" font-family="Arial" font-size="34" fill="#56645E">foto pendente</text>'
               f'<text x="400" y="290" text-anchor="middle" font-family="Arial" font-size="24" fill="#76827C">{name}</text></svg>')
        uri = 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()
        print(f'  ! imagem ausente: {rel}')
    elif path.endswith('.svg'):
        uri = 'data:image/svg+xml;base64,' + base64.b64encode(open(path, 'rb').read()).decode()
    else:
        im = Image.open(path)
        im = im.convert('RGB')
        if max(im.size) > MAX_PX:
            im.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
        buf = io.BytesIO()
        im.save(buf, 'JPEG', quality=JPEG_Q, optimize=True, progressive=True)
        uri = 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
    _cache[rel] = uri
    return uri


def font_data_uri(rel):
    data = open(os.path.join(SRC, rel), 'rb').read()
    return 'data:font/woff2;base64,' + base64.b64encode(data).decode()


def number_pages(pages):
    ids = {}
    out = []
    for n, p in enumerate(pages, 1):
        side = 'recto' if n % 2 else 'verso'
        p = re.sub(r'(<section class="page) (?:recto|verso)', rf'\1 {side}', p, count=1)
        p = re.sub(r'<div class="folio">[^<]*</div>', f'<div class="folio">{n}</div>', p, count=1)
        m = re.search(r'<section[^>]*\bid="([^"]+)"', p)
        if m:
            ids[m.group(1)] = n
        # âncoras internas (data-anchor="x") também recebem número
        for a in re.findall(r'data-anchor="([^"]+)"', p):
            ids[a] = n
        out.append(p)
    html = '\n\n'.join(out)

    def pg(m):
        key = m.group(1)
        if key not in ids:
            print(f'  ! referência sem destino: {key}')
            return '?'
        return str(ids[key])
    html = re.sub(r'\{\{pg:([\w-]+)\}\}', pg, html)
    return html, len(pages)


def build(vol, pdf=True):
    vdir = os.path.join(SRC, vol)
    gen = os.path.join(vdir, 'generate.py')
    if os.path.exists(gen):
        subprocess.run([sys.executable, gen], check=True)
    head = open(os.path.join(vdir, 'head.html'), encoding='utf-8').read()
    tail = open(os.path.join(vdir, 'tail.html'), encoding='utf-8').read()
    pdir = os.path.join(vdir, 'pages')
    files = sorted(f for f in os.listdir(pdir) if f.endswith('.html'))
    pages = [open(os.path.join(pdir, f), encoding='utf-8').read().strip() for f in files]
    body, count = number_pages(pages)
    html = head + body + tail
    html = re.sub(r'url\((fonts/[^)]+)\)', lambda m: f'url({font_data_uri(m.group(1))})', html)
    html = re.sub(r'(src|href)="(img/[^"]+)"', lambda m: f'{m.group(1)}="{img_data_uri(m.group(2))}"', html)
    out = os.path.join(ROOT, VOLUMES[vol] + '.html')
    open(out, 'w', encoding='utf-8').write(html)
    print(f'{vol}: {count} páginas, {os.path.getsize(out) / 1e6:.1f} MB -> {os.path.basename(out)}')
    if pdf:
        pdf_out = out[:-5] + '.pdf'
        subprocess.run(['node', os.path.join(SRC, 'render_pdf.js'), out, pdf_out], check=True)
        print(f'   PDF {os.path.getsize(pdf_out) / 1e6:.1f} MB -> {os.path.basename(pdf_out)}')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    pdf = '--no-pdf' not in sys.argv
    for v in (args or VOLUMES):
        build(v, pdf)
