#!/usr/bin/env python3
"""Gera o volume Diário 2027: páginas em src/diario/pages/ e head.html.

O aquário é montado em 1º de janeiro de 2027 (D1). Os marcos impressos
seguem o cronograma do guia: ciclagem de 4 a 6 semanas, camarões entre
a 7ª e a 9ª semana, betta entre a 10ª e a 14ª.
"""
import datetime as dt
import os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE)
PAGES = os.path.join(HERE, 'pages')
YEAR = 2027
D1 = dt.date(YEAR, 1, 1)

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
         'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
SEMANA = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
SEM_CURTO = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
# acento de cada mês: verão quente, outono verde, inverno água, primavera azul
ACC = ['var(--cereja)', 'var(--cereja)', 'var(--tanino)', 'var(--tanino)', 'var(--musgo)', 'var(--musgo)',
       'var(--agua-claro)', 'var(--agua-claro)', 'var(--betta)', 'var(--betta)', 'var(--cereja)', 'var(--cereja)']


def dnum(d):
    return (d - D1).days + 1


def dia(dn):
    return D1 + dt.timedelta(days=dn - 1)


def fmt(d):
    return f'{d.day} de {MESES[d.month - 1]}'


def fmt_curto(d):
    return f'{d.day:02d}/{d.month:02d}'


# ------------------------------------------------------------------ marcos
def marcos():
    """dia -> lista de (tipo, rótulo curto, texto)."""
    M = {}

    def add(d, kind, label, text=''):
        M.setdefault(d, []).append((kind, label, text))

    add(dia(1), 'm', 'Montagem', 'Hoje: substrato, hardscape, plantio e enchimento. Meça pH, GH, KH e TDS da água da torneira, ligue filtro, aquecedor (25 °C) e luz (6 h), e comece a ciclagem. Ponha as mudas emersas para enraizar num pote.')
    add(dia(2), 'f', 'Ciclagem · fase 1', 'Primeiros dias: a amônia sobe, o nitrito fica em zero. Água branca e turva é normal.')
    add(dia(15), 'f', 'Ciclagem · fase 2', 'O nitrito começa a subir: o primeiro grupo de bactérias chegou. Pó marrom nos vidros (diatomáceas) é normal.')
    add(dia(15), 'e', 'Emersas', 'Mudas emersas com raízes novas? Entre hoje e o dia 29, elas podem ir para a borda.')
    add(dia(29), 'f', 'Ciclagem · fase 3', 'O nitrito cai e o nitrato aparece. A ciclagem está perto do fim.')
    add(dia(32), 's', '1 mês de aquário', '')
    add(dia(36), 'm', 'Teste de conclusão', 'Dose amônia até 2 ppm (ou a pitada de ração de sempre). Se amanhã amônia e nitrito estiverem em zero, confirme por três a sete dias.')
    add(dia(42), 'm', 'TPA de 50%', 'Ciclo confirmado? Troque 50% da água para baixar o nitrato antes dos camarões.')
    add(dia(43), 'a', 'Janela dos camarões', 'De hoje até 26 de fevereiro: compre 15 a 20 Neocaridina de uma única linhagem, nas horas frescas, e aclimate por gotejamento.')
    add(dia(57), 'a', 'Fim da janela dos camarões', '')
    add(dia(57), 'b', 'Betta: quarentena', 'Se for fazer quarentena de 14 dias, este é o primeiro dia para comprar o betta.')
    add(dia(71), 'b', 'Janela do betta', 'De hoje até 9 de abril: o betta pode entrar no aquário. Luz apagada no primeiro dia, sem comida nas primeiras 24 horas.')
    add(dia(99), 'b', 'Fim da janela do betta', '')
    add(dia(85), 'a', 'Primeiras ovadas?', 'Fêmeas carregando ovos costumam aparecer de quatro a oito semanas depois da chegada.')
    add(dia(100), 's', '100 dias de aquário', '')
    add(dt.date(YEAR, 7, 1), 's', '6 meses de aquário', 'Meio ano: releia janeiro e compare as fotos.')
    add(dt.date(YEAR, 12, 31), 's', 'Um ano de aquário', 'Último dia do ano do aquário. A revisão do ano está no fim do diário.')
    for m in (3, 5, 7, 9, 11):
        add(dt.date(YEAR, m, 1), 'p', 'Repor pastilhas', 'Pastilhas fertilizantes junto às plantas de raiz; confira mangueiras, válvula de retenção e aquecedor.')
    # testes: a cada 2 dias na ciclagem; depois, domingos a cada 2 semanas
    for n in range(1, 43, 2):
        add(dia(n), 't', 'Teste NH₃ e NO₂')
    d = dt.date(YEAR, 2, 14)
    while d.year == YEAR:
        add(d, 't', 'Teste NO₃, GH e TDS')
        d += dt.timedelta(days=14)
    # TPA semanal aos sábados depois da ciclagem
    d = dt.date(YEAR, 2, 13)
    while d.year == YEAR:
        add(d, 'w', 'TPA')
        d += dt.timedelta(days=7)
    return M


