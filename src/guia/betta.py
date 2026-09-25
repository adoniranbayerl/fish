"""Capítulo do betta: anatomia, caudas, cores, selvagens, comportamento, saúde."""
from kit import page, header, card, grid, meter, write

CH, RH, AC = 8, 'Etapa 8: betta', 'var(--betta)'
EY = 'Etapa 8 de 9'


def anatomia():
    body = header(EY, 'Anatomia: um corpo feito para a água parada',
                  'Cada nadadeira tem uma função, e é a seleção feita pelos criadores sobre elas que dá origem às dezenas de formatos à venda.')
    body += '''
    <figure class="fig bigfish" style="margin:-2mm 0 0"><!--#svg anatomia--><figcaption>Um macho <i>halfmoon</i>, a forma mais conhecida hoje. O labirinto fica dentro da cabeça, acima das brânquias.</figcaption></figure>
    <div class="cols runin">
      <p><span class="lead">Dorsal.</span> A nadadeira de cima funciona como quilha: dá estabilidade e evita que o peixe role. Nos selvagens é pequena; nos de linhagem, pode ser maior que o próprio corpo.</p>
      <p><span class="lead">Caudal.</span> É o motor. Presa ao pedúnculo — a parte estreita antes da cauda —, é sustentada por raios que se ramificam. O número de ramificações e o ângulo de abertura definem a maior parte das “raças”.</p>
      <p><span class="lead">Anal.</span> A longa nadadeira de baixo, que vai do ventre à cauda. Equilibra a dorsal e, no macho, envolve a fêmea no abraço da desova.</p>
      <p><span class="lead">Ventrais e peitorais.</span> As ventrais, finas e compridas, pendem sob a cabeça e funcionam como antenas: o betta as usa para tatear o fundo e as plantas. As peitorais, transparentes, batem sem parar e fazem as manobras finas. Nos <i>dumbo</i>, elas são enormes.</p>
      <p><span class="lead">Opérculo.</span> A tampa das brânquias. Quando o macho a abre e eriça as nadadeiras, está fazendo o <i>flare</i>, a exibição de ameaça (p. {{pg:bt-comport}}).</p>
      <p><span class="lead">Labirinto.</span> Um órgão de lâminas ósseas cobertas de vasos sanguíneos, acima das brânquias. Com ele o betta engole ar na superfície e absorve o oxigênio. Ele <i>precisa</i> dessa respiração: um betta sem acesso à superfície se afoga.</p>
      <p><span class="lead">Escamas e cor.</span> A cor vem de quatro camadas de células sob a pele — preta, vermelha, amarela e iridescente —, e cada linhagem liga, desliga ou mistura essas camadas (p. {{pg:bt-cores3}}).</p>
      <div class="note why keep"><span class="lbl">Macho ou fêmea?</span>
        <div class="duo" style="margin:1mm 0 1.4mm"><div><!--#svg tail-halfmoon--></div><div><!--#svg femea--></div></div>
        <ul class="dash">
          <li><b>Macho:</b> nadadeiras maiores e mais coloridas, corpo mais longo, “barba” escura (a membrana sob o opérculo) bem visível, constrói ninhos.</li>
          <li><b>Fêmea:</b> corpo mais curto e barriga cheia, nadadeiras curtas, um pontinho branco entre as ventrais (o ovipositor) e, com frequência, listras verticais.</li>
          <li>Machos <i>plakat</i> jovens são facilmente confundidos com fêmeas: compare a barba e o ovipositor.</li>
        </ul>
      </div>
    </div>'''
    write('25a-bt-anat.html', page('bt-anat', CH, RH, AC, body, src='betta.py'))


