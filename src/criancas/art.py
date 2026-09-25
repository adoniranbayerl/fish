"""Ilustrações do livro infantil: personagens, ícones, cenas e passatempos.

Tudo é SVG gerado em código: o Beto (betta), a Cereja (camarão), as
Bacterinhas, os aparelhos do aquário e as cenas das atividades.
"""
import math, os, random, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'guia'))
from generate import BODY, caudal, dorsal, anal, ventral  # noqa: E402

INK = '#16324A'      # contorno
C = dict(mar='#16324A', agua='#3FA7D6', agua2='#BFE6F5', sol='#FFC83D', coral='#F2665A',
         folha='#4FB06D', folha2='#2E8A4E', folha3='#CDEFD2', roxo='#8A6FD1', areia='#F4E3C1',
         areia2='#E2C58E', terra='#8A5A36', pedra='#9AA7B0', madeira='#8C5B34', branco='#FFFFFF',
         rosa='#F7A8B8', laranja='#F29A38', azul='#3E7FD9', cinza='#B9C3CA')


def svg(inner, vb, label=None, cls='sv', style=''):
    aria = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    st = f' style="{style}"' if style else ''
    return f'<svg class="{cls}" viewBox="{vb}"{aria}{st}>{inner}</svg>'


# ------------------------------------------------------------------ Beto
def beto(body='#2F5BD3', fin='#E8465A', mood='feliz', tail='halfmoon', uid='b', line=False, bubbles=0):
    """Betta de desenho animado. Coordenadas do peixe do guia (0..200 x 0..110)."""
    kinds = {'halfmoon': ('smooth', 48, 180, 0, 'hm', 'hm'), 'veu': ('veil', 54, 110, 38, 'l', 'l'),
             'plakat': ('round', 24, 110, 0, 's', 's'), 'crown': ('crown', 50, 170, 0, 'l', 'l'),
             'doente': ('round', 30, 70, 20, 's', 's')}
    kind, R, spread, droop, ds, asz = kinds[tail]
    cpath, _ = caudal(kind, R, spread, droop)
    sw = 1.8
    if line:  # para colorir: só contorno
        fill_b = fill_f = '#fff'
        fo = 1
    else:
        fill_b, fill_f, fo = body, fin, .92
    st = f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"'
    g = []
    for d in (cpath, dorsal(ds), anal(asz), ventral('l' if tail != 'plakat' else 's')):
        g.append(f'<path d="{d}" fill="{fill_f}" fill-opacity="{fo}" {st}/>')
    if not line:
        # raios claros nas nadadeiras
        g.append(f'<g stroke="#fff" stroke-opacity=".35" stroke-width="1.2" fill="none">'
                 + ''.join(f'<path d="M72,55 l{-R * math.cos(math.radians(a)):.1f},{R * math.sin(math.radians(a)) * .9:.1f}"/>'
                           for a in range(-60, 61, 20)) + '</g>')
    g.append(f'<path d="{BODY}" fill="{fill_b}" {st}/>')
    if mood == 'estresse' and not line:
        g.append(f'<clipPath id="bc{uid}"><path d="{BODY}"/></clipPath><g clip-path="url(#bc{uid})" fill="#1c1c2a" fill-opacity=".45">'
                 '<rect x="70" y="46" width="85" height="3.2"/><rect x="70" y="54" width="85" height="3.2"/></g>')
    if mood == 'bravo':
        g.append('<path d="M146,44 C157,39 166,50 161,63 C157,71 148,69 146,63 Z" fill="#7A1426" stroke="%s" stroke-width="1.4"/>' % INK)
    # peitoral
    g.append(f'<path d="M138,57 C131,62 128,70 133,74 C138,70 141,64 142,58 Z" fill="{fill_f}" fill-opacity=".8" {st} stroke-width="1.2"/>')
    # rosto
    ex, ey = 157, 47.5
    if mood == 'dormindo':
        g.append(f'<path d="M{ex - 5},{ey} q5,4 10,0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
        g.append(f'<text x="170" y="28" font-size="11" font-family="Fredoka" font-weight="600" fill="{INK}">z</text>'
                 f'<text x="178" y="18" font-size="14" font-family="Fredoka" font-weight="600" fill="{INK}">z</text>')
    else:
        g.append(f'<circle cx="{ex}" cy="{ey}" r="7" fill="#fff" stroke="{INK}" stroke-width="1.6"/>'
                 f'<circle cx="{ex + 1.6}" cy="{ey + .6}" r="3.9" fill="{INK}"/>'
                 f'<circle cx="{ex + 2.8}" cy="{ey - 1}" r="1.4" fill="#fff"/>')
    if mood in ('feliz', 'dormindo', 'apaixonado'):
        g.append(f'<path d="M162,56.5 q4.5,4 9,-.5" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
        if not line:
            g.append('<ellipse cx="150" cy="56" rx="4" ry="2.3" fill="#FF8FA3" fill-opacity=".7"/>')
    elif mood == 'bravo':
        g.append(f'<ellipse cx="167" cy="57.5" rx="3.2" ry="2.4" fill="{INK}"/>'
                 f'<path d="M150,38.5 l13,4" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>')
    elif mood in ('estresse', 'doente'):
        g.append(f'<path d="M162,59 q4.5,-3.5 9,.5" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>'
                 f'<path d="M151,40 l11,-3" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    for i in range(bubbles):
        bx, by, r = 176 + (i % 2) * 7, 34 - i * 11, 3 + (i % 3)
        g.append(f'<circle cx="{bx}" cy="{by}" r="{r}" fill="#fff" fill-opacity=".6" stroke="{INK}" stroke-width="1.2"/>')
    return f'<g>{"".join(g)}</g>'


def beto_svg(label='O Beto, um betta', vb='-2 -8 200 118', **kw):
    return svg(beto(**kw), vb, label)


# ------------------------------------------------------------------ Cereja
def cereja(color='#E0453A', light='#F59A8E', face=True, s=1.0, x=0, y=0, flip=False, line=False, rot=0):
    """Camarão de desenho animado, virado para a direita, caixa ~0..130 x 0..80."""
    if line:
        color = light = '#fff'
    st = f'stroke="{INK}" stroke-width="{1.6 / max(s, .5):.2f}" stroke-linejoin="round"'
    g = []
    # antenas
    g.append(f'<path d="M98,31 C112,14 122,8 132,3 M97,33 C110,24 120,24 131,19" fill="none" stroke="{INK}" stroke-width="1.3" stroke-linecap="round"/>')
    # patinhas
    g.append(f'<g stroke="{INK}" stroke-width="1.6" stroke-linecap="round">'
             '<path d="M70,51 l-4,12 M77,52 l-1,13 M84,51 l2,12 M90,49 l5,10 M52,51 l-3,7 M42,54 l-4,6 M33,57 l-5,5"/></g>')
    # cauda em leque
    g.append(f'<path d="M22,62 C8,62 4,74 10,78 C16,76 20,72 24,68 Z" fill="{color}" {st}/>'
             f'<path d="M24,64 C18,72 20,82 26,82 C28,77 28,71 27,66 Z" fill="{light}" {st}/>')
    # segmentos do abdômen
    for cx, cy, rx, ry in ((24, 58, 8, 7.5), (31, 50, 9.5, 8.5), (42, 44, 11, 9.5), (55, 41, 12, 10.5)):
        g.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" {st}/>')
    # cabeça
    g.append(f'<path d="M62,30 C80,24 96,28 101,37 C103,43 96,50 82,52 C70,54 60,50 58,42 C57,36 58,32 62,30 Z" fill="{color}" {st}/>')
    g.append(f'<path d="M99,34 L116,30 L101,41 Z" fill="{color}" {st}/>')
    if not line:
        g.append(f'<path d="M64,35 C75,31 88,32 95,37" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2.4" stroke-linecap="round"/>')
    if face:
        g.append(f'<path d="M90,31 L92,25" stroke="{INK}" stroke-width="1.6"/>'
                 f'<circle cx="93" cy="22" r="5.6" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
                 f'<circle cx="94.4" cy="22.4" r="3" fill="{INK}"/><circle cx="95.4" cy="21.2" r="1.1" fill="#fff"/>'
                 f'<path d="M92,44 q3.5,3 7,-.5" fill="none" stroke="{INK}" stroke-width="1.5" stroke-linecap="round"/>')
    tr = f'translate({x},{y})'
    if flip:
        tr += f' translate({130 * s},0) scale(-1,1)'
    if rot:
        tr += f' rotate({rot} 65 45)'
    return f'<g transform="{tr} scale({s})">{"".join(g)}</g>'


def cereja_svg(label='A Cereja, um camarão', **kw):
    return svg(cereja(**kw), '0 -2 136 88', label)


# ------------------------------------------------------------------ Bacterinhas e companhia
def bacterinha(color='#F29A38', x=0, y=0, s=1.0, mood='feliz', line=False):
    if line:
        color = '#fff'
    g = [f'<path d="M6,30 C-4,34 -2,44 -8,48 M8,36 C2,44 6,52 0,58" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>',
         f'<rect x="4" y="14" width="72" height="36" rx="18" fill="{color}" stroke="{INK}" stroke-width="2"/>',
         '' if line else '<rect x="14" y="19" width="30" height="7" rx="3.5" fill="#fff" fill-opacity=".35"/>',
         f'<circle cx="46" cy="30" r="5" fill="#fff" stroke="{INK}" stroke-width="1.4"/><circle cx="47.5" cy="30.5" r="2.8" fill="{INK}"/>',
         f'<circle cx="60" cy="30" r="5" fill="#fff" stroke="{INK}" stroke-width="1.4"/><circle cx="61.5" cy="30.5" r="2.8" fill="{INK}"/>']
    if mood == 'comendo':
        g.append(f'<ellipse cx="54" cy="41" rx="5" ry="4" fill="{INK}"/>')
    else:
        g.append(f'<path d="M48,40 q6,5 12,0" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def nuvem(color, x=0, y=0, s=1.0, mood='bravo', label=''):
    """Amônia e nitrito: nuvenzinhas rabugentas; nitrato: gotinha verde feliz."""
    g = []
    if mood == 'feliz':
        g.append(f'<path d="M30,4 C44,22 54,32 54,44 C54,58 43,66 30,66 C17,66 6,58 6,44 C6,32 16,22 30,4 Z" fill="{color}" stroke="{INK}" stroke-width="2"/>'
                 f'<circle cx="23" cy="42" r="3.4" fill="{INK}"/><circle cx="37" cy="42" r="3.4" fill="{INK}"/>'
                 f'<path d="M23,51 q7,6 14,0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    else:
        g.append(f'<path d="M12,48 C2,48 0,34 10,31 C8,19 22,13 29,20 C33,8 51,8 54,21 C64,18 72,28 66,36 C74,42 68,54 58,52 C54,60 40,62 35,55 C28,61 14,58 12,48 Z" fill="{color}" stroke="{INK}" stroke-width="2"/>'
                 f'<path d="M22,30 l9,4 M49,30 l-9,4" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
                 f'<circle cx="28" cy="38" r="3" fill="{INK}"/><circle cx="43" cy="38" r="3" fill="{INK}"/>'
                 f'<path d="M28,49 q7.5,-5 15,0" fill="none" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>')
    if label:
        g.append(f'<text x="35" y="80" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="12" fill="{INK}">{label}</text>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


# ------------------------------------------------------------------ ícones (24x24)
def icon(name, size=None):
    I = {
        'adulto': f'<circle cx="8" cy="6" r="3.4" fill="{C["coral"]}"/><path d="M2.5,21 C2.5,14 4.5,11 8,11 C11.5,11 13.5,14 13.5,21 Z" fill="{C["coral"]}"/>'
                  f'<circle cx="18" cy="10" r="2.6" fill="{C["agua"]}"/><path d="M14,21 C14,16 15.5,14 18,14 C20.5,14 22,16 22,21 Z" fill="{C["agua"]}"/>'
                  f'<path d="M12.5,15.5 L15.5,16.5" stroke="{INK}" stroke-width="1.4" stroke-linecap="round"/>',
        'eu': f'<circle cx="12" cy="7" r="4" fill="{C["agua"]}"/><path d="M5,22 C5,15 8,12.5 12,12.5 C16,12.5 19,15 19,22 Z" fill="{C["agua"]}"/>',
        'experiencia': f'<path d="M9,2 h6 M10,2 v6 L4,19 C3,21 4.5,22.5 6.5,22.5 h11 C19.5,22.5 21,21 20,19 L14,8 V2" fill="{C["agua2"]}" stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
                       f'<path d="M6.5,16 h11 L19.6,19.6 C20.2,21 19.4,22 17.8,22 H6.2 C4.6,22 3.8,21 4.4,19.6 Z" fill="{C["folha"]}"/><circle cx="10" cy="18.5" r="1.2" fill="#fff"/><circle cx="14" cy="17.4" r=".9" fill="#fff"/>',
        'dica': f'<path d="M12,2.5 C7.5,2.5 5,6 5,9.5 C5,12.5 7,14 8,15.5 C8.6,16.5 8.8,17.5 8.8,18.5 H15.2 C15.2,17.5 15.4,16.5 16,15.5 C17,14 19,12.5 19,9.5 C19,6 16.5,2.5 12,2.5 Z" fill="{C["sol"]}" stroke="{INK}" stroke-width="1.5"/>'
                f'<path d="M9,20.5 h6 M10,22.8 h4" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>',
        'sabia': f'<circle cx="12" cy="12" r="10" fill="{C["roxo"]}"/><text x="12" y="17" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="15" fill="#fff">?</text>',
        'atencao': f'<path d="M12,2.5 L22.5,21 H1.5 Z" fill="{C["coral"]}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/><path d="M12,9 v6" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="18" r="1.4" fill="#fff"/>',
        'jogo': f'<path d="M12,2 L14.9,8.3 L21.8,9 L16.6,13.6 L18.1,20.4 L12,16.9 L5.9,20.4 L7.4,13.6 L2.2,9 L9.1,8.3 Z" fill="{C["sol"]}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>',
        'lapis': f'<path d="M4,20 L5,15 L16,4 L20,8 L9,19 Z" fill="{C["sol"]}" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/><path d="M4,20 L5,15 L9,19 Z" fill="{C["areia"]}" stroke="{INK}" stroke-width="1.2"/><path d="M14,6 l4,4" stroke="{INK}" stroke-width="1.2"/>',
        'estrela': f'<path d="M12,2 L14.9,8.3 L21.8,9 L16.6,13.6 L18.1,20.4 L12,16.9 L5.9,20.4 L7.4,13.6 L2.2,9 L9.1,8.3 Z" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>',
        'ok': f'<circle cx="12" cy="12" r="10" fill="{C["folha"]}"/><path d="M7,12.5 l3.5,3.5 l6.5,-7" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
        'nao': f'<circle cx="12" cy="12" r="10" fill="{C["coral"]}"/><path d="M8,8 l8,8 M16,8 l-8,8" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>',
        'coracao': f'<path d="M12,21 C5,15.5 2,12 2,8 C2,5 4.3,3 7,3 C9,3 10.8,4.2 12,6 C13.2,4.2 15,3 17,3 C19.7,3 22,5 22,8 C22,12 19,15.5 12,21 Z" fill="none" stroke="{INK}" stroke-width="1.5"/>',
        'maos': f'<path d="M6,21 V11 C6,9.5 8,9.5 8,11 V8 C8,6.5 10,6.5 10,8 V7 C10,5.5 12,5.5 12,7 V8 C12,6.5 14,6.5 14,8 V14 L16,12 C17,11 18.6,12 17.8,13.4 L14,21 Z" fill="{C["agua2"]}" stroke="{INK}" stroke-width="1.3" stroke-linejoin="round"/>'
                f'<circle cx="18" cy="5" r="1.6" fill="{C["agua"]}"/><circle cx="20.5" cy="8.5" r="1.1" fill="{C["agua"]}"/><circle cx="4" cy="6" r="1.3" fill="{C["agua"]}"/>',
    }
    st = f' style="width:{size};height:{size}"' if size else ''
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"{st}>{I[name]}</svg>'


def smile(kind, size='9mm'):
    faces = {'feliz': f'<path d="M8,14 q4,4 8,0" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>',
             'meio': f'<path d="M8,15 h8" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>',
             'triste': f'<path d="M8,16 q4,-4 8,0" fill="none" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'}
    return (f'<svg class="ic" viewBox="0 0 24 24" style="width:{size};height:{size}" aria-hidden="true">'
            f'<circle cx="12" cy="12" r="10.5" fill="none" stroke="{INK}" stroke-width="1.4"/>'
            f'<circle cx="8.5" cy="9.5" r="1.3" fill="{INK}"/><circle cx="15.5" cy="9.5" r="1.3" fill="{INK}"/>{faces[kind]}</svg>')


# ------------------------------------------------------------------ aparelhos (100x100)
def aparelho(name):
    k = INK
    A = {
        'filtro': f'<path d="M50,6 V30" stroke="{k}" stroke-width="5" stroke-linecap="round"/><rect x="30" y="30" width="40" height="58" rx="10" fill="{C["sol"]}" stroke="{k}" stroke-width="2.5"/>'
                  + ''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#D9A22A"/>' for x, y in ((40, 42), (58, 46), (46, 56), (60, 64), (40, 70), (52, 78)))
                  + f'<g fill="#fff" stroke="{k}" stroke-width="1.6"><circle cx="58" cy="14" r="4"/><circle cx="64" cy="5" r="3"/><circle cx="56" cy="24" r="2.5"/></g>',
        'compressor': f'<rect x="14" y="44" width="62" height="40" rx="10" fill="{C["cinza"]}" stroke="{k}" stroke-width="2.5"/><circle cx="36" cy="64" r="8" fill="#fff" stroke="{k}" stroke-width="2"/><path d="M36,64 l4,-5" stroke="{k}" stroke-width="2"/>'
                      f'<path d="M76,58 C92,56 90,30 72,24 C58,20 60,8 74,6" fill="none" stroke="{k}" stroke-width="3" stroke-linecap="round"/><rect x="58" y="60" width="10" height="8" rx="2" fill="{C["coral"]}"/>',
        'aquecedor': f'<rect x="38" y="6" width="24" height="86" rx="12" fill="#E8F6FC" stroke="{k}" stroke-width="2.5"/><rect x="38" y="6" width="24" height="16" rx="6" fill="{C["mar"]}"/>'
                     f'<path d="M44,34 q6,4 12,0 q-6,4 -12,8 q6,4 12,0 q-6,4 -12,8 q6,4 12,0 q-6,4 -12,8" fill="none" stroke="{C["coral"]}" stroke-width="3" stroke-linecap="round"/>'
                     f'<path d="M72,40 q6,-6 0,-12 M80,46 q8,-9 0,-18" fill="none" stroke="{C["coral"]}" stroke-width="2.4" stroke-linecap="round"/>',
        'termometro': f'<rect x="12" y="26" width="56" height="36" rx="8" fill="{C["cinza"]}" stroke="{k}" stroke-width="2.5"/><rect x="18" y="32" width="44" height="24" rx="4" fill="#DFF5E4" stroke="{k}" stroke-width="1.5"/>'
                      f'<text x="40" y="50" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="17" fill="{k}">25°</text>'
                      f'<path d="M68,44 C84,44 84,70 76,82" fill="none" stroke="{k}" stroke-width="2.4"/><rect x="71" y="80" width="10" height="16" rx="5" fill="{C["cinza"]}" stroke="{k}" stroke-width="2"/>',
        'luz': f'<rect x="8" y="22" width="84" height="16" rx="8" fill="{C["mar"]}" stroke="{k}" stroke-width="2.5"/><rect x="16" y="34" width="68" height="5" rx="2.5" fill="{C["sol"]}"/>'
               + ''.join(f'<path d="M{x},46 l{d},18" stroke="{C["sol"]}" stroke-width="3.2" stroke-linecap="round"/>' for x, d in ((22, -5), (38, -2), (50, 0), (62, 2), (78, 5))),
        'tampa': f'<path d="M10,50 L28,30 H92 L74,50 Z" fill="{C["agua2"]}" fill-opacity=".7" stroke="{k}" stroke-width="2.5" stroke-linejoin="round"/><path d="M34,36 L28,44 M44,36 L38,44" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M10,50 V56 H74 V50 M74,56 L92,36 V30" fill="none" stroke="{k}" stroke-width="2.5" stroke-linejoin="round"/>',
        'condicionador': f'<rect x="30" y="30" width="40" height="62" rx="8" fill="{C["agua"]}" stroke="{k}" stroke-width="2.5"/><rect x="40" y="16" width="20" height="16" rx="3" fill="{C["mar"]}"/>'
                         f'<rect x="36" y="48" width="28" height="26" rx="4" fill="#fff"/><path d="M50,52 C55,59 58,62 58,66 C58,70 54,72 50,72 C46,72 42,70 42,66 C42,62 45,59 50,52 Z" fill="{C["agua"]}"/>',
        'testes': ''.join(f'<rect x="{x}" y="14" width="16" height="72" rx="8" fill="#fff" stroke="{k}" stroke-width="2.5"/><rect x="{x + 2.5}" y="46" width="11" height="37" rx="5.5" fill="{c}"/><rect x="{x - 2}" y="10" width="20" height="8" rx="3" fill="{C["mar"]}"/>'
                          for x, c in ((18, '#F4D35E'), (42, '#7DC47A'), (66, '#A77BD8'))),
        'balde': f'<path d="M22,34 H78 L70,90 H30 Z" fill="{C["coral"]}" stroke="{k}" stroke-width="2.5" stroke-linejoin="round"/><path d="M22,34 C22,6 78,6 78,34" fill="none" stroke="{k}" stroke-width="2.5"/>'
                 f'<ellipse cx="50" cy="34" rx="28" ry="5" fill="{C["agua"]}" stroke="{k}" stroke-width="2"/>',
        'sifao': f'<path d="M30,10 C30,4 42,4 42,12 V60" fill="none" stroke="{k}" stroke-width="3"/><rect x="34" y="58" width="16" height="34" rx="4" fill="{C["agua2"]}" stroke="{k}" stroke-width="2.5"/>'
                 f'<path d="M30,10 V40 C30,60 64,56 70,82" fill="none" stroke="{C["folha2"]}" stroke-width="4" stroke-linecap="round"/>',
        'comida': f'<rect x="30" y="30" width="40" height="60" rx="8" fill="{C["sol"]}" stroke="{k}" stroke-width="2.5"/><rect x="34" y="18" width="32" height="14" rx="4" fill="{C["coral"]}" stroke="{k}" stroke-width="2"/>'
                  + ''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{C["terra"]}"/>' for x, y in ((42, 50), (52, 56), (58, 46), (46, 64), (56, 70))),
    }
    return svg(A[name], '0 0 100 100', name)


# ------------------------------------------------------------------ cenas
def aquario(w=400, h=240, sand=True, water=True, inner='', frame=True, line=False):
    """Moldura de aquário de frente, com água, areia inclinada e tampa."""
    g = []
    if water and not line:
        g.append(f'<rect x="0" y="24" width="{w}" height="{h - 24}" fill="{C["agua2"]}"/>')
    if sand:
        fill = '#fff' if line else C['areia']
        g.append(f'<path d="M0,{h} V{h - 50} C{w * .3},{h - 46} {w * .6},{h - 28} {w},{h - 26} V{h} Z" fill="{fill}" stroke="{INK}" stroke-width="{1.5 if line else 0}"/>')
    g.append(inner)
    if frame:
        g.append(f'<rect x="0" y="0" width="{w}" height="{h}" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M0,24 H{w}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="6 5"/>')
    return ''.join(g)


def pedra(x, y, s=1.0, fill=None, line=False):
    f = '#fff' if line else (fill or C['pedra'])
    return (f'<path transform="translate({x},{y}) scale({s})" d="M0,0 C4,-26 26,-40 46,-34 C62,-30 70,-12 68,0 Z" fill="{f}" stroke="{INK}" stroke-width="2"/>')


def planta_caule(x, y, hgt, color=None, leaves=8, line=False, flip=1):
    color = '#fff' if line else (color or C['folha'])
    g = [f'<path d="M{x},{y} C{x - 6 * flip},{y - hgt * .4} {x + 6 * flip},{y - hgt * .7} {x},{y - hgt}" fill="none" stroke="{INK}" stroke-width="2"/>']
    for i in range(leaves):
        t = (i + 1) / (leaves + 1)
        yy = y - hgt * t
        side = 1 if i % 2 else -1
        g.append(f'<ellipse cx="{x + side * 9}" cy="{yy}" rx="10" ry="4" transform="rotate({side * -25} {x + side * 9} {yy})" fill="{color}" stroke="{INK}" stroke-width="1.5"/>')
    return ''.join(g)


def tufo(x, y, n=5, hgt=40, color=None, line=False):
    color = '#fff' if line else (color or C['folha2'])
    g = []
    for i in range(n):
        a = -40 + i * 80 / max(n - 1, 1)
        ex = x + math.sin(math.radians(a)) * hgt * .6
        ey = y - math.cos(math.radians(a)) * hgt
        g.append(f'<path d="M{x - 3},{y} Q{(x + ex) / 2 - 6},{(y + ey) / 2} {ex},{ey} Q{(x + ex) / 2 + 6},{(y + ey) / 2} {x + 3},{y} Z" fill="{color}" stroke="{INK}" stroke-width="1.5"/>')
    return ''.join(g)


def anubia(x, y, s=1.0, line=False):
    f = '#fff' if line else C['folha2']
    g = []
    for dx, dy, r in ((-16, -14, -30), (0, -22, 0), (16, -14, 30), (-6, -6, -60), (8, -6, 60)):
        g.append(f'<ellipse cx="{dx}" cy="{dy}" rx="8" ry="15" transform="rotate({r} {dx} {dy})" fill="{f}" stroke="{INK}" stroke-width="1.6"/>')
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(g)}</g>'


def bolhas(x, y, n=4, line=False):
    return ''.join(f'<circle cx="{x + (i % 2) * 8}" cy="{y - i * 16}" r="{4 + i % 3}" fill="{"#fff" if line else "#fff"}" fill-opacity="{1 if line else .7}" stroke="{INK}" stroke-width="1.5"/>' for i in range(n))


def cena(diffs=(), line=False):
    """Cena do aquário usada no jogo das diferenças e na página de colorir."""
    w, h = 400, 250
    inner = []
    inner.append(f'<path d="M60,{h - 44} C90,{h - 110} 150,{h - 150} 210,{h - 170}" fill="none" stroke="{INK}" stroke-width="11" stroke-linecap="round"/>'
                 f'<path d="M60,{h - 44} C90,{h - 110} 150,{h - 150} 210,{h - 170}" fill="none" stroke="{"#fff" if line else C["madeira"]}" stroke-width="7" stroke-linecap="round"/>')
    inner.append(planta_caule(40, h - 46, 150, line=line))
    inner.append(planta_caule(62, h - 44, 120, color=C['folha3'] if not line else None, line=line, flip=-1))
    inner.append(planta_caule(84, h - 42, 170 if 3 not in diffs else 110, line=line))
    inner.append(pedra(150, h - 34, 1.3, line=line))
    if 5 not in diffs:
        inner.append(pedra(236, h - 30, .7, fill='#7E8C96' if 1 not in diffs else C['coral'], line=line))
    inner.append(anubia(175, h - 76, 1.0, line=line))
    inner.append(tufo(300, h - 28, 6, 36, line=line) + tufo(340, h - 27, 5, 30, line=line))
    # flutuantes
    for i, fx in enumerate((300, 322, 344, 366)):
        inner.append(f'<ellipse cx="{fx}" cy="28" rx="10" ry="5" fill="{"#fff" if line else C["folha"]}" stroke="{INK}" stroke-width="1.5"/>'
                     f'<path d="M{fx},32 v{14 + (i % 2) * 8}" stroke="{C["coral"] if not line else INK}" stroke-width="1.5"/>')
    inner.append(f'<g transform="translate(236,80) scale(.8)">{beto(fin=C["coral"] if 2 not in diffs else C["folha"], line=line, uid="c" + "".join(map(str, diffs)) + str(int(line)))}</g>')
    inner.append(bolhas(372, 110, 4 if 4 not in diffs else 2, line=line))
    inner.append(cereja(s=.32, x=112, y=h - 70, line=line))
    if 6 not in diffs:
        inner.append(cereja(s=.28, x=268, y=h - 52, flip=True, line=line))
    return svg(aquario(w, h, inner=''.join(inner), line=line), f'-4 -4 {w + 8} {h + 8}', 'Um aquário com o Beto, camarões e plantas')


def cena_escondidos(seed=7):
    """Aquário cheio de plantas com 7 camarões escondidos."""
    w, h = 400, 260
    rnd = random.Random(seed)
    shrimps = [(40, 170, .26, False, 0), (128, 118, .22, True, 10), (206, 186, .24, False, -8), (300, 150, .2, True, 0),
               (346, 200, .24, False, 12), (250, 70, .2, False, 0), (92, 208, .2, True, -10)]
    inner = []
    inner.append(pedra(120, h - 36, 1.2) + pedra(250, h - 30, .9))
    for sx, sy, s, f, r in shrimps:
        inner.append(cereja(s=s, x=sx, y=sy, flip=f, rot=r, face=False))
    xs = [18, 44, 70, 96, 170, 196, 222, 290, 316, 342, 368]
    for i, x in enumerate(xs):
        inner.append(planta_caule(x, h - 40 - rnd.randint(0, 8), rnd.randint(110, 190),
                                  color=[C['folha'], C['folha2'], C['folha3']][i % 3], leaves=rnd.randint(7, 10), flip=1 if i % 2 else -1))
    inner.append(tufo(140, h - 30, 7, 44) + tufo(330, h - 26, 6, 38))
    return svg(aquario(w, h, inner=''.join(inner)), f'-4 -4 {w + 8} {h + 8}', 'Aquário com camarões escondidos entre as plantas')


# ------------------------------------------------------------------ labirinto
def labirinto(cols=13, rows=15, seed=11, cell=26, solution=False):
    rnd = random.Random(seed)
    walls = {(c, r): {'N', 'S', 'L', 'O'} for c in range(cols) for r in range(rows)}
    seen = {(0, 0)}
    stack = [(0, 0)]
    moves = {'N': (0, -1, 'S'), 'S': (0, 1, 'N'), 'L': (1, 0, 'O'), 'O': (-1, 0, 'L')}
    parent = {(0, 0): None}
    while stack:
        c, r = stack[-1]
        opts = [(d, c + dx, r + dy, op) for d, (dx, dy, op) in moves.items() if 0 <= c + dx < cols and 0 <= r + dy < rows and (c + dx, r + dy) not in seen]
        if not opts:
            stack.pop()
            continue
        d, nc, nr, op = rnd.choice(opts)
        walls[(c, r)].discard(d)
        walls[(nc, nr)].discard(op)
        seen.add((nc, nr))
        parent[(nc, nr)] = (c, r)
        stack.append((nc, nr))
    goal = (cols - 1, rows - 1)
    lines = []
    for (c, r), ws in walls.items():
        x, y = c * cell, r * cell
        if 'N' in ws and not (c == 0 and r == 0):
            lines.append(f'M{x},{y} h{cell}')
        if 'O' in ws:
            lines.append(f'M{x},{y} v{cell}')
        if r == rows - 1 and 'S' in ws and (c, r) != goal:
            lines.append(f'M{x},{y + cell} h{cell}')
        if c == cols - 1 and 'L' in ws:
            lines.append(f'M{x + cell},{y} v{cell}')
    W, H = cols * cell, rows * cell
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>',
         f'<path d="{" ".join(lines)}" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" fill="none"/>']
    if solution:
        path, p = [], goal
        while p:
            path.append(p)
            p = parent[p]
        pts = ' '.join(f'{c * cell + cell / 2},{r * cell + cell / 2}' for c, r in reversed(path))
        g.append(f'<polyline points="{cell / 2},{-cell / 2} {pts} {goal[0] * cell + cell / 2},{H + cell / 2}" fill="none" stroke="{C["coral"]}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    else:
        g.append(cereja(s=.42, x=-20, y=-44))
        # musgo no fim
        g.append(f'<g transform="translate({W - cell * 1.3},{H + 4})">'
                 + ''.join(f'<circle cx="{dx}" cy="{dy}" r="{r}" fill="{C["folha"]}" stroke="{INK}" stroke-width="1.5"/>'
                           for dx, dy, r in ((10, 14, 12), (26, 10, 13), (40, 16, 11), (22, 22, 12)))
                 + '</g>')
    return svg(''.join(g), f'-30 -52 {W + 60} {H + 90}', 'Labirinto')


# ------------------------------------------------------------------ caça-palavras
def caca_palavras(words, n=11, seed=5):
    rnd = random.Random(seed)
    for _ in range(500):
        grid = [[None] * n for _ in range(n)]
        placed = {}
        ok = True
        for w in sorted(words, key=len, reverse=True):
            for _ in range(200):
                horiz = rnd.random() < .6
                r = rnd.randrange(n if horiz else n - len(w) + 1)
                c = rnd.randrange(n - len(w) + 1 if horiz else n)
                cells = [(r, c + i) if horiz else (r + i, c) for i in range(len(w))]
                if all(grid[a][b] in (None, w[i]) for i, (a, b) in enumerate(cells)):
                    for i, (a, b) in enumerate(cells):
                        grid[a][b] = w[i]
                    placed[w] = cells
                    break
            else:
                ok = False
                break
        if ok:
            break
    letters = 'ABCDEFGHIJLMNOPRSTUV'
    for r in range(n):
        for c in range(n):
            if grid[r][c] is None:
                grid[r][c] = rnd.choice(letters)
    return grid, placed


def grade_letras(grid, placed=None, cell=12.5):
    n = len(grid)
    hl = {rc for cells in (placed or {}).values() for rc in cells}
    rows = []
    for r in range(n):
        tds = ''.join(f'<td class="{"hl" if (r, c) in hl else ""}">{grid[r][c]}</td>' for c in range(n))
        rows.append(f'<tr>{tds}</tr>')
    return f'<table class="cp" style="--cell:{cell}mm">{"".join(rows)}</table>'


# ------------------------------------------------------------------ outros desenhos
def camadas():
    """Corte lateral do chão do aquário: bolo de camadas."""
    g = [f'<rect x="0" y="0" width="360" height="200" rx="6" fill="{C["agua2"]}"/>',
         f'<path d="M0,200 V120 C120,124 240,146 360,152 V200 Z" fill="{C["areia"]}" stroke="{INK}" stroke-width="2"/>',
         f'<path d="M24,200 V168 C120,170 240,178 330,182 V200 Z" fill="{C["terra"]}" stroke="{INK}" stroke-width="2"/>']
    for x, y in ((40, 140), (90, 150), (150, 150), (210, 160), (270, 166), (310, 172), (60, 160), (180, 170)):
        g.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{C["areia2"]}"/>')
    g.append(f'<rect x="0" y="0" width="360" height="200" rx="6" fill="none" stroke="{INK}" stroke-width="4"/>')
    g.append(f'<text x="12" y="22" font-family="Fredoka" font-size="14" font-weight="600" fill="{INK}">atrás</text>'
             f'<text x="348" y="22" text-anchor="end" font-family="Fredoka" font-size="14" font-weight="600" fill="{INK}">frente</text>'
             f'<path d="M16,124 V194 M10,130 l6,-8 6,8 M10,188 l6,8 6,-8" stroke="{INK}" stroke-width="2" fill="none"/><text x="26" y="112" font-family="Fredoka" font-weight="600" font-size="14" fill="{INK}">7 cm</text>'
             f'<path d="M344,156 V194 M338,162 l6,-8 6,8 M338,188 l6,8 6,-8" stroke="{INK}" stroke-width="2" fill="none"/><text x="334" y="144" text-anchor="end" font-family="Fredoka" font-weight="600" font-size="14" fill="{INK}">3 cm</text>')
    return svg(''.join(g), '-4 -4 368 208', 'Corte do chão do aquário: terra fértil embaixo e areia por cima, mais alta atrás')


def lugar(kind):
    """Painéis do 'onde colocar o aquário'."""
    k = INK
    aq = (f'<rect x="{{x}}" y="{{y}}" width="70" height="42" rx="3" fill="{C["agua2"]}" stroke="{k}" stroke-width="2.5"/>'
          f'<path d="M{{x}},{{y2}} h70" stroke="{C["areia2"]}" stroke-width="7"/>')

    def tank(x, y):
        return aq.format(x=x, y=y, y2=y + 38)
    P = {
        'sol': f'<rect x="96" y="8" width="50" height="58" fill="#DFF3FB" stroke="{k}" stroke-width="2.5"/><path d="M121,8 v58 M96,37 h50" stroke="{k}" stroke-width="2"/>'
               f'<circle cx="121" cy="30" r="11" fill="{C["sol"]}"/>' + ''.join(f'<path d="M{100 - i * 3},{40 + i * 12} L{70 - i * 12},{64 + i * 6}" stroke="{C["sol"]}" stroke-width="4" stroke-linecap="round" stroke-dasharray="7 5"/>' for i in range(3))
               + tank(20, 58) + f'<rect x="10" y="100" width="92" height="8" fill="{C["madeira"]}" stroke="{k}" stroke-width="2"/>',
        'bamba': tank(30, 38) + f'<rect x="20" y="80" width="90" height="7" fill="{C["madeira"]}" stroke="{k}" stroke-width="2"/>'
                 f'<path d="M30,87 l-6,40 M100,87 l10,38 M65,87 l-2,40" stroke="{k}" stroke-width="3"/>'
                 f'<path d="M122,60 q6,-6 0,-12 M130,64 q9,-10 0,-22" fill="none" stroke="{C["coral"]}" stroke-width="2.4" stroke-linecap="round"/>',
        'fogao': f'<rect x="92" y="60" width="56" height="64" fill="{C["cinza"]}" stroke="{k}" stroke-width="2.5"/><path d="M102,56 q6,-10 0,-18 q-6,-10 0,-18 M122,56 q6,-10 0,-18 q-6,-10 0,-18" fill="none" stroke="{C["coral"]}" stroke-width="3" stroke-linecap="round"/>'
                 f'<rect x="96" y="56" width="48" height="6" fill="{k}"/>' + tank(12, 38) + f'<rect x="6" y="80" width="84" height="44" fill="{C["madeira"]}" stroke="{k}" stroke-width="2"/>',
        'certo': tank(34, 36) + f'<rect x="22" y="78" width="94" height="46" rx="3" fill="{C["madeira"]}" stroke="{k}" stroke-width="2.5"/><path d="M69,78 v46" stroke="{k}" stroke-width="2"/>'
                 f'<rect x="128" y="96" width="14" height="18" rx="3" fill="#fff" stroke="{k}" stroke-width="2"/><circle cx="133" cy="104" r="1.5" fill="{k}"/><circle cx="137" cy="104" r="1.5" fill="{k}"/>'
                 f'<path d="M104,56 C120,56 124,90 132,96" fill="none" stroke="{k}" stroke-width="2"/>',
    }
    return svg(P[kind], '0 0 150 130', kind)


def termometro(t):
    good = 24 <= t <= 26
    return svg(f'<rect x="4" y="10" width="92" height="56" rx="12" fill="{C["cinza"]}" stroke="{INK}" stroke-width="3"/>'
               f'<rect x="14" y="20" width="72" height="36" rx="6" fill="#EAF7EE" stroke="{INK}" stroke-width="2"/>'
               f'<text x="50" y="48" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="26" fill="{INK}">{t}°</text>',
               '0 0 100 76', f'Termômetro marcando {t} graus')


def tubo(color, label):
    return svg(f'<rect x="14" y="4" width="32" height="112" rx="16" fill="#fff" stroke="{INK}" stroke-width="3"/>'
               f'<rect x="19" y="54" width="22" height="58" rx="11" fill="{color}"/>'
               f'<text x="30" y="136" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="14" fill="{INK}">{label}</text>',
               '0 0 60 142', f'Tubo de teste {label}')


def sos(kind):
    k = INK
    S = {
        'turva': f'<rect x="20" y="16" width="80" height="60" rx="6" fill="#EAEFE9" stroke="{k}" stroke-width="3"/><circle cx="44" cy="40" r="10" fill="#fff" fill-opacity=".8"/><circle cx="70" cy="52" r="13" fill="#fff" fill-opacity=".8"/><circle cx="80" cy="30" r="7" fill="#fff" fill-opacity=".8"/>',
        'fundo': f'<rect x="10" y="10" width="100" height="66" rx="6" fill="{C["agua2"]}" stroke="{k}" stroke-width="3"/><path d="M10,64 h100" stroke="{C["areia2"]}" stroke-width="10"/><g transform="translate(26,34) scale(.34)">{beto(body="#8B96B8", fin="#B9A6AE", mood="doente", tail="doente", uid="s1")}</g>',
        'pontos': f'<g transform="translate(6,10) scale(.55)">{beto(uid="s2")}</g>' + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#fff" stroke="{k}" stroke-width=".8"/>' for x, y in ((56, 36), (66, 40), (74, 34), (62, 32), (80, 38))),
        'quente': f'<g transform="translate(10,6)">' + termometro(30).replace('<svg class="sv" viewBox="0 0 100 76"', '<svg viewBox="0 0 100 76" width="100" height="76"') + '</g>',
        'deitado': f'<path d="M6,74 h108" stroke="{C["areia2"]}" stroke-width="8"/><g transform="translate(100,74) scale(-.62,-.62)">{cereja(face=False)}</g>',
        'filtro': f'<g transform="translate(20,0) scale(.8)">' + aparelho('filtro').replace('<svg class="sv" viewBox="0 0 100 100" role="img" aria-label="filtro">', '').replace('</svg>', '') + f'</g><path d="M78,14 l16,16 M94,14 l-16,16" stroke="{C["coral"]}" stroke-width="4" stroke-linecap="round"/>',
        'vazou': f'<rect x="24" y="8" width="72" height="44" rx="4" fill="{C["agua2"]}" stroke="{k}" stroke-width="3"/><path d="M60,52 C60,60 64,62 64,66" stroke="{C["agua"]}" stroke-width="3"/><ellipse cx="62" cy="74" rx="36" ry="6" fill="{C["agua"]}" fill-opacity=".7"/>',
        'cheiro': f'<path d="M40,70 C30,70 26,56 34,50 C30,38 40,26 52,28 C56,16 74,16 78,28 C92,28 96,44 88,52 C94,62 84,72 74,68" fill="#E7E3D4" stroke="{k}" stroke-width="2.5"/>' + ''.join(f'<path d="M{x},24 q6,-6 0,-12 q-6,-6 0,-12" fill="none" stroke="{C["folha2"]}" stroke-width="2.5" stroke-linecap="round" transform="translate(0,4)"/>' for x in (46, 62, 78)),
    }
    return svg(S[kind], '0 0 120 84', kind)


def trilha(stops):
    """Tabuleiro em S com as etapas (sumário lúdico)."""
    pts = []
    rows = [(60, 1), (190, -1), (320, 1)]
    per = 4
    for i in range(len(stops)):
        r = i // per
        c = i % per
        y, d = rows[min(r, 2)]
        x = 60 + c * 140 if d == 1 else 480 - c * 140
        pts.append((x, y))
    path = f'M{pts[0][0]},{pts[0][1]}'
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if y0 == y1:
            path += f' L{x1},{y1}'
        else:
            cx = 560 if x0 > 300 else -20
            path += f' C{cx},{y0} {cx},{y1} {x1},{y1}'
    g = [f'<path d="{path}" fill="none" stroke="{C["areia2"]}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>',
         f'<path d="{path}" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="2 14" stroke-linecap="round"/>']
    colors = [C['agua'], C['sol'], C['coral'], C['folha'], C['roxo']]
    for i, ((x, y), (num, title, pg)) in enumerate(zip(pts, stops)):
        col = colors[i % len(colors)]
        g.append(f'<circle cx="{x}" cy="{y}" r="31" fill="{col}" stroke="{INK}" stroke-width="3"/>'
                 f'<text x="{x}" y="{y + 9}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="26" fill="{INK}">{num}</text>'
                 f'<text x="{x}" y="{y + 52}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="14" fill="{INK}">{title}</text>'
                 f'<text x="{x}" y="{y + 69}" text-anchor="middle" font-family="Atkinson Hyperlegible Next" font-size="11.5" fill="{INK}">página {pg}</text>')
    return svg(''.join(g), '-10 10 560 420', 'A trilha do aquarista, com as etapas do livro')


def ciclo():
    """O ciclo do aquário em roda: peixe → sujeira → bactérias → comida de planta → plantas."""
    cx, cy, R = 260, 210, 150
    nodes = [(90, 'O Beto come', 'e faz cocô'), (18, 'A sujeira vira', 'amônia'), (-54, 'As Bacterinhas', 'transformam'),
             (-126, 'Vira comida', 'de planta'), (-198, 'As plantas', 'crescem e limpam')]
    g = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{C["agua2"]}" stroke-width="26"/>']
    pos = []
    for ang, a, b in nodes:
        x = cx + R * math.cos(math.radians(ang))
        y = cy - R * math.sin(math.radians(ang))
        pos.append((x, y, a, b))
    for i in range(len(pos)):
        a0 = nodes[i][0] - 20
        a1 = nodes[(i + 1) % len(nodes)][0] + 20
        if a1 > a0:
            a1 -= 360
        x0, y0 = cx + R * math.cos(math.radians(a0)), cy - R * math.sin(math.radians(a0))
        x1, y1 = cx + R * math.cos(math.radians(a1)), cy - R * math.sin(math.radians(a1))
        g.append(f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{C["agua"]}" stroke-width="5" marker-end="url(#seta)"/>')
    g.insert(0, f'<defs><marker id="seta" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{C["agua"]}"/></marker></defs>')
    art = [f'<g transform="translate(-44,-26) scale(.44)">{beto(uid="ci")}</g>',
           nuvem('#B8A6D9', -24, -24, .7),
           bacterinha(C['laranja'], -36, -22, .55) + bacterinha(C['azul'], -4, 2, .45),
           nuvem('#8FD19E', -18, -30, .7, 'feliz'),
           f'<g transform="translate(0,20)">{planta_caule(-10, 0, 56, leaves=6)}{planta_caule(10, 0, 44, color=C["folha3"], leaves=5, flip=-1)}</g>']
    for (x, y, a, b), a_svg in zip(pos, art):
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="54" fill="#fff" stroke="{INK}" stroke-width="3"/>')
        g.append(f'<g transform="translate({x:.1f},{y:.1f})">{a_svg}</g>')
        ty = y + 72 if y > cy - 10 else y - 76
        g.append(f'<text x="{x:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="16" fill="{INK}">{a}</text>'
                 f'<text x="{x:.1f}" y="{ty + 18:.1f}" text-anchor="middle" font-family="Fredoka" font-size="15" fill="{INK}">{b}</text>')
    g.append(f'<g transform="translate({cx - 34},{cy - 20}) scale(.52)">{cereja()}</g>'
             f'<text x="{cx}" y="{cy + 42}" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="14" fill="{INK}">e os camarões</text>'
             f'<text x="{cx}" y="{cy + 58}" text-anchor="middle" font-family="Fredoka" font-size="13" fill="{INK}">limpam as sobras</text>')
    return svg(''.join(g), '20 -30 480 490', 'O ciclo do aquário')


def mapa():
    """Mapa do aquário, visto de cima, para colorir, com números das plantas."""
    k = INK
    t = lambda x, y, n: (f'<circle cx="{x}" cy="{y}" r="11" fill="#fff" stroke="{k}" stroke-width="2"/>'
                         f'<text x="{x}" y="{y + 5.5}" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="15" fill="{k}">{n}</text>')
    zone = lambda d: f'<path d="{d}" fill="#fff" stroke="{k}" stroke-width="2.2"/>'
    g = [f'<rect x="0" y="0" width="400" height="200" rx="8" fill="#fff" stroke="{k}" stroke-width="4"/>',
         # 7 rotala: fundo esquerdo
         zone('M8,8 H150 C150,26 138,36 110,36 C80,36 50,40 8,44 Z'), t(40, 24, 7),
         # 5 gramado: frente esquerda
         zone('M8,150 C40,140 90,146 120,160 C130,172 128,186 120,192 H8 Z'), t(40, 172, 5),
         # 4 criptocorynes: meio direito
         zone('M246,56 C270,44 316,46 330,62 C338,78 322,94 292,96 C262,96 244,86 240,72 C240,64 242,60 246,56 Z'), t(288, 72, 4),
         # 8 flutuantes: canto direito, na superfície
         f'<circle cx="352" cy="138" r="34" fill="#fff" stroke="{k}" stroke-width="2.2" stroke-dasharray="7 5"/>', t(352, 138, 8),
         # tronco com musgo (6) e samambaia (2)
         f'<path d="M34,52 C80,64 120,82 150,100 C172,112 194,118 214,120" fill="none" stroke="{k}" stroke-width="14" stroke-linecap="round"/>',
         f'<path d="M34,52 C80,64 120,82 150,100 C172,112 194,118 214,120" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round"/>',
         t(98, 74, 6),
         zone('M52,46 C62,30 90,32 96,46 C98,56 84,60 70,60 C58,60 50,54 52,46 Z'), t(74, 48, 2),
         # pedras, anúbia (1) e bucephalandra (3)
         f'<ellipse cx="150" cy="128" rx="34" ry="22" fill="#fff" stroke="{k}" stroke-width="2.2"/>', t(150, 128, 1),
         f'<ellipse cx="104" cy="120" rx="15" ry="11" fill="#fff" stroke="{k}" stroke-width="2"/>',
         f'<ellipse cx="208" cy="148" rx="17" ry="12" fill="#fff" stroke="{k}" stroke-width="2"/>',
         zone('M166,158 C176,150 192,152 196,162 C194,172 178,176 168,170 C164,166 164,162 166,158 Z'), t(181, 163, 3),
         # aparelhos
         f'<rect x="12" y="12" width="28" height="10" rx="4" fill="#fff" stroke="{k}" stroke-width="1.6"/>',
         f'<text x="286" y="160" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="12" fill="{k}">piscina</text>'
         f'<text x="286" y="174" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="12" fill="{k}">do Beto</text>',
         f'<text x="200" y="224" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="15" fill="{k}">frente do aquário (onde você fica)</text>']
    return svg(''.join(g), '-6 -6 412 238', 'Mapa do aquário visto de cima, para colorir')


def selo(icon_inner, color):
    return svg(f'<circle cx="50" cy="50" r="44" fill="#fff" stroke="{INK}" stroke-width="3"/>'
               f'<circle cx="50" cy="50" r="36" fill="none" stroke="{color}" stroke-width="5" stroke-dasharray="3 5"/>'
               f'<g transform="translate(26,26) scale(1.2)">{icon_inner}</g>', '0 0 100 100', 'Selo de conquista')


def regua(which='ambos'):
    """Régua em milímetros de verdade, com o Beto (7 cm) e a Cereja (3 cm) em tamanho real."""
    L = 90
    g = [f'<rect x="0" y="34" width="{L}" height="14" rx="1.5" fill="{C["sol"]}" stroke="{INK}" stroke-width=".5"/>']
    for mm in range(0, 86):
        h = 5 if mm % 10 == 0 else (3.5 if mm % 5 == 0 else 2)
        g.append(f'<path d="M{2 + mm},34 v{h}" stroke="{INK}" stroke-width=".25"/>')
        if mm % 10 == 0:
            g.append(f'<text x="{2 + mm}" y="45.5" text-anchor="middle" font-family="Fredoka" font-weight="600" font-size="3.6" fill="{INK}">{mm // 10}</text>')
    g.append(f'<text x="{L - 2}" y="45.5" text-anchor="end" font-family="Fredoka" font-size="3" fill="{INK}">cm</text>')
    if which in ('ambos', 'beto'):
        # o betta do desenho mede ~150 unidades da ponta da cauda ao focinho (x 22 a 172)
        # versão plakat: da ponta da cauda (x 48) ao focinho (x 172) são 124 unidades
        s = 70 / 124
        g.append(f'<g transform="translate({2 - 48 * s},{33 - 76 * s}) scale({s})">{beto(uid="regua", tail="plakat")}</g>')
    if which == 'cereja':
        s = 30 / 112
        g.append(f'<g transform="translate({2 - 4 * s},{33 - 84 * s}) scale({s})">{cereja()}</g>')
        g.append(f'<circle cx="52" cy="30" r="1" fill="{C["coral"]}" stroke="{INK}" stroke-width=".2"/>'
                 f'<path d="M52,28.5 C54,22 60,18 64,18" fill="none" stroke="{INK}" stroke-width=".3"/>'
                 f'<text x="65" y="19" font-family="Fredoka" font-weight="600" font-size="3.4" fill="{INK}">um filhote: 2 mm</text>')
    top = 4 if which != 'cereja' else 11
    return (f'<svg class="sv" viewBox="0 {top} {L} {50 - top}" style="width:{L}mm; height:{50 - top}mm; flex:none" role="img" '
            f'aria-label="Régua com os bichos em tamanho real">{"".join(g)}</svg>')