ESPERAR = {
    1: 'O mês da ciclagem. Nenhum animal ainda: só plantas, bactérias e paciência. É também o mês mais quente — anote a temperatura máxima todos os dias.',
    2: 'Fim da ciclagem, TPA grande e a chegada dos camarões. As primeiras semanas deles são as mais delicadas: aclimatação lenta e pouca comida.',
    3: 'Colônia se firmando, primeiras mudas e, talvez, as primeiras ovadas. A janela do betta abre no dia 12.',
    4: 'O betta chega até o dia 9, se ainda não chegou. Observe a convivência com atenção nas duas primeiras semanas.',
    5: 'O tapete e o musgo começam a fechar. As noites esfriam: confira se o aquecedor está ligando.',
    6: 'Rotina de podas. É um bom mês para fotografar o aquário de frente, sempre do mesmo ângulo.',
    7: 'Seis meses. Repor pastilhas, revisar equipamentos e comparar a foto de hoje com a de janeiro.',
    8: 'Inverno: aquecedor trabalhando, evaporação menor. Fique de olho no TDS.',
    9: 'Primavera. Mais luz no cômodo pode significar mais algas: confira o fotoperíodo.',
    10: 'A colônia de camarões deve estar em várias gerações. Hora de doar o excesso, se houver.',
    11: 'O calor volta. Releia a página de verão do guia antes dos primeiros dias quentes.',
    12: 'Fim do ano do aquário. Uma revisão completa, os aprendizados e os planos para 2028.',
}

CHIP_CLASS = {'m': 'cm', 'f': 'cf', 'e': 'ce', 'a': 'ca', 'b': 'cb', 's': 'cs', 'p': 'cp', 't': 'ct', 'w': 'cw'}


def chips(items):
    return ''.join(f'<span class="chip {CHIP_CLASS[k]}">{lab}</span>' for k, lab, _ in items)


def box(label=''):
    return f'<span class="bx"></span>{label}'


def circles(n=5):
    return '<span class="cc">' + '<i></i>' * n + '</span>'


def blank(w=12, unit=''):
    return f'<span class="bl" style="width:{w}mm"></span>{unit}'


# ------------------------------------------------------------------ blocos
def page(pid, month, rh, body, extra='', side=None):
    acc = ACC[month - 1] if month else 'var(--agua-claro)'
    tab = f'<div class="tab dtab" style="--ch:{month - 1}">{month}</div>' if month else ''
    return (f'<section class="page recto diario {extra}" id="{pid}" style="--accent:{acc}">'
            f'<div class="rh"><span>Diário 2027 · Vinte litros de mundo</span><span class="sec">{rh}</span></div>'
            f'<div class="folio">0</div>{tab}\n  <div class="frame">\n{body}\n  </div>\n</section>\n')


