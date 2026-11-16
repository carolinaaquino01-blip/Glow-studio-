#!/usr/bin/env python3
"""Marca frases que el que habla repitió (retomas): busca secuencias de >= N palabras que aparecen dos veces.
Uso: python3 find_repeats.py carpeta/words.json [N=3]
Regla práctica: quedarse con la ÚLTIMA toma completa de cada frase (suele ser la buena) y cortar las anteriores."""
import json, re, sys
d = json.load(open(sys.argv[1], encoding="utf-8", errors="replace"))
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
W = [(re.sub(r"[^\wáéíóúñü]", "", s["text"].lower()), s["offsets"]["from"] / 1000, s["offsets"]["to"] / 1000)
     for s in d["transcription"] if s["text"].strip()]
W = [w for w in W if w[0]]
seen, hits = {}, []
for i in range(len(W) - N + 1):
    key = " ".join(w for w, _, _ in W[i:i + N])
    if key in seen and i - seen[key] >= N:
        hits.append((seen[key], i, key))
    seen.setdefault(key, i)
if not hits:
    print("No encontré repeticiones de", N, "palabras."); sys.exit()
# juntar coincidencias seguidas (misma retoma) en un solo tramo
runs = []
for a, b, key in sorted(hits, key=lambda h: (h[1] - h[0], h[0])):
    if runs and runs[-1][1] - runs[-1][0] == b - a and a <= runs[-1][2] + 1:
        runs[-1][2] = a + N - 1
    else:
        runs.append([a, b, a + N - 1])
for a, b, e in sorted(runs, key=lambda r: r[1]):
    frase = " ".join(w for w, _, _ in W[a:e + 1])
    print(f'retoma: "{frase}"  dicho en {W[a][1]:.2f}s y de nuevo en {W[b][1]:.2f}s  ->  candidato a cortar {W[a][1]:.2f}–{W[b][1]:.2f}')
