// Renderiza cada .slide de carrusel.html a PNG 1080x1350 y una hoja de revisión.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const dir = __dirname, out = process.argv[2] || path.join(dir, 'out');
  require('fs').mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'carrusel.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const n = await p.locator('.slide').count();
  for (let i = 0; i < n; i++) {
    await p.locator('.slide').nth(i).screenshot({ path: path.join(out, `glow-laser-${String(i + 1).padStart(2, '0')}.png`) });
  }
  console.log('fonts:', await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + f.weight).join(',')));
  await b.close();
})();
