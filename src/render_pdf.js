// Gera o PDF de um HTML com o Chromium do Playwright.
// Uso: node render_pdf.js entrada.html saida.pdf
const path = require('path');
const { execSync } = require('child_process');

function loadPlaywright() {
  try { return require('playwright'); } catch (e) {
    const root = execSync('npm root -g').toString().trim();
    return require(path.join(root, 'playwright'));
  }
}

(async () => {
  const [input, output] = process.argv.slice(2);
  const { chromium } = loadPlaywright();
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.resolve(input), { waitUntil: 'load', timeout: 180000 });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: output, preferCSSPageSize: true, printBackground: true, timeout: 600000 });
  await browser.close();
})();
