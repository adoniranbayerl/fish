#!/usr/bin/env python3
"""Gera o livro infantil: src/criancas/pages/*.html e head.html.

Mesmo conteúdo do guia (etapas, números e datas), escrito para leitores
de 6 a 8 anos, com personagens, experiências e passatempos.
"""
import datetime as dt
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import art  # noqa: E402
from art import C, icon, svg, beto, cereja, bacterinha, nuvem  # noqa: E402

PAGES = os.path.join(HERE, 'pages')
ONDA = ('<svg class="onda" viewBox="0 0 297 15" preserveAspectRatio="none" aria-hidden="true">'
        '<path d="M0,6 C18,1 34,9 52,5 S88,1 106,5 S142,10 160,5 S196,1 214,5 S250,10 268,5 S290,2 297,5 V15 H0 Z" style="fill:var(--cor)" fill-opacity=".35"/>'
        '<path d="M0,9 C20,5 38,12 58,8 S96,4 116,8 S154,13 174,8 S212,4 232,8 S270,12 297,8 V15 H0 Z" style="fill:var(--cor)"/></svg>')


def page(pid, cor, body, chip=None, chip_icon='jogo', cls=''):
    ch = f'<p class="chip">{icon(chip_icon)}{chip}</p>' if chip else ''
    return (f'<section class="page recto k {cls}" id="{pid}" style="--cor:var(--{cor})">{ONDA}<div class="folio">0</div>'
            f'<div class="frame">{ch}{body}</div></section>')


def titulo(t, lead=None, sub=None):
    s = f'<small>{sub}</small>' if sub else ''
    lp = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<h2 class="t">{t}{s}</h2>{lp}'


def box(kind, label, html, ic=None):
    ic = ic or {'adulto': 'adulto', 'sabia': 'sabia', 'dica': 'dica', 'exp': 'experiencia', 'jogo': 'jogo'}[kind]
    return f'<div class="box {kind}"><p class="bh">{icon(ic, "8mm")}{label}</p>{html}</div>'


def foto(src, h, pos=None, cap=None):
    st = f' style="object-position:{pos}"' if pos else ''
    c = f'<p class="cap">{cap} <span class="cr" data-cr="img/{src}"></span></p>' if cap is not None else f'<p class="cap"><span class="cr" data-cr="img/{src}"></span></p>'
    return f'<div><div class="foto" style="height:{h}mm"><img src="img/{src}" alt=""{st}></div>{c}</div>'


def fala(quem_svg, html, w='38mm'):
    return f'<div class="fala"><div class="quem" style="width:{w}">{quem_svg}</div><div class="balao">{html}</div></div>'


def cols(*parts, t='1fr 1fr', gap=8, cls='', style=''):
    inner = ''.join(f'<div class="col">{x}</div>' for x in parts)
    return f'<div class="cols {cls}" style="grid-template-columns:{t}; gap:{gap}mm; {style}">{inner}</div>'


def pts(n):
    return '<span class="pts">' + ''.join('<i class="on"></i>' if i < n else '<i></i>' for i in range(5)) + '</span>'


BETO = lambda **kw: art.beto_svg(**kw)
CEREJA = lambda **kw: art.cereja_svg(**kw)


# =================================================================== páginas
def capa():
    k = art.INK
    g = [f'<path d="M-260,296 C-180,286 -80,302 0,300 C80,280 150,300 220,292 C300,282 360,300 420,290 V380 H-260 Z" fill="{C["areia"]}" stroke="{k}" stroke-width="3"/>',
         art.tufo(-200, 296, 6, 40), art.tufo(-60, 294, 5, 30), art.pedra(-140, 300, .8), art.planta_caule(30, 300, 190, leaves=10), art.planta_caule(58, 298, 150, color=C['folha3'], leaves=8, flip=-1),
         art.planta_caule(390, 292, 170, leaves=9, flip=-1), art.planta_caule(362, 294, 120, color=C['folha3'], leaves=7),
         art.pedra(96, 300, 1.4), art.pedra(290, 294, 1.0, fill='#7E8C96'), art.anubia(130, 262, 1.3),
         art.tufo(230, 294, 7, 44), art.tufo(330, 292, 5, 34),
         f'<g transform="translate(92,118) scale(1.28)">{beto(uid="capa", bubbles=0)}</g>',
         art.bolhas(342, 150, 4),
         art.cereja(s=.75, x=170, y=240, flip=True), art.cereja(s=.45, x=40, y=238),
         art.bacterinha(C['laranja'], 300, 216, .55), art.bacterinha(C['azul'], 250, 240, .45)]
    body = (f'<div class="ct"><p class="kicker">Vinte litros de mundo · edição para crianças</p>'
            f'<h1>Meu primeiro<br>aquário</h1><p class="sub">Um livro para montar, esperar,<br>cuidar e brincar</p></div>'
            f'<div class="age">6 a 8<small>anos</small></div>'
            '<div class="polaroid" style="right:20mm; top:12mm; width:62mm; height:52mm; transform:rotate(4deg)"><img src="img/capa-betta.jpg" alt="Um betta de verdade" style="object-position:40% 60%"><p>Um betta de verdade!</p></div>'
            f'<div class="arte">{svg("".join(g), "-260 100 680 280", "O Beto, os camarões e as Bacterinhas num aquário plantado")}</div>'
            '<div style="position:absolute; left:18mm; width:118mm; bottom:18mm; z-index:2; background:#fff; border:2.4pt solid var(--ink); border-radius:6mm; padding:4mm 6mm; '
            'font:600 16pt/1 var(--display); color:var(--ink); display:flex; align-items:flex-end; gap:3mm">Este livro é de:<span class="linha" style="flex:1; min-width:0"></span></div>')
    return f'<section class="page recto k capa nochrome" id="capa" style="--cor:var(--agua)"><div class="folio">0</div>{body}</section>'


def meu_livro():
    legend = [('adulto', 'Faça com um adulto', 'Tarefas com tomada, água pesada, tesoura ou líquidos que não são de brincar.'),
              ('sabia', 'Você sabia?', 'Curiosidades para contar para todo mundo.'),
              ('dica', 'Dica do Beto', 'Conselhos de quem mora no aquário.'),
              ('experiencia', 'Experiência', 'Ciência de verdade, para fazer em casa.'),
              ('jogo', 'Jogo', 'Passatempos, desafios e desenhos.'),
              ('lapis', 'Escreva ou desenhe', 'Este livro é seu: pode escrever nele!')]
    items = ''.join(f'<div class="row" style="gap:3mm; align-items:flex-start">{icon(i, "10mm")}<div><b style="font-family:var(--display); font-weight:600">{a}</b><p class="small">{b}</p></div></div>' for i, a, b in legend)
    left = ('<p class="lead">Meu nome é <span class="linha" style="min-width:100mm"></span></p>'
            '<p class="lead">Tenho <span class="linha" style="min-width:18mm"></span> anos.</p>'
            '<p class="lead">Meu aquário começa no dia <b>1º de janeiro de 2027</b>.</p>'
            '<p class="lead">Quem me ajuda é <span class="linha" style="min-width:70mm"></span>.</p>'
            + fala(BETO(), '<p>Oi! Eu sou o <b>Beto</b>. Vou te ensinar tudo sobre a minha casa nova.</p>', '40mm'))
    body = (titulo('Tudo sobre mim') +
            cols(left, '<div class="desenho" style="height:78mm">Desenhe você aqui</div>', t='1fr 88mm') +
            f'<h3 class="h">Os sinais deste livro</h3><div class="g3" style="gap:3mm 6mm">{items}</div>'
            '<p class="tiny" style="margin-top:auto">Adultos: a página {{pg:adultos}} foi escrita para vocês.</p>')
    return page('meu-livro', 'sol', body)


def combinado():
    crianca = ('<div class="box jogo" style="height:100%"><p class="h">Eu, <span class="linha" style="min-width:70mm"></span>, prometo:</p>'
               '<ul class="bol check" style="--cor:#fff">'
               '<li>lavar as mãos antes e depois de mexer no aquário;</li>'
               '<li>dar só a comida certa, na hora certa;</li>'
               '<li>olhar os bichinhos todos os dias;</li>'
               '<li>chamar um adulto quando alguma coisa parecer estranha;</li>'
               '<li>nunca mexer nos fios, na tomada nem nos potinhos de teste;</li>'
               '<li>nunca bater no vidro.</li></ul>'
               '<p style="margin-top:4mm">Assinatura: <span class="linha" style="min-width:80mm"></span></p></div>')
    adulto = ('<div class="box adulto" style="height:100%"><p class="h">E eu, adulto, <span class="linha" style="min-width:55mm"></span>, prometo:</p>'
              '<ul class="bol check" style="--cor:#fff">'
              '<li>cuidar da parte elétrica, dos testes e dos remédios;</li>'
              '<li>ajudar na troca de água toda semana;</li>'
              '<li>responder às perguntas com paciência;</li>'
              '<li>garantir que os bichos nunca fiquem sem cuidado, nem nas férias.</li></ul>'
              '<p style="margin-top:4mm">Assinatura: <span class="linha" style="min-width:80mm"></span></p></div>')
    body = (titulo('O combinado', 'Cuidar de bichos é coisa séria — e muito divertida. Antes de começar, vamos fazer um combinado?') +
            cols(crianca, adulto, cls='fill') +
            fala(BETO(), '<p>Combinado é combinado! Agora a gente é um time.</p>', '34mm') + '<p class="lead center" style="max-width:none">Data do combinado: <span class="linha" style="min-width:16mm"></span> / <span class="linha" style="min-width:16mm"></span> / <span class="linha" style="min-width:24mm"></span></p>')
    return page('combinado', 'coral', body)


def turma():
    cards = [
        (BETO(), 'Beto, o betta', 'Um peixe colorido e curioso que respira ar. O rei da superfície. (O seu pode ter outro nome!)'),
        (CEREJA(), 'Cereja e as irmãs', 'Camarõezinhos vermelhos que passam o dia limpando o aquário.'),
        (svg(bacterinha(C['laranja'], 0, 0, .9) + bacterinha(C['azul'], 70, 24, .8), '-10 8 150 70'), 'As Bacterinhas', 'Tão pequenas que ninguém vê. Elas limpam a água dia e noite.'),
        (svg(art.planta_caule(30, 96, 88) + art.anubia(78, 96, 1.2) + art.tufo(120, 96, 5, 40), '0 0 150 100'), 'A turma verde', 'As plantas: dão casa, sombra, comida e ar para todo mundo.'),
        (svg(f'<circle cx="60" cy="30" r="20" fill="{C["sol"]}" stroke="{art.INK}" stroke-width="3"/><path d="M26,98 C26,68 40,56 60,56 C80,56 94,68 94,98 Z" fill="{C["agua"]}" stroke="{art.INK}" stroke-width="3"/>'
             f'<circle cx="53" cy="28" r="2.6" fill="{art.INK}"/><circle cx="67" cy="28" r="2.6" fill="{art.INK}"/><path d="M52,37 q8,6 16,0" fill="none" stroke="{art.INK}" stroke-width="2.4" stroke-linecap="round"/>', '0 0 120 100'),
         'Você, o aquarista', 'Quem cuida de aquário se chama aquarista. A partir de hoje, é você!'),
        (svg(f'<circle cx="60" cy="24" r="17" fill="{C["coral"]}" stroke="{art.INK}" stroke-width="3"/><path d="M22,98 C22,62 38,46 60,46 C82,46 98,62 98,98 Z" fill="{C["coral"]}" stroke="{art.INK}" stroke-width="3"/>'
             f'<circle cx="54" cy="22" r="2.4" fill="{art.INK}"/><circle cx="66" cy="22" r="2.4" fill="{art.INK}"/><path d="M53,30 q7,5 14,0" fill="none" stroke="{art.INK}" stroke-width="2.2" stroke-linecap="round"/>', '0 0 120 100'),
         'O adulto ajudante', 'Cuida das tomadas, dos testes e da água pesada. E ajuda você em tudo.'),
    ]
    cs = ''.join(f'<div class="card"><div class="pic" style="height:20mm">{s}</div><b>{n}</b><p>{t}</p></div>' for s, n, t in cards)
    fotos = (foto('capa-betta.jpg', 36, '40% 60%', 'O Beto de verdade.') + foto('neo-cereja.jpg', 36, None, 'A Cereja de verdade.'))
    body = (titulo('Conheça a turma', 'Estes são os moradores do aquário — e quem cuida deles.') +
            cols(f'<div class="g3" style="gap:4mm">{cs}</div>', fotos, t='1fr 66mm', gap=6) +
            box('sabia', 'Você sabia?', '<p>Um peixe, alguns camarões e muitas plantas cabem em <b>20 litros</b>: é como 10 garrafas de refrigerante de 2 litros.</p>'))
    return page('turma', 'agua', body)


