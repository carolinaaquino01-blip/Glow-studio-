#!/usr/bin/env python3
"""Arma un proyecto HyperFrames (video vertical con subtítulos, títulos y overlays) desde un config JSON.

Uso:
  python3 build.py proyecto/config.json --prep          # corta, normaliza audio, pasa a SDR
  python3 build.py proyecto/config.json                 # solo reescribe las composiciones
  python3 build.py proyecto/config.json --render v1     # renderiza a <carpeta padre>/<out> - v1.mp4

Config (los tiempos de "captions" van en el tiempo del ORIGINAL; titles y overlays en el tiempo FINAL):
{
  "src": "/ruta/al/crudo.MOV",           # absoluta o relativa al config
  "out": "Video 1",
  "scale": "1080:1920",                   # opcional: para fuentes 4K o de otra resolución
  "segments": [[0.4, 12.3], [13.1, 30.0]],
  "captions": [["texto del bloque", start, end], ...],
  "titles":   [["Título fijo arriba", start, end], ...],
  "overlays": [
     {"kind": "img",   "src": "/ruta/captura.jpg", "start": 3, "end": 6, "top": 180, "width": 700},
     {"kind": "html",  "src": "/ruta/tarjeta.html", "start": 8, "end": 11, "top": 180, "scale": 1.0},
     {"kind": "video", "src": "/ruta/broll.mp4", "start": 12, "end": 15, "media_start": 0}
  ],
  "click_sound": "/ruta/click.mp3",       # opcional: suena al entrar cada overlay con "click": true
  "style": { ... }                         # opcional: ver STYLE_DEFAULTS (salen del ESTILO.md del usuario)
}
"""
import json, os, subprocess, sys, shutil, html

STYLE_DEFAULTS = {
    # subtítulos
    "cap_font": "Montserrat", "cap_weight": 600, "cap_size": 54, "cap_color": "#ffffff",
    "cap_stroke": 5, "cap_stroke_color": "#000000", "cap_top": 1170, "cap_max_width": 860,
    "cap_box": None,                        # p.ej. "#000000" para subtítulo con caja en vez de contorno
    "cap_uppercase": False,
    # títulos fijos de arriba
    "title_font": "Montserrat", "title_weight": 700, "title_size": 58, "title_top": 260,
    "title_color": "#ffffff", "title_box": "#000000", "title_radius": 14, "title_max_width": 880,
    # overlays
    "ov_radius": 0, "ov_shadow": "0 14px 40px rgba(0,0,0,0.35)",
}


def run(cmd, **kw):
    print("+", " ".join(cmd) if isinstance(cmd, list) else cmd)
    subprocess.run(cmd, check=True, **kw)


def remap(t, segs):
    acc = 0.0
    for a, b in segs:
        if a <= t <= b:
            return round(acc + (t - a), 3)
        acc += b - a
    return None


def final_duration(segs):
    return round(sum(b - a for a, b in segs), 3)


def absp(root, p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(root, p))


def is_hdr(src):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=color_transfer", "-of", "csv=p=0", src], capture_output=True, text=True).stdout
    return any(k in out for k in ("arib-std-b67", "smpte2084"))


def prep(cfg, root):
    src = absp(root, cfg["src"])
    assets = os.path.join(root, "assets")
    os.makedirs(assets, exist_ok=True)
    segs = cfg["segments"]
    vf = f",scale={cfg['scale']}" if cfg.get("scale") else ""
    parts = []
    for i, (a, b) in enumerate(segs):
        parts.append(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS{vf}[v{i}];"
                     f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:st=0:d=0.012,afade=t=out:st={b-a-0.012:.3f}:d=0.012[a{i}];")
    concat = "".join(f"[v{i}][a{i}]" for i in range(len(segs)))
    fc = "".join(parts) + f"{concat}concat=n={len(segs)}:v=1:a=1[v][a];[a]loudnorm=I=-14:TP=-1.5:LRA=11[ao]"
    hdr = is_hdr(src)
    mac = shutil.which("avconvert") is not None
    if hdr and mac:
        # iPhone HDR (HLG): se corta en 10 bit y se pasa a SDR con la conversión de Apple (la que mejor respeta la piel)
        tmp = os.path.join(assets, "footage_hdr.mp4")
        venc = ["-c:v", "hevc_videotoolbox", "-b:v", "45M", "-profile:v", "main10", "-pix_fmt", "p010le", "-tag:v", "hvc1",
                "-color_primaries", "bt2020", "-color_trc", "arib-std-b67", "-colorspace", "bt2020nc"]
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[ao]", *venc,
             "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
        run(["avconvert", "--source", tmp, "--preset", "PresetHighestQuality",
             "--output", os.path.join(assets, "footage.mov"), "--replace"])
        os.remove(tmp)
    else:
        if hdr:
            # fuera de macOS: tonemap con zscale (si tu ffmpeg lo trae). Revisar la piel en un cuadro.
            fc = fc.replace("[v][a];", "[vr][a];[vr]zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,"
                                       "tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p[v];")
        run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", fc, "-map", "[v]", "-map", "[ao]",
             "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p",
             "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
             os.path.join(assets, "footage.mov")])