def caudas1():
    body = header(EY, 'Caudas longas: do véu ao halfmoon',
                  'Os nomes descrevem a cauda aberta ao máximo, no flare. Quanto maior e mais ramificada, mais bonita na foto — e mais pesada para o peixe carregar.')
    body += '''
    <div class="spreads">
      <figure class="fig"><!--#svg spread-100--></figure>
      <figure class="fig"><!--#svg spread-130--></figure>
      <figure class="fig"><!--#svg spread-165--></figure>
      <figure class="fig"><!--#svg spread-180--></figure>
      <figure class="fig"><!--#svg spread-215--></figure>
    </div>
    <p class="small" style="margin-top:-3mm">Abertura da cauda, medida no flare: de menos de 130° (véu, delta) a mais de 180° (<i>over-halfmoon</i>).</p>'''
    cards = [
        card('betta/cauda-veu.jpg', 'Cauda-véu', 'veiltail · VT',
             'O betta “pet” clássico, o mais vendido em lojas no Brasil. A caudal é longa, assimétrica e cai para baixo como um véu; a dorsal também é comprida. Foi a primeira forma de nadadeira longa fixada pelos criadores.',
             f'Correnteza: fraca · Caça: {meter(1)}', 'tail-veu'),
        card('betta/delta.jpg', 'Delta e super delta', 'D · SD',
             'Cauda simétrica, em leque triangular, com bordas retas. No delta ela abre bem menos que 180°; no super delta chega perto disso. São a etapa intermediária entre o véu e o halfmoon.',
             f'Correnteza: fraca · Caça: {meter(1)}', 'tail-superdelta'),
        card('betta/halfmoon.jpg', 'Halfmoon', 'meia-lua · HM',
             'Cauda em “D” perfeito de 180°, com bordas retas, e dorsal e anal enormes. Desenvolvido por criadores dos EUA nos anos 1980 e 1990, virou o padrão das competições. Sujeito a rasgos e a morder a própria cauda.',
             f'Correnteza: mínima · Caça: {meter(1)}', 'tail-halfmoon'),
        card('betta/over-halfmoon.jpg', 'Over-halfmoon', 'OHM',
             'Um halfmoon que passa dos 180°: as bordas da cauda se sobrepõem às da dorsal e da anal. É a mesma linhagem, só que levada ao extremo — ainda mais nadadeira para o mesmo corpo.',
             f'Correnteza: mínima · Caça: {meter(1)}', 'tail-ohm'),
        card('betta/rosetail.jpg', 'Rosetail e feathertail', 'rosa · pena',
             'Halfmoons com ramificação excessiva dos raios: a borda fica ondulada como pétalas (rosetail) ou serrilhada como pena (feathertail). Bonitos, mas de nadadeiras quebradiças; muitos criadores evitam a linha.',
             f'Correnteza: mínima · Caça: {meter(1)}', 'tail-rosetail'),
        card('betta/double-tail.jpg', 'Double tail', 'cauda dupla · DT',
             'Uma mutação divide a caudal em dois lobos e deixa a dorsal quase tão larga quanto a anal. O corpo costuma ser mais curto, o que favorece problemas de flutuação: evite superalimentar.',
             f'Correnteza: fraca · Caça: {meter(1)}', 'tail-doubletail'),
    ]
    body += '\n' + grid(cards)
    body += '''
    <div class="grid2">
      <div class="note why"><span class="lbl">Por quê? Mais nadadeira, mais cuidado</span>Nadadeiras longas encharcadas pesam. O peixe nada menos, descansa mais e fica sujeito a rasgos — o <i>blowout</i>, quando a membrana se abre entre os raios. Folhas largas perto da superfície e correnteza mínima fazem toda a diferença.</div>
      <div class="note fit"><span class="lbl">No seu 40 × 20</span>Filtro de esponja com o ar regulado no mínimo que ainda mexe a superfície. Se o betta for arrastado ou evitar um lado do aquário, diminua a vazão ou aponte a saída para o vidro.</div>
    </div>'''
    write('25b-bt-caudas1.html', page('bt-caudas1', CH, RH, AC, body, src='betta.py'))