def day_block(d, M):
    items = M.get(d, [])
    notes = [t for k, lab, t in items if t]
    note_html = ''.join(f'<p class="dnote">{t}</p>' for t in notes)
    n = dnum(d)
    week = (n - 1) // 7 + 1
    return f'''    <div class="day">
      <div class="dh">
        <span class="dn">{d.day}</span>
        <div class="dm"><b>{SEMANA[d.weekday()]}</b><span>{fmt(d)} · D{n} · semana {week} do aquário</span></div>
        <div class="chips">{chips(items)}</div>
      </div>
      {note_html}
      <div class="dg">
        <div class="r"><b>Água</b><span>manhã {blank(10, '°C')}</span><span>noite {blank(10, '°C')}</span><span>máx. {blank(10, '°C')}</span><span class="sepv"></span><b>Cômodo</b><span>{blank(10, '°C')}</span><span class="sepv"></span><span>{box('luz ok')}</span></div>
        <div class="r"><b>Betta</b><span>manhã {box('R')}{box('C')}{box('V')}</span><span>noite {box('R')}{box('C')}{box('V')}</span><span>{box('jejum')}</span><span class="sepv"></span><b>Camarões</b><span>{box('ração')}{box('legume')}{box('nada')}</span></div>
        <div class="r"><b>Betta</b><span>ânimo {circles()}</span><span>cor {circles()}</span><span>{box('ninho')}</span><span class="sepv"></span><b>Camarões</b><span>vistos {blank(8)}</span><span>ovadas {blank(6)}</span><span>{box('mudas')}{box('filhotes')}</span></div>
        <div class="r"><b>Plantas</b><span>{box('folha nova')}{box('derreteu')}{box('poda')}{box('emersas ok')}</span><span class="sepv"></span><b>Algas</b><span class="sc"><i>0</i><i>1</i><i>2</i><i>3</i></span><span class="sepv"></span><b>TPA</b><span>{blank(8, '%')}</span><span>{box('evaporação')}</span></div>
      </div>
      <div class="dt"><span>NH₃</span><span>NO₂</span><span>NO₃</span><span>pH</span><span>GH</span><span>KH</span><span>TDS</span><div class="gen"><b>O dia</b>{circles()}<span>{box('foto')}</span></div></div>
      <div class="dl"></div>
    </div>'''


def month_notes_block():
    return '''    <div class="day mnotes">
      <div class="dh"><span class="dn">+</span><div class="dm"><b>Notas do mês</b><span>o que não coube nos dias</span></div></div>
      <div class="dl"></div>
    </div>'''


def mini_cal(year, month, M, big=False):
    first = dt.date(year, month, 1)
    start = first - dt.timedelta(days=first.weekday())
    cells = ''.join(f'<th>{s}</th>' for s in SEM_CURTO)
    rows = ''
    d = start
    while True:
        row = ''
        for _ in range(7):
            if d.month != month:
                row += '<td class="off"></td>'
            else:
                kinds = {k for k, _, _ in M.get(d, [])}
                dots = ''.join(f'<i class="k{k}"></i>' for k in 'mfaebsp' if k in kinds)
                dn = f'<small>D{dnum(d)}</small>' if big else ''
                row += f'<td><span>{d.day}</span>{dn}<em>{dots}</em></td>'
            d += dt.timedelta(days=1)
        rows += f'<tr>{row}</tr>'
        if d.month != month and d > first:
            break
    cls = 'cal big' if big else 'cal'
    return f'<table class="{cls}"><thead><tr>{cells}</tr></thead><tbody>{rows}</tbody></table>'


LEGEND = ('<div class="legend"><span><i class="km"></i>marco</span><span><i class="kf"></i>fase da ciclagem</span>'
          '<span><i class="ka"></i>camarões</span><span><i class="kb"></i>betta</span><span><i class="ke"></i>emersas</span>'
          '<span><i class="kp"></i>pastilhas</span><span><i class="ks"></i>data especial</span></div>')