def write_compositions(cfg, root):
    st = dict(STYLE_DEFAULTS, **cfg.get("style", {}))
    segs = cfg["segments"]
    D = final_duration(segs)
    comp = os.path.join(root, "compositions")
    assets = os.path.join(root, "assets")
    os.makedirs(comp, exist_ok=True)
    os.makedirs(assets, exist_ok=True)

    # ---------- subtítulos: cada bloque dura hasta que empieza el siguiente
    caps = []
    for text, s, e in cfg["captions"]:
        rs = remap(s, segs)
        if rs is None:
            nxt = [a for a, b in segs if a > s]
            rs = remap(nxt[0], segs) if nxt else None
        if rs is not None:
            caps.append([text, rs])
    caps.sort(key=lambda c: c[1])
    rows = []
    for i, (text, s) in enumerate(caps):
        e = caps[i + 1][1] if i + 1 < len(caps) else D
        if e - s > 0.05:
            rows.append((f"c{i}", html.escape(text.upper() if st["cap_uppercase"] else text), round(s, 3), round(e - s, 3)))
    divs = "\n".join(f'    <div id="{i}" class="clip cap" data-start="{s}" data-duration="{d}" data-track-index="0"><span>{t}</span></div>'
                     for i, t, s, d in rows)
    sets = ["    tl.set('.cap span', { opacity: 0 }, 0);"]
    for i, t, s, d in rows:
        sets.append(f"    tl.set('#{i} span', {{ opacity: 1 }}, {s});")
        sets.append(f"    tl.set('#{i} span', {{ opacity: 0 }}, {round(s + d, 3)});")
    if st["cap_box"]:
        cap_look = f"background: {st['cap_box']}; padding: 4px 16px 8px; border-radius: 10px; -webkit-box-decoration-break: clone; box-decoration-break: clone; display: inline;"
        wrap_open, wrap_close = '<div class="w">', "</div>"
    else:
        cap_look = (f"-webkit-text-stroke: {st['cap_stroke']}px {st['cap_stroke_color']}; paint-order: stroke fill;"
                    " text-shadow: 0 2px 8px rgba(0,0,0,0.45); display: block;")
        wrap_open = wrap_close = ""
    divs = divs.replace("<span>", wrap_open + "<span>").replace("</span>", "</span>" + wrap_close)
    open(os.path.join(comp, "captions.html"), "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 0; right: 0; top: {st["cap_top"]}px; display: flex; justify-content: center; text-align: center; overflow: visible; }}
    .cap .w {{ max-width: {st["cap_max_width"]}px; text-wrap: balance; line-height: 1.38; }}
    .cap span {{
      max-width: {st["cap_max_width"]}px; text-wrap: balance;
      font-family: "{st["cap_font"]}", sans-serif; font-weight: {st["cap_weight"]}; font-size: {st["cap_size"]}px; line-height: 1.12;
      color: {st["cap_color"]}; letter-spacing: -0.005em; {cap_look}
    }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{divs}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(sets)}
    window.__timelines["captions"] = tl;
  </script>
</template>
''')

    # ---------- títulos: se recortan alrededor de los overlays (nunca título y overlay a la vez)
    ovs = sorted((o["start"], o["end"]) for o in cfg.get("overlays", []))
    titles = []
    for text, s, e in cfg.get("titles", []):
        pieces = [(s, e)]
        for a, b in ovs:
            nxt = []
            for ps, pe in pieces:
                if b <= ps or a >= pe:
                    nxt.append((ps, pe)); continue
                if a > ps: nxt.append((ps, a))
                if b < pe: nxt.append((b, pe))
            pieces = nxt
        titles += [[text, round(ps, 3), round(pe, 3)] for ps, pe in pieces if pe - ps >= 1.0]
    tdivs = [f'    <div id="t{k}" class="clip topic" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="0">'
             f'<div class="wrap"><span data-var-text="topic{k}">{html.escape(t)}</span></div></div>'
             for k, (t, s, e) in enumerate(titles, 1)]
    box = (f"background: {st['title_box']}; padding: 4px 20px 8px; border-radius: {st['title_radius']}px; "
           "-webkit-box-decoration-break: clone; box-decoration-break: clone;") if st["title_box"] else \
          "text-shadow: 0 2px 10px rgba(0,0,0,0.5);"
    open(os.path.join(comp, "title.html"), "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    .topic {{ position: absolute; left: 0; right: 0; top: {st["title_top"]}px; display: flex; justify-content: center; text-align: center; }}
    .topic .wrap {{ max-width: {st["title_max_width"]}px; text-wrap: balance; font-family: "{st["title_font"]}", sans-serif; font-weight: {st["title_weight"]}; font-size: {st["title_size"]}px; line-height: 1.38; letter-spacing: -0.01em; }}
    .topic .wrap span {{ color: {st["title_color"]}; {box} }}
  </style>
  <div id="root" data-composition-id="title" data-width="1080" data-height="1920">
{chr(10).join(tdivs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["title"] = tl;
  </script>
</template>
''')

    # ---------- overlays
    click = cfg.get("click_sound")
    if click:
        shutil.copy(absp(root, click), os.path.join(assets, "click.mp3"))
    hosts, audios, vids = [], [], []
    for k, ov in enumerate(cfg.get("overlays", []), 1):
        oid = f"ov{k}"
        s, e = ov["start"], ov["end"]
        d = round(e - s, 3)
        if click and ov.get("click", ov["kind"] != "video"):
            audios.append(f'      <audio id="sfx-click-{k}" src="assets/click.mp3" data-start="{s}" data-duration="0.37" data-track-index="{20 + k}" data-volume="0.7"></audio>')
        src = absp(root, ov["src"])
        name = f"{oid}_{os.path.basename(src)}"
        if ov["kind"] != "html":
            shutil.copy(src, os.path.join(assets, name))
        if ov["kind"] == "video":
            vids.append(f'      <video id="{oid}" class="clip broll" src="assets/{name}" data-start="{s}" data-duration="{d}" '
                        f'data-media-start="{ov.get("media_start", 0)}" data-track-index="{3 + k}" muted playsinline></video>')
            continue
        if ov["kind"] == "html":
            inner = open(src).read()
            sc = ov.get("scale", 1.0)
            body = f'<div class="scaler" style="transform: scale({sc}); transform-origin: 50% 0;">{inner}</div>'
            css = ""
        else:  # img
            body = f'<img src="assets/{name}" alt="">'
            css = (f"#{oid}-box img {{ display: block; width: {ov.get('width', 760)}px; height: auto; "
                   f"border-radius: {st['ov_radius']}px; box-shadow: {st['ov_shadow']}; }}")
        open(os.path.join(comp, f"{oid}.html"), "w").write(f'''<template>
  <style>
    #root {{ position: absolute; inset: 0; }}
    #{oid}-box {{ position: absolute; left: 0; right: 0; top: {ov.get("top", 180)}px; display: flex; justify-content: center; }}
    {css}
  </style>
  <div id="root" data-composition-id="{oid}" data-width="1080" data-height="1920">
    <div id="{oid}-box" class="clip" data-start="0" data-duration="{d}" data-track-index="0">{body}</div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["{oid}"] = tl;
  </script>
</template>
''')
        hosts.append(f'      <div id="{oid}-host" class="ovhost" data-composition-id="{oid}" data-composition-src="compositions/{oid}.html" '
                     f'data-start="{s}" data-duration="{d}" data-track-index="{3 + k}" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')

    tvars = [{"id": f"topic{k}", "type": "string", "label": f"Título {k}", "default": t[0]} for k, t in enumerate(titles, 1)]
    open(os.path.join(root, "index.html"), "w").write(f'''<!doctype html>
<html lang="es" data-composition-variables='{json.dumps(tvars, ensure_ascii=False).replace("'", "&#39;")}'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; }}
      #footage, .broll {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
      #footage {{ z-index: 0; }} .broll {{ z-index: 1; }}
      #title-host {{ z-index: 2; }} .ovhost {{ z-index: 3; }} #captions-host {{ z-index: 4; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920">
      <video id="footage" class="clip" src="assets/footage.mov" data-start="0" data-duration="{D}" data-track-index="0" data-has-audio="true" playsinline></video>
{chr(10).join(vids)}
{chr(10).join(audios)}
      <div id="title-host" data-composition-id="title" data-composition-src="compositions/title.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
{chr(10).join(hosts)}
      <div id="captions-host" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
''')
    print(f"duración final {D}s · {len(rows)} subtítulos · {len(titles)} títulos · {len(cfg.get('overlays', []))} overlays")


def main():
    cfgp = os.path.abspath(sys.argv[1])
    cfg = json.load(open(cfgp))
    root = os.path.dirname(cfgp)
    if not os.path.exists(os.path.join(root, "hyperframes.json")):
        open(os.path.join(root, "hyperframes.json"), "w").write(json.dumps({
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
            "media": {"autoProxy": True}}, indent=2))
        open(os.path.join(root, "meta.json"), "w").write(json.dumps({"id": os.path.basename(root), "name": os.path.basename(root)}))
    if "--prep" in sys.argv:
        prep(cfg, root)
    write_compositions(cfg, root)
    if "--render" in sys.argv:
        ver = sys.argv[sys.argv.index("--render") + 1]
        out = os.path.join(os.path.dirname(root), f"{cfg['out']} - {ver}.mp4")
        run(["npx", "hyperframes", "render", "--sdr", "--crf", "16", "--output", out], cwd=root)


if __name__ == "__main__":
    main()
