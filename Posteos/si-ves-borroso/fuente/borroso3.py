#!/usr/bin/env python3
# "Si ves borroso…" v3: paleta Glow (vino/bordó/taupe/beige/marfil), terciopelo, estrellas y sticker en relieve.
import os
D = os.path.dirname(os.path.abspath(__file__))
F = "node_modules/@fontsource"
WINE, BORDO, TAUPE, BEIGE, IVORY, SHADOW = "#531B24", "#6A2931", "#C6B7A2", "#E7D8C3", "#F3ECE2", "#2A0A10"

BASE = [("Si", 0, 0), ("ves", 0, 0), ("borroso", 5, 1), ("es", 0, 0), ("porque", 0, 0), ("necesitás", 3.5, 1)]
PIEZAS = [
    ("alisado",  BASE + [("un", 0, 0), ("alisado", 5.5, 2)]),
    ("unas",     BASE + [("uñas", 5.5, 2), ("nuevas", 4, 2)]),
    ("pestanas", BASE + [("hacerte", 0, 0), ("lifting", 5.5, 2), ("de", 1.5, 2), ("pestañas", 4.5, 2)]),
    ("cejas",    BASE + [("un", 0, 0), ("laminado", 5.5, 2), ("de", 1.5, 2), ("cejas", 4.5, 2)]),
    ("masajes",  BASE + [("unos", 0, 0), ("masajes", 5.5, 2)]),
]
LAYOUT = [
    dict(stars=[(800, 140, 170, 10), (745, 280, 76, -8), (90, 1040, 110, 6)], st=(620, 1100, -7), g=(560, 420, 1150, -8), seed=3),
    dict(stars=[(100, 150, 160, -8), (235, 275, 72, 12), (850, 1020, 116, 4)], st=(110, 1105, 6), g=(-200, 380, 1150, 6), seed=7),
    dict(stars=[(820, 1000, 170, 8), (760, 1135, 74, -10), (90, 140, 112, -4)], st=(100, 1120, -5), g=(600, 300, 1150, -6), seed=11),
    dict(stars=[(800, 140, 170, 10), (745, 280, 76, -8), (110, 1050, 104, 6)], st=(610, 1110, 6), g=(-180, 460, 1150, 8), seed=19),
    dict(stars=[(90, 1000, 170, -8), (232, 1135, 72, 10), (850, 140, 112, 6)], st=(610, 1100, -6), g=(560, 260, 1150, -4), seed=23),
]
STAR = "M50 0 C54 34 66 46 100 50 C66 54 54 66 50 100 C46 66 34 54 0 50 C34 46 46 34 50 0Z"

DEFS = f'''<svg width="0" height="0" style="position:absolute"><defs>
<linearGradient id="starFill" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{IVORY}"/><stop offset=".55" stop-color="{BEIGE}"/><stop offset="1" stop-color="{TAUPE}"/></linearGradient>
<filter id="bevel" x="-20%" y="-20%" width="140%" height="140%">
  <feGaussianBlur in="SourceAlpha" stdDeviation="2.6" result="b"/>
  <feSpecularLighting in="b" surfaceScale="6" specularConstant="1.1" specularExponent="28" lighting-color="#fff" result="s">
    <fePointLight x="-40" y="-80" z="140"/></feSpecularLighting>
  <feComposite in="s" in2="SourceAlpha" operator="in" result="s2"/>
  <feComposite in="SourceGraphic" in2="s2" operator="arithmetic" k1="0" k2="1" k3=".75" k4="0"/>
</filter></defs></svg>'''

def star(x, y, s, rot):
    return (f'<svg class="star" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg)" viewBox="-12 -12 124 124">'
            f'<path d="{STAR}" fill="url(#starFill)" stroke="{BEIGE}" stroke-width="5" stroke-linejoin="round" filter="url(#bevel)"/></svg>')

def velvet(seed):
    # terciopelo arrugado: manchas de brillo de baja frecuencia + fibras finas
    sheen = (f"<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1350'><filter id='v'>"
             f"<feTurbulence type='fractalNoise' baseFrequency='.0032 .0042' numOctaves='4' seed='{seed}'/>"
             f"<feColorMatrix values='0 0 0 0 1  0 0 0 0 .78  0 0 0 0 .78  1.6 0 0 0 -.62'/></filter>"
             f"<rect width='1080' height='1350' filter='url(%23v)'/></svg>")
    shade = (f"<svg xmlns='http://www.w3.org/2000/svg' width='1080' height='1350'><filter id='d'>"
             f"<feTurbulence type='fractalNoise' baseFrequency='.0045 .003' numOctaves='3' seed='{seed+40}'/>"
             f"<feColorMatrix values='0 0 0 0 .16  0 0 0 0 .02  0 0 0 0 .05  1.8 0 0 0 -.75'/></filter>"
             f"<rect width='1080' height='1350' filter='url(%23d)'/></svg>")
    return (f'<div class="vel"></div>'
            f'<div class="crush" style="background-image:url(&quot;data:image/svg+xml;utf8,{shade}&quot;)"></div>'
            f'<div class="crush sheen" style="background-image:url(&quot;data:image/svg+xml;utf8,{sheen}&quot;)"></div>')