def caudas2():
    body = header(EY, 'Raios à mostra e caudas curtas',
                  'Nos crowntails, a membrana entre os raios encolhe; nos plakats, a nadadeira inteira volta ao tamanho do peixe selvagem.')
    cards = [
        card('betta/crowntail.jpg', 'Crowntail', 'coroa · CT',
             'Os raios ultrapassam a membrana e formam pontas, como uma coroa. Surgiu na Indonésia no fim dos anos 1990 e se espalhou depressa pelas lojas. As pontas enroscam em plantas e decorações ásperas.',
             f'Correnteza: fraca · Caça: {meter(2)}', 'tail-crowntail'),
        card('betta/combtail.jpg', 'Combtail', 'pente',
             'Uma versão discreta do crowntail: a membrana recua só um pouco e a borda parece um pente. Muitas vezes vem de cruzamentos entre crowntail e halfmoon ou delta.',
             f'Correnteza: fraca · Caça: {meter(1)}', 'tail-combtail'),
        card('betta/spadetail.jpg', 'Spadetail e roundtail', 'espada · redonda',
             'Duas formas antigas, hoje raras. No spadetail, a cauda se afunila numa ponta, como a espada do baralho; no roundtail, forma um leque arredondado, sem ângulos.',
             f'Correnteza: fraca · Caça: {meter(1)}', 'tail-spade'),
        card('betta/plakat.jpg', 'Plakat tradicional', 'PK',
             '<i>Pla kat</i> quer dizer “peixe que morde” em tailandês: é a forma de briga, próxima do selvagem, com nadadeiras curtas e arredondadas. Ágil, forte e o mais caçador de todos.',
             f'Correnteza: tolera · Caça: {meter(3)}', 'tail-plakat'),
        card('betta/halfmoon-plakat.jpg', 'Halfmoon plakat', 'HMPK',
             'Nadadeiras curtas, mas com a cauda em “D” de 180° e bordas retas. É hoje uma das formas mais populares entre criadores, porque junta o desenho do halfmoon à saúde das nadadeiras curtas.',
             f'Correnteza: tolera · Caça: {meter(3)}', 'tail-hmpk'),
        card('betta/crowntail-plakat.jpg', 'Crowntail plakat', 'CTPK',
             'O plakat com os raios da cauda saindo da membrana, em pontas curtas. Menos comum que o HMPK, mas cada vez mais visto em criadores brasileiros.',
             f'Correnteza: tolera · Caça: {meter(3)}', 'tail-ctpk'),
    ]
    body += '\n' + grid(cards)
    body += '''
    <div class="note why"><span class="lbl">Por quê? Curtas combinam com nanos</span>Nadadeiras longas pesam quando molhadas: o peixe nada menos, descansa mais e rasga a cauda com facilidade. Plakats vivem mais soltos — mas são exatamente os que mais caçam camarões.</div>'''
    write('25c-bt-caudas2.html', page('bt-caudas2', CH, RH, AC, body, src='betta.py'))


def porte():
    body = header(EY, 'Tamanhos especiais e qual formato escolher',
                  'Além da cauda, criadores selecionam o tamanho do corpo e das peitorais. Na tabela, todos os formatos lado a lado, pensando no seu 40 × 20.')
    cards = [
        card('betta/giant.jpg', 'Giant e king', 'gigante · rei',
             ['Linhagens selecionadas pelo porte. O <i>king</i> é um plakat grande, de uns 7 a 8 cm; o <i>giant</i> chega a 10 ou 12 cm e cresce mais tempo que um betta comum.',
              'Em 13 litros de água um giant ainda cabe, mas come mais, suja mais e caça camarões adultos com facilidade.'],
             f'Correnteza: tolera · Caça: {meter(3)}', 'tail-giant'),
        card('betta/dumbo.jpg', 'Dumbo', '<i>elephant ear</i> · EE',
             ['As peitorais crescem muito e costumam ser brancas: batem como orelhas de elefante. Aparece combinado com halfmoon (<i>dumbo HM</i>) ou plakat (<i>dumbo HMPK</i>).',
              'Nada como uma borboleta, devagar; prefere água quase parada e folhas largas para descansar.'],
             f'Correnteza: mínima · Caça: {meter(1)}', 'tail-dumbo'),
    ]
    body += '\n' + grid(cards, 'c2')
    rows = [
        ('Cauda-véu', 'lento', '●○○', '●○○', 'O mais fácil de achar e de manter.'),
        ('Delta / super delta', 'lento', '●○○', '●○○', 'Parecido com o véu, mais simétrico.'),
        ('Halfmoon / OHM', 'lento', '●○○', '●○○', 'Morde a cauda por estresse; folhas de descanso.'),
        ('Rosetail / feather', 'muito lento', '●○○', '●○○', 'Nadadeiras frágeis; evite para começar.'),
        ('Double tail', 'lento', '●○○', '●○○', 'Porções pequenas: tende a problemas de flutuação.'),
        ('Crowntail / combtail', 'médio', '●●○', '●●○', 'Retire tudo que for áspero ou pontudo.'),
        ('Plakat / HMPK / CTPK', 'rápido', '●●●', '●●●', 'O mais saudável; o maior risco para camarões.'),
        ('Giant / king', 'médio', '●●●', '●●●', 'Come e suja mais; caça adultos.'),
        ('Dumbo', 'muito lento', '●○○', '●○○', 'Água quase parada e folhas largas.'),
    ]
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td><td class="c">{meter(c.count("●"))}</td><td class="c">{meter(d.count("●"))}</td><td>{e}</td></tr>' for a, b, c, d, e in rows)
    body += f'''
    <div>
      <h3 class="h3">Qual combina com o seu aquário</h3>
      <table class="t tight"><thead><tr><th>Formato</th><th>Nado</th><th class="c">Tolera correnteza</th><th class="c">Risco aos camarões</th><th>Observação</th></tr></thead><tbody>{tr}</tbody></table>
    </div>
    <div class="note fit"><span class="lbl">No seu 40 × 20</span>Para conviver com uma colônia de camarões, um <b>cauda-véu</b>, <b>delta</b> ou <b>halfmoon</b> de temperamento calmo é a aposta mais segura. Se preferir um plakat, capriche no musgo e no tapete, e comece a colônia maior.</div>'''
    write('25d-bt-porte.html', page('bt-porte', CH, RH, AC, body, src='betta.py'))


