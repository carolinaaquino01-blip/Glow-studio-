#!/usr/bin/env bash
# Hoja de contacto: un cuadro cada N segundos en una grilla, para "ver" un video de un vistazo.
# Uso: sheet.sh video.mov salida.jpg [cada_seg=2] [columnas=6]
set -e
N="${3:-2}"; C="${4:-6}"
ffmpeg -v error -y -i "$1" -vf "fps=1/$N,scale=240:-1,tile=${C}x6" -frames:v 1 "$2" && echo "$2 (cuadro i = segundo i*$N, fila por fila)"