def mundo():
    right = (foto('diario/mes-07.jpg', 62, None, 'Um aquário plantado é um mundo inteiro.') +
             box('sabia', 'Você sabia?', '<p>Uma casa onde plantas, bichos e bactérias vivem juntos e cuidam uns dos outros se chama <b>ecossistema</b>. Uma floresta é um ecossistema. Um lago também. E o seu aquário!</p>'))
    body = (titulo('Um aquário é um mundo pequeno', 'Dentro do vidro, cada morador ajuda o outro. É uma roda que não para de girar.') +
            cols(f'<div style="width:128mm; margin:0 auto">{art.ciclo()}</div>', right, t='1fr 118mm'))
    return page('mundo', 'folha', body)


def trilha():
    stops = [(1, 'Ferramentas', '{{pg:e1-caixa}}'), (2, 'O lugar', '{{pg:e2-lugar}}'), (3, 'O chão', '{{pg:e3-chao}}'),
             (4, 'A paisagem', '{{pg:e4-paisagem}}'), (5, 'As plantas', '{{pg:e5-plantas}}'), (6, 'A espera', '{{pg:e6-bacterinhas}}'),
             (7, 'Os camarões', '{{pg:e7-cerejinhas}}'), (8, 'O Beto', '{{pg:e8-beto}}'), (9, 'As tarefas', '{{pg:e9-tarefas}}'),
             ('+', 'Jogos', '{{pg:cacapalavras}}')]
    tl = [('1º jan', 'Montar o aquário', 'sol'), ('6 semanas', 'Esperar as Bacterinhas', 'roxo2'), ('12 fev', 'Chegam os camarões', 'coral'), ('12 mar', 'Chega o Beto', 'agua')]
    tlh = ''.join(f'<div class="row" style="gap:3mm"><div style="width:30mm; flex:none; height:10mm; border:2pt solid var(--ink); border-radius:5mm; background:var(--{c}); font:600 13pt/9.6mm var(--display); text-align:center">{d}</div><p class="small">{t}</p></div>' for d, t, c in tl)
    right = ('<h3 class="h">Quanto tempo leva?</h3>' + f'<div style="display:flex; flex-direction:column; gap:2.4mm">{tlh}</div>'
             + box('dica', 'Dica do Beto', '<p>Primeiro as plantas, depois as Bacterinhas, depois os camarões — e eu chego por último. Cada um na sua vez!</p>'))
    body = (titulo('A trilha do aquarista', 'O aquário se monta em 9 etapas, uma depois da outra. Siga a trilha!') +
            cols(art.trilha(stops, per=5) + '<div class="g4" style="gap:3mm">' + foto('diario/mes-01.jpg', 30, None, '1. Pedras e tronco.') + foto('plant-aquario.jpg', 30, None, '2. As plantas.') + foto('neo-cereja.jpg', 30, None, '3. Os camarões.') + foto('capa-betta.jpg', 30, '40% 60%', '4. O Beto!') + '</div>', right, t='1fr 76mm'))
    return page('trilha', 'sol', body)


def regras():
    rs = [('maos', 'Lave as mãos <b>antes e depois</b> de mexer no aquário. E nunca ponha a mão molhada na boca.'),
          ('adulto', 'Só mexa na água com um <b>adulto por perto</b>.'),
          ('atencao', 'Tomada e água não se misturam: os <b>fios são do adulto</b>. Antes de pôr a mão na água, ele desliga tudo.'),
          ('nao', '<b>Nada de sabão</b>, perfume ou creme nas mãos perto do aquário.'),
          ('coracao', '<b>Não bata no vidro</b>: para o peixe, é como um trovão.'),
          ('dica', 'Comida só <b>na medida</b>: 2 ou 3 grãozinhos.'),
          ('experiencia', 'Potinhos de teste, remédios e o condicionador são <b>só do adulto</b>. Eles podem ser venenosos.'),
          ('ok', '<b>Nunca solte</b> peixe, camarão ou planta em rio, lago ou ralo.')]
    items = ''.join(f'<li style="break-inside:avoid"><div class="row" style="gap:3mm">{icon(i, "10mm")}<p>{t}</p></div></li>' for i, t in rs)
    body = (titulo('Regras de ouro', 'Oito regras para um aquário feliz e um aquarista seguro. Leia com um adulto.') +
            f'<ol class="num" style="--cor:var(--sol); display:grid; grid-auto-flow:column; grid-template-rows:repeat(4,auto); grid-template-columns:1fr 1fr; gap:3mm 10mm; font-size:15pt; line-height:20pt">{items}</ol>' +
            fala(BETO(), '<p>Se todo mundo seguir as regras, eu vivo muitos anos com você!</p>'))
    return page('regras', 'coral', body, 'Antes de tudo', 'atencao')


def e1_caixa():
    it = [('filtro', 'Filtro', 'A esponja que limpa a água. Dentro dela moram as Bacterinhas.'),
          ('compressor', 'Compressor', 'Sopra ar pela mangueira e faz o filtro funcionar. Fica fora do aquário.'),
          ('aquecedor', 'Aquecedor', 'O cobertor do aquário: deixa a água morninha, do jeito que o Beto gosta.'),
          ('termometro', 'Termômetro', 'Mostra se a água está quente ou fria. O número bom é 24, 25 ou 26.'),
          ('luz', 'Luz', 'O sol das plantas. Um relógio acende e apaga sozinho: 6 a 8 horas por dia.'),
          ('tampa', 'Tampa', 'O telhado. O Beto pula! Ela cobre a frente; atrás ficam as plantas da borda.'),
          ('condicionador', 'Condicionador', 'Tira o cloro da água da torneira, que faz mal aos bichos. Só o adulto usa.'),
          ('testes', 'Testes', 'Os tubinhos de detetive: mostram se a água está boa. Só o adulto pinga.')]
    cs = ''.join(f'<div class="card" style="padding:2.4mm 3mm 3mm"><div class="pic" style="height:21mm">{art.aparelho(a)}</div><b>{n}</b><p style="font-size:11pt; line-height:14.5pt">{t}</p></div>' for a, n, t in it)
    right = (foto('equip-nano.jpg', 74, '50% 60%', 'Um aquário pequeno, com luz e tampa.') +
             box('adulto', 'Com um adulto', '<p class="small">O filtro, o aquecedor e a luz vão na tomada. <b>Quem liga, desliga e mexe nos fios é sempre o adulto.</b></p>'))
    body = titulo('A caixa de ferramentas', 'Oito coisas fazem o aquário funcionar. Vamos conhecer cada uma?') + \
        cols(f'<div class="g4" style="gap:3.5mm">{cs}</div>', right, t='1fr 64mm', gap=6)
    return page('e1-caixa', 'agua', body, 'Etapa 1 · Ferramentas', 'lapis')


LIGUE = [('aquecedor', 'deixa a água morninha'), ('tampa', 'não deixa o Beto pular para fora'), ('filtro', 'limpa a água'),
         ('termometro', 'mostra se a água está quente ou fria'), ('luz', 'é o sol das plantas')]
LIGUE_DIR = [4, 2, 0, 3, 1]   # ordem embaralhada das frases


def e1_ligue():
    left = ''.join(f'<div class="row" style="height:23mm; justify-content:space-between"><div style="width:21mm">{art.aparelho(a)}</div><span class="circ"></span></div>' for a, _ in LIGUE)
    right = ''.join(f'<div class="row" style="height:23mm"><span class="circ"></span><p style="font-size:14pt">{LIGUE[i][1]}</p></div>' for i in LIGUE_DIR)
    litros = ''.join('<span style="display:inline-block; width:7.2mm; height:11mm; margin:0 1.6mm 1.6mm 0; border:1.6pt solid var(--ink); border-radius:1.6mm 1.6mm 2.4mm 2.4mm; background:#fff"></span>' for _ in range(20))
    jogo = (f'<div class="box jogo" style="display:grid; grid-template-columns:40mm 1fr; gap:14mm">'
            f'<div>{left}</div><div>{right}</div></div>')
    contas = ('<h3 class="h">As contas do aquário</h3>'
              '<p>Nosso aquário tem <b>40 cm</b> de comprimento, <b>20 cm</b> de largura e <b>25 cm</b> de altura. Nele cabem <b>20 litros</b>. '
              'Mas areia, pedras e o espaço de ar em cima ocupam lugar: sobram uns <b>13 litros</b> de água. Cheio, ele pesa <b>28 quilos</b>, quase o peso de uma criança de 8 anos! '
              'Por isso quem carrega é o adulto.</p>'
              f'<div class="box jogo"><p class="bh">{icon("lapis", "8mm")}Cada potinho é 1 litro. Pinte de azul os 13 litros de água.</p><div style="width:100mm">{litros}</div></div>')
    body = (titulo('Jogo: ligue cada coisa ao que ela faz', 'Faça uma linha do círculo da esquerda até o círculo da direita.') +
            cols(jogo, contas, t='1fr 118mm'))
    return page('e1-ligue', 'agua', body, 'Etapa 1 · Ferramentas', 'jogo')


def e2_lugar():
    ps = [('A', 'sol', 'Na janela, com sol batendo'), ('B', 'bamba', 'Numa mesinha bamba'),
          ('C', 'certo', 'Num móvel firme, longe da janela, perto da tomada'), ('D', 'fogao', 'Ao lado do fogão')]
    alto = lambda k: art.lugar(k).replace('class="sv"', 'class="sv" style="height:100%; width:auto"')
    cs = ''.join(f'<div class="card"><div class="row" style="justify-content:space-between"><b style="font-size:20pt">{l}</b><span class="circ" style="width:11mm; height:11mm"></span></div>'
                 f'<div style="height:40mm; display:flex; justify-content:center">{alto(k)}</div><p class="small">{t}</p></div>' for l, k, t in ps)
    body = (titulo('Onde o aquário vai morar?', 'Qual destes lugares é o melhor? Pinte o círculo do lugar certo.') +
            f'<div class="g4">{cs}</div>' +
            cols(box('dica', 'Limpar sem sabão', '<p class="small">O vidro se lava <b>só com água</b>. Sabão, detergente e álcool deixam restinhos que fazem mal aos bichos.</p>') +
                 box('exp', 'O teste do vazamento', '<p class="small">O adulto enche o aquário e vocês esperam <b>um dia inteiro</b>. Depois, passem papel nos cantinhos do vidro. Está sequinho? Oba, não vaza!</p>'),
                 foto('local-movel.jpg', 50, '15% 70%', 'Um aquário pequeno numa casa de verdade.'), t='1fr 96mm', gap=6))
    return page('e2-lugar', 'coral', body, 'Etapa 2 · O lugar', 'lapis')


