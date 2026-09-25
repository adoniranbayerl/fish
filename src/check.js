// Confere cada página: conteúdo vazando da moldura e capturas em PNG.
// Uso: node check.js arquivo.html pasta_saida [id1,id2,...]
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
function loadPlaywright() {
  try { return require('playwright'); } catch (e) {
    return require(path.join(execSync('npm root -g').toString().trim(), 'playwright'));
  }
}
(async () => {
  const [input, outDir, only] = process.argv.slice(2);
  const want = only ? only.split(',') : null;
  fs.mkdirSync(outDir, { recursive: true });
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1300 } });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load', timeout: 180000 });
  await page.evaluate(() => document.fonts.ready);
  const problems = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('section.page').forEach((sec, i) => {
      const pr = sec.getBoundingClientRect();
      const mb = parseFloat(getComputedStyle(sec).getPropertyValue('--mb')) || 20;
      const limit = pr.bottom - mb * 3.7795 + 2; // mm -> px
      sec.querySelectorAll('.frame, .op-body, .bt-body, .body-abs').forEach(fr => {
        fr.querySelectorAll('*').forEach(el => {
          const r = el.getBoundingClientRect();
          if (r.height > 0 && r.bottom > limit && !el.closest('.bleed')) {
            out.push(`${i + 1} #${sec.id}: <${el.tagName.toLowerCase()} class="${el.className && el.className.baseVal === undefined ? el.className : ''}"> passa ${(r.bottom - limit).toFixed(0)}px`);
          }
        });
        if (fr.scrollHeight > fr.clientHeight + 2) out.push(`${i + 1} #${sec.id}: moldura com overflow ${fr.scrollHeight - fr.clientHeight}px`);
      });
    });
    return out;
  });
  const seen = new Set();
  problems.forEach(p => { const k = p.split(':')[0]; if (!seen.has(k)) { seen.add(k); console.log('OVERFLOW', p); } });
  const secs = await page.$$('section.page');
  for (let i = 0; i < secs.length; i++) {
    const id = await secs[i].getAttribute('id');
    if (want && !want.includes(id) && !want.includes(String(i + 1))) continue;
    await secs[i].screenshot({ path: path.join(outDir, `${String(i + 1).padStart(3, '0')}-${id}.png`) });
  }
  await browser.close();
})();
