#!/usr/bin/env python3
"""Desenhos paramétricos do betta (tipos de cauda e padrões de cor).

Gera src/guia/svg/*.svg, incluídos nas páginas com <!--#svg nome-->.
O peixe olha para a direita; a cauda sai do pedúnculo em (70, 55).
"""
import hashlib, math, os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'svg')
BLUE = '#33449C'

BODY = ('M70,50.5 C84,41 118,37 148,40.5 C161,42 169.5,47 172,52.5 '
        'C170,58.5 162,62.5 149,64 C118,67 86,64 70,59.5 Z')


def pol(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def fmt(pts):
    return ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)


def caudal(kind, R, spread, droop=0, sx=1.0):
    """Contorno da nadadeira caudal. Ângulos: 180° = para trás (esquerda)."""
    cx, cy = 72, 55
    a0, a1 = 180 - spread / 2 + droop, 180 + spread / 2 + droop
    n = 60
    edge = []
    for i in range(n + 1):
        t = i / n
        a = a0 + (a1 - a0) * t
        r = R
        if kind == 'round':
            r = R * (0.82 + 0.18 * math.sin(math.pi * t))
        elif kind == 'spade':
            r = R * (0.55 + 0.45 * (1 - abs(2 * t - 1)) ** 0.6)
        elif kind == 'veil':
            r = R * (0.45 + 0.65 * t ** 1.3)
        elif kind == 'delta':
            r = R * (0.9 + 0.1 * math.sin(math.pi * t))
        elif kind == 'double':
            r = R * (0.62 + 0.38 * abs(math.sin(2 * math.pi * t)) ** 0.5)
        edge.append((t, a, r))
    pts = []
    if kind in ('crown', 'comb'):
        rays = 12 if kind == 'crown' else 14
        web = 0.58 if kind == 'crown' else 0.84
        for i in range(rays * 2 + 1):
            t = i / (rays * 2)
            a = a0 + (a1 - a0) * t
            r = R if i % 2 == 0 else R * web
            if i % 2 == 0 and kind == 'crown':
                r = R * (1.02 if i % 4 == 0 else 0.97)
            pts.append(pol(cx, cy, r, a))
    elif kind in ('rose', 'feather'):
        waves = 22 if kind == 'rose' else 16
        amp = 0.05 if kind == 'rose' else 0.09
        for t, a, r in edge:
            pts.append(pol(cx, cy, r * (1 - amp * abs(math.sin(math.pi * waves * t))), a))
    else:
        pts = [pol(cx, cy, r, a) for t, a, r in edge]
    pts = [(cx + (x - cx) * sx, y) for x, y in pts]
    return f'M70,50.5 L{fmt(pts)} L70,59.5 Z', (cx, cy, a0, a1, R, sx)


def rays_path(cx, cy, a0, a1, R, sx, n=13, k=0.94):
    d = []
    for i in range(1, n):
        a = a0 + (a1 - a0) * i / n
        x, y = pol(cx, cy, R * k, a)
        d.append(f'M{cx},{cy} L{cx + (x - cx) * sx:.1f},{y:.1f}')
    return ' '.join(d)


def dorsal(size):
    if size == 's':
        return 'M96,40 C100,30 114,28 124,38.5 Z'
    if size == 'm':
        return 'M88,42 C92,24 112,18 126,38.5 C112,34 98,38 88,42 Z'
    if size == 'hm':
        return 'M76,50 C66,34 66,14 84,8 C102,4 122,14 128,38.5 C110,36 92,40 76,50 Z'
    return 'M80,47 C74,32 80,16 96,12 C112,10 124,22 128,38.5 C110,36 94,40 80,47 Z'


def anal(size):
    if size == 's':
        return 'M142,63.5 C126,74 96,74 76,61 C96,63 122,64 142,63.5 Z'
    if size == 'hm':
        return 'M144,63 C136,92 104,104 70,100 C64,88 66,70 74,60 C98,65 124,65 144,63 Z'
    return 'M144,63 C134,84 106,92 74,86 C70,76 70,66 74,60 C98,65 124,65 144,63 Z'