def e3_chao():
    left = (f'<div>{art.camadas()}</div>'
            '<div class="row" style="justify-content:center; gap:10mm"><span class="row" style="gap:2mm"><span class="circ" style="background:#8A5A36"></span> terra fértil</span>'
            '<span class="row" style="gap:2mm"><span class="circ" style="background:#F4E3C1"></span> areia</span></div>'
            + foto('subs-seixos.jpg', 34, None, 'Pedrinhas de rio: lavadas, também servem de chão.'))
    right = ('<ol class="num" style="--cor:var(--sol)">'
             '<li>Lave a areia num balde, mexendo e trocando a água até ela sair limpinha. <b>Essa parte você pode fazer!</b></li>'
             '<li>O adulto espalha a terra fértil só onde vão ficar as plantas.</li>'
             '<li>Cubram tudo com areia: <b>mais alta atrás</b> e <b>mais baixa na frente</b>, como uma rampa. Assim o aquário parece mais fundo, como uma paisagem de verdade.</li></ol>' +
             box('sabia', 'Você sabia?', '<p class="small">Cada grão de areia é a casa de muitas Bacterinhas. O chão também ajuda a limpar a água!</p>') +
             box('jogo', 'Conta rápida', '<p class="small">Vamos usar <b>5 quilos</b> de areia: é o peso de 5 pacotes de açúcar de 1 quilo.</p>'))
    body = (titulo('O chão é um bolo de camadas', 'Embaixo vai a terra fértil: é o recheio que alimenta as raízes. Em cima vai a areia: é a cobertura.') +
            cols(left, right, t='118mm 1fr'))
    return page('e3-chao', 'sol', body, 'Etapa 3 · O chão', 'lapis')


def mini(kind):
    k = art.INK
    if kind == 'meio':
        inner = art.pedra(166, 190, 1.0)
    elif kind == 'lado':
        inner = art.pedra(236, 190, 1.0) + art.pedra(150, 196, .5)
    else:
        inner = (f'<path d="M40,196 C90,110 150,70 230,48" stroke="{k}" stroke-width="9" fill="none" stroke-linecap="round"/>'
                 f'<path d="M40,196 C90,110 150,70 230,48" stroke="{C["madeira"]}" stroke-width="5" fill="none" stroke-linecap="round"/>'
                 + art.pedra(96, 196, 1.2) + art.planta_caule(30, 200, 150) + art.pedra(210, 200, .5))
    return svg(art.aquario(400, 240, inner=inner), '-4 -4 408 248')


def e4_paisagem():
    tips = [('meio', 'nao', 'A pedra grande <b>bem no meio</b> fica sem graça.'),
            ('lado', 'ok', 'Um pouco <b>para o lado</b> fica mais bonito.'),
            ('montanha', 'ok', 'Faça uma <b>montanha</b>: alto de um lado, baixinho do outro.')]
    cs = ''.join(f'<div><div style="position:relative">{mini(m)}<div style="position:absolute; right:-2mm; top:-3mm">{icon(i, "9mm")}</div></div><p class="small" style="margin-top:1.2mm; font-size:11pt; line-height:14pt">{t}</p></div>' for m, i, t in tips)
    left = (foto('diario/mes-01.jpg', 40, '50% 60%', 'Pedras e tronco montados, antes das plantas.') + f'<div class="g3" style="gap:4mm">{cs}</div>')
    right = ('<h3 class="h">Desenhe a sua paisagem</h3>'
             f'<div>{svg(art.aquario(400, 170, water=False), "-4 -4 408 178", "Aquário vazio para desenhar")}</div>' +
             box('dica', 'Dica do Beto', '<p class="small">Deixe um espaço livre na frente: é a minha <b>piscina</b>! E faça frestinhas e cavernas: são o esconderijo dos camarões.</p>') +
             box('adulto', 'Com um adulto', '<p class="small">O tronco é fervido na panela antes de ir para o aquário. Isso limpa e ajuda ele a afundar. Panela quente é trabalho do adulto.</p>'))
    body = (titulo('Pedras e troncos: a paisagem', 'Antes das plantas, montamos as pedras e o tronco. Eles são os ossos da paisagem.') +
            cols(left, right))
    return page('e4-paisagem', 'folha', body, 'Etapa 4 · A paisagem', 'lapis')


def exp_pedra():
    k = art.INK
    exp_svg = svg(art.pedra(40, 150, 2.2) +
                  ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{k}" stroke-width="2"/>' for x, y, r in ((96, 68, 5), (112, 58, 4), (86, 54, 3.5), (120, 76, 3), (104, 44, 3)))
                  + f'<path d="M150,6 h24 v10 h-6 v34 l-6,10 l-6,-10 v-34 h-6 Z" fill="{C["agua2"]}" stroke="{k}" stroke-width="2.5" stroke-linejoin="round"/>'
                  + f'<path d="M162,64 C166,70 168,73 168,76 C168,79 165,81 162,81 C159,81 156,79 156,76 C156,73 158,70 162,64 Z" fill="{C["agua"]}"/>',
                  '0 0 200 160', 'Vinagre pingando numa pedra que faz bolhinhas')
    left = (f'<div class="g2" style="grid-template-columns:1fr 50mm; align-items:center"><div>'
            '<h3 class="h">Você vai precisar de</h3><ul class="bol" style="--cor:var(--folha)"><li>pedras secas</li><li>vinagre</li><li>um conta-gotas ou uma colher</li><li>um adulto!</li></ul>'
            f'</div><div>{exp_svg}</div></div>'
            '<ol class="num" style="--cor:var(--folha)">'
            '<li>Com um adulto, pingue umas gotas de vinagre na pedra.</li>'
            '<li>Olhe bem de pertinho e escute.</li>'
            '<li>Fez bolhinhas e um chiadinho? Essa pedra fica <b>fora</b> do aquário.</li>'
            '<li>Nada aconteceu? <b>Pedra aprovada!</b></li></ol>')
    right = ('<table class="tab" style="--cor:var(--folha2)"><tr><th>Pedra</th><th>Fez bolhinhas?</th><th>Aprovada?</th></tr>'
             + ''.join(f'<tr><td>Pedra {i}</td><td>sim <span class="circ" style="width:6mm;height:6mm"></span> &nbsp; não <span class="circ" style="width:6mm;height:6mm"></span></td><td>sim <span class="circ" style="width:6mm;height:6mm"></span> &nbsp; não <span class="circ" style="width:6mm;height:6mm"></span></td></tr>' for i in (1, 2, 3)) +
             '</table>' +
             cols(foto('hard2-seixos.jpg', 40, None, 'Pedras de rio: teste antes de usar.'),
                  box('sabia', 'Por que borbulha?', '<p class="small">O vinagre é um <b>ácido</b>. Quando encontra o <b>calcário</b> da pedra, os dois reagem e soltam um gás: as bolhinhas!</p>'), gap=4) +
             box('exp', 'Teste da meia-calça', '<p class="small">Passe uma meia-calça velha na pedra e no tronco. Enroscou? Tem uma ponta que pode rasgar a nadadeira do Beto.</p>'))
    body = (titulo('A pedra que faz bolhinhas', 'Algumas pedras mudam a água do aquário e deixam ela “dura”. Vamos descobrir quais, como cientistas de verdade!') +
            cols(left, right, t='1fr 1fr'))
    return page('exp-pedra', 'folha', body, 'Experiência', 'experiencia')


def e5_plantas():
    podes = [('Comem a sujeira', 'O cocô dos bichos vira comida de planta. Elas comem e a água fica limpa.'),
             ('Fazem ar', 'Com a luz, as folhas soltam bolhinhas de oxigênio, o ar que os bichos respiram.'),
             ('Dão esconderijo', 'Os filhotes de camarão se escondem entre as folhas.'),
             ('Fazem sombra', 'O Beto gosta de descansar na sombrinha, perto da superfície.')]
    cs = ''.join(f'<div class="card" style="background:var(--folha2)"><b>{a}</b><p>{b}</p></div>' for a, b in podes)
    left = (f'<div class="g2" style="gap:3.5mm">{cs}</div>'
            '<h3 class="h">Como plantar</h3>'
            '<ul class="bol" style="--cor:var(--folha)"><li><b>Plantas de raiz</b> vão na areia. O adulto usa uma pinça comprida para enterrar só as raízes.</li>'
            '<li><b>Plantas de pedra</b> — a anúbia, a samambaia e a bucephalandra — não gostam de ser enterradas! Elas ficam amarradas numa pedra ou num tronco com uma linha.</li>'
            '<li>As plantas que <b>boiam</b> são as últimas: vão depois que a água já está lá.</li></ul>')
    right = (foto('plant-aquario.jpg', 90, cap='Um aquário bem plantado.') +
             box('dica', 'Dica do Beto', '<p class="small">Plante <b>bastante</b> desde o primeiro dia. Assim sobra pouco espaço para as algas, aquelas plantinhas verdes que sujam o vidro.</p>'))
    body = (titulo('As plantas trabalham muito', 'Elas parecem só enfeite, mas têm quatro superpoderes.') + cols(left, right, t='1fr 100mm'))
    return page('e5-plantas', 'folha', body, 'Etapa 5 · As plantas', 'lapis')


CARTAS = [
    ('A cama do Beto', 'Anúbia', 'anubia-pedra.jpg', '#9ED39A', 'um país da África chamado <b>Camarões</b>! Igualzinho ao bicho.', 'presa numa pedra',
     'Quase nunca morre. O Beto adora dormir deitado em cima das folhas.', (2, 1, 5)),
    ('A floresta do fundo', 'Samambaia-de-java', 'samambaia-windelov.jpg', '#BFE3A3', 'Ásia, na beira de cachoeiras', 'amarrada no tronco',
     'Nascem plantinhas-filhotes na ponta das folhas!', (3, 2, 5)),
    ('A joia', 'Bucephalandra', 'buce-aquario.jpg', '#C9B6EE', 'ilha de Bornéu — e só de lá', 'nas frestas das pedras',
     'As folhas brilham e mudam de cor: verde, azul e vinho.', (1, 1, 3)),
    ('A mágica', 'Criptocoryne', 'crypt-wendtii.jpg', '#E7C79A', 'Sri Lanka, uma ilha perto da Índia', 'na areia, no meio',
     'Às vezes as folhas derretem... e depois ela volta a crescer!', (3, 2, 4)),
    ('O gramado', 'Helanthium', 'hel-tapete.jpg', '#A8E0B5', 'Américas — inclusive o <b>Brasil</b>!', 'na frente, na areia',
     'Vira um tapete de grama onde os filhotes de camarão se escondem.', (3, 3, 3)),
    ('O berçário', 'Musgo-de-java', 'musgo-camarao.jpg', '#D6EFA0', 'florestas da Ásia', 'grudado no tronco',
     'Os filhotes de camarão comem e se escondem lá dentro. O Beto não consegue entrar!', (2, 3, 5)),
    ('A faxineira', 'Rotala', 'rotala-moita.jpg', '#F6B8C8', 'Ásia', 'no fundo, atrás do tronco',
     'Cresce rapidinho e come a sujeira antes das algas. As pontas ficam cor-de-rosa!', (5, 5, 4)),
    ('O guarda-sol', 'Flutuante', 'phyl-folhas.jpg', '#F4A79D', 'Amazônia, no <b>Brasil</b>', 'boiando lá em cima',
     'Faz sombra e tem raízes vermelhas. O Beto faz o ninho de bolhas embaixo dela.', (4, 5, 3)),
]


