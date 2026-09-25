"""Flora: funções das plantas, alternativas e plantas emersas sobre o aquário."""
import os, re
from kit import page, header, card, grid, write, PAGES

CH, AC = 5, 'var(--musgo)'


def funcs_html(bio, est):
    li = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    return (f'<div class="funcs"><div><h4>Função biológica</h4><ul class="dash">{li(bio)}</ul></div>'
            f'<div><h4>Função estética</h4><ul class="dash">{li(est)}</ul></div></div>')


# ---------------------------------------------------------------- 8 fichas originais
FUNCS = {
    'fl-anubia': (['Folhas duráveis, cobertas de biofilme: pasto permanente para os camarões.',
                   'Cama do betta perto da superfície.'],
                  ['Folhas escuras e brilhantes que contrastam com o musgo claro.',
                   'Na escala ‘Petite’, parece uma planta grande em miniatura: aumenta a sensação de profundidade.']),
    'fl-samambaia': (['Absorve nitrato de forma constante, o ano todo.',
                      'Abrigo entre as folhas para camarões recém-mudados.'],
                     ['Volume e textura rendada no fundo.',
                      'Esconde filtro e aquecedor e suaviza as linhas da madeira.']),
    'fl-buce': (['Superfície de biofilme nas frestas das pedras.',
                 'Quase não disputa nutrientes: não atrapalha as outras plantas.'],
                ['Cor — do verde-azulado ao vinho — e brilho no primeiro plano.',
                 'Acabamento natural que integra pedra e planta.']),
    'fl-crypt': (['Raízes profundas que arejam o substrato e evitam bolsões sem oxigênio.',
                  'Consome os nutrientes do fundo, onde as algas não chegam.'],
                 ['Faz a transição entre a frente baixa e o fundo alto.',
                  'Folhas largas e bronzeadas contrastam com as folhas finas ao redor.']),
    'fl-hel': (['Cobre o substrato e vira berçário para filhotes de camarão.',
                'Raízes finas que trabalham a camada de cima do fundo.'],
                ['Gramado de primeiro plano que dá escala ao aquário.',
                 'Conduz o olhar da frente para a pedra principal.']),
    'fl-musgo': (['Berçário: biofilme e microfauna para filhotes de 1 a 2 mm.',
                  'Filtro mecânico fino, que segura partículas.'],
                 ['Envelhece o hardscape: pedras e galhos parecem estar ali há anos.',
                  'Suaviza bordas e une madeira, pedra e planta.']),
    'fl-rotala': (['A maior consumidora de nitrato do aquário submerso.',
                   'Compete com as algas nas primeiras semanas.'],
                  ['Fundo macio e cheio, com pontas rosadas sob luz mais forte.',
                   'Movimento: balança com a corrente suave do filtro.']),
    'fl-phyl': (['Retira nitrato depressa, com CO<sub>2</sub> do ar.',
                 'Sombra que reduz algas e acalma o betta.',
                 'Âncora para o ninho de bolhas.'],
                ['Vermelho na superfície: a única cor quente do projeto.',
                 'Desenha sombras e manchas de luz no fundo.']),
}


def add_funcs():
    for f in sorted(os.listdir(PAGES)):
        m = re.match(r'\d+-(fl-[\w-]+)\.html$', f)
        if not m or m.group(1) not in FUNCS:
            continue
        path = os.path.join(PAGES, f)
        s = open(path, encoding='utf-8').read()
        s = re.sub(r'\s*<div class="funcs">.*?</ul></div></div>', '', s, flags=re.S)
        block = funcs_html(*FUNCS[m.group(1)])
        s = s.replace('      </aside>', f'        {block}\n      </aside>', 1)
        open(path, 'w', encoding='utf-8').write(s)


# ---------------------------------------------------------------- alternativas
# (id, arquivo, planta original, id da original, nome, científico, para que serve,
#  ficha[dict], textos[list of (lead, text)], bio, est, diferença)
def dots(n):
    return '<span class="dots">' + ''.join('<i class="on"></i>' if i < n else '<i></i>' for i in range(5)) + '</span>'