def ventral(size):
    if size == 's':
        return 'M146,63 C144,70 140,74 136,76 C140,70 141,66 142,63.5 Z'
    return 'M147,63 C146,76 140,86 132,92 C137,82 140,72 142,63.5 Z'


def pectoral(dumbo=False):
    if dumbo:
        return ('<path d="M140,55 C124,58 112,74 116,90 C126,92 140,80 144,60 Z" '
                'fill="#fff" fill-opacity=".9" stroke="#fff" stroke-opacity=".6"/>')
    return '<ellipse cx="139" cy="56.5" rx="6" ry="3.2" transform="rotate(-24 139 56.5)" fill="#fff" fill-opacity=".35"/>'


TAILS = {
    #            kind      R   spread droop dorsal anal ventral sx
    'plakat':    ('round',  24, 110, 0,  's',  's',  's', 1.0),
    'hmpk':      ('smooth', 27, 180, 0,  'm',  's',  's', 1.0),
    'ctpk':      ('crown',  27, 150, 0,  'm',  's',  's', 1.0),
    'veu':       ('veil',   56, 110, 38, 'l',  'l',  'l', 1.0),
    'delta':     ('delta',  50, 110, 0,  'l',  'l',  'l', 1.0),
    'superdelta':('delta',  50, 160, 0,  'l',  'l',  'l', 1.0),
    'halfmoon':  ('smooth', 50, 180, 0,  'hm', 'hm', 'l', 1.0),
    'ohm':       ('smooth', 50, 215, 0,  'hm', 'hm', 'l', 1.0),
    'rosetail':  ('rose',   52, 190, 0,  'hm', 'hm', 'l', 1.0),
    'feather':   ('feather',54, 195, 0,  'hm', 'hm', 'l', 1.0),
    'doubletail':('double', 50, 175, 0,  'hm', 'hm', 'l', 0.92),
    'crowntail': ('crown',  54, 170, 0,  'l',  'l',  'l', 1.0),
    'combtail':  ('comb',   50, 160, 0,  'l',  'l',  'l', 1.0),
    'spade':     ('spade',  50, 100, 0,  'l',  'l',  'l', 1.0),
    'round':     ('round',  46, 140, 0,  'l',  'l',  'l', 1.0),
    'dumbo':     ('smooth', 48, 180, 0,  'hm', 'hm', 'l', 1.0),
    'giant':     ('round',  26, 110, 0,  's',  's',  's', 1.0),
    'wild':      ('round',  22, 100, 0,  's',  's',  's', 1.0),
    'femea':     ('round',  18, 100, 0,  's',  's',  's', 1.0),
}


