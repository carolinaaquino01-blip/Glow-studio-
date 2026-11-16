import json, sys, re, math

PUNCT = r'[¿?¡!.,;:"“”…]'


def _clean(t):
    t = re.sub(PUNCT, '', t).lower().replace('/', ' ')
    return re.sub(r'\s+', ' ', t).strip()


def groups(wjson, maxw=6, maxc=34, fixes=None, pause=0.25):
    d = json.load(open(wjson, encoding='utf-8', errors='replace'))
    W = [(s['text'].strip(), s['offsets']['from'] / 1000, s['offsets']['to'] / 1000)
         for s in d['transcription'] if s['text'].strip()]
    # 1) cláusulas: cortar en puntuación fuerte, coma (si la cláusula ya es larga) o pausa
    clauses, cur = [], []
    for i, (w, a, b) in enumerate(W):
        cur.append((w, a, b))
        gap = (W[i + 1][1] - b) if i + 1 < len(W) else 9
        if re.search(r'[.?!]$', w) or gap >= pause or (re.search(r',$', w) and len(cur) >= 4):
            clauses.append(cur); cur = []
    if cur:
        clauses.append(cur)
    # cláusulas de 1 palabra se pegan a la anterior si entra
    merged = []
    for c in clauses:
        if merged and len(c) == 1 and len(merged[-1]) < maxw + 2:
            merged[-1] = merged[-1] + c
        else:
            merged.append(c)
    out = []
    for c in merged:
        text = _clean(" ".join(w for w, _, _ in c))
        for k, v in (fixes or {}).items():
            text = text.replace(k, v)
        words = text.split()
        n0, n = len(c), len(words)
        if n == 0:
            continue
        # tiempos por palabra (interpolados si la corrección cambió la cantidad)
        times = [c[min(n0 - 1, round(i * n0 / n))][1] for i in range(n)]
        end = c[-1][2]
        # 2) partir parejo en trozos de <= maxw palabras y <= maxc caracteres
        k = max(math.ceil(n / maxw), math.ceil(len(text) / maxc))
        size = math.ceil(n / k)
        for j in range(0, n, size):
            chunk = words[j:j + size]
            if len(chunk) == 1 and out and j > 0:
                out[-1][0] += " " + chunk[0]
                continue
            s = times[j]
            e = times[j + size] if j + size < n else end
            out.append([" ".join(chunk), round(s, 2), round(e, 2)])
    # no terminar un grupo en palabra "colgada" (artículo/preposición): pasarla al siguiente
    WEAK = {"a","la","el","de","en","un","una","que","y","los","las","del","al","te","tu","mi","se","con","por","para","lo","o","es","sus","su"}
    for i in range(len(out) - 1):
        ws = out[i][0].split()
        moved = []
        while len(ws) > 2 and ws[-1] in WEAK and len(moved) < 2:
            moved.insert(0, ws.pop())
        if moved:
            n_old = len(out[i][0].split())
            dur = out[i][2] - out[i][1]
            cut = out[i][1] + dur * len(ws) / n_old
            out[i][0] = " ".join(ws)
            out[i + 1][0] = " ".join(moved) + " " + out[i + 1][0]
            out[i + 1][1] = round(cut, 2)
            out[i][2] = round(cut, 2)
    return out


if __name__ == "__main__":
    for g in groups(sys.argv[1]):
        print(g)