def cores1():
    body = header(EY, 'Cores sólidas e metálicas',
                  'Um betta “sólido” tem a mesma cor no corpo e nas nadadeiras. Os nomes de mercado variam de criador para criador; estas são as famílias que você vai encontrar.')
    c = [
        ('vermelho', 'Vermelho', 'red', 'A cor mais comum e a mais antiga das linhagens. Um bom vermelho é uniforme, sem manchas azuladas no corpo.', 'cor-solido-vermelho'),
        ('azul', 'Azul royal e steel', 'royal · steel', 'Dois dos três azuis iridescentes: o royal, intenso e escuro; o steel, azul-acinzentado, quase metálico.', 'cor-solido-azul'),
        ('turquesa', 'Turquesa', 'turquoise · “verde”', 'O terceiro azul, puxado para o verde. Quase todo betta vendido como “verde” é um turquesa: o verde puro é raro.', 'cor-turquesa'),
        ('preto', 'Preto', 'melano · black lace', 'Pretos foscos e profundos. As fêmeas da linhagem melano costumam ser inférteis, por isso criadores usam outras linhas pretas para reproduzir.', 'cor-preto'),
        ('amarelo', 'Amarelo e pineapple', 'yellow · non-red', 'Um betta sem o pigmento vermelho. No <i>pineapple</i>, as escamas têm contorno escuro, como a casca de um abacaxi.', 'cor-amarelo'),
        ('laranja', 'Laranja', 'orange · tangerine', 'Laranja uniforme, do tangerina ao quase vermelho. Com pintinhas escuras, costuma ser vendido como <i>dalmata</i>.', 'cor-laranja'),
        ('branco', 'Branco opaco e platinum', 'opaque · platinum', 'Uma camada branca e fosca cobre as outras cores. No <i>platinum</i>, o branco tem brilho perolado.', 'cor-branco'),
        ('celofane', 'Celofane e pastel', 'cellophane · pastel', 'O celofane quase não tem pigmento: é translúcido e rosado, porque se vê a carne. Não é albino — o albino verdadeiro, de olhos vermelhos, é raríssimo.', 'cor-celofane'),
        ('cobre', 'Cobre, ouro e mustard gas', 'copper · gold · mustard', 'O brilho metálico veio de cruzamentos com espécies selvagens. O <i>mustard gas</i> tem corpo azul-escuro e nadadeiras amarelo-mostarda.', 'cor-mustard'),
    ]
    cards = [card(f'betta/cor-{k}.jpg', n, s, t, svg=sv) for k, n, s, t, sv in c]
    body += '\n' + grid(cards, 'flat')
    body += '''
    <div class="note why"><span class="lbl">Por quê? Escolha pela saúde, não pela cor</span>Cor não muda os cuidados: um betta vermelho e um <i>avatar</i> pedem a mesma água e a mesma comida. O que muda é o preço — e o risco de comprar por impulso um peixe abatido. Primeiro a saúde (p. {{pg:betta2}}); depois, a cor de que você mais gosta.</div>'''
    write('25e-bt-cores1.html', page('bt-cores1', CH, RH, AC, body, src='betta.py'))


