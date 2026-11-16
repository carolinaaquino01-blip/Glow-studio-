---
name: editor-videos-referencia
description: >
  Editor de videos verticales (reels, TikToks, anuncios, shorts) que primero aprende el estilo de edición
  de los videos de referencia del usuario y después edita sus crudos con ese estilo. Corta repeticiones y
  silencios, pone subtítulos, títulos, imágenes o capturas, b-roll y capturas de webs, y renderiza en MP4
  1080x1920. Usar cuando el usuario diga "editame este video", "quiero editar como estos videos",
  "aprendé mi estilo de edición", "ponele subtítulos", "sacá las partes donde me repito", o pase videos
  de referencia o crudos para editar.
user-invokable: true
argument-hint: "[videos de referencia o crudos]"
---

# Editor de videos por referencia

Esta skill trabaja en dos fases y siempre en este orden:

1. **Aprender el estilo.** El usuario pasa 2 a 5 videos de referencia (suyos o que le gusten). Se analizan y se escribe un `ESTILO.md` con números concretos. El usuario lo confirma.
2. **Editar.** El usuario pasa sus crudos y se editan uno por uno con ese estilo. Cada corrección que haga el usuario se anota en `ESTILO.md`, así el siguiente video ya sale bien.

No inventes un estilo propio. Todo lo que se vea en pantalla tiene que salir del `ESTILO.md` del usuario. Si algo no está ahí, preguntá o mantenelo mínimo.

Herramientas: **ffmpeg**, **whisper-cli** (transcripción con tiempos por palabra), **HyperFrames** (HTML → video, render cuadro a cuadro), **Chrome/puppeteer** (capturas de webs) y, en macOS, **avconvert** para los videos HDR de iPhone. Los scripts están en `scripts/`; en esta guía `$S` es la carpeta `scripts/` de esta skill.

Si están instaladas las skills `hyperframes`, `hyperframes-cli`, `media-use` o `reverse-any-video`, sumalas: `hyperframes` tiene el contrato de render y `media-use` consigue sonidos (por ejemplo un click) e imágenes.

---

## Paso 0: preparar la máquina (una sola vez)

```bash
bash $S/setup_check.sh
```

Que sea lo más automático posible para la persona: casi nunca sabe qué es ffmpeg ni una terminal.

- **Si está todo**, decile "ya tenés todo instalado" en una línea y seguí. No muestres la lista técnica.
- **Si falta algo**, preguntale una sola vez, en simple: "Me faltan unas herramientas para editar (programas gratis para video y transcripción). ¿Las instalo yo? Tarda unos minutos." Con un sí, corré:

  ```bash
  bash $S/setup_check.sh --install      # en segundo plano si incluye el modelo de whisper (≈1,5 GB)
  ```

  Mientras se instala, avanzá con la Fase 1.1 (pedir referencias), así no espera de brazos cruzados.
- **Si el script imprime `NECESITA_A_LA_PERSONA`**, es algo que pide la contraseña de la compu (Homebrew o `sudo`) o una instalación a mano (Chrome). Explicalo paso a paso, como para alguien que nunca abrió la Terminal: cómo abrirla (Cmd + Espacio, escribir "Terminal", Enter), qué pegar, que la contraseña no se ve mientras se escribe y que es normal. Cuando avise que terminó, corré `--install` de nuevo.
- Nunca escribas vos la contraseña de la persona ni le pidas que te la pase.
- HyperFrames no hace falta instalarlo: `npx` lo baja solo la primera vez.

Antes de empezar, preguntale dónde trabajar. Por defecto, una carpeta `Edicion/` con esta estructura:

```
Edicion/
  ESTILO.md            ← el estilo aprendido (se va corrigiendo)
  referencias/         ← videos de referencia y análisis
  crudos/              ← lo que manda para editar
  video1/ video2/ …    ← un proyecto HyperFrames por video (config.json adentro)
  Video 1 - v1.mp4 …   ← los renders
```

---

## Fase 1: aprender el estilo desde las referencias

