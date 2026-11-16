// Captura una web como la ve un celular (para mostrarla en el video): pantalla visible + página completa.
// Uso: node capture_site.cjs https://tu-landing.com carpeta_salida
// Requiere Chrome instalado y puppeteer-core (npm i -g puppeteer-core, o el que trae el caché de npx).
const path = require('path'), fs = require('fs'), os = require('os');
function findPuppeteer() {
  try { return require('puppeteer-core'); } catch (e) {}
  const base = path.join(os.homedir(), '.npm/_npx');
  for (const d of fs.existsSync(base) ? fs.readdirSync(base) : []) {
    const p = path.join(base, d, 'node_modules/puppeteer-core');
    if (fs.existsSync(p)) return require(p);
  }
  throw new Error('Instalá puppeteer-core: npm i -g puppeteer-core');
}
const CHROME = process.env.CHROME || ({darwin: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  win32: 'C:/Program Files/Google/Chrome/Application/chrome.exe'}[process.platform] || '/usr/bin/google-chrome');
(async () => {
  const [url, out] = process.argv.slice(2);
  fs.mkdirSync(out, {recursive: true});
  const b = await findPuppeteer().launch({executablePath: CHROME, headless: 'new'});
  const pg = await b.newPage();
  await pg.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1');
  // 390 de ancho x 2.77 = 1080 px: la captura sale justo al ancho del video
  await pg.setViewport({width: 390, height: 693, deviceScaleFactor: 2.77, isMobile: true, hasTouch: true});
  await pg.goto(url, {waitUntil: 'networkidle2', timeout: 60000});
  await new Promise(r => setTimeout(r, 2500));
  await pg.screenshot({path: path.join(out, 'pantalla.png')});
  await pg.screenshot({path: path.join(out, 'pagina_completa.png'), fullPage: true});
  console.log('listo:', path.join(out, 'pantalla.png'), path.join(out, 'pagina_completa.png'));
  await b.close();
})();
