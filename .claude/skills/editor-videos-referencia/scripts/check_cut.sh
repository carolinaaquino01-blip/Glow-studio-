#!/usr/bin/env bash
# Prueba una unión antes de renderizar: pega [A_ini, A_fin] + [B_ini, B_fin] del audio y lo transcribe.
# Si aparece una sílaba de más ("una", "me", "eh") o falta una, mové el corte 30–60 ms y repetí.
# Uso: check_cut.sh audio.wav A_fin B_ini [contexto=1.5]
set -e
WAV="$1"; AE="$2"; BS="$3"; C="${4:-1.5}"
M="${WHISPER_MODEL:-$(ls ~/.cache/hyperframes/whisper/models/*medium*.bin ~/.cache/whisper/*medium*.bin 2>/dev/null | head -1)}"
T=$(mktemp -d)
AS=$(python3 -c "print(max(0,$AE-$C))"); BE=$(python3 -c "print($BS+$C)")
ffmpeg -v error -y -i "$WAV" -filter_complex "[0]atrim=$AS:$AE,asetpts=PTS-STARTPTS[a];[0]atrim=$BS:$BE,asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1,apad=pad_dur=0.5" "$T/t.wav"
echo -n "$AE | $BS : "; whisper-cli -m "$M" -l es -f "$T/t.wav" -nt 2>/dev/null | tr -d '\n'; echo
python3 - "$WAV" "$AE" "$BS" <<'PY'
import wave,struct,math,sys
w=wave.open(sys.argv[1]);sr=w.getframerate();x=struct.unpack(f"<{w.getnframes()*w.getnchannels()}h",w.readframes(w.getnframes()))
def r(a): s=x[int(a*sr):int((a+0.025)*sr)]; return 20*math.log10(math.sqrt(sum(v*v for v in s)/max(1,len(s)))/32768+1e-9)
for t in (float(sys.argv[2]),float(sys.argv[3])):
    print(f"  nivel alrededor de {t:.2f}s:", " ".join(f"{t+d/100:.2f}:{r(t+d/100):.0f}dB" for d in range(-12,13,3)))
print("  (buscá el valle más bajo, ~-35 dB o menos: ahí va el corte)")
PY
