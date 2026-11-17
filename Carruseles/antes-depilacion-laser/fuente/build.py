#!/usr/bin/env python3
# Genera carrusel.html (7 láminas 1080x1350) con la marca Glow.
import os
D = os.path.dirname(os.path.abspath(__file__))
F = "node_modules/@fontsource"

BROWN, DARK, BORDO, BG = "#51210C", "#2A1206", "#861724", "#E8E3D8"

def star(x, y, s, rot=0):
    # estrella de 4 puntas con borde blanco tipo sticker
    p = "M50 0 C54 34 66 46 100 50 C66 54 54 66 50 100 C46 66 34 54 0 50 C34 46 46 34 50 0Z"
    return (f'<svg class="star" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg)" '
            f'viewBox="-8 -8 116 116"><path d="{p}" fill="#fff" stroke="#fff" stroke-width="14" stroke-linejoin="round"/>'
            f'<path d="{p}" fill="{DARK}"/></svg>')

ICONS = {
 "pinza": '<path d="M52 16 H68"/><path d="M52 16 Q30 62 57 102"/><path d="M68 16 Q90 62 63 102"/><path d="M42 50 h6 M72 50 h6"/>',
 "sol": '<circle cx="60" cy="60" r="20"/>' + "".join(
     f'<line x1="{60+30*c:.1f}" y1="{60+30*s:.1f}" x2="{60+42*c:.1f}" y2="{60+42*s:.1f}"/>'
     for c, s in [(1,0),(0.707,0.707),(0,1),(-0.707,0.707),(-1,0),(-0.707,-0.707),(0,-1),(0.707,-0.707)]),
 "exfol": '<circle cx="60" cy="60" r="36"/><circle cx="48" cy="48" r="3.5" fill="currentColor"/><circle cx="70" cy="52" r="3.5" fill="currentColor"/>'
          '<circle cx="56" cy="70" r="3.5" fill="currentColor"/><circle cx="74" cy="72" r="3.5" fill="currentColor"/><circle cx="44" cy="66" r="3.5" fill="currentColor"/>',
 "maquinita": '<rect x="28" y="22" width="64" height="20" rx="6"/><path d="M60 42 V98"/><path d="M34 32 h52" stroke-dasharray="4 6"/>',
 "gota": '<path d="M60 18 C60 18 32 52 32 72 a28 28 0 0 0 56 0 C88 52 60 18 60 18Z"/><path d="M48 74 a12 12 0 0 0 12 12"/>',
 "remera": '<path d="M44 22 L22 34 L30 52 L40 48 V98 H80 V48 L90 52 L98 34 L76 22 Q60 36 44 22Z"/>',
 "pastilla": '<rect x="22" y="44" width="76" height="32" rx="16" transform="rotate(-35 60 60)"/><line x1="51" y1="48" x2="69" y2="72"/>',
 "panza": '<path d="M60 26 C38 6 14 34 34 58 L60 88 L86 58 C106 34 82 6 60 26Z"/>',
 "lunar": '<circle cx="60" cy="60" r="38"/><circle cx="48" cy="52" r="7" fill="currentColor"/><path d="M62 70 l6 -12 l6 12 l-6 6z"/>',
}

def icon(name, badge):
    b = {"no": f'<g class="badge no"><circle cx="100" cy="100" r="18"/><path d="M92 92 L108 108 M108 92 L92 108"/></g>',
         "si": f'<g class="badge si"><circle cx="100" cy="100" r="18"/><path d="M91 100 L98 107 L110 93"/></g>',
         "ojo": f'<g class="badge ojo"><circle cx="100" cy="100" r="18"/><path d="M100 90 V102"/><circle cx="100" cy="109" r="1.5"/></g>'}[badge]
    return f'<svg class="icon" viewBox="0 0 122 122"><circle class="ring" cx="60" cy="60" r="56"/><g class="glyph">{ICONS[name]}</g>{b}</svg>'

def head(script, big, color=BROWN):
    return (f'<div class="head"><div class="script">{script}</div>'
            f'<div class="big" style="color:{color}">{big}</div></div>')