ALTS = [
    dict(id='alt-anubia', orig='anúbia ‘Petite’', orig_id='fl-anubia',
         nome='Anúbia-nana comum e ‘Bonsai’', sci='<i>Anubias barteri</i> var. <i>nana</i> e cultivar ‘Bonsai’',
         serve='A mesma folha de descanso, em tamanhos que se acham em qualquer loja.',
         ficha=[('Origem', 'Camarões, na África Ocidental'), ('Tipo', 'Epífita de rizoma'),
                ('Posição', 'Meio, sobre pedras e madeira'), ('Altura', 'Nana 5 a 10 cm; ‘Bonsai’ 3 a 5 cm'),
                ('Crescimento', 'Muito lento'), ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'),
                ('Temperatura', '22 a 28 °C'), ('Dificuldade', dots(1) + 'muito fácil'),
                ('Quantidade', '1 muda de nana ou 2 a 3 de ‘Bonsai’')],
         txt=[('Na natureza', 'É a mesma espécie da ‘Petite’: a <i>nana</i> é a forma anã original, cultivada desde os anos 1970, e a ‘Bonsai’ é uma seleção compacta, de folhas mais arredondadas e muito próximas umas das outras.'),
              ('No aquário', 'Tudo o que vale para a ‘Petite’ vale aqui: folhas que duram anos, biofilme para os camarões e uma superfície larga onde o betta descansa. A diferença é a escala: a nana comum tem folhas de 3 a 5 cm, e um exemplar grande já ocupa o espaço de três ‘Petite’.'),
              ('Como plantar', 'Amarre ou cole o rizoma na pedra ou na madeira, nunca enterrado. Uma muda grande de nana pode ser dividida com tesoura em pedaços de três ou quatro folhas.'),
              ('Cuidados', 'Como cresce devagar, acumula algas em pontos nas folhas velhas: mantenha-a na meia-sombra e retire as folhas mais manchadas.')],
         bio=['Biofilme e descanso do betta, como a ‘Petite’.'], est=['Folhas maiores pedem posição mais ao fundo para não “achatar” a paisagem.'],
         dif='Use a nana comum no meio e no fundo, perto da samambaia; a ‘Bonsai’ ocupa exatamente o lugar da ‘Petite’, sobre a pedra principal.'),
    dict(id='alt-samambaia', orig='samambaia ‘Windeløv’', orig_id='fl-samambaia',
         nome='Samambaia-de-java comum e ‘Trident’', sci='<i>Leptochilus pteropus</i> e cultivar ‘Trident’',
         serve='Fundo verde e resistente, sem trabalho — com folhas mais simples ou mais finas.',
         ficha=[('Origem', 'Ásia tropical'), ('Tipo', 'Epífita de rizoma'), ('Posição', 'Fundo, sobre a madeira'),
                ('Altura', 'Comum 15 a 25 cm; ‘Trident’ 10 a 15 cm'), ('Crescimento', 'Lento'), ('Luz', 'Baixa'),
                ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '20 a 28 °C'), ('Dificuldade', dots(1) + 'muito fácil'),
                ('Quantidade', '1 rizoma')],
         txt=[('Na natureza', 'A forma comum, de folhas inteiras e lanceoladas, é a planta selvagem que cresce na beira de riachos e cachoeiras da Índia ao Sudeste Asiático. A ‘Trident’ é uma seleção de folhas estreitas, divididas em três a cinco lobos, como um tridente.'),
              ('No aquário', 'Mesma função da ‘Windeløv’: pano de fundo que esconde equipamentos, faz sombra e abriga os camarões. A comum é a mais fácil de encontrar, mas é grande para os 17 cm de água do seu aquário: escolha mudas pequenas e corte as folhas que encostarem na superfície.'),
              ('Como plantar', 'Amarre ou cole o rizoma na madeira; em semanas as raízes escuras se prendem sozinhas. Nunca enterre o rizoma.'),
              ('Cuidados', 'Pontinhos escuros organizados sob as folhas são soros, normais. Plantinhas-filhas nascem nas pontas das folhas e podem ser presas em outro galho.')],
         bio=['Absorve nitrato o ano todo e abriga camarões.'], est=['A ‘Trident’ dá textura fina, parecida com a da ‘Windeløv’; a comum, folhas largas e mais “selvagens”.'],
         dif='Prefira a ‘Trident’, cuja escala combina com o nano. A comum funciona se você podar as folhas mais longas a cada um ou dois meses.'),
    dict(id='alt-parva', orig='bucephalandra', orig_id='fl-buce',
         nome='Criptocoryne parva', sci='<i>Cryptocoryne parva</i>',
         serve='A menor das criptocorynes: detalhe verde e baixinho entre as pedras.',
         ficha=[('Origem', 'Sri Lanka (só existe lá)'), ('Tipo', 'Enraizada, em roseta'), ('Posição', 'Frente, junto às pedras'),
                ('Altura', '3 a 5 cm'), ('Crescimento', 'Muito lento'), ('Luz', 'Média; com pouca luz, estica'),
                ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '22 a 28 °C'), ('Dificuldade', dots(2) + 'fácil'),
                ('Quantidade', '1 vaso dividido em 6 a 10 mudas')],
         txt=[('Na natureza', 'Cresce em margens rasas de riachos do Sri Lanka, muitas vezes fora d’água parte do ano. É a menor espécie do gênero: raramente passa de 5 cm, com folhas estreitas e verde-vivas.'),
              ('No aquário', 'Não tem a cor nem o brilho da bucephalandra, mas ocupa o mesmo lugar: tufos pequenos nas frestas e na base das pedras, que dão acabamento ao hardscape. Também serve como alternativa ao tapete de helanthium, se plantada densa — só que leva meses para fechar.'),
              ('Como plantar', 'Ao contrário da bucephalandra, vai no substrato: separe as mudas e enterre as raízes com pinça, com a coroa rente ao fundo, a 2 cm uma da outra. Precisa do substrato fértil ou de pastilhas por perto.'),
              ('Cuidados', 'Como toda criptocoryne, pode “derreter” depois do plantio e rebrotar em semanas. Não mude de lugar.')],
         bio=['Raízes que arejam a frente do substrato.', 'Abrigo baixo para filhotes.'], est=['Tufos verdes e finos que ligam pedra e areia.'],
         dif='Vai no substrato, não presa à pedra. Plante-a no fértil junto às pedras da frente. Se preferir uma epífita, use mais anúbias ‘Petite’ ou ‘Bonsai’.'),
    dict(id='alt-lutea', orig='criptocoryne wendtii', orig_id='fl-crypt',
         nome='Criptocoryne lutea', sci='<i>Cryptocoryne walkeri</i>, vendida como ‘Lutea’',
         serve='Uma criptocoryne verde-clara e muito resistente para o meio do aquário.',
         ficha=[('Origem', 'Sri Lanka'), ('Tipo', 'Enraizada, em roseta'), ('Posição', 'Meio, em grupos'),
                ('Altura', '10 a 15 cm'), ('Crescimento', 'Lento a médio'), ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'),
                ('Temperatura', '20 a 28 °C'), ('Dificuldade', dots(1) + 'muito fácil'), ('Quantidade', '3 a 5 mudas')],
         txt=[('Na natureza', 'Vem de riachos das terras baixas do Sri Lanka. O nome comercial ‘Lutea’ (amarelada, em latim) vem do tom claro das folhas e do verso bronzeado; os botânicos hoje a tratam como uma forma de <i>C. walkeri</i>.'),
              ('No aquário', 'Folhas lanceoladas, verde-claras, um pouco mais estreitas que as da wendtii. É uma das criptocorynes que menos derretem, e forma touceiras firmes por estolões.'),
              ('Como plantar', 'Com a pinça, enterre as raízes e deixe a coroa rente ao substrato, em grupos de três a cinco, a 3 ou 4 cm uma da outra. Pastilhas no substrato inerte, a cada dois ou três meses.'),
              ('Cuidados', 'Depois de estabelecida, não mude de lugar. Retire folhas velhas pela base.')],
         bio=['Raízes profundas que trabalham o substrato.', 'Abrigo na base.'], est=['Verde mais claro que a wendtii: ilumina o meio do aquário.'],
         dif='Ocupa exatamente o lugar da wendtii, no meio do lado direito. Por ser mais clara, contrasta bem com a samambaia escura.'),
    dict(id='alt-beckettii', orig='criptocoryne wendtii', orig_id='fl-crypt',
         nome='Criptocoryne beckettii', sci='<i>Cryptocoryne beckettii</i>',
         serve='Tons de oliva e bronze para o meio, com o verso das folhas rosado.',
         ficha=[('Origem', 'Sri Lanka'), ('Tipo', 'Enraizada, em roseta'), ('Posição', 'Meio, em grupos'),
                ('Altura', '10 a 15 cm'), ('Crescimento', 'Lento'), ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'),
                ('Temperatura', '22 a 28 °C'), ('Dificuldade', dots(2) + 'fácil'), ('Quantidade', '3 a 5 mudas')],
         txt=[('Na natureza', 'Outra criptocoryne do Sri Lanka, de riachos com correnteza e fundo de areia. É uma das espécies mais antigas no aquarismo e forma populações densas por estolões.'),
              ('No aquário', 'Folhas onduladas, verde-oliva a bronze por cima e rosadas por baixo. Com luz baixa, fica mais verde e mais alta; com luz média, compacta e acobreada.'),
              ('Como plantar', 'Igual à wendtii: pinça, raízes enterradas, coroa rente. Grupos ímpares, a 3 ou 4 cm uma da outra.'),
              ('Cuidados', 'Derrete com facilidade depois do plantio e com mudanças bruscas. Paciência: rebrota das raízes.')],
         bio=['Arejamento do substrato e abrigo.'], est=['Cor quente no meio verde — faz eco ao vermelho da flutuante.'],
         dif='Mesmo lugar da wendtii. É um pouco mais sensível a mudanças: plante-a logo na montagem, para que derreta e se recupere ainda na ciclagem.'),
    dict(id='alt-sagittaria', orig='helanthium', orig_id='fl-hel',
         nome='Sagitária-anã', sci='<i>Sagittaria subulata</i>',
         serve='Um gramado de folhas finas que se espalha rápido e aguenta pouca luz.',
         ficha=[('Origem', 'Américas: costa leste dos EUA à América do Sul'), ('Tipo', 'Enraizada; tapete por estolões'),
                ('Posição', 'Primeiro plano'), ('Altura', '5 a 15 cm; mais baixa com mais luz'), ('Crescimento', 'Médio a rápido'),
                ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '20 a 28 °C'),
                ('Dificuldade', dots(1) + 'muito fácil'), ('Quantidade', '1 vaso ou copo, em 8 a 10 tufos')],
         txt=[('Na natureza', 'Vive em estuários, margens de rios e lagoas de água doce ou levemente salobra, do leste dos Estados Unidos à América do Sul. Submersa, forma folhas em fita; fora d’água, folhas em seta, o que deu nome ao gênero (<i>sagitta</i>, flecha).'),
              ('No aquário', 'Mais fácil e mais rápida que o helanthium: lança estolões sem parar e fecha a frente em poucos meses, mesmo sem CO<sub>2</sub>. As folhas são um pouco mais largas e mais escuras.'),
              ('Como plantar', 'Separe em tufos de duas ou três folhas e plante a cada 3 cm, com a coroa rente. Não enterre fundo.'),
              ('Cuidados', 'Com pouca luz, as folhas passam de 15 cm: corte as mais altas pela base. Retire os estolões que invadirem pedras e o musgo.')],
         bio=['Cobre o fundo e abriga filhotes.', 'Consome nutrientes do substrato e da água.'], est=['Gramado verde-escuro, mais rústico que o helanthium.'],
         dif='Ocupa a mesma frente esquerda. Cresce mais rápido — ótimo para fechar antes das algas —, mas pede podas de contenção a cada duas ou três semanas.'),
    dict(id='alt-staurogyne', orig='helanthium', orig_id='fl-hel',
         nome='Staurogyne repens', sci='<i>Staurogyne repens</i>, nativa do Brasil',
         serve='Um arbusto rasteiro e compacto para a frente — e uma planta brasileira.',
         ficha=[('Origem', 'Brasil, no Mato Grosso'), ('Tipo', 'Caule rasteiro'), ('Posição', 'Primeiro plano'),
                ('Altura', '5 a 10 cm'), ('Crescimento', 'Médio'), ('Luz', 'Média'), ('CO<sub>2</sub>', 'Dispensável; com ele, mais densa'),
                ('Temperatura', '20 a 28 °C'), ('Dificuldade', dots(2) + 'fácil'), ('Quantidade', '1 copo <i>in vitro</i> ou 6 a 8 hastes')],
         txt=[('Na natureza', 'Foi coletada em riachos de água clara do Mato Grosso e chegou ao aquarismo europeu nos anos 2000, onde virou uma das plantas de primeiro plano mais usadas do mundo.'),
              ('No aquário', 'Não forma um gramado, e sim um tapete baixo de folhas verde-vivas, que cresce para os lados por brotos laterais. Em vez da textura de grama, dá um ar de arbusto em miniatura.'),
              ('Como plantar', 'Separe as hastes e enterre a base de cada uma com pinça, a 2 ou 3 cm, com as folhas de baixo fora do substrato.'),
              ('Cuidados', 'Pede substrato fértil ou pastilhas e luz média. Pode com tesoura rente ao fundo para que brote mais baixa e cheia; replante os topos.')],
         bio=['Cobre o substrato e abriga filhotes.', 'Consome nutrientes do fundo.'], est=['Frente compacta, de folhas mais largas e verde-claro.'],
         dif='Mesmo lugar do helanthium. É ótima se você quiser uma planta nativa no projeto, mas fica mais bonita com podas regulares.'),
    dict(id='alt-christmas', orig='musgo-de-java', orig_id='fl-musgo',
         nome='Musgo Christmas', sci='<i>Vesicularia montagnei</i>',
         serve='Um musgo em forma de pinheirinho: berçário mais organizado e mais bonito.',
         ficha=[('Origem', 'Sudeste Asiático'), ('Tipo', 'Musgo'), ('Posição', 'Sobre galhos e pedras'),
                ('Altura', 'Camadas de 2 a 5 cm'), ('Crescimento', 'Lento'), ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'),
                ('Temperatura', '20 a 27 °C'), ('Dificuldade', dots(2) + 'fácil'), ('Quantidade', '1 porção')],
         txt=[('Na natureza', 'Vive sobre pedras e troncos úmidos na beira de riachos do Sudeste Asiático. O nome vem dos ramos, que se abrem em triângulos sobrepostos, como pinheirinhos de Natal.'),
              ('No aquário', 'Mais denso e mais organizado que o musgo-de-java, prende detritos e biofilme do mesmo jeito e é ainda mais difícil para o betta caçar lá dentro. Cresce mais devagar e prefere água abaixo de 27 °C.'),
              ('Como plantar', 'Camada fina, de 1 cm, amarrada com linha de algodão ou presa com pontos de cola sobre a madeira e a base das pedras.'),
              ('Cuidados', 'Apare quando engrossar e recolha os fragmentos. No verão, se a água passar de 28 °C, ele escurece: mantenha a temperatura estável.')],
         bio=['Berçário e alimento para filhotes.'], est=['Textura geométrica, que valoriza galhos finos.'],
         dif='Mesmo lugar do musgo-de-java. Por crescer mais devagar, compre uma porção um pouco maior.'),
    dict(id='alt-flame', orig='musgo-de-java', orig_id='fl-musgo',
         nome='Musgo Flame', sci='<i>Taxiphyllum</i> sp. ‘Flame’',
         serve='Um musgo que cresce para cima, em espirais como chamas.',
         ficha=[('Origem', 'Ásia'), ('Tipo', 'Musgo'), ('Posição', 'Galhos e base da madeira'),
                ('Altura', 'Chamas de 5 a 10 cm'), ('Crescimento', 'Lento'), ('Luz', 'Baixa a média'), ('CO<sub>2</sub>', 'Dispensável'),
                ('Temperatura', '20 a 28 °C'), ('Dificuldade', dots(2) + 'fácil'), ('Quantidade', '1 porção')],
         txt=[('Na natureza', 'Parente próximo do musgo-de-java, conhecido só no comércio. Em vez de se espalhar, cada ramo cresce na vertical e se torce, formando tufos que lembram labaredas.'),
              ('No aquário', 'Menos denso que o musgo-de-java, ainda abriga filhotes e acumula biofilme. O efeito é de pequenas árvores ou chamas saindo da madeira.'),
              ('Como plantar', 'Prenda pequenos tufos, espaçados, com cola ou linha, na parte de cima dos galhos e na base das pedras. Eles se erguem sozinhos.'),
              ('Cuidados', 'Não apare as pontas, ou o efeito de chama se perde: corte pela base os tufos que ficarem altos demais.')],
         bio=['Abrigo e biofilme, um pouco menos que o musgo-de-java.'], est=['Linhas verticais, que dão altura ao lado esquerdo.'],
         dif='Combine com um pouco de musgo-de-java ou Christmas na base das pedras: sozinho, ele protege menos os filhotes.'),
    dict(id='alt-ambulia', orig='rotala', orig_id='fl-rotala',
         nome='Ambulia', sci='<i>Limnophila sessiliflora</i>',
         serve='Uma planta de caule muito rápida, de folhas rendadas, que “come” nitrato.',
         ficha=[('Origem', 'Ásia tropical'), ('Tipo', 'Planta de caule'), ('Posição', 'Fundo, atrás da madeira'),
                ('Altura', '20 a 40 cm; pode-se a 15 cm'), ('Crescimento', 'Muito rápido'), ('Luz', 'Média'),
                ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '22 a 28 °C'), ('Dificuldade', dots(1) + 'muito fácil'),
                ('Quantidade', '5 a 7 hastes')],
         txt=[('Na natureza', 'Cresce em arrozais, valas e lagoas do sul e do sudeste da Ásia. Fora da região, onde foi solta, virou invasora — um bom lembrete de que sobras de poda nunca vão para rios ou lagos.'),
              ('No aquário', 'Folhas finamente divididas, em verticilos, como pequenos pinheiros verde-claros. Cresce mais rápido que a rotala e, por isso, consome ainda mais nitrato: é a planta mais “trabalhadora” desta lista.'),
              ('Como plantar', 'Retire as folhas dos 2 cm de baixo e enterre cada haste separada, a 2 cm uma da outra.'),
              ('Cuidados', 'Pode toda semana nas primeiras semanas: quando chega à superfície, deita e sombreia o resto. Replante os topos e descarte as bases.')],
         bio=['Consome muito nitrato; forte competidora das algas.', 'Oxigena de dia.'], est=['Fundo verde-claro, macio e rendado.'],
         dif='Use menos hastes que a rotala — ela cresce o dobro. Se a poda semanal virar trabalho demais, troque pela ludwigia.'),
    dict(id='alt-ludwigia', orig='rotala', orig_id='fl-rotala',
         nome='Ludwigia repens', sci='<i>Ludwigia repens</i>',
         serve='Uma planta de caule de folhas redondas, que avermelha com a luz.',
         ficha=[('Origem', 'América do Norte, América Central e Caribe'), ('Tipo', 'Planta de caule'), ('Posição', 'Fundo'),
                ('Altura', '20 a 30 cm; pode-se a 15 cm'), ('Crescimento', 'Médio'), ('Luz', 'Média; mais luz, mais vermelho'),
                ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '20 a 28 °C'), ('Dificuldade', dots(1) + 'muito fácil'),
                ('Quantidade', '6 a 8 hastes')],
         txt=[('Na natureza', 'Vive em margens de rios, lagoas e brejos, enraizada no fundo raso, com os ramos rastejando pela lama — daí o <i>repens</i>, “rasteira”.'),
              ('No aquário', 'Folhas opostas e arredondadas, verdes por cima e avermelhadas por baixo; com luz média e ferro, o topo inteiro fica cobre. Cresce mais devagar que a rotala e a ambulia, então dá menos trabalho de poda.'),
              ('Como plantar', 'Hastes separadas, sem as folhas dos 2 cm de baixo, enterradas com pinça a 2 cm uma da outra.'),
              ('Cuidados', 'Sem poda, a base perde folhas por falta de luz. Corte os topos e replante-os, formando uma moita escalonada.')],
         bio=['Consome nitrato de forma constante.', 'Oxigena de dia.'], est=['Cor quente no fundo e folhas redondas que contrastam com a samambaia.'],
         dif='Mesmo lugar da rotala, com metade do trabalho. O vermelho aparece mais perto da luz: deixe crescer até 3 ou 4 cm da superfície.'),
    dict(id='alt-egeria', orig='rotala', orig_id='fl-rotala',
         nome='Elódea-brasileira', sci='<i>Egeria densa</i>, nativa do Brasil',
         serve='A planta de caule mais fácil de achar no Brasil — e a mais barata.',
         ficha=[('Origem', 'Sudeste da América do Sul, inclusive o Brasil'), ('Tipo', 'Planta de caule'), ('Posição', 'Fundo'),
                ('Altura', 'Chega à superfície; pode-se à vontade'), ('Crescimento', 'Rápido'), ('Luz', 'Baixa a média'),
                ('CO<sub>2</sub>', 'Dispensável'), ('Temperatura', '10 a 26 °C; sofre acima de 27'), ('Dificuldade', dots(1) + 'muito fácil'),
                ('Quantidade', '4 a 6 hastes')],
         txt=[('Na natureza', 'Nativa de rios e lagoas do Sudeste e do Sul do Brasil, da Argentina e do Uruguai. Foi levada ao mundo inteiro como planta de aquário e hoje é invasora em vários países.'),
              ('No aquário', 'Folhas em verticilos de quatro, verde-vivo, em hastes que crescem vários centímetros por semana. É uma excelente consumidora de nutrientes e, por isso, ajuda muito no controle de algas.'),
              ('Como plantar', 'Hastes separadas, enterradas 3 cm. Também cresce solta, flutuando, o que facilita as podas.'),
              ('Cuidados', 'Prefere água fresca: acima de 27 °C, amolece e perde folhas. No verão, fique de olho; se a água esquentar, ela é a primeira a sofrer.')],
         bio=['Consome muitos nutrientes e compete com as algas.', 'Oxigena de dia.'], est=['Fundo verde e denso, de aspecto “de lagoa”.'],
         dif='Ótima para os primeiros meses de ciclagem e no inverno. Com a água a 26 °C ou mais, prefira a ambulia ou a ludwigia.'),
    dict(id='alt-salvinia', orig='flutuante-de-raiz-vermelha', orig_id='fl-phyl',
         nome='Salvínia', sci='<i>Salvinia minima</i> e <i>S. auriculata</i>, nativas do Brasil',
         serve='Uma samambaia flutuante nativa, que faz sombra e ancora o ninho do betta.',
         ficha=[('Origem', 'Américas tropicais, inclusive o Brasil'), ('Tipo', 'Samambaia flutuante'), ('Posição', 'Superfície, num anel'),
                ('Tamanho', 'Folhas de 1 a 2 cm'), ('Crescimento', 'Muito rápido'), ('Luz', 'Média'), ('CO<sub>2</sub>', 'Usa o do ar'),
                ('Temperatura', '20 a 30 °C'), ('Dificuldade', dots(1) + 'muito fácil'), ('Quantidade', '6 a 10 plantinhas')],
         txt=[('Na natureza', 'Flutua em lagoas, brejos e remansos de rios, onde forma tapetes. As folhas são cobertas de pelinhos que prendem ar e repelem a água; as “raízes” são, na verdade, folhas modificadas.'),
              ('No aquário', 'Faz o mesmo que a flutuante-de-raiz-vermelha: sombra, abrigo e retirada de nitrato. É mais fácil — aguenta gotas e água mexida —, mas cresce tão rápido que precisa de retirada semanal.'),
              ('Como plantar', 'Solte as plantinhas dentro do anel flutuante, no canto mais calmo.'),
              ('Cuidados', 'Retire o excesso toda semana, deixando no máximo um terço da superfície coberto. Espécies do grupo são invasoras em outros países: o excesso vai para a composteira, nunca para rios.')],
         bio=['Retira nitrato rápido e sombreia algas.', 'Âncora para o ninho de bolhas.'], est=['Tapete verde-claro de textura aveludada.'],
         dif='Perde o vermelho da original. Em troca, é a flutuante mais tolerante à tampa parcial e às gotas de condensação.'),
    dict(id='alt-limnobium', orig='flutuante-de-raiz-vermelha', orig_id='fl-phyl',
         nome='Limnobium', sci='<i>Limnobium laevigatum</i>, esponja-d’água',
         serve='Folhas redondas e esponjosas, com raízes longas que viram cortina.',
         ficha=[('Origem', 'América Central e do Sul, inclusive o Brasil'), ('Tipo', 'Flutuante'), ('Posição', 'Superfície, num anel'),
                ('Tamanho', 'Folhas de 1 a 3 cm'), ('Crescimento', 'Rápido'), ('Luz', 'Média'), ('CO<sub>2</sub>', 'Usa o do ar'),
                ('Temperatura', '18 a 30 °C'), ('Dificuldade', dots(2) + 'fácil'), ('Quantidade', '4 a 6 plantinhas')],
         txt=[('Na natureza', 'Forma tapetes em lagoas e remansos. O verso das folhas é um tecido esponjoso, cheio de ar, que mantém a planta boiando mesmo quando molhada.'),
              ('No aquário', 'Retira nitrato rápido e faz sombra densa. As raízes pendem 10 cm ou mais: uma cortina onde os camarões pastam e onde o betta passeia e descansa.'),
              ('Como plantar', 'Solte no anel flutuante, com as folhas secas por cima.'),
              ('Cuidados', 'Apare as raízes que tocarem as plantas de baixo. Como a original, não gosta de gotas nem de água agitada: a folga de 4 cm e a tampa parcial ajudam.')],
         bio=['Retira nitrato e faz sombra.', 'Raízes longas com biofilme.'], est=['Folhas brilhantes e raízes que desenham linhas verticais.'],
         dif='As raízes longas sombreiam mais do que a original: mantenha o anel pequeno, sobre a área aberta, longe das plantas que precisam de luz.'),
]