def cores2():
    body = header(EY, 'Padrões: como as cores se distribuem',
                  'Os padrões combinam duas ou mais cores num desenho definido. Alguns, como o marble, mudam ao longo da vida do peixe.')
    c = [
        ('bicolor', 'Bicolor', 'bicolor', 'Corpo de uma cor e nadadeiras de outra — em geral corpo escuro e nadadeiras claras, ou o contrário.', 'cor-bicolor'),
        ('butterfly', 'Butterfly', 'borboleta', 'Faixas nítidas nas nadadeiras: a base da cor do corpo e a borda clara. O ideal é metade e metade, com a divisa bem marcada.', 'cor-butterfly'),
        ('multicolor', 'Multicolor e fancy', 'multicolor · fancy', 'Três cores ou mais, sem padrão fixo. Cada peixe é único — e raramente os filhotes saem iguais ao pai.', 'cor-multicolor'),
        ('marble', 'Marble', 'mármore', 'Manchas que aparecem, somem e mudam de lugar ao longo da vida, por causa de um gene “saltador”. O peixe que você compra não é o que você terá daqui a um ano.', 'cor-marble'),
        ('koi', 'Koi', 'koi · carpa', 'Um marble com manchas vermelhas, pretas e brancas, como as carpas japonesas. Por ser um marble, o desenho também muda com o tempo.', 'cor-koi'),
        ('galaxy', 'Nemo e galaxy', 'nemo · galaxy koi', 'Variações do koi: o <i>nemo</i> soma laranja e amarelo, como o peixe-palhaço; o <i>galaxy</i> tem pontos iridescentes azuis espalhados, como estrelas.', 'cor-galaxy'),
        ('dragon', 'Dragon scale', 'escama de dragão', 'Escamas grossas, opacas e metálicas, cada uma com o contorno marcado. Em alguns peixes, essa camada cresce sobre os olhos e compromete a visão.', 'cor-dragon'),
        ('cambodian', 'Cambodian', 'cambojano', 'Corpo claro, de celofane rosado, com nadadeiras vermelhas. É um dos padrões mais antigos do comércio.', 'cor-cambodian'),
        ('grizzle', 'Grizzle', 'pontilhado', 'Um salpicado fino de cor sobre fundo claro, como se as nadadeiras tivessem sido pintadas com spray.', 'cor-grizzle'),
    ]
    cards = [card(f'betta/cor-{k}.jpg', n, s, t, svg=sv) for k, n, s, t, sv in c]
    body += '\n' + grid(cards)
    write('25f-bt-cores2.html', page('bt-cores2', CH, RH, AC, body, src='betta.py'))


def cores3():
    body = header(EY, 'Nomes de vitrine e a genética da cor',
                  'Criadores batizam as linhagens com nomes chamativos, que mudam de país para país. Saber de onde vem a cor ajuda a entender o que você está comprando.')
    c = [
        ('mascarado', 'Mascarado', '<i>full mask</i>', 'A iridescência cobre também a cabeça, sem a “máscara” escura natural do rosto. Comum em azuis e turquesas.', 'cor-mascarado'),
        ('black-orchid', 'Black orchid', 'orquídea negra', 'Preto com iridescência azul-arroxeada nas nadadeiras, que forma estrias entre os raios.', 'cor-black-orchid'),
        ('samurai', 'Samurai', 'black samurai', 'Corpo preto com escamas metálicas contornadas, como uma armadura. Em geral, halfmoon plakat.', 'cor-samurai'),
        ('avatar', 'Avatar', 'avatar', 'Iridescência metálica azul-turquesa que cobre corpo e cabeça como uma armadura de escamas. As nadadeiras variam: escuras, vermelhas ou da mesma cor.', 'cor-avatar'),
        ('hellboy', 'Hellboy e red dragon', 'nomes de criador', 'Vermelhos escuros com escamas metálicas. Cada criador usa o nome para um peixe um pouco diferente: confie na foto, não no nome.', 'cor-hellboy'),
        ('alien', 'Alien', 'híbrido', 'Cruzamento de <i>B. splendens</i> com espécies selvagens (p. {{pg:bt-selvagens}}): corpo esverdeado e iridescência em escamas, nadadeiras curtas.', 'wild-mahachai'),
    ]
    cards = [card(f'betta/cor-{k}.jpg', n, s, t, svg=sv) for k, n, s, t, sv in c]
    body += '\n' + grid(cards, 'flat')
    body += '''
    <div class="grid2">
      <div class="runin">
        <h3 class="h3">De onde vem a cor</h3>
        <p>Sob a pele do betta há quatro camadas de células de pigmento: <b>preta</b> (melanóforos), <b>vermelha</b> (eritróforos), <b>amarela</b> (xantóforos) e <b>iridescente</b> (iridóforos, que refletem a luz e fazem os azuis, verdes e metálicos). Uma camada extra, <b>opaca</b>, dá o branco fosco. Tirar o vermelho deixa o peixe amarelo; tirar quase tudo deixa-o celofane; somar o opaco sobre o vermelho dá o rosa-pastel.</p>
        <p>Por isso as cores mudam com a luz, com o humor e com a idade — e por isso fotos de venda, tiradas com flash sobre fundo preto, nem sempre batem com o peixe em casa.</p>
      </div>
      <div>
        <h3 class="h3">Como ler um anúncio</h3>
        <div class="decode"><span>forma<b>HMPK</b></span><span>padrão<b>Nemo Galaxy Koi</b></span><span>sexo<b>♂</b></span><span>idade<b>4 meses</b></span></div>
        <p class="small" style="margin-top:2mm; text-indent:0">Leia assim: halfmoon plakat, padrão koi com laranja e pontos iridescentes, macho, quatro meses. Termos como <i>grade A</i> ou <i>show</i> indicam só a opinião do criador sobre a qualidade. Pergunte sempre a idade: bettas de loja muitas vezes já têm mais de um ano.</p>
        <div class="note warn" style="margin-top:3mm"><span class="lbl">Atenção: cor que some</span>Um betta que desbota em poucos dias está estressado ou doente — não é o padrão mudando. Só o marble e o koi mudam de verdade, e devagar, ao longo de meses.</div>
      </div>
    </div>'''
    write('25g-bt-cores3.html', page('bt-cores3', CH, RH, AC, body, src='betta.py'))