def item(num, ic, badge, title, body):
    return (f'<div class="item">{icon(ic, badge)}<div class="txt"><div class="num">{num}</div>'
            f'<div class="ititle">{title}</div><div class="ibody">{body}</div></div></div>')

def slide(n, inner, g=(560, 300, 1050, 0), stars=()):
    gx, gy, gh, gr = g
    st = "".join(star(*s) for s in stars)
    return (f'<section class="slide" id="s{n}"><div class="paper"></div>'
            f'<img class="wm" src="g_big.png" style="left:{gx}px;top:{gy}px;height:{gh}px;transform:rotate({gr}deg)">'
            f'<img class="logo" src="logo_big.png">{st}{inner}'
            f'<div class="count">{n:02d} / 07</div></section>')

S = []
S.append(slide(1, f'''
<div class="cover">
  <div class="script c1"><span class="w" style="--d:.1s">Si</span> <span class="w" style="--d:.3s">tenés</span></div>
  <div class="big c2"><span class="w" style="--d:.6s">TURNO</span><br><span class="w" style="--d:.85s">DE</span> <span class="w" style="--d:1.05s">LÁSER</span></div>
  <div class="save w" style="--d:1.5s"><svg viewBox="0 0 40 52" class="bm"><path d="M4 4 H36 V48 L20 36 L4 48Z"/></svg>
     <span class="script">guardá este post</span></div>
  <div class="sub w" style="--d:1.9s">esto hacé <span class="ser">(y esto</span> <b>NO</b><span class="ser">)</span><br>antes de tu sesión</div>
</div>
<div class="swipe script">deslizá &gt;&gt;&gt;</div>''',
  g=(600, 520, 1100, -8), stars=((830, 110, 170, 8), (760, 230, 80, -10), (70, 1080, 110, 0))))

S.append(slide(2, head("lo que", "NO tenés<br>que hacer", BORDO) + '<div class="items one">' +
  item("01", "pinza", "no", "Cera, pinza ni depiladora eléctrica",
       "<span class='hl'>la semana previa<svg class='ring2' viewBox='0 0 200 60' preserveAspectRatio='none'><path pathLength='1' d='M18 34 C14 12 70 4 112 6 C160 8 196 18 192 34 C188 50 140 58 96 56 C50 54 8 48 12 30 C14 20 30 12 52 9'/></svg></span>. Arrancan el pelo de raíz, <em>y el láser necesita ese pelo para funcionar.</em>") + '</div>',
  g=(-180, 560, 1000, 6), stars=((860, 120, 150, 10), (800, 240, 70, -6))))

S.append(slide(3, head("lo que", "NO tenés<br>que hacer", BORDO) + '<div class="items">' +
  item("02", "sol", "no", "Sol, cama solar ni autobronceante",
       "<span class='hl'>unas 2 semanas antes<svg class='ring2' viewBox='0 0 200 60' preserveAspectRatio='none'><path pathLength='1' d='M18 34 C14 12 70 4 112 6 C160 8 196 18 192 34 C188 50 140 58 96 56 C50 54 8 48 12 30 C14 20 30 12 52 9'/></svg></span>. Con la piel bronceada <em>aumenta el riesgo de manchas o quemaduras.</em>") +
  item("03", "exfol", "no", "Exfoliaciones ni peelings",
       "en la zona <span class='hl'>los días previos<svg class='ring2' viewBox='0 0 200 60' preserveAspectRatio='none'><path pathLength='1' d='M18 34 C14 12 70 4 112 6 C160 8 196 18 192 34 C188 50 140 58 96 56 C50 54 8 48 12 30 C14 20 30 12 52 9'/></svg></span>.") + '</div>',
  g=(640, 640, 1000, -6), stars=((850, 110, 150, 8), (790, 230, 70, -10))))

