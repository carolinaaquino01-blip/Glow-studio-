# Carrusel: antes de tu sesión de láser

Subir a Instagram en este orden (carrusel mixto de fotos y videos):

| # | Archivo |
|---|---|
| 1 | `glow-laser-01.mp4` (animada) |
| 2 | `glow-laser-02.mp4` (animada) |
| 3 | `glow-laser-03.mp4` (animada) |
| 4 | `glow-laser-04.png` |
| 5 | `glow-laser-05.png` |
| 6 | `glow-laser-06.mp4` (animada) |
| 7 | `glow-laser-07.png` |

Los PNG 01, 02, 03 y 06 quedan como versión estática por si se prefiere sin animación.

Rehacer: `python3 fuente/build.py` (+ `--anim`), `node fuente/shot.cjs` y `node fuente/render_anim.cjs <salida>`; requiere `npm i` en `fuente/`.