def carta(c):
    apel, nome, img, cor, vem, mora, poder, (l, cr, f) = c
    return (f'<div class="carta" style="--c:{cor}"><div class="topo"><b>{apel}</b><span>{nome}</span></div>'
            f'<div class="img"><img src="img/{img}" alt="{nome}"></div>'
            f'<div class="txt"><p><b>Superpoder:</b> {poder}</p><p><b>Vem de:</b> {vem}.</p><p><b>Mora:</b> {mora}.</p>'
            f'<div class="stats"><span>Limpa a água</span>{pts(l)}<span>Cresce</span>{pts(cr)}<span>Fácil de cuidar</span>{pts(f)}</div></div>'
            f'<span class="cr" data-cr="img/{img}"></span></div>')


def cartas(n):
    grupo = CARTAS[(n - 1) * 4:n * 4]
    body = (titulo(f'Cartas das plantas · {n} de 2', 'Cada planta tem um superpoder. Qual é a sua preferida? Pinte o coração dela!' if n == 1 else None) +
            '<div class="g4 grow">' + ''.join(carta(c) for c in grupo) + '</div>')
    return page(f'cartas{n}', 'folha', body, 'Etapa 5 · As plantas', 'coracao')


def borda():
    ps = [('emersas/jiboia.jpg', 'Jiboia', 'A mais fácil. Cria raiz na água em uma ou duas semanas.'),
          ('emersas/clorofito.jpg', 'Clorofito', 'Folhas compridas, listradas. Não faz mal para gatos e cachorros.'),
          ('emersas/hydrocotyle.jpg', 'Pinheirinho-d’água', 'Uma planta brasileira que vive dentro e fora da água.')]
    cs = ''.join(f'<div>{foto(i, 56)}<p style="margin-top:.5mm"><b style="font-family:var(--display); font-weight:600; font-size:14pt">{n}</b></p><p class="small">{t}</p></div>' for i, n, t in ps)
    dias = ''.join(f'<td style="height:22mm; border:1.8pt solid var(--ink); border-radius:3mm; vertical-align:bottom; text-align:center; font:600 11pt/1 var(--display); padding-bottom:1.5mm">dia {d}</td>' for d in (1, 3, 5, 7, 10, 14))
    left = (f'<div class="g3" style="gap:4mm">{cs}</div>' +
            box('adulto', 'Atenção', '<p class="small"><b>Nunca coma nenhuma planta.</b> A jiboia faz mal se for mastigada — para pessoas, gatos e cachorros.</p>', 'atencao'))
    right = box('exp', 'Experiência: a muda que cria raiz',
                '<ol class="num" style="--cor:var(--folha); margin-top:1mm"><li>Com um adulto, corte um pedaço de jiboia com 2 folhas.</li>'
                '<li>Coloque num copo com água, num lugar claro, sem sol forte.</li>'
                '<li>Troque a água a cada 2 dias. Desenhe a raiz nos dias marcados:</li></ol>'
                f'<table style="width:100%; border-collapse:separate; border-spacing:1.6mm; table-layout:fixed"><tr>{dias}</tr></table>'
                '<p class="small">Em umas 2 semanas, a muda está pronta para ir para a borda do aquário!</p>')
    body = (titulo('Plantas que moram na borda', 'Algumas plantas de casa ficam com as folhas para fora e só as raízes dentro da água. As raízes bebem a sujeira!') +
            cols(left, right, t='1fr 112mm'))
    return page('borda', 'folha', body, 'Etapa 5 · As plantas', 'experiencia')


def mapa_pg():
    leg = [(1, 'Anúbia', 'verde-escuro'), (2, 'Samambaia', 'verde'), (3, 'Bucephalandra', 'roxo'), (4, 'Criptocoryne', 'marrom'),
           (5, 'Gramado', 'verde-claro'), (6, 'Musgo', 'verde-limão'), (7, 'Rotala', 'rosa'), (8, 'Flutuantes', 'vermelho')]
    ls = ''.join(f'<div class="row" style="gap:2.4mm"><span class="circ" style="font:700 12pt/8mm var(--display); text-align:center">{n}</span><p><b>{p}</b><br><span class="small">{c}</span></p></div>' for n, p, c in leg)
    right = (f'<div class="g2" style="gap:3mm 4mm">{ls}</div>'
             '<p class="small">O <b>tronco</b> é marrom e as <b>pedras</b> são cinza. O espaço branco da frente é a <b>piscina do Beto</b>: lá não vai planta nenhuma!</p>'
             + fala(CEREJA(), '<p class="small">O musgo (6) fica grudado no tronco. É lá que os meus filhotes vão morar!</p>', '30mm'))
    body = (titulo('O mapa do nosso aquário', 'Assim é o aquário visto de cima, como um passarinho veria. Pinte cada lugar com a cor da planta!') +
            cols(art.mapa(), right, t='1fr 92mm'))
    return page('mapa', 'folha', body, 'Etapa 5 · As plantas', 'lapis')


def quadro(inner, legenda, n):
    return (f'<div class="card" style="padding:2.4mm"><div style="position:relative">{svg(inner, "0 0 200 130")}'
            f'<span style="position:absolute; left:1mm; top:1mm; width:8mm; height:8mm; border-radius:50%; background:var(--sol); border:1.8pt solid var(--ink); font:600 12pt/7.4mm var(--display); text-align:center">{n}</span></div>'
            f'<p style="margin-top:2mm; font-size:11.5pt; line-height:15pt">{legenda}</p></div>')


def e6_bacterinhas():
    fundo = f'<rect x="0" y="0" width="200" height="130" rx="8" fill="{C["agua2"]}"/><path d="M0,112 C60,106 140,116 200,110 V130 H0 Z" fill="{C["areia"]}"/>'
    q1 = fundo + f'<g transform="translate(6,6) scale(.5)">{beto(uid="q1")}</g><circle cx="80" cy="100" r="4" fill="{C["terra"]}"/><circle cx="92" cy="104" r="3" fill="{C["terra"]}"/>' + nuvem('#B8A6D9', 110, 50, .95)
    q2 = fundo + nuvem('#B8A6D9', 12, 30, .7) + bacterinha(C['laranja'], 70, 38, .8, 'comendo') + nuvem('#E8A77A', 142, 44, .7)
    q3 = fundo + nuvem('#E8A77A', 12, 34, .7) + bacterinha(C['azul'], 70, 38, .8, 'comendo') + nuvem('#8FD19E', 150, 36, .8, 'feliz')
    q4 = fundo + nuvem('#8FD19E', 20, 34, .7, 'feliz') + art.planta_caule(120, 112, 96, leaves=8) + art.planta_caule(150, 112, 80, color=C['folha3'], leaves=6, flip=-1) + art.planta_caule(176, 112, 90, leaves=7)
    qs = [(q1, 'Comida que sobra e cocô viram <b>amônia</b>: uma sujeira invisível e venenosa.'),
          (q2, 'A <b>Bacterinha Laranja</b> come a amônia e solta <b>nitrito</b>. O nitrito ainda é venenoso!'),
          (q3, 'A <b>Bacterinha Azul</b> come o nitrito e solta <b>nitrato</b>: comida de planta!'),
          (q4, 'As plantas comem o nitrato e crescem. <b>A água fica limpa!</b>')]
    body = (titulo('As Bacterinhas: heroínas invisíveis', 'Antes de os bichos chegarem, o aquário precisa de um time de limpeza. Ele é tão pequeno que só dá para ver no microscópio!') +
            '<div class="g4" style="gap:4mm">' + ''.join(quadro(q, l, i + 1) for i, (q, l) in enumerate(qs)) + '</div>' +
            cols(box('sabia', 'Você sabia?', '<p>As Bacterinhas moram grudadas na <b>esponja do filtro</b>, nas pedras e na areia. Por isso a esponja nunca é lavada na torneira: o cloro da água mataria o time todo!</p>'),
                 '<div class="row" style="gap:4mm; align-items:flex-start"><div class="foto" style="width:74mm; height:50mm; flex:none"><img src="img/cycle-riacho.jpg" alt=""></div>'
                 '<p>Nos rios e lagos, as Bacterinhas também trabalham: limpam a água das pedras, do chão e das plantas. <span class="cr" data-cr="img/cycle-riacho.jpg"></span></p></div>', t='1fr 1fr', gap=6))
    return page('e6-bacterinhas', 'roxo', body, 'Etapa 6 · A espera', 'sabia')


def e6_detetive():
    cores = [('#F4E27A', '0'), ('#D8E27A', '0,5'), ('#9CCB6E', '1'), ('#4E9A58', '4')]
    tubos = ''.join(f'<div style="width:19mm">{art.tubo(c, l)}</div>' for c, l in cores)
    vazios = ''.join(f'<div style="text-align:center"><div style="width:20mm; margin:0 auto">{art.tubo("#fff", "")}</div><p class="small">dia <span class="linha" style="min-width:8mm"></span>/<span class="linha" style="min-width:8mm"></span></p></div>' for _ in range(4))
    left = ('<div class="box jogo"><p class="bh">Exemplo: o teste de amônia</p>'
            f'<div class="row" style="justify-content:space-around; align-items:flex-end">{tubos}</div>'
            '<div class="row" style="justify-content:space-around; font:600 12pt/1.2 var(--display); text-align:center; margin-top:1mm">'
            '<span style="width:24mm">ótimo!</span><span style="width:24mm">atenção</span><span style="width:24mm">perigo</span><span style="width:24mm">muito perigo</span></div>'
            '<p class="small" style="margin-top:2mm">As cores mudam de um kit para outro: compare sempre com a cartela que vem na caixa.</p></div>' +
            box('adulto', 'Só o adulto', '<p class="small">O líquido do teste é <b>venenoso</b>. Quem pinga e guarda os frascos é o adulto. Você observa e compara.</p>'))
    right = ('<h3 class="h">Pinte o tubo com a cor que apareceu</h3>'
             f'<div class="g4">{vazios}</div>' +
             box('sabia', 'Por que esperar tanto?', '<p class="small">As Bacterinhas levam umas <b>6 semanas</b> para crescer. Se os bichos chegassem antes, a amônia faria mal para eles. <b>Esperar é cuidar!</b></p>') +
             fala(BETO(), '<p class="small">Eu só chego quando os testes disserem que a água está boa!</p>', '30mm'))
    body = (titulo('Detetive da água', 'Como saber se as Bacterinhas já chegaram? Com testes! O adulto pinga o líquido no tubinho. Você compara as cores.') +
            cols(left, right))
    return page('e6-detetive', 'roxo', body, 'Etapa 6 · A espera', 'experiencia')


