#!/usr/bin/env bash
# Convierte una captura de página completa (1080 de ancho) en un "screen recording" vertical que scrollea.
# Uso: scroll_video.sh pagina_completa.png salida.mp4 duracion y_inicio y_fin [quieto_al_inicio=1.5] [duracion_scroll=1.1]
set -e
IMG="$1"; OUT="$2"; DUR="$3"; Y0="$4"; Y1="$5"; H="${6:-1.5}"; S="${7:-1.1}"
ffmpeg -v error -y -loop 1 -framerate 30 -t "$DUR" -i "$IMG" -vf "scale=1080:-2,crop=1080:1920:0:'if(lt(t,$H),$Y0,if(lt(t,$H+$S),$Y0+($Y1-$Y0)*(0.5-0.5*cos(PI*(t-$H)/$S)),$Y1))',format=yuv420p" -c:v libx264 -crf 14 -preset slow -movflags +faststart "$OUT" && echo "$OUT"
