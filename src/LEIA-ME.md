# Vinte litros de mundo — fontes

Os arquivos da raiz (`vinte-litros-de-mundo`, `diario-2027` e `vinte-litros-de-mundo-criancas`, em HTML e PDF) são gerados a partir desta pasta.

- `guia/pages/*.html` — uma página por arquivo, na ordem do nome. Numeração, recto/verso, sumário (`{{pg:id}}`) e créditos são automáticos.
- `guia/betta.py`, `guia/flora.py` — geram os catálogos do betta, as alternativas e as plantas emersas (edite o texto lá, não nos `.html` gerados).
- `guia/generate.py` — desenhos dos bettas (SVG) e chamada dos geradores.
- `diario/generate.py` — o Diário 2027 inteiro, com os marcos do cronograma.
- `criancas/generate.py`, `criancas/art.py`, `criancas/kids.css` — o livro infantil (6 a 8 anos): texto, desenhos e passatempos.
- `shared/semanal.html` — a tabela semanal em A4 paisagem, usada nos dois volumes.
- `photos.json` — crédito de cada foto; `photos_todo.json` — buscas e candidatas para as fotos que faltam.

## Comandos

```
python3 src/build.py                 # os três volumes, HTML + PDF
python3 src/build.py guia --no-pdf   # só o HTML do guia
node src/check.js vinte-litros-de-mundo.html /tmp/paginas   # vazamentos + capturas

python3 src/fetch_photos.py status   # fotos que faltam
python3 src/fetch_photos.py search   # baixa candidatas e gera src/img/_candidatos/index.html
python3 src/fetch_photos.py pick betta/crowntail 3
python3 src/fetch_photos.py manual SLOT URL AUTOR FONTE LICENÇA PÁGINA [recorte]
```

Precisa de Python 3 com Pillow e do Playwright (Chromium) para o PDF. Fotos ausentes aparecem como “foto pendente”.
