#!/usr/bin/env python3
# Piezas "Si ves borroso…" con la marca Glow (1080x1350). Genera borroso.html.
import os
D = os.path.dirname(os.path.abspath(__file__))
F = "node_modules/@fontsource"
DARK, BORDO, BG = "#2A1206", "#861724", "#E8E3D8"

# (palabra, desenfoque en px, es_servicio)
BASE = [("Si", 0), ("ves", 1.5), ("borroso", 6), ("es", 0), ("porque", 0), ("necesitás", 4)]
PIEZAS = [
    ("alisado",  BASE + [("un", 0), ("alisado", 6, 1)]),
    ("unas",     BASE + [("uñas", 6, 1), ("nuevas", 4, 1)]),
    ("pestanas", BASE + [("hacerte", 0), ("lifting", 6, 1), ("de", 1.5, 1), ("pestañas", 4.5, 1)]),
    ("cejas",    BASE + [("un", 0), ("laminado", 6, 1), ("de", 1.5, 1), ("cejas", 4.5, 1)]),
    ("masajes",  BASE + [("unos", 0), ("masajes", 6, 1)]),
]

def pieza(n, slug, words):
    spans = []
    for w in words:
        txt, blur = w[0], w[1]
        cls = "w svc" if len(w) > 2 else "w"
        spans.append(f'<span class="{cls}" style="--b:{blur}px">{txt}</span>')
    return (f'<section class="slide" id="{slug}"><div class="paper"></div>'
            f'<img class="logo" src="logo_dark.png"><p class="txt">{" ".join(spans)}</p></section>')

html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:Ser;font-weight:600;src:url({F}/cormorant-garamond/files/cormorant-garamond-latin-600-normal.woff2)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#999}}
.slide{{position:relative;width:1080px;height:1350px;overflow:hidden;background:{BG};margin:0 0 20px;display:flex;align-items:center;justify-content:center}}
.paper{{position:absolute;inset:0;opacity:.35;mix-blend-mode:multiply;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 .55  0 0 0 0 .5  0 0 0 0 .42  0 0 0 .35 0'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}}
.logo{{position:absolute;left:50%;top:92px;width:230px;margin-left:-115px}}
.txt{{position:relative;top:40px;width:940px;text-align:center;font:600 150px/1.0 Ser;letter-spacing:-.01em;color:{DARK};text-wrap:balance}}
.w{{display:inline-block;filter:blur(var(--b))}}
.svc{{color:{BORDO}}}
</style></head><body>{"".join(pieza(i+1, s, w) for i, (s, w) in enumerate(PIEZAS))}</body></html>'''
open(os.path.join(D, "borroso.html"), "w", encoding="utf-8").write(html)
print("ok")