def orig_info(oid):
    """Lê a ficha e o minimapa da planta original."""
    for f in os.listdir(PAGES):
        if f.endswith(f'-{oid}.html'):
            s = open(os.path.join(PAGES, f), encoding='utf-8').read()
            ficha = dict((re.sub('<[^>]+>', '', k), v) for k, v in re.findall(r'<dt>(.*?)</dt><dd>(.*?)</dd>', s))
            mm = re.search(r'<figure class="minimap">.*?</figure>', s, re.S)
            name = re.search(r'<h2 class="h1">(.*?)</h2>', s).group(1)
            return ficha, (mm.group(0) if mm else ''), name
    raise SystemExit(f'original não encontrada: {oid}')


def alt_page(a, idx):
    ficha = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in a['ficha'])
    txt = ''.join(f'<p><span class="lead">{k}.</span> {v}</p>' for k, v in a['txt'])
    slug = a['id'].replace('alt-', '')
    of, minimap, oname = orig_info(a['orig_id'])
    af = dict((re.sub('<[^>]+>', '', k), v) for k, v in a['ficha'])
    comp = ''
    for k in ('Altura', 'Tamanho', 'Crescimento', 'Luz', 'Dificuldade'):
        if k in af and k in of:
            clean = lambda v: re.sub(r'<span class="dots">.*?</span>', '', v)
            comp += f'<tr><td>{k}</td><td>{clean(of[k])}</td><td>{clean(af[k])}</td></tr>'
    plain = re.sub('<[^>]+>', '', a['nome'])
    body = f'''    <header class="fl-head">
      <p class="eyebrow">Alternativa {idx} de {len(ALTS)} · no lugar da {a['orig']}</p>
      <h2 class="h1">{a['nome']}</h2>
      <p class="sci">{a['sci']}</p>
      <p class="func"><span>Para que serve</span>{a['serve']}</p>
    </header>
    <div class="fl-grid">
      <figure class="fig"><img src="img/flora/{slug}.jpg" alt="{plain}"><figcaption>{plain}. <span class="cr" data-cr="img/flora/{slug}.jpg"></span></figcaption></figure>
      <dl class="ficha">{ficha}</dl>
      <div class="fl-text runin">{txt}
        <div style="margin-top:3.4mm">{funcs_html(a['bio'], a['est'])}</div>
      </div>
      <aside class="fl-side">
        <div class="note fit"><span class="lbl">No seu 40 × 20</span>{a['dif']}</div>
        <div><h3 class="h3" style="font-size:8.6pt">Comparada à original</h3>
          <table class="t tight cmp"><thead><tr><th></th><th>{oname} <span class="cr">p. {{{{pg:{a['orig_id']}}}}}</span></th><th>{plain}</th></tr></thead><tbody>{comp}</tbody></table></div>
        {minimap.replace('<b>No seu 40 × 20:</b>', '<b>Mesmo lugar da original:</b>')}
      </aside>
    </div>'''
    return page(a['id'], CH, 'Flora: alternativas', AC, body, 'flora', src='flora.py')