def fish(tail, body=BLUE, fin=None, fin_op=.5, band=None, patches=(), scales=False,
         mask=False, stripes=False, bars=False, label=None, viewbox='0 0 200 110',
         dumbo=False, ray_op=.35, body_scale=1.0, extra=''):
    kind, R, spread, droop, dsz, asz, vsz, sx = TAILS[tail]
    fin = fin or body
    cpath, geo = caudal(kind, R, spread, droop, sx)
    uid = tail + hashlib.md5(repr((body, fin, band, patches, scales, mask, stripes, bars, extra)).encode()).hexdigest()[:6]
    parts = []
    clip = f'<clipPath id="c{uid}"><path d="{BODY}"/></clipPath>'
    finclip = f'<clipPath id="f{uid}"><path d="{cpath}"/><path d="{dorsal(dsz)}"/><path d="{anal(asz)}"/></clipPath>'
    parts.append(f'<defs>{clip}{finclip}</defs>')
    g = []
    for d in (cpath, dorsal(dsz), anal(asz), ventral(vsz)):
        g.append(f'<path d="{d}" fill="{fin}" fill-opacity="{fin_op}"/>')
    if band:
        # borda clara nas nadadeiras (butterfly, multicolor): a nadadeira
        # inteira na cor da faixa e, por cima, uma cópia menor na cor base
        inner_c, _ = caudal(kind, R * 0.6, spread, droop, sx)
        g = [f'<path d="{d}" fill="{band}"/>' for d in (cpath, dorsal(dsz), anal(asz))]
        g.append(f'<path d="{inner_c}" fill="{fin}" fill-opacity="{fin_op}"/>')
        g.append(f'<path d="{dorsal(dsz)}" fill="{fin}" fill-opacity="{fin_op}" transform="translate(120 40) scale(.62) translate(-120 -40)"/>')
        g.append(f'<path d="{anal(asz)}" fill="{fin}" fill-opacity="{fin_op}" transform="translate(118 63) scale(.62) translate(-118 -63)"/>')
        g.append(f'<path d="{ventral(vsz)}" fill="{fin}" fill-opacity="{fin_op}"/>')
    g.append(f'<path d="{rays_path(*geo)}" stroke="#fff" stroke-opacity="{ray_op}" stroke-width=".7" fill="none"/>')
    g.append(f'<path d="{BODY}" fill="{body}"/>')
    inner = []
    for (x, y, rx, ry, c) in patches:
        inner.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c}"/>')
    if scales:
        for row, yy in enumerate(range(42, 66, 4)):
            for xx in range(76 + (row % 2) * 3, 148, 6):
                inner.append(f'<path d="M{xx},{yy} a3,3 0 0 0 6,0" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width=".8"/>')
    if stripes:
        inner.append('<rect x="70" y="47" width="80" height="3" fill="#1c1c1c" fill-opacity=".55"/>'
                     '<rect x="70" y="55" width="80" height="3" fill="#1c1c1c" fill-opacity=".55"/>')
    if bars:
        for xx in range(92, 146, 9):
            inner.append(f'<rect x="{xx}" y="36" width="3.4" height="32" fill="#2a1d12" fill-opacity=".55"/>')
    if mask:
        inner.append(f'<path d="M140,38 L176,38 L176,66 L140,66 Z" fill="{body}"/>')
    if inner:
        g.append(f'<g clip-path="url(#c{uid})">{"".join(inner)}</g>')
    g.append('<path d="M146,44 C149,50 149,58 145,63" stroke="#fff" stroke-opacity=".35" stroke-width=".8" fill="none"/>')
    g.append(pectoral(dumbo))
    g.append('<circle cx="160" cy="49" r="3" fill="#fff"/><circle cx="160.6" cy="49" r="1.6" fill="#0f1a2a"/>')
    g.append('<path d="M168.5,53.6 L172,52.6" stroke="#0f1a2a" stroke-opacity=".6" stroke-width=".8"/>')
    transform = ''
    if body_scale != 1.0:
        transform = f' transform="translate({100 - 100 * body_scale:.1f},{55 - 55 * body_scale:.1f}) scale({body_scale})"'
    parts.append(f'<g{transform}>{"".join(g)}</g>{extra}')
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    return f'<svg class="sv fish" viewBox="{viewbox}"{aria}>{"".join(parts)}</svg>'


def spread_diagram(deg, label):
    """Leque que mostra a abertura da cauda em graus."""
    cx, cy, R = 40, 36, 30
    a0, a1 = 180 - deg / 2, 180 + deg / 2
    x0, y0 = pol(cx, cy, R, a0)
    x1, y1 = pol(cx, cy, R, a1)
    large = 1 if deg > 180 else 0
    return (f'<svg class="sv" viewBox="0 0 60 72" role="img" aria-label="{label}">'
            f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 {large} 0 {x1:.1f},{y1:.1f} Z" fill="{BLUE}" fill-opacity=".45"/>'
            f'<path d="M{cx},{cy} L{x0:.1f},{y0:.1f} M{cx},{cy} L{x1:.1f},{y1:.1f}" stroke="{BLUE}" stroke-width="1"/>'
            f'<circle cx="{cx}" cy="{cy}" r="2" fill="{BLUE}"/>'
            f'<text x="30" y="70" text-anchor="middle" font-size="8.5" class="t1">{label}</text></svg>')