S.append(slide(4, head("lo que", "SÍ tenés<br>que hacer") + '<div class="items one">' +
  item("04", "maquinita", "si", "Rasurate 24 horas antes",
       "con maquinita. <em>El pelo tiene que estar al ras.</em>") + '</div>',
  g=(600, 560, 1050, 6), stars=((860, 120, 150, 10), (800, 240, 70, -6))))

S.append(slide(5, head("lo que", "SÍ tenés<br>que hacer") + '<div class="items">' +
  item("05", "gota", "si", "Piel limpia",
       "sin cremas, aceites, perfume ni maquillaje en la zona. <em>Si es axila, sin desodorante.</em>") +
  item("06", "remera", "si", "Ropa cómoda",
       "para que la zona quede accesible.") + '</div>',
  g=(-200, 620, 1000, -4), stars=((850, 130, 150, 8), (790, 250, 70, -10))))

S.append(slide(6, head("avisanos", "SI…", BORDO) + '<div class="items three">' +
  item("07", "pastilla", "ojo", "Tomás medicación",
       "sobre todo antibióticos, isotretinoína (Roaccutane) o retinoides.") +
  item("08", "panza", "ojo", "Estás embarazada", "") +
  item("09", "lunar", "ojo", "Tenés tatuajes o lunares en la zona",
       "<em>se protegen durante la sesión.</em>") + '</div>',
  g=(660, 180, 900, 8), stars=((850, 110, 150, 8), (790, 230, 70, -10))))

S.append(slide(7, f'''
<div class="close">
  <div class="big k1">¿LISTA PARA TU</div>
  <div class="script k2">próxima sesión?</div>
  <div class="ser k3">YA TENEMOS FECHA</div>
  <div class="pill"><svg viewBox="0 0 48 48"><path d="M8 10 H40 Q44 10 44 14 V30 Q44 34 40 34 H22 L12 42 V34 H8 Q4 34 4 30 V14 Q4 10 8 10Z"/></svg>¡ESCRIBINOS!</div>
  <img class="biglogo" src="logo_big.png">
</div>''',
  g=(-160, 420, 1100, -6), stars=((850, 100, 160, 10), (790, 220, 75, -8), (90, 1090, 110, 4))))

