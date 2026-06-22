// Render cocktail-menu.html to PDF using Playwright (Node.js)
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const htmlPath = path.resolve(__dirname, 'cocktail-menu.html');
  const outDir = path.resolve(__dirname, 'output');
  const outPath = path.join(outDir, 'cocktail-menu.pdf');

  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  console.log('Launching Chromium…');
  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();

  console.log('Loading HTML…');
  await page.goto('file://' + htmlPath, { waitUntil: 'networkidle', timeout: 30000 });

  // Give fonts a moment to fully render
  await page.waitForTimeout(1000);

  console.log('Generating PDF…');
  await page.pdf({
    path: outPath,
    width: '148mm',
    height: '210mm',
    printBackground: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });

  await browser.close();
  console.log(`PDF written: ${outPath}`);
  console.log(`Size: ${(fs.statSync(outPath).size / 1024).toFixed(0)} KB`);
})();