def contagem():
    start = dt.date(2026, 12, 28)
    special = {dt.date(2027, 1, 1): 'm', dt.date(2027, 2, 5): 'tst', dt.date(2027, 2, 12): 'cam', dt.date(2027, 3, 12): 'bet'}
    meses = {1: 'jan', 2: 'fev', 3: 'mar'}
    rows = []
    d = start
    while d <= dt.date(2027, 3, 14):
        tds = []
        for _ in range(7):
            off = d < dt.date(2027, 1, 1) or d > dt.date(2027, 3, 12)
            cls = special.get(d, '')
            lab = f'<small>{meses.get(d.month, "")}</small>' if d.day == 1 or d in special else ''
            tds.append(f'<td class="{"off" if off else ""}"><div class="d {cls}">{d.day}{lab}</div></td>')
            d += dt.timedelta(days=1)
        rows.append('<tr>' + ''.join(tds) + '</tr>')
    head = ''.join(f'<th>{w}</th>' for w in ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'))
    left = (f'<p class="chip">{icon("lapis")}Etapa 6 · A espera</p>' +
            titulo('Contagem regressiva', 'Pinte uma bolinha por dia. Quando chegar na vermelha, os camarões podem vir. Na azul, é a vez do Beto!') +
            '<div class="leg" style="flex-direction:column; gap:2.4mm"><span><i style="background:var(--sol)"></i>1º de janeiro: montar o aquário</span><span><i style="background:var(--roxo2)"></i>5 de fevereiro: grande teste</span>'
            '<span><i style="background:var(--coral)"></i>12 de fevereiro: camarões</span><span><i style="background:var(--agua)"></i>12 de março: o Beto</span></div>' +
            fala(BETO(), '<p class="small">Esperar é difícil, eu sei. Mas cada bolinha pintada deixa a água mais pronta para mim!</p>', '30mm'))
    body = cols(left, f'<table class="cal"><tr>{head}</tr>{"".join(rows)}</table>', t='88mm 1fr')
    return page('contagem', 'roxo', body)


def e7_cerejinhas():
    fatos = [('Tamanho', 'Uns <b>3 cm</b>: do tamanho de uma moeda de 1 real.'),
             ('Filhotes', 'Nascem com 1 ou 2 mm: <b>menores que um grão de arroz</b>!'),
             ('Trocam de roupa', 'A casca não cresce. Então o camarão sai dela e faz uma nova. A casca vazia parece um <b>camarão fantasma</b> — não tire: eles comem!'),
             ('Mamães', 'A mamãe carrega <b>20 a 30 ovinhos</b> embaixo da barriga por umas 3 semanas.'),
             ('Faxineiros', 'Passam o dia comendo o limo das folhas, das pedras e do vidro.'),
             ('Namoro', 'Depois da troca de casca, os machos nadam agitados procurando a mamãe.')]
    fs = ''.join(f'<div class="card" style="background:var(--coral2); padding:2.4mm 3mm 3mm"><b>{a}</b><p style="font-size:10.5pt; line-height:13.5pt">{b}</p></div>' for a, b in fatos)
    cores = [('neo-cereja.jpg', 'Cereja'), ('neo-sakura.jpg', 'Sakura'), ('neo-verde.jpg', 'Verde'), ('diario/mes-10.jpg', 'Amarela')]
    cs = ''.join(f'<div><div class="foto" style="height:30mm"><img src="img/{i}" alt=""></div><p class="small center" style="margin-top:1mm"><b>{n}</b></p><p class="crs" style="line-height:8pt"><span class="cr" data-cr="img/{i}"></span></p></div>' for i, n in cores)
    left = (f'<div class="g3" style="gap:3.5mm">{fs}</div>'
            + box('adulto', 'Muito importante', '<p class="small"><b>Nunca solte</b> camarões, peixes ou plantas em rios, lagos ou ralos. Eles atrapalham os bichos que já moram lá. Se sobrar, dê para outro aquarista.</p>', 'atencao'))
    right = ('<h3 class="h" style="margin:0">Existem camarões de muitas cores</h3>'
             f'<div class="g4" style="gap:3mm">{cs}</div>'
             '<div class="box jogo"><p class="bh">' + icon('lapis', '8mm') + 'Tamanho de verdade</p>' + art.regua('cereja') +
             '<p class="small">A Cereja adulta tem 3 cm. O filhote é do tamanho do pontinho vermelho!</p></div>')
    body = (titulo('As Cerejinhas', 'Os camarões chegam antes do Beto. Eles são pequenos, mas fazem um trabalhão!') + cols(left, right, t='1fr 118mm', gap=6))
    return page('e7-cerejinhas', 'coral', body, 'Etapa 7 · Os camarões', 'sabia')


def e7_chegada():
    k = art.INK
    gota = svg(f'<rect x="10" y="10" width="120" height="70" rx="4" fill="{C["agua2"]}" stroke="{k}" stroke-width="3"/><path d="M10,70 h120" stroke="{C["areia2"]}" stroke-width="10"/>'
               f'<path d="M100,30 C118,30 150,20 158,60 V110" fill="none" stroke="{k}" stroke-width="3"/><circle cx="158" cy="122" r="3.5" fill="{C["agua"]}"/><circle cx="158" cy="134" r="3" fill="{C["agua"]}"/>'
               f'<path d="M126,140 h64 l-6,40 h-52 Z" fill="#fff" stroke="{k}" stroke-width="3"/><path d="M129,156 h58 l-3,22 h-52 Z" fill="{C["agua2"]}"/>'
               + cereja(s=.22, x=140, y=154) + cereja(s=.2, x=160, y=160, flip=True)
               + f'<path d="M0,184 H200" stroke="{C["madeira"]}" stroke-width="6"/><rect x="4" y="80" width="140" height="104" fill="{C["madeira"]}" fill-opacity=".25"/>',
               '0 0 200 190', 'A água do aquário pinga devagar no pote dos camarões')
    left = ('<div class="g2" style="grid-template-columns:1fr 48mm; align-items:start">'
            '<ol class="num" style="--cor:var(--coral)">'
            '<li>Apague a luz e deixe o saquinho <b>boiando 20 minutos</b>.</li>'
            '<li>O adulto passa os camarões para um pote.</li>'
            '<li>Com uma mangueirinha, a água do aquário <b>pinga</b> no pote: pinga, pinga, pinga... por 1 ou 2 horas. <b>Conte 20 gotinhas!</b></li>'
            '<li>Com uma colher, os camarões vão para o aquário, sem a água da loja.</li>'
            '<li>Luz apagada até o dia seguinte e <b>nada de comida</b> no primeiro dia.</li></ol>'
            f'<div>{gota}</div></div>')
    right = (foto('neo2-madeira.jpg', 50, '50% 40%', 'Uma Cereja passeando no tronco.') +
             '<div class="box sabia"><p class="bh">' + icon('sabia', '8mm') + 'Isso é normal, não se assuste</p>'
             '<ul class="bol small" style="--cor:var(--roxo2)"><li>Nos primeiros dias, os camarões ficam escondidos.</li>'
             '<li>Aparece uma casca vazia: alguém trocou de roupa!</li>'
             '<li>De repente, todos nadam agitados: é época de namoro.</li></ul></div>')
    body = (titulo('A chegada dos camarões', 'Eles chegam num saquinho com a água da loja. A água nova é diferente: eles precisam de tempo para se acostumar.') +
            cols(left + box('dica', 'Quantos e quais?', '<p class="small">Vêm de <b>15 a 20</b> camarões, todos da mesma cor. Se misturar cores, os filhotes nascem marronzinhos, como os camarões da natureza.</p>'),
                 right, t='1fr 96mm'))
    return page('e7-chegada', 'coral', body, 'Etapa 7 · Os camarões', 'adulto')


def jogo_camaroes():
    bol = ''.join(f'<span class="circ" style="width:12mm; height:12mm; font:600 13pt/11mm var(--display); text-align:center">{i}</span>' for i in range(1, 8))
    left = (f'<p class="chip">{icon("jogo")}Jogo</p>' +
            titulo('Onde estão os camarões?', 'Sete camarões se esconderam entre as plantas. Encontre todos e circule cada um!') +
            f'<p class="small"><b>A cada camarão que achar, pinte uma bolinha:</b></p><div class="row" style="flex-wrap:wrap; gap:2.4mm">{bol}</div>' +
            fala(CEREJA(), '<p class="small">No aquário de verdade, a gente também se esconde. Procure à noite com uma lanterna!</p>', '28mm'))
    body = cols(left, f'<div class="box jogo">{art.cena_escondidos()}</div>', t='80mm 1fr')
    return page('jogo-camaroes', 'coral', body)


def e8_beto():
    fatos = [('Respiro ar!', 'Tenho um <b>canudinho secreto</b> chamado labirinto. Subo até a superfície e respiro ar, igual a você.'),
             ('De onde venho', 'Dos <b>arrozais da Tailândia</b>, do outro lado do mundo. Lá, sou marronzinho. As cores fortes vieram de criadores.'),
             ('Meu tamanho', '6 ou 7 cm: do tamanho de um dedo de adulto. Vivo de <b>2 a 4 anos</b>.'),
             ('Moro sozinho', 'Dois bettas machos brigam. Por isso, sou o <b>único peixe</b> do aquário.'),
             ('Ninho de bolhas', 'Quando estou feliz, faço um ninho de bolhinhas na superfície.'),
             ('Eu pulo!', 'Sou ótimo de salto. Por isso o aquário tem tampa.')]
    fs = ''.join(f'<div class="card" style="background:var(--agua2); padding:2.4mm 3mm 3mm"><b>{a}</b><p style="font-size:10.5pt; line-height:13.5pt">{b}</p></div>' for a, b in fatos)
    left = (foto('betta-halfmoon-azul.jpg', 76, '50% 25%', 'Um betta de verdade, com as nadadeiras abertas.') +
            fala(BETO(), '<p class="small">Muito prazer! Agora é a minha vez de contar quem eu sou.</p>', '30mm') +
            box('sabia', 'Meu nome científico', '<p class="small"><i>Betta splendens</i>. <i>Splendens</i> quer dizer <b>brilhante</b>!</p>'))
    right = (f'<div class="g3" style="gap:3.5mm">{fs}</div>'
             '<div class="box jogo" style="display:flex; gap:5mm; align-items:center">' + art.regua('beto') +
             '<div><p class="bh">' + icon('lapis', '8mm') + 'Tamanho de verdade</p><p class="small">Este Beto tem o tamanho de um betta de verdade: 7 cm, do nariz ao fim da cauda. '
             'Pegue uma régua e confira! Depois, meça o seu dedo.</p></div></div>')
    body = titulo('Beto, o peixe que respira ar') + cols(left, right, t='92mm 1fr', gap=6)
    return page('e8-beto', 'agua', body, 'Etapa 8 · O Beto', 'sabia')


def e8_caudas():
    fotos = [('betta/cauda-veu.jpg', 'Véu', 'Cauda comprida, caída como um véu.'), ('betta/halfmoon.jpg', 'Meia-lua', 'Abre a cauda como uma lua pela metade.'),
             ('betta/crowntail.jpg', 'Coroa', 'A cauda tem pontinhas, como uma coroa.'), ('betta/plakat.jpg', 'Curtinha', 'Nadadeiras curtas: nada rapidinho.'),
             ('betta/dumbo.jpg', 'Orelha de elefante', 'As nadadeiras do peito são enormes.'), ('betta/double-tail.jpg', 'Cauda dupla', 'A cauda é dividida em duas.'),
             ('betta/cor-koi.jpg', 'Koi', 'Manchado como uma carpa japonesa.'), ('betta/cor-dragon.jpg', 'Dragão', 'Escamas grossas e brilhantes.'),
             ('betta/giant.jpg', 'Gigante', 'Quase o dobro do tamanho de um betta comum.'), ('betta/wild-splendens.jpg', 'Da natureza', 'Assim é o betta nos arrozais da Tailândia.')]
    cs = ''.join(f'<div><div class="foto" style="height:44mm"><img src="img/{i}" alt=""></div><div class="row" style="justify-content:space-between; margin-top:1.4mm"><b style="font:600 12.5pt/1.1 var(--display)">{n}</b>{icon("coracao", "6.5mm")}</div><p class="small" style="font-size:10.5pt; line-height:13.5pt">{t}</p><p class="crs" style="line-height:8pt"><span class="cr" data-cr="img/{i}"></span></p></div>' for i, n, t in fotos)
    body = (titulo('Caudas e cores', 'Existem bettas de muitos jeitos. Pinte o coração do seu preferido!') + f'<div class="g5" style="gap:3mm 4mm">{cs}</div>')
    return page('e8-caudas', 'agua', body, 'Etapa 8 · O Beto', 'coracao')


def e8_sente():
    ms = [(dict(), 'Feliz', 'Cores fortes, nada pelo aquário e vem te ver na frente do vidro.', 'Tudo certo!'),
          (dict(mood='bravo'), 'Se exibindo', 'Abre as guelras e as nadadeiras para parecer maior.', 'Ele viu o próprio reflexo. Normal, se for rapidinho.'),
          (dict(mood='estresse'), 'Com medo', 'Aparecem listras escuras no corpo.', 'Normal nos primeiros dias. Se durar muito, chame um adulto.'),
          (dict(mood='dormindo'), 'Dormindo', 'Fica quietinho, deitado numa folha.', 'Peixes dormem! Deixe ele descansar.'),
          (dict(body='#8B96B8', fin='#B9A6AE', mood='doente', tail='doente'), 'Doente', 'Cores apagadas, nadadeiras fechadas, parado no fundo.', 'Chame um adulto na hora!')]
    rows = ''.join(f'<tr><td style="width:36mm; padding:.6mm 3mm">{BETO(uid="s" + str(i), **kw)}</td><td><b style="font:600 14pt/1.2 var(--display)">{n}</b><p class="small" style="font-size:11pt; line-height:14pt">{d}</p></td><td style="width:52mm"><p class="small" style="font-size:11pt; line-height:14pt"><b>{o}</b></p></td></tr>'
                   for i, (kw, n, d, o) in enumerate(ms))
    right = (foto('betta/ninho.jpg', 34, None, 'Um betta embaixo do ninho de bolhas.') +
             box('sabia', 'E o ninho de bolhas?', '<p class="small">Um montinho de bolhas grudadas na superfície quer dizer que ele está <b>contente</b> e se sentindo em casa.</p>') +
             box('jogo', 'Brincadeira de mímica', '<p class="small">Um faz a cara e o corpo do Beto — feliz, se exibindo, com medo, dormindo — e o outro tenta adivinhar!</p>'))
    body = (titulo('O que o Beto está sentindo?', 'O Beto não fala, mas mostra tudo com o corpo. Aprenda a ler os sinais!') +
            cols(f'<table class="tab" style="--cor:var(--agua2)"><tr><th>Como ele fica</th><th>O que é</th><th>O que fazer</th></tr>{rows}</table>', right, t='1fr 76mm', gap=6))
    return page('e8-sente', 'agua', body, 'Etapa 8 · O Beto', 'coracao')


def e8_chegou():
    left = ('<p class="lead">O nome do meu betta vai ser: <span class="linha" style="min-width:60mm"></span></p>'
            '<p class="lead">Ele chegou no dia <span class="linha" style="min-width:14mm"></span> / <span class="linha" style="min-width:14mm"></span> / 2027.</p>'
            '<div class="desenho" style="height:92mm">Desenhe o seu betta, com as cores dele</div>')
    right = (foto('betta2-convivencia.jpg', 46, '50% 40%', 'Um betta conhecendo a casa nova.') +
             '<ol class="num small" style="--cor:var(--agua)">'
             '<li>No primeiro dia: <b>luz apagada e sem comida</b>. Ele está cansado da viagem.</li>'
             '<li>O Beto vai olhar os camarões. Os filhotes se escondem no musgo.</li>'
             '<li>Fale baixinho perto do aquário e <b>nunca bata no vidro</b>.</li></ol>' +
             fala(BETO(), '<p class="small">Eu reconheço quem me dá comida! Em poucos dias, vou nadar até a frente do vidro quando você chegar.</p>', '28mm'))
    body = (titulo('O Beto chegou!', 'Ele vem depois dos camarões, entre <b>12 de março e 9 de abril</b>.') + cols(left, right, t='1fr 110mm'))
    return page('e8-chegou', 'agua', body, 'Etapa 8 · O Beto', 'lapis')


def e9_tarefas():
    eu, ad, jt = icon('eu', '8mm'), icon('adulto', '8mm'), icon('adulto', '8mm')
    ts = [('Todo dia, de manhã', 'Dar bom-dia, ver se o filtro faz bolhinhas e ler o termômetro.', eu),
          ('Todo dia, de manhã e à noite', 'Dar <b>2 ou 3 grãozinhos</b> para o Beto.', eu),
          ('Todo dia, à noite', 'Contar os camarões que dá para ver.', eu),
          ('Segunda, quarta e sexta', 'Dar um pouquinho de comida para os camarões.', eu),
          ('Domingo', 'Dia sem comida para o Beto: a barriguinha descansa.', eu),
          ('Sábado', 'Trocar um pouco da água e tirar a sujeira do fundo. O adulto faz, você ajuda.', jt),
          ('Quando precisar', 'Limpar o vidro <b>por fora</b> com um pano seco.', eu),
          ('A cada mês', 'Podar as plantas e fazer os testes da água.', ad)]
    rows = ''.join(f'<tr><td style="width:44mm; padding:1.2mm 3mm"><b>{q}</b></td><td style="padding:1.2mm 3mm">{t}</td><td class="q" style="padding:.6mm">{w}</td></tr>' for q, t, w in ts)
    left = (f'<table class="tab" style="--cor:var(--sol2); font-size:11.5pt; line-height:14.5pt"><tr><th>Quando</th><th>O que fazer</th><th class="q">Quem</th></tr>{rows}</table>'
            f'<div class="row" style="gap:8mm; font:500 12pt/1 var(--display)"><span class="row" style="gap:2mm">{eu} eu faço</span><span class="row" style="gap:2mm">{ad} com um adulto</span></div>')
    right = (foto('intro-betta.jpg', 36, '60% 40%', 'Um betta bem cuidado passeia pelas plantas.') +
             box('dica', 'A regra do olhinho', '<p class="small">A barriga do Beto é do tamanho do <b>olho</b> dele. Comida demais faz mal e suja a água.</p>') +
             box('adulto', 'Dica para o adulto', '<p class="small">Separe as porções da semana num potinho com divisões. Assim a criança alimenta sozinha, sem errar a medida.</p>') +
             '<p class="small"><b>Use a tabela de estrelas da página {{pg:estrelas}} para marcar tudo!</b></p>')
    body = (titulo('Minhas tarefas de aquarista', 'Um pouquinho todo dia vale mais que muito de vez em quando.') + cols(left, right, t='1fr 90mm', gap=6))
    return page('e9-tarefas', 'sol', body, 'Etapa 9 · As tarefas', 'estrela')


def estrelas():
    dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    star = icon('estrela', '9mm')
    rows = [(art.aparelho('filtro'), 'O filtro faz bolhinhas?', [1] * 7, False),
            (art.aparelho('termometro'), 'Termômetro: escrevo o número', [1] * 7, True),
            (art.aparelho('comida'), 'Comida do Beto de manhã', [1] * 6 + [0], False),
            (art.aparelho('comida'), 'Comida do Beto à noite', [1] * 6 + [0], False),
            (art.cereja_svg(), 'Contei os camarões: quantos?', [1] * 7, True),
            (art.cereja_svg(), 'Comida dos camarões', [1, 0, 1, 0, 1, 0, 0], False),
            (art.aparelho('balde'), 'Troca de água com o adulto', [0, 0, 0, 0, 0, 1, 0], False),
            (icon('maos'), 'Lavei as mãos', [1] * 7, False)]
    trs = []
    for pic, lab, on, num in rows:
        tds = ''.join((f'<td class="n">{"" if num else star}</td>' if o else '<td class="x"></td>') for o in on)
        trs.append(f'<tr><td><div class="lab">{pic}<span>{lab}</span></div></td>{tds}</tr>')
    head = '<th></th>' + ''.join(f'<th>{d}</th>' for d in dias)
    return ('<section class="page landscape k" id="estrelas" style="--cor:var(--sol)"><div class="folio" style="display:none">0</div><div class="est">'
            '<div class="top"><h2>Minha semana de estrelas</h2><p style="font:500 13pt/1 var(--display)">Semana de <span class="linha" style="min-width:26mm"></span> a <span class="linha" style="min-width:26mm"></span>'
            ' &nbsp; Estrelas: <span class="linha" style="min-width:16mm"></span></p></div>'
            f'<table class="st"><tr>{head}</tr>{"".join(trs)}</table>'
            '<p style="font:500 11pt/1.3 var(--display); color:#51606B">Pinte uma estrela a cada tarefa feita. Domingo é dia de descanso da barriga do Beto; os camarões comem segunda, quarta e sexta. '
            'Para usar toda semana: plastifique e use caneta de quadro branco.</p></div></section>')


TERMOS = [22, 25, 29, 24, 31, 26]


def termometro_pg():
    cs = ''.join(f'<div class="card row" style="padding:3mm; gap:4mm"><div style="width:48mm; flex:none">{art.termometro(t)}</div>'
                 f'<div style="display:flex; flex-direction:column; gap:3mm"><span class="row" style="gap:1.5mm">{art.smile("feliz")}<span>tudo bem</span></span>'
                 f'<span class="row" style="gap:1.5mm">{art.smile("triste")}<span>chamar adulto</span></span></div></div>' for t in TERMOS)
    reta = ''.join(f'<div style="flex:1; text-align:center; border-left:1.5pt solid var(--ink); padding:1.5mm 0; font:600 12pt/1 var(--display); background:{"var(--folha2)" if 24 <= n <= 26 else "transparent"}">{n}</div>' for n in range(20, 33))
    body = (titulo('Aprenda a ler o termômetro', 'O número bom para o aquário é <b>24, 25 ou 26</b>. Olhe cada termômetro e pinte a carinha certa.') +
            f'<div class="g3" style="gap:4mm">{cs}</div>' +
            cols('<h3 class="h" style="margin:0">A régua da temperatura</h3>'
                 f'<div style="display:flex; border:2pt solid var(--ink); border-radius:3mm; overflow:hidden; background:#fff">{reta}</div>'
                 '<p class="small">A parte verde é a zona boa. Números fora dela: chame um adulto.</p>',
                 box('adulto', 'No verão', '<p class="small">Em janeiro, a água pode esquentar demais. <b>Se passar de 28, chame um adulto.</b> E nunca jogue gelo dentro do aquário!</p>', 'atencao'),
                 t='1fr 100mm'))
    return page('termometro', 'coral', body, 'Etapa 9 · As tarefas', 'lapis')


def sos_pg():
    ss = [('turva', 'A água ficou branca ou verde'), ('fundo', 'O Beto parou no fundo, sem cor'), ('pontos', 'Pontinhos brancos no Beto'),
          ('quente', 'Termômetro fora de 24 a 26'), ('deitado', 'Um camarão de barriga para cima'), ('filtro', 'O filtro parou de fazer bolhinhas'),
          ('vazou', 'Água no chão ou no móvel'), ('cheiro', 'Um cheiro ruim')]
    cs = ''.join(f'<div class="card center" style="padding:3mm"><div style="width:100%; margin:0 auto">{art.sos(k)}</div><p style="margin-top:2mm; font-size:13pt; line-height:17pt">{t}</p></div>' for k, t in ss)
    right = ('<div class="box sabia"><p class="bh">' + icon('sabia', '8mm') + 'Isso é normal, não se assuste</p>'
             '<ul class="bol small" style="--cor:var(--roxo2)"><li>Uma casca vazia de camarão: ele trocou de roupa.</li>'
             '<li>A criptocoryne derreteu: ela volta a crescer.</li>'
             '<li>Água branquinha nos primeiros dias da montagem.</li>'
             '<li>Um pozinho marrom no vidro nas primeiras semanas.</li>'
             '<li>O Beto dormindo deitado numa folha.</li></ul></div>')
    body = (titulo('Chame um adulto!', 'Se você vir alguma destas coisas, avise um adulto na hora. Você é o vigia do aquário!') +
            cols(f'<div class="g4" style="gap:3.5mm">{cs}</div>', right, t='1fr 78mm', gap=6))
    return page('sos', 'coral', body, 'Etapa 9 · As tarefas', 'atencao')


PALAVRAS = ['BETTA', 'CAMARAO', 'PLANTA', 'FILTRO', 'AGUA', 'MUSGO', 'BOLHAS', 'PEDRA', 'AREIA', 'NINHO']
GRID, PLACED = art.caca_palavras(PALAVRAS, 11, seed=5)


def cacapalavras():
    lista = ''.join(f'<li>{w}</li>' for w in PALAVRAS)
    left = (f'<p class="chip">{icon("jogo")}Jogos</p>' +
            titulo('Caça-palavras', 'Encontre 10 palavras do aquário. Elas estão deitadas ou em pé. Marque cada uma que achar!') +
            f'<ul class="bol check" style="columns:2; font:600 13pt/1.2 var(--display); --cor:#fff">{lista}</ul>'
            '<p class="small">No caça-palavras não tem acento: CAMARÃO vira CAMARAO e ÁGUA vira AGUA.</p>' +
            fala(BETO(), '<p class="small">Dica: comece pelas palavras mais compridas!</p>', '30mm'))
    body = cols(left, f'<div class="box jogo">{art.grade_letras(GRID, cell=13.2)}</div>', t='1fr auto', gap=10)
    return page('cacapalavras', 'agua', body)


def labirinto_pg():
    left = (f'<p class="chip">{icon("jogo")}Jogos</p>' +
            titulo('Labirinto', 'Ajude a Cereja a chegar ao musgo, onde ela fica protegida.') +
            f'<div style="width:56mm">{CEREJA()}</div>' +
            foto('musgo-camarao.jpg', 46, None, 'O musgo de verdade, com um camarão escondido.'))
    body = cols(left, f'<div class="box jogo"><div style="width:130mm">{art.labirinto(11, 13, seed=11, cell=30)}</div></div>', t='1fr auto', gap=10)
    return page('labirinto', 'folha', body)


DIFFS = (1, 2, 3, 4, 6)


def diferencas():
    body = (titulo('Jogo das 5 diferenças', 'Os dois aquários parecem iguais, mas têm 5 diferenças. Circule todas no desenho da direita!') +
            f'<div class="g2" style="gap:6mm"><div class="box jogo">{art.cena()}</div><div class="box jogo">{art.cena(DIFFS)}</div></div>'
            f'<div class="row" style="justify-content:center">' + ''.join(f'<span class="circ" style="width:11mm; height:11mm; font:600 13pt/10mm var(--display); text-align:center">{i}</span>' for i in range(1, 6)) + '</div>')
    return page('diferencas', 'roxo', body, 'Jogos', 'jogo')


def colorir1():
    body = (titulo('Pinte o aquário', 'Use muitas cores! O Beto pode ser azul, vermelho, amarelo... do jeito que você quiser.') +
            f'<div class="grow" style="display:flex; justify-content:center"><div style="width:212mm">{art.cena(line=True)}</div></div>')
    return page('colorir1', 'sol', body, 'Jogos', 'lapis')


def colorir2():
    body = (titulo('Pinte a Cereja, as Bacterinhas e o Beto') +
            '<div class="grow" style="display:grid; grid-template-columns:1fr 1fr; grid-template-rows:auto 1fr; gap:6mm 10mm; align-items:center">'
            f'<div>{art.cereja_svg(line=True)}</div>'
            f'<div>{art.beto_svg(line=True, mood="dormindo")}</div>'
            f'<div style="grid-column:1 / -1; width:160mm; margin:0 auto">{svg(bacterinha(line=True) + bacterinha(line=True, x=100, y=10, mood="comendo"), "-12 6 196 60")}</div></div>')
    return page('colorir2', 'coral', body, 'Jogos', 'lapis')


QUIZ = [('O betta respira o ar da superfície.', 'V'), ('Podemos colocar dois bettas machos juntos.', 'F'),
        ('O camarão troca de casca para crescer.', 'V'), ('Pode lavar o aquário com sabão.', 'F'),
        ('As Bacterinhas ajudam a limpar a água.', 'V'), ('Quanto mais comida, melhor para o peixe.', 'F'),
        ('As plantas comem a sujeira da água.', 'V'), ('Podemos soltar os camarões no rio.', 'F'),
        ('O aquecedor deixa a água morninha.', 'V'), ('Bater no vidro é legal para o peixe.', 'F')]


def quiz():
    rows = ''.join(f'<p>{i}. {q}</p><span class="o"><span>V</span><span>F</span></span>' for i, (q, _) in enumerate(QUIZ, 1))
    right = (foto('diario/mes-04.jpg', 64, '50% 50%', 'Um betta nadando perto da superfície.') +
             fala(BETO(mood='feliz'), '<p class="small">Acertou quase tudo? Então você já é um aquarista de verdade! As respostas estão na página {{pg:respostas}}.</p>', '30mm'))
    body = (titulo('Verdadeiro ou falso?', 'Pinte o V se for verdade e o F se for mentira. Você já sabe tudo isso!') +
            cols(f'<div class="box jogo"><div class="vf" style="font-size:14.5pt; line-height:18pt; gap:3mm 5mm">{rows}</div></div>', right, t='1fr 92mm', gap=6))
    return page('quiz', 'roxo', body, 'Jogos', 'jogo')


def diario(n):
    entrada = ('<div class="card" style="display:flex; flex-direction:column; gap:3mm; height:100%">'
               '<p class="lead">Dia <span class="linha" style="min-width:12mm"></span> / <span class="linha" style="min-width:12mm"></span> / 2027</p>'
               f'<div class="row" style="gap:2mm"><span class="small">O Beto estava:</span>{art.smile("feliz")}{art.smile("meio")}{art.smile("triste")}</div>'
               '<div class="desenho" style="height:58mm">Hoje eu vi...</div><div class="linhas" style="flex:1"></div></div>')
    body = titulo('Meu diário de aquarista', 'Desenhe e escreva o que você viu no aquário.' if n == 1 else None) + \
        f'<div class="g2 grow" style="gap:6mm">{entrada}{entrada}</div>'
    return page(f'diario{n}', 'folha', body, 'Diário', 'lapis')


def conquistas():
    k = art.INK
    tank = (f'<rect x="2" y="8" width="36" height="26" rx="2" fill="{C["agua2"]}" stroke="{k}" stroke-width="2.4"/>'
            f'<path d="M3,29 C14,26 26,30 37,27 V33 H3 Z" fill="{C["areia"]}"/>')
    it = [('Montei o aquário', tank, C['agua']),
          ('Plantei minha primeira planta', art.planta_caule(20, 38, 34, leaves=6), C['folha']),
          ('Esperei as Bacterinhas', bacterinha(C['laranja'], 0, 0, .5), C['roxo']),
          ('Fiz um teste com o adulto', f'<rect x="12" y="2" width="14" height="36" rx="7" fill="#fff" stroke="{k}" stroke-width="2.4"/><rect x="15" y="20" width="8" height="16" rx="4" fill="#F4E27A"/>', C['roxo']),
          ('Chegaram os camarões', cereja(s=.32, x=-2, y=6), C['coral']),
          ('Achei uma casca vazia', f'<g opacity=".45">{cereja(s=.32, x=-2, y=6, face=False)}</g>', C['coral']),
          ('Vi uma mamãe com ovinhos', cereja(s=.32, x=-2, y=6) + ''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="{C["sol"]}" stroke="{k}" stroke-width=".6"/>' for x, y in ((12, 26), (16, 28), (20, 27))), C['coral']),
          ('Vi um filhote', cereja(s=.16, x=10, y=14), C['coral']),
          ('O Beto chegou', f'<g transform="scale(.2) translate(0,20)">{beto(uid="sel")}</g>', C['agua']),
          ('Vi um ninho de bolhas', art.bolhas(14, 34, 3) + art.bolhas(26, 30, 2), C['agua']),
          ('Uma semana de estrelas', f'<g transform="translate(6,4) scale(1.3)"><path d="M12,2 L14.9,8.3 L21.8,9 L16.6,13.6 L18.1,20.4 L12,16.9 L5.9,20.4 L7.4,13.6 L2.2,9 L9.1,8.3 Z" fill="{C["sol"]}" stroke="{k}" stroke-width="1.4"/></g>', C['sol']),
          ('Um mês de aquário', f'<rect x="4" y="6" width="32" height="30" rx="4" fill="#fff" stroke="{k}" stroke-width="2.4"/><path d="M4,14 h32" stroke="{k}" stroke-width="2.4"/><text x="20" y="31" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="13" fill="{k}">30</text>', C['sol'])]
    ss = ''.join(f'<div class="selo">{art.selo(i, c)}<b>{t}</b><span>Data: <span class="linha" style="min-width:24mm; height:6mm"></span></span></div>' for t, i, c in it)
    body = titulo('Minhas conquistas', 'Cada vez que conseguir uma destas coisas, pinte o selo e escreva a data.') + f'<div class="selos">{ss}</div>'
    return page('conquistas', 'sol', body, 'Conquistas', 'estrela')


def dicionario():
    ps = [('Aquarista', 'Quem cuida de um aquário. Você!'), ('Amônia', 'Sujeira invisível e venenosa que sai do cocô e da comida que sobra.'),
          ('Aquecedor', 'Aparelho que deixa a água morninha.'), ('Bacterinhas', 'Seres tão pequenos que ninguém vê. Transformam a sujeira em comida de planta.'),
          ('Ciclagem', 'As semanas de espera enquanto as Bacterinhas crescem.'), ('Ecossistema', 'Lugar onde plantas, bichos e bactérias vivem juntos e se ajudam.'),
          ('Filtro', 'A esponja que limpa a água e é a casa das Bacterinhas.'), ('Labirinto', 'O “canudinho” que o betta usa para respirar ar.'),
          ('Limo', 'Camada fininha que cresce em tudo dentro da água. Os camarões adoram comer.'), ('Muda', 'Quando o camarão troca de casca para crescer.'),
          ('Ninho de bolhas', 'Montinho de bolhas que o betta faz quando está contente.'), ('Nitrato', 'Comida de planta que as Bacterinhas fazem.'),
          ('Oxigênio', 'O ar que os bichos respiram. As plantas fazem oxigênio com a luz.'), ('Substrato', 'O chão do aquário: terra e areia.'),
          ('Troca de água', 'Tirar um pouco da água velha e colocar água nova, toda semana.')]
    items = ''.join(f'<div style="break-inside:avoid; margin-bottom:2.6mm"><b style="font:600 14pt/1.2 var(--display); color:var(--ink)">{a}</b><p class="small">{b}</p></div>' for a, b in ps)
    body = titulo('Dicionário do aquarista', 'Palavras novas que você aprendeu neste livro.') + f'<div style="columns:3; column-gap:8mm; font-size:14pt">{items}</div>'
    return page('dicionario', 'roxo', body, 'Para consultar', 'sabia')


def respostas():
    quiz_r = ' · '.join(f'{i} {a}' for i, (_, a) in enumerate(QUIZ, 1))
    ligue_r = '; '.join(f'{a}: {t}' for a, t in [('aquecedor', 'deixa a água morninha'), ('tampa', 'não deixa o Beto pular'), ('filtro', 'limpa a água'), ('termômetro', 'quente ou fria'), ('luz', 'sol das plantas')])
    mini_grade = art.grade_letras(GRID, PLACED, cell=8).replace('class="cp"', 'class="cp mini"')
    termo_r = ' · '.join(f'{t}°: {"tudo bem" if 24 <= t <= 26 else "chamar adulto"}' for t in TERMOS)
    textos = ('<div class="small" style="display:flex; flex-direction:column; gap:2.4mm">'
              '<div><h3 class="h">As 5 diferenças</h3><p>A pedra pequena mudou de cor; as nadadeiras do Beto ficaram verdes; uma planta do fundo ficou mais baixa; sumiram bolhinhas; sumiu um camarão.</p></div>'
              f'<div><h3 class="h">Verdadeiro ou falso</h3><p>{quiz_r}</p></div>'
              '<div><h3 class="h">Onde o aquário vai morar</h3><p>C: no móvel firme, longe da janela, perto da tomada.</p></div>'
              f'<div><h3 class="h">Termômetros</h3><p>{termo_r}.</p></div>'
              f'<div><h3 class="h">Ligue cada coisa</h3><p>{ligue_r}.</p></div></div>')
    body = (titulo('Respostas', 'Só olhe depois de tentar!') +
            cols(f'<h3 class="h" style="margin:0">Caça-palavras</h3>{mini_grade}',
                 f'<h3 class="h" style="margin:0">Labirinto</h3><div style="width:78mm">{art.labirinto(11, 13, seed=11, cell=30, solution=True)}</div>',
                 textos, t='auto auto 1fr'))
    return page('respostas', 'sol', body, 'Respostas', 'ok')


def adultos():
    body = (titulo('Para os adultos', 'Este livro acompanha o guia <i>Vinte litros de mundo</i>: as mesmas etapas, datas e números, numa linguagem para crianças de 6 a 8 anos.') +
            '<div class="g3" style="align-items:start; font-size:11pt; line-height:14.8pt; gap:7mm">'
            '<div><h3 class="h">Como usar</h3><p>Aos 6 anos, leia junto; aos 8, a criança lê quase tudo sozinha. Siga o livro no ritmo do aquário: a Etapa 6 dura seis semanas, e a contagem regressiva ajuda a esperar. As páginas de colorir, o diário e a tabela de estrelas podem ser impressos de novo quantas vezes quiser.</p>'
            '<h3 class="h" style="margin-top:4mm">O que a criança pode fazer</h3><p>Observar, contar, ler o termômetro, alimentar com a porção já separada, lavar a areia, limpar o vidro por fora, anotar no diário e avisar quando algo parecer errado.</p></div>'
            '<div><h3 class="h">O que é sempre do adulto</h3><ul class="bol" style="--cor:var(--coral)">'
            '<li>Tomadas, aquecedor, compressor e luminária — desligue tudo antes de pôr a mão na água.</li>'
            '<li>Reagentes dos testes, condicionador, fertilizantes e remédios: são tóxicos. Guarde fora do alcance.</li>'
            '<li>Cola, tesoura, pinças longas e a madeira fervendo.</li><li>Carregar o aquário, sifonar e trocar a água.</li></ul>'
            '<h3 class="h" style="margin-top:4mm">Higiene</h3><p>Lavem as mãos antes e depois. A água de aquário pode ter bactérias que causam infecções de pele: nada de mãos com cortes na água, nem mão na boca.</p></div>'
            '<div><h3 class="h">Responsabilidade</h3><p>A criança ajuda, mas o bem-estar dos animais é do adulto: férias, esquecimentos e doenças acontecem. Um camarão pode morrer, e o betta vive de 2 a 4 anos. Falar disso com honestidade faz parte do aprendizado.</p>'
            '<div class="box dica" style="margin-top:4mm"><p class="bh">' + icon('dica', '8mm') + 'Para imprimir</p>'
            '<p>O livro inteiro está em A4 paisagem. Imprima a tabela de estrelas (página {{pg:estrelas}}) em papel grosso e plastifique. As respostas dos jogos estão na página {{pg:respostas}}. Os detalhes técnicos de cada etapa — quantidades, parâmetros da água, doenças — estão no guia para adultos e no <i>Diário 2027</i>.</p></div></div></div>')
    return page('adultos', 'coral', body, 'Para os adultos', 'adulto')


def creditos():
    body = (titulo('Créditos das fotos', 'As fotos deste livro são de uso livre, com as licenças indicadas. Licenças NC permitem apenas uso não comercial.') +
            '<div class="credits" style="columns:3; column-gap:7mm; font-size:8pt; line-height:10.5pt"><!--#credits--></div>'
            '<p class="tiny">Desenhos feitos para este livro. Fontes: Fredoka e Atkinson Hyperlegible Next, ambas com licença livre (SIL Open Font License). '
            'Atkinson Hyperlegible foi criada pelo Braille Institute para ser fácil de ler.</p>')
    return page('creditos', 'agua', body, 'Créditos', 'sabia')


def certificado():
    deco = svg(f'<g transform="translate(10,10) scale(.9)">{beto(uid="cert")}</g>' + art.cereja(s=.6, x=196, y=40, flip=True) + art.bolhas(186, 60, 3), '0 0 280 120')
    body = ('<div style="flex:1; border:3pt solid var(--ink); border-radius:8mm; outline:2pt dashed var(--agua); outline-offset:-5mm; padding:10mm 14mm; display:flex; flex-direction:column; align-items:center; gap:4mm; text-align:center; background:#fff">'
            '<div class="row" style="gap:8mm">' + f'<div style="width:96mm">{deco}</div>' +
            '<p style="font:700 40pt/1.05 var(--display); color:var(--ink); text-align:left">Certificado de<br>Pequeno Aquarista</p></div>'
            '<p class="lead" style="font-size:18pt">Certificamos que</p><span class="linha" style="width:170mm; height:14mm"></span>'
            '<p class="lead" style="max-width:200mm; font-size:17pt; line-height:24pt">montou, esperou com paciência e cuidou de um aquário de verdade, com plantas, camarões e um betta.</p>'
            '<div class="row" style="gap:5mm; align-items:center">' + ''.join(icon('jogo', '18mm') for _ in range(3)) +
            '<p style="font:600 18pt/1.2 var(--display); color:var(--ink)">Aquarista de verdade!</p></div>'
            '<div class="row" style="gap:20mm; margin-top:auto"><div><span class="linha" style="width:70mm"></span><p class="small">data</p></div>'
            '<div><span class="linha" style="width:70mm"></span><p class="small">assinatura do adulto</p></div></div></div>')
    return page('certificado', 'sol', body)


def contracapa():
    g = svg(f'<g transform="translate(40,20) scale(1.3)">{beto(uid="cc", bubbles=3)}</g>' + art.cereja(s=.6, x=40, y=150) + art.bacterinha(C['laranja'], 220, 170, .6), '0 0 320 220')
    body = ('<div style="position:absolute; inset:20mm 22mm; display:grid; grid-template-columns:1fr 120mm; gap:14mm; align-items:center; color:#fff">'
            '<div style="display:flex; flex-direction:column; gap:8mm">'
            '<p style="font:600 26pt/32pt var(--display)">Todo grande aquarista começou com um aquário pequeno.</p>'
            '<p style="font:400 14pt/20pt var(--texto)">Um livro para montar um aquário de 20 litros com plantas, camarões e um betta — e para aprender, esperar, observar e brincar com ele durante o ano todo.</p>'
            '<p style="font:600 15pt/1 var(--display)">Vinte litros de mundo · edição para crianças</p></div>'
            f'<div>{g}</div></div>')
    return f'<section class="page recto k contra nochrome" id="contracapa" style="--cor:var(--agua)"><div class="folio">0</div>{body}</section>'


SEQ = [capa, meu_livro, combinado, turma, mundo, trilha, regras, e1_caixa, e1_ligue, e2_lugar, e3_chao, e4_paisagem, exp_pedra,
       e5_plantas, lambda: cartas(1), lambda: cartas(2), borda, mapa_pg, e6_bacterinhas, e6_detetive, contagem, e7_cerejinhas,
       e7_chegada, jogo_camaroes, e8_beto, e8_caudas, e8_sente, e8_chegou, e9_tarefas, estrelas, termometro_pg, sos_pg,
       cacapalavras, labirinto_pg, diferencas, colorir1, colorir2, quiz, lambda: diario(1), lambda: diario(2), lambda: diario(3),
       conquistas, dicionario, respostas, adultos, creditos, certificado, contracapa]


def head():
    fonts = ("@font-face{font-family:'Fredoka';font-style:normal;font-weight:300 700;font-display:block;src:url(fonts/fredoka.woff2) format('woff2');}\n"
             "@font-face{font-family:'Atkinson Hyperlegible Next';font-style:normal;font-weight:200 800;font-display:block;src:url(fonts/font1.woff2) format('woff2');}\n"
             "@font-face{font-family:'Atkinson Hyperlegible Next';font-style:italic;font-weight:200 800;font-display:block;src:url(fonts/font0.woff2) format('woff2');}\n")
    css = open(os.path.join(HERE, 'kids.css'), encoding='utf-8').read()
    return ('<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>Meu primeiro aquário — Vinte litros de mundo para crianças</title>\n'
            f'<style>{fonts}</style>\n<style>{css}</style>\n</head>\n<body>\n')


def main():
    if os.path.isdir(PAGES):
        shutil.rmtree(PAGES)
    os.makedirs(PAGES)
    open(os.path.join(HERE, 'head.html'), 'w', encoding='utf-8').write(head())
    open(os.path.join(HERE, 'tail.html'), 'w', encoding='utf-8').write('\n</body>\n</html>\n')
    for i, fn in enumerate(SEQ):
        open(os.path.join(PAGES, f'{i:03d}.html'), 'w', encoding='utf-8').write(fn())
    print('crianças:', len(SEQ), 'páginas geradas')


if __name__ == '__main__':
    main()