def selvagens():
    body = header(EY, 'Selvagens, híbridos e fêmeas',
                  'O <i>Betta splendens</i> faz parte de um pequeno grupo de espécies aparentadas, o “complexo splendens”. Algumas já aparecem em criadores brasileiros.')
    c = [
        ('splendens', '<i>Betta splendens</i> selvagem', 'Tailândia central e Camboja', 'Corpo verde-acastanhado e nadadeiras curtas com raios vermelhos. Só mostra cor forte quando excitado.', 'wild-splendens'),
        ('imbellis', '<i>Betta imbellis</i>', 'sul da Tailândia e Malásia', 'O “betta pacífico”: azul com a borda da cauda vermelha. Machos se toleram melhor que os de <i>splendens</i>, mas ainda brigam em espaço pequeno.', 'wild-imbellis'),
        ('smaragdina', '<i>Betta smaragdina</i>', 'nordeste da Tailândia e Laos', 'Escamas verde-esmeralda contornadas, como uma rede. Vive em arrozais e brejos rasos.', 'wild-smaragdina'),
        ('mahachaiensis', '<i>Betta mahachaiensis</i>', 'manguezais perto de Bangkok', 'Verde-azulado metálico. Vive em água levemente salobra, numa área minúscula ameaçada pela urbanização. Deu o brilho metálico às linhagens.', 'wild-mahachai'),
        ('siamorientalis', '<i>Betta siamorientalis</i>', 'leste da Tailândia e Camboja', 'Descrito só em 2012. Parecido com o <i>splendens</i> selvagem, com escamas esverdeadas e nadadeiras com vermelho e azul.', 'wild-splendens'),
        ('femea', 'Fêmea de <i>B. splendens</i>', 'qualquer linhagem', 'Menor, de nadadeiras curtas, tão colorida quanto o macho em muitas linhagens. Não é “mais calma”: fêmeas também brigam e defendem território.', 'femea'),
    ]
    cards = [card(f'betta/wild-{k}.jpg', n, s, t, svg=sv) for k, n, s, t, sv in c]
    body += '\n' + grid(cards, 'flat')
    body += '''
    <div class="grid2">
      <div class="note why"><span class="lbl">Por quê? Selvagem num nano</span>Um macho selvagem pode viver muito bem nos seus 20 litros — são peixes de poças rasas. Pedem água mais mole e ácida, com folhas de catappa, e são mais tímidos e caçadores que os de linhagem. Compre só de criadores, nunca peixes coletados sem procedência.</div>
      <div class="note warn"><span class="lbl">Atenção: “aquário comunitário de fêmeas”</span>Grupos de fêmeas, as <i>sororities</i>, exigem aquários grandes, muitas plantas e um plano B pronto. Em 20 litros, termina em brigas. Este aquário é para <b>um único betta</b>, macho ou fêmea.</div>
    </div>'''
    write('25h-bt-selvagens.html', page('bt-selvagens', CH, RH, AC, body, src='betta.py'))