### 1.1 Pedir referencias (guiado)

Explicale al usuario en una o dos frases qué se va a hacer y pedile:

- **2 a 5 videos de referencia**: archivos (arrastrados al chat o una ruta) o links públicos de Instagram/TikTok/YouTube.
- Para cada uno, **qué le gusta**: los subtítulos, el ritmo, los títulos, las imágenes que aparecen, todo.
- Si hay **marca**: colores (hex), tipografía y logo. Si no tiene, se usa lo que se vea en las referencias.

Si pasa links, intentá bajarlos con `yt-dlp` (pedí permiso para instalarlo si no está). Si no se puede, pedile que los descargue y te pase el archivo.

### 1.2 Analizar cada referencia

Por cada video:

```bash
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate,color_transfer -of compact ref.mp4
bash $S/sheet.sh ref.mp4 referencias/ref1_hoja.jpg 1 6          # un cuadro por segundo
bash $S/transcribe.sh ref.mp4 referencias/ref1                  # transcripción con tiempos
ffmpeg -i ref.mp4 -vf "select='gt(scene,0.3)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"   # cortes de plano
```

Mirá la hoja de contacto (Read sobre el .jpg) y sacá cuadros puntuales en tamaño real donde haya subtítulos o gráficos:

```bash
ffmpeg -v error -y -ss 4.2 -i ref.mp4 -frames:v 1 referencias/ref1_4s.png
```

Medí y anotá, siempre con números:

| Qué | Cómo medirlo |
|---|---|
| Subtítulos | Fuente parecida, peso, tamaño en px a 1080 de ancho, color, contorno o caja, posición vertical (en px y en % de la altura), palabras por bloque, mayúsculas o minúsculas, puntuación, si aparecen de golpe o palabra por palabra |
| Títulos fijos | Si hay, texto, posición, caja, cuánto duran, si cambian |
| Ritmo | Palabras por segundo (palabras ÷ duración), cortes visibles por video, si hay aire al principio |
| Imágenes y gráficos | Qué tipo (capturas, fotos, tarjetas, b-roll), cuánto duran, dónde aparecen, si tapan la cara, cómo entran (en seco o animadas), si tienen sonido |
| Audio | Música sí o no, efectos de sonido sí o no, nivel |
| Cámara y color | Selfie o trípode, color natural o con filtro |
| Estructura | Gancho → desarrollo → llamado a la acción, con la duración de cada parte |

### 1.3 Escribir ESTILO.md y confirmarlo

Usá la plantilla de `references/estilo_template.md`. Cada punto lleva un número o una regla que se pueda comprobar ("subtítulo 54 px, top 1170"), nunca un adjetivo suelto ("subtítulos lindos").

Mostrale al usuario un resumen corto, de 6 a 10 líneas, y preguntale si lo representa. Ajustá lo que diga.

Si quiere verlo antes de editar, armá una muestra de 5 segundos con un crudo suyo (fase 2 recortada) y que la apruebe.

---

## Fase 2: editar los crudos

Editá **uno primero**, esperá correcciones y recién después seguí con el resto. Así las correcciones se aplican a todos.