def anatomy():
    """Betta halfmoon com as partes nomeadas."""
    f = fish('halfmoon', label='Anatomia do betta: nadadeiras e órgãos', viewbox='-74 -4 334 116')
    labels = [  # ponto no peixe -> ponto do rótulo
        (98, 10, 60, -1, 'nadadeira dorsal'),
        (30, 40, -18, 24, 'nadadeira caudal'),
        (44, 76, -18, 86, 'raios'),
        (72, 55, -18, 55, 'pedúnculo'),
        (104, 96, 60, 108, 'nadadeira anal'),
        (136, 84, 190, 104, 'ventrais'),
        (139, 57, 190, 86, 'peitoral'),
        (146, 58, 190, 70, 'opérculo'),
        (136, 45, 190, 20, 'labirinto (interno)'),
        (160, 49, 190, 38, 'olho'),
        (120, 52, 190, 54, 'escamas'),
    ]
    extra = ['<ellipse cx="136" cy="45" rx="7" ry="4.2" fill="none" stroke="#fff" stroke-dasharray="1.6 1.2" stroke-width=".8"/>']
    for x, y, tx, ty, t in labels:
        anchor = 'end' if tx < x else 'start'
        extra.append(f'<path d="M{x},{y} L{tx},{ty}" stroke="#3A4843" stroke-width=".4"/>'
                     f'<circle cx="{x}" cy="{y}" r="1.1" fill="#16221E"/>'
                     f'<text x="{tx + (-1.8 if anchor == "end" else 1.8)}" y="{ty + 2.2}" font-size="6.6" text-anchor="{anchor}">{t}</text>')
    return f.replace('</svg>', ''.join(extra) + '</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    names = {
        'plakat': 'Plakat tradicional', 'hmpk': 'Halfmoon plakat', 'ctpk': 'Crowntail plakat',
        'veu': 'Cauda-véu', 'delta': 'Delta', 'superdelta': 'Super delta', 'halfmoon': 'Halfmoon',
        'ohm': 'Over-halfmoon', 'rosetail': 'Rosetail', 'feather': 'Feathertail',
        'doubletail': 'Double tail', 'crowntail': 'Crowntail', 'combtail': 'Combtail',
        'spade': 'Spadetail', 'round': 'Roundtail',
    }
    for k, name in names.items():
        open(os.path.join(OUT, f'tail-{k}.svg'), 'w').write(fish(k, label=f'Betta {name}'))
    open(os.path.join(OUT, 'tail-dumbo.svg'), 'w').write(
        fish('dumbo', label='Betta dumbo, de peitorais grandes', dumbo=True))
    open(os.path.join(OUT, 'tail-giant.svg'), 'w').write(
        fish('giant', label='Betta giant, maior que um plakat comum', body_scale=1.0,
             extra='<text x="100" y="106" text-anchor="middle" font-size="7">até 12 cm</text>'))
    open(os.path.join(OUT, 'anatomia.svg'), 'w').write(anatomy())
    for deg, lab in ((100, '< 130°'), (130, 'delta'), (165, 'super delta'), (180, '180°'), (215, '> 180°')):
        open(os.path.join(OUT, f'spread-{deg}.svg'), 'w').write(spread_diagram(deg, lab))

    # Padrões de cor (cauda halfmoon, para comparar só a cor)
    C = {
        'red': '#C0262D', 'blue': '#2F4FB5', 'royal': '#2338A8', 'steel': '#6F86A8', 'turq': '#2AA5A0',
        'black': '#1B1B22', 'yellow': '#E8C23A', 'orange': '#E3782A', 'white': '#F4F1EA',
        'copper': '#B8834A', 'green': '#2F8C7A', 'lav': '#9C8AC0', 'pink': '#E7B7B0', 'cello': '#EBD2C8',
    }
    pats = {
        'solido-vermelho': dict(body=C['red'], fin=C['red'], fin_op=.8),
        'solido-azul': dict(body=C['royal'], fin=C['royal'], fin_op=.8),
        'turquesa': dict(body=C['turq'], fin=C['turq'], fin_op=.75),
        'steel': dict(body=C['steel'], fin=C['steel'], fin_op=.75),
        'preto': dict(body=C['black'], fin=C['black'], fin_op=.9),
        'amarelo': dict(body='#EBD27A', fin=C['yellow'], fin_op=.85),
        'laranja': dict(body=C['orange'], fin=C['orange'], fin_op=.8),
        'branco': dict(body=C['white'], fin=C['white'], fin_op=.95, ray_op=.0),
        'celofane': dict(body=C['cello'], fin=C['pink'], fin_op=.45, ray_op=.0),
        'cobre': dict(body=C['copper'], fin='#8F5E34', fin_op=.8, scales=True),
        'mustard': dict(body='#26407A', fin='#E1B53A', fin_op=.9,
                        patches=[(110, 52, 40, 20, '#26407A')]),
        'bicolor': dict(body='#2D2A5E', fin=C['red'], fin_op=.85),
        'butterfly': dict(body=C['blue'], fin=C['blue'], fin_op=.5, band=C['white']),
        'marble': dict(body=C['white'], fin=C['white'], fin_op=.9,
                       patches=[(95, 46, 10, 6, C['blue']), (128, 56, 9, 7, C['red']), (150, 46, 6, 5, C['blue']), (84, 58, 7, 4, C['red'])]),
        'koi': dict(body=C['white'], fin=C['white'], fin_op=.9,
                    patches=[(96, 46, 12, 7, C['red']), (126, 58, 10, 6, C['black']), (152, 48, 8, 6, C['orange']), (84, 57, 6, 4, C['black'])]),
        'galaxy': dict(body=C['white'], fin=C['blue'], fin_op=.55, scales=True,
                       patches=[(98, 48, 12, 7, C['red']), (130, 57, 10, 6, C['blue']), (152, 47, 7, 5, C['black'])]),
        'dragon': dict(body='#D9DDE6', fin=C['red'], fin_op=.8, scales=True),
        'cambodian': dict(body=C['cello'], fin=C['red'], fin_op=.85),
        'grizzle': dict(body='#C7C1D8', fin=C['lav'], fin_op=.7,
                        patches=[(90 + 7 * i, 44 + (i % 3) * 6, 1.6, 1.6, '#3A2E6A') for i in range(9)]),
        'mascarado': dict(body=C['turq'], fin=C['turq'], fin_op=.75, mask=True, scales=True),
        'black-orchid': dict(body='#1D1B35', fin='#3B2F6E', fin_op=.9,
                             patches=[(110, 50, 38, 12, '#2E3F86')]),
        'samurai': dict(body='#16161C', fin='#16161C', fin_op=.95, scales=True),
        'avatar': dict(body='#6DB3B3', fin='#1F2A44', fin_op=.9, scales=True),
        'hellboy': dict(body='#1B1B22', fin=C['red'], fin_op=.9,
                        patches=[(150, 50, 20, 14, C['red'])]),
        'multicolor': dict(body=C['blue'], fin=C['red'], fin_op=.7, band=C['yellow']),
        'selvagem': dict(body='#6B6A48', fin='#4F6A68', fin_op=.6, bars=False, ray_op=.25),
        'estresse': dict(body='#9A6B5A', fin='#8A5A4A', fin_op=.5, stripes=True),
    }
    for k, kw in pats.items():
        open(os.path.join(OUT, f'cor-{k}.svg'), 'w').write(fish('halfmoon', label=f'Padrão {k}', **kw))
    # selvagens (cauda curta)
    wilds = {
        'wild-splendens': dict(body='#5F5A3C', fin='#8A2C2C', fin_op=.55, bars=True),
        'wild-imbellis': dict(body='#253A5C', fin='#2E4E8E', fin_op=.6, band='#C0262D'),
        'wild-smaragdina': dict(body='#2C6F63', fin='#2C6F63', fin_op=.55, scales=True),
        'wild-mahachai': dict(body='#1F3A40', fin='#2A7E7A', fin_op=.6, scales=True),
        'femea': dict(body='#7C8FB8', fin='#7C8FB8', fin_op=.5, bars=True),
    }
    for k, kw in wilds.items():
        t = 'femea' if k == 'femea' else 'wild'
        open(os.path.join(OUT, f'{k}.svg'), 'w').write(fish(t, label=k, **kw))
    # comportamento: flare (opérculo aberto)
    flare = fish('halfmoon', label='Betta em flare, com o opérculo aberto',
                 extra='<path d="M146,44 C156,40 164,50 160,62 C156,70 148,68 146,63 Z" fill="#8A1C1C" fill-opacity=".85"/>')
    open(os.path.join(OUT, 'comp-flare.svg'), 'w').write(flare)
    print('svgs:', len(os.listdir(OUT)))


if __name__ == '__main__':
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
    import betta
    betta.main()