def alt_index():
    rows = {}
    for a in ALTS:
        rows.setdefault((a['orig'], a['orig_id']), []).append(a)
    tr = ''
    for (orig, oid), alts in rows.items():
        names = '<br>'.join(f"{x['nome']} <span class=\"cr\">p. {{{{pg:{x['id']}}}}}</span>" for x in alts)
        tr += f'<tr><td>{orig[0].upper() + orig[1:]} <span class="cr">p. {{{{pg:{oid}}}}}</span></td><td>{names}</td><td>{alts[0]["dif"].split(". ")[0]}.</td></tr>'
    body = header('Flora · plano B', 'Se não encontrar a planta, troque pela função',
                  'Cada planta do mapa tem um trabalho no ecossistema e um papel na paisagem. Uma boa substituta faz os dois — mesmo que tenha outra cara.')
    body += f'''
    <div class="grid2">
      <div class="runin">
        <p><span class="lead">Função biológica</span> é o que a planta faz pelo equilíbrio do aquário: consumir nitrato, fazer sombra, arejar o substrato, abrigar filhotes, oferecer biofilme ou um lugar de descanso para o betta. É a parte que não pode faltar.</p>
        <p><span class="lead">Função estética</span> é o papel dela na composição: primeiro plano, transição ou fundo; textura fina ou folha larga; verde, bronze ou vermelho. Aqui dá para improvisar — o aquário continua saudável com outra cara.</p>
      </div>
      <div class="note why"><span class="lbl">Por quê? Por que a função vem primeiro</span>Se faltar a rotala, o aquário perde a maior consumidora de nitrato e fica mais sujeito a algas nas primeiras semanas. Troque por outra planta de caule rápida, e não por uma epífita bonita que cresce devagar. As fichas a seguir já estão agrupadas assim.</div>
    </div>
    <table class="t"><thead><tr><th style="width:26%">Planta do mapa</th><th style="width:34%">Alternativas</th><th>Como usar</th></tr></thead><tbody>{tr}</tbody></table>
    <div class="note warn"><span class="lbl">Atenção: plantas de loja e camarões</span>Toda planta de vaso pode trazer pesticida, caramujos e algas. Prefira <i>in vitro</i>; se vier em vaso, deixe de molho por três a cinco dias em água declorada, trocando a água todo dia, antes de plantar.</div>'''
    return page('alt-index', CH, 'Flora: alternativas', AC, body, src='flora.py')