### 2.1 Revisar el crudo

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,color_transfer:stream_side_data=rotation:format=duration -of compact crudo.MOV
bash $S/sheet.sh crudo.MOV video1/hoja.jpg 3 6
```

- `color_transfer=arib-std-b67` o `smpte2084` es **HDR**. `build.py --prep` lo convierte solo; no renderices nunca en HDR.
- Si es **4K** o tiene `rotation=-90`, poné `"scale": "1080:1920"` en el config.
- Mirá en la hoja dónde está la cara (sobre todo dónde arranca el pelo), porque define dónde entran los títulos y las imágenes.

### 2.2 Transcribir y encontrar las repeticiones

```bash
bash $S/transcribe.sh crudo.MOV video1/tx
python3 $S/find_repeats.py video1/tx/words.json 3
```

Leé la transcripción completa vos mismo; el script solo ayuda. Las repeticiones suelen estar al principio: arranca una frase, se traba y la vuelve a decir.

- Quedate con la **última toma completa** de cada frase y cortá las anteriores.
- Cortá también muletillas sueltas ("ok", "eh", "bueno", "una cosa es…") cuando cortan el ritmo.
- **No cortes palabras de contenido** sin preguntar.
- El video tiene que **arrancar en la primera sílaba**, sin aire.

Probá cada unión **antes** de renderizar:

```bash
bash $S/check_cut.sh video1/tx/audio.wav <fin_tramo_A> <inicio_tramo_B>
```

Si la transcripción de la unión muestra una sílaba de más o de menos, mové el corte al valle de nivel más bajo que imprime el script (unos 30 a 60 ms) y volvé a probar. Los tiempos de whisper no son exactos: confiá en el nivel de audio.

### 2.3 Subtítulos

`autogroup.py` arma bloques parejos por frase, sin cortar palabras y sin dejar artículos colgados al final:

```bash
python3 -c "import sys; sys.path.insert(0,'$S'); from autogroup import groups; import json; print(json.dumps(groups('video1/tx/words.json', maxw=6, maxc=34), ensure_ascii=False, indent=0))"
```

- Ajustá `maxw` y `maxc` a lo que diga `ESTILO.md`.
- Revisalos a mano: corregí nombres, marcas y números en cifra ("15 de noviembre", "40%") y lo que whisper entendió mal.
- Respetá la forma de hablar: si es rioplatense, "podés", no "puedes".
- Borrá los bloques que caen en tramos cortados.

### 2.4 config.json

Escribí `video1/config.json` (el formato completo está arriba de `scripts/build.py`). Lo central:

- `segments`: los tramos del original que se quedan.
- `captions`: van en tiempo del **original**; `build.py` los reacomoda solo.
- `titles` y `overlays`: van en tiempo **final**, después de cortar. Para calcularlo: `final = suma de los tramos anteriores + (t − inicio del tramo)`.
- `style`: los valores de `ESTILO.md` (las claves están en `STYLE_DEFAULTS` dentro de `build.py`).

Tipos de overlay:

| `kind` | Para qué | Notas |
|---|---|---|
| `img` | Captura, foto o screenshot | Va en la franja de arriba (`top` y `width`), sin tapar la cara |
| `html` | Tarjeta armada en HTML: un dato, una lista, una agenda, un gráfico | Escribí un HTML chico con los colores de la marca del usuario |
| `video` | Pantalla completa, sin sonido: b-roll o una web que scrollea | Tapa la cara a propósito por unos segundos, como un corte |

- Los títulos se esconden solos mientras hay un overlay.
- Si el estilo lleva sonido al aparecer las imágenes, conseguí un click (skill `media-use` o uno del usuario) y poné `"click_sound"`.

### 2.5 B-roll y capturas de webs

**B-roll** de otro video:

1. Mirá la hoja de contacto a 5 o 30 cuadros por segundo para ubicar el principio y el fin exacto de cada plano.
2. Revisá que no tenga **subtítulos quemados**. Si los tiene, usá solo los tramos limpios o pedile al usuario el original sin texto.
3. Armá un mp4 sin audio con los planos:

```bash
ffmpeg -y -i evento.mov -filter_complex "[0:v]trim=0:0.53,setpts=1.6*(PTS-STARTPTS)[a];[0:v]trim=1.25:1.85,setpts=1.6*(PTS-STARTPTS)[b];[a][b]concat=n=2:v=1:a=0,fps=30,scale=1080:1920,format=yuv420p[v]" -map "[v]" -an -c:v libx264 -crf 14 broll.mp4
```

`setpts=1.6*` lo pasa a 0,625x. Sirve cuando los planos limpios son cortos; no bajes de 0,6x.

**Web o landing**: capturala hoy, porque las cuentas regresivas y los precios cambian.

```bash
node $S/capture_site.cjs https://la-web.com video1/web
bash $S/scroll_video.sh video1/web/pagina_completa.png video1/web/scroll.mp4 4 0 1700
```

- Chrome headless con `--screenshot` corta las webs del lado derecho. Usá `capture_site.cjs`, que emula un celular.
- Elegí `y_inicio` de modo que el subtítulo (en `cap_top`) no caiga encima de un texto grande de la web.

### 2.6 Armar, revisar y renderizar

```bash
python3 $S/build.py video1/config.json --prep      # corta, normaliza el audio a -14 LUFS, pasa a SDR
cd video1 && npx hyperframes check --json          # arreglá todos los errores
npx hyperframes snapshot --at 0.5,3,6,9,12,15      # cuadros en los cambios importantes
```

Mirá los snapshots (están en `.hyperframes/artifacts/snapshots/<id>/contact-sheet.jpg`) y revisá:

- [ ] Ningún subtítulo o título tapa la cara.
- [ ] Ninguna palabra quedó cortada entre dos bloques.
- [ ] Los títulos no se pisan con los overlays.
- [ ] El subtítulo se lee arriba del b-roll y de las capturas.
- [ ] La piel se ve natural, no naranja ni lavada.

Después renderizá y verificá:

```bash
python3 $S/build.py video1/config.json --render v1
ffmpeg -i "Video 1 - v1.mp4" -ar 16000 -ac 1 /tmp/out.wav && whisper-cli -m <modelo> -l es -f /tmp/out.wav -nt
```

Leé la transcripción del render: no tiene que quedar ninguna repetición ni sílaba suelta en las uniones. Mandale el MP4 al usuario.

### 2.7 Correcciones

Cada corrección del usuario va a dos lugares:

1. Al video actual: subí la versión (`v2`, `v3`…) y no pises la anterior.
2. A `ESTILO.md`, en la sección "Correcciones del usuario", con la regla general ("imágenes sin bordes redondeados", "nunca tapar la cara").

Así los próximos videos ya salen corregidos.

---

## Errores que ya se pagaron (leer antes de empezar)

- **HDR de iPhone**: renderizar en HDR encima los subtítulos, y convertirlo con el pipeline de HyperFrames deja la piel naranja. Usá `--prep`, que en macOS pasa por `avconvert`, y renderizá con `--sdr` (`build.py` ya lo hace).
- **Subtítulos encimados**: cada bloque se prende y apaga con `tl.set(... opacity)` sobre el `span`, no sobre el clip. `build.py` ya lo hace así.
- **Uniones con sílabas de más**: los tiempos de whisper no son exactos. Probá siempre con `check_cut.sh` y escuchá el render transcribiéndolo.
- **Encodes lentos**: en Mac usá `hevc_videotoolbox` para los intermedios (segundos contra minutos con x265). No corras dos renders a la vez.
- **Shell**: en zsh, `for c in "a b"` no separa palabras. Para esos bucles usá `bash -c '...'`.
- **Capturas de webs cortadas**: usá `capture_site.cjs`, no `--screenshot` de Chrome.
- **Capturas viejas**: si la web tiene cuenta regresiva o fecha, recapturala el día que editás.
- **B-roll con subtítulos quemados**: revisalo en una hoja de contacto de la franja del medio antes de usarlo.
- **Contraste**: texto blanco sobre colores claros o saturados (naranja, amarillo) no se lee. Usá texto negro.
- **Caras**: nunca le pongas nombre a una cara por tu cuenta. Preguntá quién es quién.
- **Animaciones**: si las referencias son "orgánicas", no agregues zooms, rebotes, whooshes ni música. Que entre y salga en seco.
- **Archivos de Meta y otras plataformas**: algunas aceptan hasta 100 MB por video. Si te pasás, re-encodeá con `-crf 20`.

## Entrega

- Mandá el MP4 con `SendUserFile`, o decí la ruta.
- Resumí en 3 a 5 líneas qué se cortó, qué se agregó y qué quedó pendiente (por ejemplo: "el b-roll tenía subtítulos quemados, pasame el original").
- Ofrecé seguir con el próximo crudo.