def comportamento():
    body = header(EY, 'Linguagem corporal: o que o betta está dizendo',
                  'Bettas são expressivos. Cor, postura e nadadeiras mostram quase tudo — basta saber ler e comparar com o comportamento normal do seu peixe.')
    rows = [
        ('Opérculos abertos, nadadeiras eriçadas', 'Flare: ameaça a outro macho ou ao reflexo', 'Normal em doses curtas. Se for constante, reduza reflexos com fundo escuro e mais plantas.'),
        ('Ninho de bolhas na superfície', 'Macho maduro e confortável', 'Nada. Pode desmanchar na manutenção; ele refaz.'),
        ('Listras horizontais escuras no corpo', 'Estresse ou medo', 'Comum na chegada. Se durar dias, teste a água e procure a causa.'),
        ('Listras verticais claras (fêmea)', 'Fêmea pronta para desovar', 'Nada; some sozinha.'),
        ('Cores apagadas e nadadeiras fechadas', 'Água ruim, frio ou início de doença', 'Temperatura e testes antes de qualquer remédio (p. {{pg:bt-saude}}).'),
        ('Sobe e desce colado ao vidro', 'Tédio, reflexo ou incômodo com a água', 'Teste a água; mude algo de lugar; ofereça alimento vivo.'),
        ('Deitado numa folha ou no fundo', 'Descanso: bettas dormem, às vezes de lado', 'Normal por períodos. O dia inteiro deitado não é.'),
        ('Sobe à superfície com muita frequência', 'Pouco oxigênio ou água quente demais', 'Confira a temperatura; mexa um pouco mais a superfície.'),
        ('Cauda encurtando em poucos dias, com bordas lisas', 'Ele está mordendo a própria cauda', 'Mais abrigo e plantas, menos reflexos. Comum em halfmoons.'),
        ('Cospe a ração e come de novo', 'Amolecendo o grão', 'Normal. Se cuspir e largar, desconfie.'),
        ('Salta ou tenta saltar', 'Água nova, piora da água ou susto', 'Mantenha a tampa parcial e a folga de ar de 4 cm (p. {{pg:emersas}}).'),
    ]
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    body += f'''
    <div class="split" style="grid-template-columns:1fr 50mm">
      <table class="t tight"><thead><tr><th style="width:36%">O que você vê</th><th style="width:28%">O que significa</th><th>O que fazer</th></tr></thead><tbody>{tr}</tbody></table>
      <div class="stack">
        <figure class="fig"><!--#svg comp-flare--><figcaption><b>Flare.</b> O macho abre o opérculo e mostra a “barba” escura para parecer maior.</figcaption></figure>
        <figure class="fig"><!--#svg cor-estresse--><figcaption><b>Listras de estresse.</b> Faixas escuras horizontais, comuns nos primeiros dias.</figcaption></figure>
        <figure class="fig"><img src="img/betta/ninho.jpg" alt="Ninho de bolhas de betta na superfície"><figcaption>Ninho de bolhas junto às flutuantes. <span class="cr" data-cr="img/betta/ninho.jpg"></span></figcaption></figure>
      </div>
    </div>
    <div class="grid2">
    <div>
      <h3 class="h3">Sinais de um betta saudável</h3>
      <ul class="dash">
        <li>Vem à frente do vidro quando você chega e reconhece a hora da comida.</li>
        <li>Come tudo em poucos segundos e explora o aquário entre as refeições.</li>
        <li>Nadadeiras abertas na maior parte do tempo, sem bordas escuras.</li>
        <li>Cores firmes, que se intensificam quando ele se exibe.</li>
        <li>Barriga levemente arredondada depois das refeições.</li>
      </ul>
    </div>
    <div class="note why"><span class="lbl">Por quê? Um betta entediado adoece mais</span>Em aquários vazios, bettas ficam apáticos e mordem a cauda. Neste aquário, plantas, flutuantes e camarões já são estímulo. Some a isso: alimento vivo uma vez por semana, uma folha de catappa nova de vez em quando e, se quiser, um espelho por um ou dois minutos — nunca mais que isso.</div>
    </div>'''
    write('25i-bt-comport.html', page('bt-comport', CH, RH, AC, body, src='betta.py'))