def pieza(slug, words, lay):
    spans = []
    for txt, blur, kind in words:
        cls = ["w", "w soft", "w soft svc"][kind]
        spans.append(f'<span class="{cls}" style="--b:{blur}px">{txt}</span>')
    gx, gy, gh, gr = lay["g"]
    sx, sy, sr = lay["st"]
    return (f'<section class="slide" id="{slug}">{velvet(lay["seed"])}'
            f'<img class="wm" src="g_wine.png" style="left:{gx}px;top:{gy}px;height:{gh}px;transform:rotate({gr}deg)">'
            f'<div class="fibers"></div><div class="grain"></div><div class="vign"></div>'
            f'<img class="logo" src="logo_ivory.png">'
            + "".join(star(*s) for s in lay["stars"]) +
            f'<p class="txt">{" ".join(spans)}</p>'
            f'<div class="sticker" style="left:{sx}px;top:{sy}px;transform:rotate({sr}deg)"><span>reservá tu turno</span></div></section>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Ser;font-weight:600;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2)}}
@font-face{{font-family:Ser;font-weight:600;font-style:italic;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff2)}}
@font-face{{font-family:Script;src:url({F}/pinyon-script/files/pinyon-script-latin-400-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#333}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{BORDO};margin:0 0 20px;display:flex;align-items:center;justify-content:center}}
.vel{{position:absolute;inset:0;background:
  radial-gradient(ellipse 60% 45% at 38% 30%, rgba(140,60,70,.22), transparent 70%),
  radial-gradient(ellipse 55% 40% at 70% 72%, rgba(130,52,62,.16), transparent 70%),
  linear-gradient(160deg, {BORDO} 0%, {WINE} 100%)}}
.crush{{position:absolute;inset:0;mix-blend-mode:multiply;opacity:.75}}
.crush.sheen{{mix-blend-mode:soft-light;opacity:.55}}
.fibers{{position:absolute;inset:0;opacity:.32;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400'><filter id='f'><feTurbulence type='fractalNoise' baseFrequency='.9 .06' numOctaves='2' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='400' height='400' filter='url(%23f)'/></svg>")}}
.grain{{position:absolute;inset:0;opacity:.35;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='260' height='260' filter='url(%23n)'/></svg>")}}
.vign{{position:absolute;inset:0;background:radial-gradient(ellipse 85% 75% at 50% 48%, transparent 55%, rgba(30,6,10,.55) 100%)}}
.wm{{position:absolute;opacity:.55;filter:drop-shadow(0 2px 0 rgba(243,236,226,.07)) drop-shadow(0 -2px 1px rgba(20,4,8,.5))}}
.logo{{position:absolute;left:50%;top:92px;width:230px;margin-left:-115px;filter:drop-shadow(0 3px 4px rgba(20,4,8,.45))}}
.star{{position:absolute;overflow:visible;filter:drop-shadow(0 10px 10px rgba(20,4,8,.55)) drop-shadow(0 2px 2px rgba(20,4,8,.4))}}
.txt{{position:relative;top:10px;width:930px;text-align:center;font:600 150px/1.0 Ser;letter-spacing:-.01em;color:{IVORY};text-wrap:balance;
  text-shadow:0 3px 0 rgba(30,6,10,.25), 0 8px 24px rgba(30,6,10,.45)}}
.w{{display:inline-block;filter:blur(var(--b))}}
.soft{{font-style:italic}}
.svc{{color:{BEIGE}}}
.sticker{{position:absolute;padding:6px;border-radius:999px;background:linear-gradient(180deg,#fff,#efe6da);
  box-shadow:0 14px 22px rgba(20,4,8,.5), 0 3px 4px rgba(20,4,8,.35)}}
.sticker span{{display:block;font:58px/1 Script;color:{WINE};padding:20px 42px 26px;border-radius:999px;
  background:linear-gradient(165deg,{IVORY} 0%,{BEIGE} 60%,{TAUPE} 130%);
  box-shadow:inset 0 3px 2px rgba(255,255,255,.8), inset 0 -4px 6px rgba(106,41,49,.18)}}
</style></head><body>{DEFS}{"".join(pieza(s, w, l) for (s, w), l in zip(PIEZAS, LAYOUT))}</body></html>'''
open(os.path.join(D, "borroso3.html"), "w", encoding="utf-8").write(html)
print("ok")