def month_open(m, M):
    first = dt.date(YEAR, m, 1)
    last = dt.date(YEAR + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
    ms = [(d, it) for d, its in sorted(M.items()) if d.month == m for it in its if it[0] not in 'tw']
    lst = ''.join(f'<li><b>{fmt_curto(d)}</b> {lab}</li>' for d, (k, lab, t) in ms) or '<li>Nenhum marco impresso: é um mês de rotina.</li>'
    band = (f'<figure class="mband"><img src="img/diario/mes-{m:02d}.jpg" alt="Foto de abertura de {MESES[m - 1]}"></figure>'
            f'<p class="mcr"><span class="cr" data-cr="img/diario/mes-{m:02d}.jpg"></span></p>')
    body = f'''    <header>
      <p class="eyebrow">Mês {m} do aquário · D{dnum(first)} a D{dnum(last)}</p>
      <h2 class="h1 mtitle">{MESES[m - 1].capitalize()} <span>{YEAR}</span></h2>
      <p class="deck">{ESPERAR[m]}</p>
    </header>
    {mini_cal(YEAR, m, M, big=True)}
    {LEGEND}
    <div class="grid2">
      <div>
        <h3 class="h3">Marcos do mês</h3>
        <ul class="dash small">{lst}</ul>
        <h3 class="h3">Metas do mês</h3>
        <div class="lines5"></div>
      </div>
      <div class="photo"><span>Cole aqui a foto do começo do mês<br><small>sempre do mesmo ângulo, de frente</small></span></div>
    </div>'''
    html = page(f'mes-{m:02d}', m, MESES[m - 1].capitalize(), body, 'mopen')
    return html.replace('\n  <div class="frame">', band + '\n  <div class="frame">', 1)


def chart(title, ylabels, days, unit):
    rows = len(ylabels)
    y = ''.join(f'<span>{v}</span>' for v in ylabels)
    x = ''.join(f'<span>{i}</span>' for i in range(1, days + 1))
    return f'''<div class="chart"><h4>{title} <small>{unit}</small></h4>
      <div class="cg"><div class="cy">{y}</div><div class="cplot" style="--cols:{days}; --rows:{rows - 1}"></div><div class="cx" style="--cols:{days}">{x}</div></div></div>'''


def month_close(m):
    days = (dt.date(YEAR + (m == 12), m % 12 + 1, 1) - dt.date(YEAR, m, 1)).days
    body = f'''    <header>
      <p class="eyebrow">Fechamento do mês</p>
      <h2 class="h1">{MESES[m - 1].capitalize()} em resumo</h2>
    </header>
    {chart('Temperatura da água, dia a dia', [32, 30, 28, 26, 24, 22, 20], days, 'um ponto por dia, em °C; ligue os pontos')}
    {chart('Nitrato nos dias de teste', [40, 30, 20, 10, 0], days, 'mg/L; alvo até 20')}
    <div class="grid2 sumgrid">
      <div class="sf"><h4>Camarões</h4><p>no início {blank(10)} no fim {blank(10)}</p><p>ovadas vistas {blank(10)} perdas {blank(10)}</p></div>
      <div class="sf"><h4>Trocas parciais</h4><p>quantas {blank(10)} litros trocados {blank(12)}</p><p>algas, de 0 a 3 {blank(10)}</p></div>
      <div class="sf"><h4>Plantas</h4><div class="lines3"></div></div>
      <div class="sf"><h4>Betta</h4><div class="lines3"></div></div>
      <div class="sf"><h4>Compras e gastos</h4><div class="lines3"></div><p>total R$ {blank(20)}</p></div>
      <div class="sf"><h4>O melhor momento do mês</h4><div class="lines3"></div></div>
    </div>
    <div class="sf wide"><h4>O que aprendi e o que muda no mês que vem</h4><div class="lines3"></div></div>
    <div class="grade"><b>Nota do mês</b>{circles()}</div>'''
    return page(f'fim-{m:02d}', m, f'{MESES[m - 1].capitalize()}: fechamento', body, 'mclose')


def front(M):
    out = []
    out.append('''<section class="page recto diario cover-d nochrome" id="capa-d" style="--accent:var(--agua-claro)">
  <div class="cd-top"><p class="cv-eyebrow">Vinte litros de mundo · volume 2</p></div>
  <h1 class="cd-title">Diário<br>2027</h1>
  <figure class="cd-photo"><img src="img/diario/capa.jpg" alt="Betta de nadadeiras longas"></figure>
  <p class="cd-cr"><span class="cr" data-cr="img/diario/capa.jpg"></span></p>
  <p class="cd-deck">Um ano de aquário, dia a dia: de 1º de janeiro, quando o vidro recebe a primeira pedra, a 31 de dezembro.</p>
  <dl class="cd-own"><div><dt>Aquário de</dt><dd></dd></div><div><dt>Montado em</dt><dd>1º de janeiro de 2027</dd></div><div><dt>Nome do betta</dt><dd></dd></div></dl>
</section>''')
    # como usar
    body = '''    <header>
      <p class="eyebrow">Antes de começar</p>
      <h2 class="h1">Como usar este diário</h2>
      <p class="deck">Uma página para cada dois dias. Os campos fixos levam um minuto; as linhas são para o que você quiser contar.</p>
    </header>
    <div class="grid2">
      <div class="runin">
        <p><span class="lead">D1, D2, D3…</span> Cada dia traz a data e o “dia do aquário”: D1 é 1º de janeiro, o dia da montagem. O guia fala em semanas desde a montagem — é só conferir aqui.</p>
        <p><span class="lead">Marcos impressos.</span> Os dias importantes já vêm marcados: fases da ciclagem, teste de conclusão, janelas dos camarões e do betta, pastilhas, dias de teste e de troca parcial. São estimativas: se o seu ciclo fechar antes ou depois, risque e anote a data real.</p>
        <p><span class="lead">Um mês de cada vez.</span> Cada mês abre com um calendário, os marcos e um lugar para a foto; e fecha com gráficos para preencher à mão e um resumo.</p>
        <p><span class="lead">A tabela semanal</span> das páginas seguintes é para plastificar e deixar ao lado do aquário: ela resolve a rotina, e o diário fica com as histórias.</p>
        <p><span class="lead">Dia sem nada?</span> Deixe em branco. Um diário com buracos ainda conta a história do ano.</p>
      </div>
      <div>
        <h3 class="h3" style="margin-top:0">Os campos de cada dia</h3>
        <table class="t tight">
          <tbody>
            <tr><td>Água</td><td>temperatura de manhã, à noite e a máxima, se tiver termômetro de máxima; e a do cômodo.</td></tr>
            <tr><td>Betta</td><td>R ração, C congelado, V vivo; ânimo e cor de 1 a 5; ninho de bolhas.</td></tr>
            <tr><td>Camarões</td><td>o que comeram; quantos você viu; ovadas; mudas e filhotes.</td></tr>
            <tr><td>Plantas</td><td>folha nova, derretimento, poda e as emersas.</td></tr>
            <tr><td>Algas</td><td>0 nenhuma, 1 pontos, 2 visível, 3 incomoda.</td></tr>
            <tr><td>TPA</td><td>porcentagem trocada e evaporação reposta.</td></tr>
            <tr><td>Testes</td><td>só nos dias de teste; o resto fica em branco.</td></tr>
            <tr><td>O dia</td><td>uma nota geral, de 1 a 5, e se você tirou foto.</td></tr>
          </tbody>
        </table>
        <h3 class="h3">As etiquetas</h3>
        <p class="small" style="text-indent:0"><span class="chip cm">Marco</span> <span class="chip cf">Ciclagem</span> <span class="chip ca">Camarões</span> <span class="chip cb">Betta</span> <span class="chip ce">Emersas</span> <span class="chip cp">Pastilhas</span> <span class="chip cs">Data especial</span> <span class="chip ct">Teste</span> <span class="chip cw">TPA</span></p>
        <div class="note fit" style="margin-top:3mm"><span class="lbl">Alvos do aquário</span>24 a 26 °C · pH 6,8 a 7,5 · GH 6 a 8 · KH 2 a 5 · TDS 150 a 250 ppm · amônia e nitrito 0 · nitrato até 20 mg/L.</div>
      </div>
    </div>'''
    out.append(page('como-usar', 0, 'Como usar', body))
    # o ano
    cals = ''.join(f'<div class="ym"><h4>{MESES[m - 1].capitalize()}</h4>{mini_cal(YEAR, m, M)}</div>' for m in range(1, 13))
    body = f'''    <header>
      <p class="eyebrow">Visão geral</p>
      <h2 class="h1">O ano do aquário</h2>
      <p class="deck">Os marcos de 2027 num relance. As datas seguem o cronograma do guia a partir da montagem em 1º de janeiro.</p>
    </header>
    <div class="year">{cals}</div>
    {LEGEND}
    <table class="t tight"><tbody>
      <tr><td>01/01 · D1</td><td>Montagem e início da ciclagem; mudas emersas para enraizar.</td></tr>
      <tr><td>05/02 · D36</td><td>Teste de conclusão da ciclagem; TPA de 50% quando confirmar.</td></tr>
      <tr><td>12 a 26/02</td><td>Janela dos camarões (semanas 7 a 9).</td></tr>
      <tr><td>12/03 a 09/04</td><td>Janela do betta (semanas 10 a 14). Com quarentena, compre a partir de 26/02.</td></tr>
      <tr><td>10/04 · D100</td><td>Cem dias de aquário.</td></tr>
      <tr><td>01/03, 01/05, 01/07, 01/09, 01/11</td><td>Repor as pastilhas fertilizantes e revisar os equipamentos.</td></tr>
      <tr><td>A cada dois dias até 11/02</td><td>Teste de amônia e nitrito, durante a ciclagem.</td></tr>
      <tr><td>Sábados, a partir de 13/02</td><td>Troca parcial de 10 a 20%.</td></tr>
      <tr><td>Domingos alternados, a partir de 14/02</td><td>Teste de nitrato, GH e TDS.</td></tr>
      <tr><td>31/12 · D365</td><td>Um ano de aquário: revisão do ano no fim do diário.</td></tr>
    </tbody></table>'''
    out.append(page('ano', 0, 'O ano do aquário', body))
    # ficha
    rows = lambda labels: ''.join(f'<tr><td>{l}</td><td></td></tr>' for l in labels)
    body = f'''    <header>
      <p class="eyebrow">Para consultar o ano todo</p>
      <h2 class="h1">Ficha do aquário</h2>
    </header>
    <div class="grid2">
      <div>
        <h3 class="h3" style="margin-top:0">A água da torneira, já condicionada</h3>
        <table class="t form"><tbody>{rows(['Data da medição', 'pH', 'GH', 'KH', 'TDS', 'Condicionador usado'])}</tbody></table>
        <h3 class="h3">Equipamentos</h3>
        <table class="t form"><tbody>{rows(['Filtro', 'Compressor', 'Aquecedor', 'Termômetro', 'Luminária e timer', 'Horário da luz', 'Substrato', 'Fertilizantes', 'Testes'])}</tbody></table>
      </div>
      <div>
        <h3 class="h3" style="margin-top:0">Contatos</h3>
        <table class="t form"><tbody>{rows(['Loja de aquarismo', 'Criador de camarões', 'Criador do betta', 'Veterinário de peixes', 'Quem cuida nas viagens'])}</tbody></table>
        <h3 class="h3">Plantas que entraram</h3>
        <table class="t form grid3"><thead><tr><th>Data</th><th>Planta</th><th>Onde comprou</th></tr></thead><tbody>{''.join('<tr><td></td><td></td><td></td></tr>' for _ in range(10))}</tbody></table>
      </div>
    </div>
    <div>
      <h3 class="h3">Animais</h3>
      <table class="t form grid3"><thead><tr><th style="width:22mm">Data</th><th>Animal e linhagem</th><th style="width:22mm">Quantos</th><th>Origem e preço</th><th>Observações</th></tr></thead><tbody>{''.join('<tr><td></td><td></td><td></td><td></td><td></td></tr>' for _ in range(10))}</tbody></table>
    </div>'''
    out.append(page('ficha', 0, 'Ficha do aquário', body))
    return out


def back_matter():
    out = []
    body = f'''    <header>
      <p class="eyebrow">31 de dezembro</p>
      <h2 class="h1">2027, o ano do aquário</h2>
      <p class="deck">Releia janeiro antes de preencher. A diferença entre as duas fotos é o que este ano construiu.</p>
    </header>
    <div class="grid2">
      <div class="photo"><span>Foto de 1º de janeiro</span></div>
      <div class="photo"><span>Foto de 31 de dezembro</span></div>
    </div>
    <div class="grid2 sumgrid">
      <div class="sf"><h4>Em números</h4>
        <p>trocas parciais {blank(14)} litros trocados {blank(14)}</p>
        <p>camarões no começo {blank(10)} hoje {blank(10)}</p>
        <p>gerações de camarões {blank(10)} gasto total R$ {blank(18)}</p>
        <p>dias anotados {blank(12)} fotos tiradas {blank(12)}</p></div>
      <div class="sf"><h4>O melhor mês, e por quê</h4><div class="lines3"></div></div>
      <div class="sf"><h4>O que deu errado e como resolvi</h4><div class="lines3"></div></div>
      <div class="sf"><h4>O que eu faria diferente</h4><div class="lines3"></div></div>
    </div>
    <div><h3 class="h3">Linha do tempo: uma frase por mês</h3>
    <table class="t tl"><tbody>{''.join(f'<tr><td>{m.capitalize()}</td><td></td></tr>' for m in MESES)}</tbody></table></div>'''
    out.append(page('revisao', 0, 'Revisão do ano', body))
    body = '''    <header>
      <p class="eyebrow">Revisão do ano</p>
      <h2 class="h1">Planos para 2028</h2>
    </header>
    <div class="grid2 sumgrid">
      <div class="sf"><h4>Plantas para experimentar</h4><div class="lines5"></div></div>
      <div class="sf"><h4>Mudanças no aquário</h4><div class="lines5"></div></div>
      <div class="sf"><h4>O que aprender</h4><div class="lines5"></div></div>
      <div class="sf"><h4>Um segundo aquário?</h4><div class="lines5"></div></div>
    </div>
    <div class="sf wide"><h4>Um recado para quem vai ler este diário daqui a um ano</h4><div class="lines8"></div></div>'''
    out.append(page('planos', 0, 'Planos para 2028', body))
    body = '''    <header>
      <p class="eyebrow">Créditos</p>
      <h2 class="h1">Fotos deste diário</h2>
      <p class="deck">Todas as fotos são de uso livre, com as licenças indicadas. Licenças NC permitem apenas uso não comercial; este diário é para uso pessoal.</p>
    </header>
    <div class="credits c3"><!--#credits--></div>'''
    out.append(page('creditos-d', 0, 'Créditos', body))
    return out


def head():
    s = open(os.path.join(SRC, 'guia', 'head.html'), encoding='utf-8').read()
    s = re.sub(r'<title>.*?</title>', '<title>Diário 2027 — Vinte litros de mundo</title>', s)
    css = open(os.path.join(HERE, 'diario.css'), encoding='utf-8').read()
    return s.replace('</head>', f'<style>\n{css}\n</style>\n</head>')


def main():
    M = marcos()
    if os.path.isdir(PAGES):
        shutil.rmtree(PAGES)
    os.makedirs(PAGES)
    # os desenhos vêm do guia
    svg = os.path.join(HERE, 'svg')
    if os.path.isdir(svg):
        shutil.rmtree(svg)
    shutil.copytree(os.path.join(SRC, 'guia', 'svg'), svg)
    open(os.path.join(HERE, 'head.html'), 'w', encoding='utf-8').write(head())
    seq = front(M)
    seq.append('<!--#include shared/semanal.html-->')
    for m in range(1, 13):
        seq.append(month_open(m, M))
        d = dt.date(YEAR, m, 1)
        blocks = []
        while d.month == m:
            blocks.append(day_block(d, M))
            d += dt.timedelta(days=1)
        if len(blocks) % 2:
            blocks.append(month_notes_block())
        for i in range(0, len(blocks), 2):
            first = dt.date(YEAR, m, i + 1)
            seq.append(page(f'd-{m:02d}-{i + 1:02d}', m, f'{MESES[m - 1].capitalize()}', blocks[i] + '\n' + blocks[i + 1], 'dias'))
        seq.append(month_close(m))
    seq += back_matter()
    for i, html in enumerate(seq):
        open(os.path.join(PAGES, f'{i:04d}.html'), 'w', encoding='utf-8').write(html)
    print('diário:', len(seq), 'páginas geradas')


if __name__ == '__main__':
    main()