def saude():
    body = header(EY, 'Saúde: reconhecer cedo, tratar à parte',
                  'Quase toda doença de betta começa com água ruim ou estresse. Descubra a causa antes do remédio — e nunca medique o aquário dos camarões.')
    rows = [
        ('Pó dourado ou cor de ferrugem, visível com lanterna', 'Velvet (<i>Piscinoodinium</i>)', 'Muito contagioso. Aquário-hospital, escuro e morno, com medicamento específico.'),
        ('Pontinhos brancos, como grãos de sal', 'Ictio (<i>Ichthyophthirius</i>)', 'Aquário-hospital; subir a temperatura aos poucos e medicar segundo o rótulo.'),
        ('Bordas escuras ou brancas que recuam', 'Podridão das nadadeiras (bactéria)', 'Água impecável: trocas frequentes no hospital. Antibiótico só se avançar sobre o corpo.'),
        ('Tufos de “algodão” no corpo ou na boca', 'Fungo ou columnaris (bactéria)', 'Isolar logo; tratamento específico. Columnaris é rápido e grave.'),
        ('Escamas eriçadas como pinha, barriga inchada', 'Hidropsia', 'É um sintoma de falência interna; prognóstico ruim. Isole e procure um veterinário de peixes.'),
        ('Nada torto, boia ou não consegue descer', 'Problema de flutuação, quase sempre constipação', 'Jejum de dois ou três dias; depois, dáfnia e porções menores.'),
        ('Olho saltado', 'Exoftalmia', 'Um olho: trauma, costuma sarar com água limpa. Os dois: infecção; trate à parte.'),
        ('Barriga funda mesmo comendo', 'Vermes ou outros parasitas internos', 'Isolar e tratar com vermífugo próprio para peixes.'),
        ('Rasgos limpos depois da manutenção', 'Ferimento em planta ou pedra', 'Água limpa; a nadadeira regenera em semanas. Procure a ponta que machucou.'),
    ]
    tr = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in rows)
    body += f'''
    <table class="t tight"><thead><tr><th style="width:34%">Sinal</th><th style="width:26%">Provável causa</th><th>O que fazer</th></tr></thead><tbody>{tr}</tbody></table>
    <div class="grid2">
      <div>
        <h3 class="h3">O aquário-hospital</h3>
        <ul class="dash">
          <li>Um recipiente de 5 a 10 litros, com tampa, aquecedor e um filtro de esponja pequeno ou uma pedra porosa bem fraca.</li>
          <li>Sem substrato nem decoração, para você enxergar tudo e sifonar com facilidade.</li>
          <li>Água do próprio aquário no primeiro dia; depois, trocas diárias com água nova condicionada, na mesma temperatura.</li>
          <li>Guarde-o limpo e seco: serve também para a quarentena e para emergências.</li>
        </ul>
        <h3 class="h3">Quarentena em cinco passos</h3>
        <ol class="steps">
          <li>Monte o hospital um dia antes, com água do aquário principal e o aquecedor ligado.</li>
          <li>Aclimate o betta no hospital, não no aquário dos camarões.</li>
          <li>Observe por 14 dias: apetite, fezes, cor, nadadeiras, respiração.</li>
          <li>Troque 25% da água a cada dois dias e anote tudo no diário.</li>
          <li>Sem nenhum sinal no fim do prazo, aclimate de novo e solte no aquário principal.</li>
        </ol>
      </div>
      <div class="stack">
        <div class="note warn"><span class="lbl">Atenção: remédios e camarões</span>Muitos remédios para peixes — e o sal de aquário — matam camarões ou as bactérias do filtro. Trate o betta sempre no hospital e só o devolva curado, depois de uma semana sem sinais.</div>
        <div class="note why"><span class="lbl">Por quê? Prevenir é quase tudo</span>Quarentena de duas semanas na chegada, trocas parciais regulares, temperatura estável e porções pequenas evitam a grande maioria dos casos. Na dúvida, procure um veterinário que atenda peixes: diagnósticos por foto erram muito.</div>
      </div>
    </div>'''
    write('25j-bt-saude.html', page('bt-saude', CH, RH, AC, body, src='betta.py'))


def main():
    anatomia(); caudas1(); caudas2(); porte(); cores1(); cores2(); cores3()
    selvagens(); comportamento(); saude()
