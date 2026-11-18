#!/usr/bin/env python3
# "Si ves borroso…" v2: fondo bordó, letras claras, palabras borrosas en cursiva. Genera borroso2.html.
import os
D = os.path.dirname(os.path.abspath(__file__))
F = "node_modules/@fontsource"
BG, BG2, CREAM, PINK, DARK = "#7A1222", "#4E0913", "#F3EBDD", "#F2C9C1", "#2A1206"

# (palabra, desenfoque px, tipo) tipo: 0 nítida, 1 borrosa, 2 servicio borroso
BASE = [("Si", 0, 0), ("ves", 0, 0), ("borroso", 5, 1), ("es", 0, 0), ("porque", 0, 0), ("necesitás", 3.5, 1)]
PIEZAS = [
    ("alisado",  BASE + [("un", 0, 0), ("alisado", 5.5, 2)]),
    ("unas",     BASE + [("uñas", 5.5, 2), ("nuevas", 4, 2)]),
    ("pestanas", BASE + [("hacerte", 0, 0), ("lifting", 5.5, 2), ("de", 1.5, 2), ("pestañas", 4.5, 2)]),
    ("cejas",    BASE + [("un", 0, 0), ("laminado", 5.5, 2), ("de", 1.5, 2), ("cejas", 4.5, 2)]),
    ("masajes",  BASE + [("unos", 0, 0), ("masajes", 5.5, 2)]),
]
# posición de estrellas y sticker por pieza, para que no sean idénticas
LAYOUT = [
    dict(stars=[(812, 150, 150, 10), (760, 270, 66, -8), (96, 1050, 96, 6)], st=(640, 1105, -7), g=(560, 420, 1150, -8)),
    dict(stars=[(110, 160, 140, -8), (232, 268, 62, 12), (850, 1030, 104, 4)], st=(120, 1105, 6), g=(-200, 380, 1150, 6)),
    dict(stars=[(830, 1010, 150, 8), (770, 1130, 66, -10), (90, 150, 100, -4)], st=(110, 1120, -5), g=(600, 300, 1150, -6)),
    dict(stars=[(812, 150, 150, 10), (760, 270, 66, -8), (120, 1060, 90, 6)], st=(620, 1110, 6), g=(-180, 460, 1150, 8)),
    dict(stars=[(100, 1010, 150, -8), (230, 1130, 64, 10), (850, 150, 100, 6)], st=(620, 1105, -6), g=(560, 260, 1150, -4)),
]

def star(x, y, s, rot):
    p = "M50 0 C54 34 66 46 100 50 C66 54 54 66 50 100 C46 66 34 54 0 50 C34 46 46 34 50 0Z"
    return (f'<svg class="star" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({rot}deg)" viewBox="-10 -10 120 120">'
            f'<path d="{p}" fill="{DARK}" stroke="{DARK}" stroke-width="16" stroke-linejoin="round" transform="translate(2 4)" opacity=".35"/>'
            f'<path d="{p}" fill="{CREAM}" stroke="{CREAM}" stroke-width="12" stroke-linejoin="round"/>'
            f'<path d="{p}" fill="{BG}" transform="translate(50 50) scale(.62) translate(-50 -50)"/></svg>')

def pieza(slug, words, lay):
    spans = []
    for txt, blur, kind in words:
        cls = ["w", "w soft", "w soft svc"][kind]
        spans.append(f'<span class="{cls}" style="--b:{blur}px">{txt}</span>')
    gx, gy, gh, gr = lay["g"]
    sx, sy, sr = lay["st"]
    return (f'<section class="slide" id="{slug}"><div class="vel"></div>'
            f'<img class="wm" src="g_bordo.png" style="left:{gx}px;top:{gy}px;height:{gh}px;transform:rotate({gr}deg)">'
            f'<div class="grain"></div><div class="frame"></div>'
            f'<img class="logo" src="logo_cream.png">'
            + "".join(star(*s) for s in lay["stars"]) +
            f'<p class="txt">{" ".join(spans)}</p>'
            f'<div class="sticker" style="left:{sx}px;top:{sy}px;transform:rotate({sr}deg)">reservá tu turno</div></section>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Ser;font-weight:600;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2)}}
@font-face{{font-family:Ser;font-weight:600;font-style:italic;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-italic.woff2)}}
@font-face{{font-family:Script;src:url({F}/pinyon-script/files/pinyon-script-latin-400-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#333}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{BG};margin:0 0 20px;display:flex;align-items:center;justify-content:center}}
.vel{{position:absolute;inset:0;background:
  radial-gradient(ellipse 70% 55% at 50% 45%, rgba(255,120,120,.16), transparent 70%),
  radial-gradient(ellipse 120% 90% at 50% 50%, transparent 55%, {BG2} 100%)}}
.wm{{position:absolute;opacity:.5}}
.grain{{position:absolute;inset:0;opacity:.5;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='260' height='260'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3' stitchTiles='stitch'/><feColorMatrix type='saturate' values='0'/></filter><rect width='260' height='260' filter='url(%23n)'/></svg>")}}
.frame{{position:absolute;inset:40px;border:1.5px solid rgba(243,235,221,.35);border-radius:6px}}
.logo{{position:absolute;left:50%;top:92px;width:230px;margin-left:-115px}}
.star{{position:absolute}}
.txt{{position:relative;top:10px;width:930px;text-align:center;font:600 150px/1.0 Ser;letter-spacing:-.01em;color:{CREAM};text-wrap:balance;
  text-shadow:0 4px 18px rgba(40,0,8,.35)}}
.w{{display:inline-block;filter:blur(var(--b))}}
.soft{{font-style:italic;font-weight:600}}
.svc{{color:{PINK}}}
.sticker{{position:absolute;font:56px/1 Script;color:{BG};background:{CREAM};padding:22px 40px 26px;border-radius:999px;
  box-shadow:0 0 0 7px #fff, 0 10px 18px rgba(30,0,6,.4)}}
</style></head><body>{"".join(pieza(s, w, l) for (s, w), l in zip(PIEZAS, LAYOUT))}</body></html>'''
open(os.path.join(D, "borroso2.html"), "w", encoding="utf-8").write(html)
print("ok")