ANIM_CSS = open(os.path.join(D,"anim.css")).read()
import sys
ANIM = "--anim" in sys.argv
if ANIM: S = [S[i] for i in (0,1,2,5)]
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Mont;font-weight:500;src:url({F}/montserrat/files/montserrat-latin-500-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:600;src:url({F}/montserrat/files/montserrat-latin-600-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:800;src:url({F}/montserrat/files/montserrat-latin-800-normal.woff2)}}
@font-face{{font-family:Mont;font-weight:500;font-style:italic;src:url({F}/montserrat/files/montserrat-latin-500-italic.woff2)}}
@font-face{{font-family:Script;src:url({F}/pinyon-script/files/pinyon-script-latin-400-normal.woff2)}}
@font-face{{font-family:Ser;font-weight:600;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2)}}
@font-face{{font-family:Ser;font-weight:600;font-style:italic;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#999;font-family:Mont;color:{DARK}}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{BG};margin:0 0 20px}}
.paper{{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .35 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}}
.wm{{position:absolute;opacity:.55}}
.logo{{position:absolute;left:50%;top:56px;width:200px;margin-left:-100px}}
.star{{position:absolute;filter:drop-shadow(0 4px 6px rgba(42,18,6,.18))}}
.count{{position:absolute;left:0;right:0;bottom:48px;text-align:center;font:600 22px Mont;letter-spacing:.3em;color:{BROWN};opacity:.6}}
.script{{font-family:Script;color:{BORDO};line-height:1}}
.ser{{font-family:Ser;font-weight:600}}
.big{{font:800 118px/0.9 Mont;letter-spacing:-.035em;text-transform:uppercase;color:{BROWN}}}
em{{font-style:normal;color:{BORDO};font-weight:600}}
/* portada */
.cover{{position:absolute;left:0;right:0;top:300px;text-align:center}}
.c1{{font-size:150px;margin-bottom:-14px}}
.c2{{font-size:150px}}
.save{{display:inline-flex;align-items:center;gap:18px;margin-top:44px}}
.save .script{{font-size:92px}}
.bm{{width:40px;height:52px;fill:none;stroke:{BORDO};stroke-width:4}}
.sub{{margin:56px auto 0;width:820px;font:600 48px/1.25 Mont;color:{DARK};border-top:2px solid {BROWN};border-bottom:2px solid {BROWN};padding:30px 0}}
.sub .ser{{font-size:58px;font-style:italic}} .sub b{{color:{BORDO};font-weight:800}}
.swipe{{position:absolute;right:70px;bottom:110px;font-size:64px;color:{DARK}}}
/* encabezado */
.head{{position:absolute;left:90px;right:90px;top:250px}}
.head .script{{font-size:120px;margin-bottom:-6px}}
.head .big{{font-size:110px}}
.items{{position:absolute;left:90px;right:90px;top:640px;bottom:130px;display:flex;flex-direction:column;justify-content:center;gap:64px}}
.items.three{{top:520px;gap:48px}}
.items.one{{top:600px;bottom:150px}}
.items.one .item{{flex-direction:column;align-items:center;text-align:center;gap:26px}}
.items.one .icon{{flex-basis:auto;width:190px;height:190px}}
.items.one .icon .glyph{{stroke-width:3}}
.item{{display:flex;gap:40px;align-items:flex-start}}
.icon{{flex:0 0 150px;width:150px;height:150px;color:{BROWN}}}
.icon .ring{{fill:#F3EFE7;stroke:{BROWN};stroke-width:2.5}}
.icon .glyph{{fill:none;stroke:{BROWN};stroke-width:4;stroke-linecap:round;stroke-linejoin:round}}
.badge circle{{stroke:#fff;stroke-width:4}} .badge path{{fill:none;stroke:#fff;stroke-width:4.5;stroke-linecap:round;stroke-linejoin:round}}
.badge.no circle{{fill:{BORDO}}} .badge.si circle{{fill:{BROWN}}} .badge.ojo circle{{fill:{BORDO}}}
.badge.ojo circle:last-child{{fill:#fff;stroke:none}}
.num{{font:italic 600 48px Ser;color:{BORDO};line-height:1;margin-bottom:6px}}
.ititle{{font:800 50px/1.02 Mont;letter-spacing:-.02em;text-transform:uppercase;color:{BROWN}}}
.ibody{{font:500 38px/1.32 Mont;color:{DARK};margin-top:14px}}
.items.one .ititle{{font-size:60px}} .items.one .ibody{{font-size:41px;max-width:820px;margin:16px auto 0}} .items.one .num{{font-size:60px}}
.items.three .ititle{{font-size:44px}} .items.three .ibody{{font-size:34px;margin-top:10px}}
.items.three .icon{{flex-basis:130px;width:130px;height:130px}}
/* cierre */
.close{{position:absolute;left:0;right:0;top:330px;text-align:center}}
.k1{{font-size:100px}} .k2{{font-size:150px;margin-top:6px}}
.k3{{font-size:56px;letter-spacing:.18em;color:{BROWN};margin-top:40px}}
.pill{{display:inline-flex;align-items:center;gap:22px;margin-top:60px;background:{BORDO};color:#F6F1E8;font:800 50px Mont;letter-spacing:.02em;padding:30px 64px;border-radius:999px;box-shadow:0 10px 0 {DARK}}}
.pill svg{{width:54px;height:54px;fill:none;stroke:#F6F1E8;stroke-width:3.5;stroke-linejoin:round}}
.biglogo{{display:block;width:300px;margin:110px auto 0;opacity:.9}}
.slide#s7 .logo{{display:none}}
{ANIM_CSS if ANIM else ''}
.hl{{position:relative;white-space:nowrap}} .ring2{{display:none}}
</style></head><body class="{'anim' if ANIM else ''}">{"".join(S)}</body></html>'''
open(os.path.join(D, "carrusel_anim.html" if ANIM else "carrusel.html"), "w", encoding="utf-8").write(html)
print("ok")