# ---------------------------------------------------------------- emersas
EMERSAS = [
    ('jiboia', 'Jiboia', '<i>Epipremnum aureum</i>', ['A mais fácil. Enraíza na água em uma ou duas semanas, aguenta pouca luz e cresce em cascata. Folhas verdes, douradas (‘Golden’) ou mescladas de branco (‘Marble Queen’).', '<b>Na composição:</b> ramos que descem pela lateral do móvel e emolduram o vidro.'],
     'Consome muito nitrato', 'Tóxica para gatos e cães se mastigada.'),
    ('filodendro', 'Filodendro-brasil', '<i>Philodendron hederaceum</i> ‘Brasil’', ['Folhas em coração, verde com uma faixa amarela no centro. Mais delicado que a jiboia, cresce igualmente bem com as raízes na água.', '<b>Na composição:</b> o amarelo das folhas conversa com os verdes-claros do tapete.'],
     'Consome nitrato', 'Tóxico para gatos e cães se mastigado.'),
    ('singonio', 'Singônio', '<i>Syngonium podophyllum</i>', ['Folhas em ponta de flecha, verde-claras ou rosadas. Forma uma moita compacta que, com o tempo, começa a pender.', '<b>Na composição:</b> volume no canto de trás, sobre o lado alto do aquário.'],
     'Consome nitrato', 'Tóxico para gatos e cães se mastigado.'),
    ('lirio', 'Lírio-da-paz', '<i>Spathiphyllum</i> spp.', ['Uma das poucas plantas de interior que florescem com as raízes na água. Folhas escuras e brilhantes e flores brancas; prefira variedades compactas.', '<b>Na composição:</b> um ponto alto e vertical, que equilibra a pedra principal.'],
     'Consome nitrato', 'Tóxico para gatos e cães se mastigado.'),
    ('clorofito', 'Clorofito', '<i>Chlorophytum comosum</i>, planta-aranha', ['Folhas em fita, verde com borda branca, e mudinhas penduradas em hastes. As raízes grossas crescem bem na água. Uma das mais seguras para quem tem gatos.', '<b>Na composição:</b> linhas finas e arqueadas, que repetem fora d’água o gramado da frente.'],
     'Consome nitrato', 'Não tóxico para gatos e cães.'),
    ('bambu', 'Bambu-da-sorte', '<i>Dracaena sanderiana</i>', ['Hastes verticais com folhas no topo, vendidas em qualquer floricultura. Crescem devagar. Só a base das hastes na água.', '<b>Na composição:</b> linhas retas e verticais, de ar oriental, que não cobrem a vista do aquário.'],
     'Consumo moderado', 'Tóxico para gatos e cães se mastigado.'),
    ('hydrocotyle', 'Pinheirinho-d’água', '<i>Hydrocotyle leucocephala</i>, nativa do Brasil', ['Uma planta aquática de verdade, que também cresce fora d’água: folhas redondas em hastes que sobem pela borda e pendem para fora. Pode ficar parte submersa, parte emersa.', '<b>Na composição:</b> liga o dentro e o fora do vidro, como uma margem de rio.'],
     'Consome muito nitrato', 'Sem toxicidade conhecida.'),
    ('hortela', 'Hortelã', '<i>Mentha</i> spp.', ['Enraíza na água em dias e cresce rápido com a luz da janela ou da luminária. De bônus, você colhe folhas para o chá — desde que nunca use adubo ou defensivos nela.', '<b>Na composição:</b> uma moita verde-clara e macia; precisa de podas para não esconder o aquário.'],
     'Consome muito nitrato', 'Segura para pessoas; evite deixar ao alcance de gatos.'),
]


