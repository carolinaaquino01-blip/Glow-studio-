#!/usr/bin/env bash
# Transcribe un video con whisper-cli y deja <salida>.json con timestamps por palabra + imprime "inicio fin palabra".
# Uso: transcribe.sh video.mov carpeta_salida [idioma=es]
set -e
V="$1"; OUT="$2"; LANG_="${3:-es}"
mkdir -p "$OUT"
M="${WHISPER_MODEL:-$(ls ~/.cache/hyperframes/whisper/models/*medium*.bin ~/.cache/whisper/*medium*.bin 2>/dev/null | head -1)}"
[ -z "$M" ] && { echo "No encuentro el modelo de whisper. Definí WHISPER_MODEL=/ruta/ggml-medium.bin"; exit 1; }
ffmpeg -v error -y -i "$V" -ar 16000 -ac 1 "$OUT/audio.wav"
whisper-cli -m "$M" -l "$LANG_" -f "$OUT/audio.wav" -oj -ml 1 -sow -of "$OUT/words" >/dev/null 2>&1
python3 - "$OUT/words.json" <<'PY'
import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8",errors="replace"))
for s in d["transcription"]:
    t=s["text"].strip()
    if t: print(f'{s["offsets"]["from"]/1000:6.2f} {s["offsets"]["to"]/1000:6.2f} {t}')
PY
