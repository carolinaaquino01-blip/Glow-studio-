// Renderiza cada .slide de carrusel_anim.html cuadro a cuadro y arma un MP4 por lámina.
// Uso: node render_anim.cjs carpeta_salida [segundos=5] [fps=30]
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs'), { execFileSync } = require('child_process');
(async () => {
  const dir = __dirname, out = process.argv[2], DUR = +(process.argv[3] || 5), FPS = +(process.argv[4] || 30);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(dir, 'carrusel_anim.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  const ids = await p.$$eval('.slide', els => els.map(e => e.id));
  for (const id of ids) {
    const fr = fs.mkdtempSync(path.join(out, 'fr-'));
    await p.evaluate(id => { document.querySelectorAll('.slide').forEach(s => s.style.display = s.id === id ? 'block' : 'none'); window.scrollTo(0, 0); }, id);
    const el = p.locator('#' + id);
    for (let i = 0; i < DUR * FPS; i++) {
      const t = (i / FPS) * 1000;
      await p.evaluate(t => document.getAnimations().forEach(a => { a.pause(); a.currentTime = t; }), t);
      await el.screenshot({ path: path.join(fr, `f${String(i).padStart(4, '0')}.png`) });
    }
    const n = id.slice(1).padStart(2, '0');
    const mp4 = path.join(out, `glow-laser-${n}.mp4`);
    execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', String(FPS), '-i', path.join(fr, 'f%04d.png'),
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4]);
    fs.rmSync(fr, { recursive: true });
    console.log(mp4);
  }
  await b.close();
})();