def emersas_pages():
    body = header('Etapa 5 de 9 · plantas sobre o aquário', 'Raízes na água, folhas no ar',
                  'Plantas de interior presas à borda, com as raízes mergulhadas, filtram a água melhor que muitas aquáticas — e fazem o aquário continuar para fora do vidro.')
    body += '''
    <div class="split" style="grid-template-columns:1fr 74mm">
      <div class="runin">
        <p><span class="lead">Por que funciona.</span> Plantas terrestres crescem rápido, com luz e CO<sub>2</sub> do ar à vontade. Tudo o que elas precisam retirar da água são nutrientes — e o principal é o nitrato. Com duas ou três mudas na borda, o nitrato cai, as algas perdem espaço e as trocas parciais ficam mais tranquilas. As raízes finas ainda viram mais uma superfície de biofilme para os camarões.</p>
        <p><span class="lead">A regra de ouro.</span> Só as raízes ficam na água. Folhas e caules submersos apodrecem em dias e sujam o aquário. Se a planta cair, tire-a na hora.</p>
        <p><span class="lead">Preparar as mudas.</span> Planta de floricultura vem com terra, adubo e, muitas vezes, pesticida — que mata camarões. Retire toda a terra, lave as raízes em água corrente sem sabão e corte as que estiverem escuras ou moles. Depois, deixe as mudas enraizando num pote de vidro com água declorada, trocada a cada dois ou três dias, por <b>duas a quatro semanas</b>. Só então elas vão para o aquário. Melhor ainda: faça estacas de uma planta que você já tem em casa.</p>
        <p><span class="lead">Como prender.</span> Suportes plásticos de borda, vendidos para aquários, ou pequenos vasos de encaixe com argila expandida lavada, sem terra. As raízes descem até a água; a coroa da planta fica fora. Deixe-as na faixa de trás, sobre o fundo esquerdo, onde já está o lado alto da composição.</p>
        <p><span class="lead">Luz.</span> A jiboia e o clorofito vivem com a luz do cômodo; as demais agradecem uma janela clara por perto (sem sol direto no vidro) ou uma luminária com braço, que ilumine o aquário e as folhas de cima.</p>
      </div>
      <div class="stack">
        <figure class="fig"><!--#svg emersas-corte--><figcaption><b>Em corte, pelo lado.</b> Tampa parcial cobrindo a frente; a faixa de trás fica aberta para as plantas. A água para 4 cm abaixo da borda, e a luminária fica num braço.</figcaption></figure>
        <div class="note warn"><span class="lbl">Atenção: aquário sem tampa</span>Bettas saltam — sobretudo nas primeiras semanas, quando a água piora ou quando são perseguidos. Com a faixa de trás aberta, mantenha a folga de 4 cm e plantas densas junto à abertura. Nunca deixe o aquário todo destampado.</div>
        <div class="note fit"><span class="lbl">No seu 40 × 20</span>Com 4 cm de folga, a água real fica em torno de <b>13 litros</b>. Use esse número para condicionador e fertilizantes. A evaporação dobra: reponha com água destilada a cada dois ou três dias.</div>
      </div>
    </div>
    <div class="grid2">
      <div>
        <h3 class="h3">O que comprar</h3>
        <ul class="dash">
          <li>Tampa de vidro ou acrílico cortada para cobrir só a frente: 27 × 20 cm (dois terços dos 40 cm).</li>
          <li>Braço ou suporte para a luminária, já que ela não apoia mais na tampa.</li>
          <li>Dois ou três suportes de borda para plantas, ou vasinhos de encaixe.</li>
          <li>Argila expandida, bem lavada, e um pote de vidro para o enraizamento.</li>
        </ul>
      </div>
      <div>
        <h3 class="h3">Sinais de que está funcionando</h3>
        <ul class="dash">
          <li>Raízes novas, brancas e finas, crescendo dentro da água em poucas semanas.</li>
          <li>Folhas novas saindo da coroa, sem amarelar.</li>
          <li>Nitrato estável ou caindo entre as trocas parciais, com menos algas nos vidros.</li>
        </ul>
      </div>
    </div>
    <div class="note why"><span class="lbl">No seu calendário</span>Ponha as mudas para enraizar no próprio dia da montagem, 1º de janeiro. Elas ficam prontas entre 15 e 29 de janeiro, no meio da ciclagem — a tempo de ajudar a consumir o nitrato do fim do ciclo, antes dos camarões.</div>'''
    write('205-emersas.html', page('emersas', CH, 'Etapa 5: plantas emersas', AC, body, src='flora.py'))

    for i, chunk in enumerate((EMERSAS[:4], EMERSAS[4:])):
        cards = []
        for slug, nome, sci, txt, bio, tox in chunk:
            cards.append(card(f'emersas/{slug}.jpg', nome, sci, txt, f'{bio} · {tox}'))
        body = header('Etapa 5 de 9 · plantas sobre o aquário',
                      'Oito plantas para a borda' if i == 0 else 'Mais quatro, e os cuidados de rotina',
                      'Todas enraízam bem na água e toleram a luz de um cômodo. A função estética é sempre a mesma: levar o verde para fora do vidro.' if i == 0 else None)
        body += '\n' + grid(cards, 'c2 wide' if i == 0 else 'c2')
        if i == 0:
            rows = [('Jiboia', 'baixa', 'rápido', 'grande, pendente', 'não'),
                    ('Filodendro-brasil', 'baixa a média', 'médio', 'média, pendente', 'não'),
                    ('Singônio', 'média', 'médio', 'moita compacta', 'não'),
                    ('Lírio-da-paz', 'baixa a média', 'lento', 'moita alta', 'não'),
                    ('Clorofito', 'média', 'médio', 'tufo arqueado', 'sim'),
                    ('Bambu-da-sorte', 'baixa a média', 'lento', 'vertical', 'não'),
                    ('Pinheirinho-d’água', 'média', 'rápido', 'pendente', 'sim'),
                    ('Hortelã', 'média a alta', 'rápido', 'moita', 'sim')]
            tr = ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td></tr>' for a, b, c, d, e in rows)
            body += f'''
    <div><h3 class="h3">Qual escolher</h3>
    <table class="t tight"><thead><tr><th>Planta</th><th>Luz</th><th>Crescimento</th><th>Forma</th><th>Segura com gatos e cães</th></tr></thead><tbody>{tr}</tbody></table></div>'''
        if i == 1:
            body += '''
    <div class="grid2">
      <div>
        <h3 class="h3">Rotina</h3>
        <ul class="dash">
          <li><b>Toda semana:</b> retire folhas amarelas e confira se nenhuma folha encostou na água.</li>
          <li><b>A cada mês:</b> apare as raízes que passarem de 10 cm ou que se enroscarem nas plantas aquáticas.</li>
          <li><b>Nunca:</b> adube, borrife inseticida ou limpe as folhas com produto de brilho. Tudo escorre para a água.</li>
        </ul>
      </div>
      <div class="note warn"><span class="lbl">Atenção: gatos, cães e crianças</span>Jiboia, filodendro, singônio, lírio-da-paz e bambu-da-sorte contêm cristais de oxalato de cálcio, que irritam a boca e o estômago se forem mastigados. Com animais curiosos em casa, fique com o clorofito, o pinheirinho-d’água e a hortelã.</div>
    </div>'''
        write(f'20{6 + i}-emersas{i + 2}.html', page(f'emersas{i + 2}', CH, 'Etapa 5: plantas emersas', AC, body, src='flora.py'))


def main():
    add_funcs()
    write('201-alt-index.html', alt_index())
    for i, a in enumerate(ALTS, 1):
        write(f'202-{i:02d}-{a["id"]}.html', alt_page(a, i))
    emersas_pages()
