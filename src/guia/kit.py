"""Blocos de montagem das páginas geradas (catálogos e fichas)."""
import os

PAGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pages')
AVISO = '<!-- gerado por src/guia/generate.py a partir de src/guia/{src}; edite lá -->\n'


def page(pid, ch, rh, accent, body, extra_class='', src='conteudo'):
    tab = '+' if ch == 10 else str(ch)
    return (AVISO.format(src=src) +
            f'<section class="page recto {extra_class}" id="{pid}" data-ch="{ch}" data-rh="{rh}" style="--accent:{accent}">'
            f'<div class="rh"><span>Vinte litros de mundo</span><span class="sec">{rh}</span></div>'
            f'<div class="folio">0</div><div class="tab" style="--ch:{ch}">{tab}</div>\n'
            f'  <div class="frame">\n{body}\n  </div>\n</section>\n')


def header(eyebrow, title, deck=None, extra=''):
    d = f'\n      <p class="deck">{deck}</p>' if deck else ''
    return (f'    <header>\n      <p class="eyebrow">{eyebrow}</p>\n'
            f'      <h2 class="h1">{title}{extra}</h2>{d}\n    </header>')


IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')


def card(img, name, sub='', text='', tags='', svg=None, alt=None, pos=None):
    sub_html = f'<small>{sub}</small>' if sub else ''
    style = f' style="object-position:{pos}"' if pos else ''
    paras = ''.join(f'<p>{t}</p>' for t in (text if isinstance(text, list) else [text]) if t)
    tag_html = f'<p class="tags">{tags}</p>' if tags else ''
    if os.path.exists(os.path.join(IMG_DIR, img)):
        fish = f'<!--#svg {svg}-->' if svg else ''
        pic = f'<img src="img/{img}" alt="{alt or name}"{style}>'
        cr = f'<span class="cr" data-cr="img/{img}"></span>'
    else:
        # sem foto de licença livre: o desenho ocupa o lugar da foto
        fish = ''
        pic = f'<div class="vdraw"><!--#svg {svg}--></div>'
        cr = '<span class="cr">Desenho: não há foto de uso livre desta variedade.</span>'
    return (f'      <div class="vcard">{pic}'
            f'<div class="vh"><div><b>{name}</b>{sub_html}</div>{fish}</div>'
            f'{paras}{tag_html}{cr}</div>')


def grid(cards, cls=''):
    return f'    <div class="vgrid {cls}">\n' + '\n'.join(cards) + '\n    </div>'


def meter(n, total=3):
    return '<span class="meter">' + ''.join('<i class="on"></i>' if i < n else '<i></i>' for i in range(total)) + '</span>'


def write(fname, html):
    open(os.path.join(PAGES, fname), 'w', encoding='utf-8').write(html)
