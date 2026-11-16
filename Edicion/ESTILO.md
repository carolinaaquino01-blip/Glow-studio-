# Estilo de edición: Glow Studio

Referencias analizadas:
- `referencias/ref1.mov` (reel de @hannarek, 14,6 s). Le gusta: "el dinamismo, colores que matchean con el entorno y seguimiento de los subtítulos". Solo se toman esas tres cosas.
- `referencias/ref2.mov` (reel de @andybadilloo, 14,6 s). Le gusta: "cómo plantea solución, es gráfica, agrega memes, hace chistes y ayuda a alguien puntual".

> Ojo: la caja gris chica de abajo ("tu casa si estás rentando…") son los subtítulos automáticos de Instagram, no son parte de la edición. No se imitan.

## Idea madre
Le habla a alguien puntual con un problema concreto y le da la solución, con humor. El texto sigue la voz palabra por palabra, los colores salen de lo que hay en cuadro y los memes refuerzan los chistes. Rápido y vivo, pero la persona sigue siendo la protagonista.

## Formato
- 1080x1920, 30 fps, 15–30 s
- Cámara: trípode, plano medio a cuerpo entero. Color natural, sin filtro.

## Ritmo y cortes (dinamismo)
- Voz: ~3,2 palabras por segundo
- Un cambio de plano cada **~2,5 s** (en la ref: 5 cortes en 14,6 s): saltos de plano (cerca ↔ lejos), un inserto de detalle de 2–4 s
- Aire al principio: 0 s, arranca en la primera sílaba
- Se corta siempre: repeticiones, muletillas, silencios de más de 0,3 s

## Subtítulos (texto cinético)
- Fuente: sans **extendida y muy pesada** (ref: tipo Druk Wide / Clash). Equivalente libre: **Archivo Expanded Black (900)**, ancho 125
- TODO EN MAYÚSCULAS, interletrado justo (-1 %), interlineado 0,9, **centrado**, sin contorno, sin caja, sin sombra
- Tamaños a 1080 de ancho: base **~100 px**; la palabra clave de la frase **~150 px** (ej. "UN HACK", "CASA"); palabras de relleno **~80 px**
- Posición: bloque en el **tercio de arriba**, top **~150–220 px** (8–11 %), nunca sobre la cara
- Palabras sueltas de transición ("ES", "NADA", "SI ESTÁS"): blancas, ~90 px, a la altura del pecho (~35 % = 670 px), al costado del cuerpo
- **Seguimiento**: cada palabra **aparece en seco en el momento exacto en que se dice** y se suma a las anteriores; la frase se arma en 1–3 renglones y se borra entera cuando arranca la siguiente
- Frases de 3–6 palabras, máximo 3 renglones
- Repeticiones habladas se apilan: "LO NECESITO." ×3 = 3 renglones iguales; "NO NO NO" = cada "NO" aparece en un lugar distinto alrededor de la persona
- Puntuación: casi nada; punto final solo en frases remate ("LO NECESITO.")
- Variante tranquila (ref2), para partes explicativas: **una sola palabra a la vez**, en minúscula normal, letra redonda y gruesa (tipo Fredoka Bold), ~100 px, top ~20 % (≈380 px). Cada palabra reemplaza a la anterior justo cuando se dice
- Cuándo usar cada una: **armado en mayúsculas** para gancho, chistes y remate; **palabra a palabra** para la explicación o la solución

## Colores que matchean con el entorno
**Es una regla, no una paleta fija.** Los colores de las referencias son solo ejemplos: en cada video se sacan de nuevo de lo que tiene la persona alrededor.
1. Mirar el cuadro y elegir 2–3 objetos con color propio: ropa, accesorios, lámparas, cuadros, plantas, muebles.
2. Sacar el color con cuentagotas de esos objetos y quedarse con el tono (el matiz), no con el valor exacto.
3. Ajustar el brillo según lo que hay **detrás del texto**:
   - Fondo claro → versión **oscura y saturada** del tono (ref1: pared blanca → rojo de la bufanda y azul marino de los marcos).
   - Fondo oscuro → versión **clara y pastel** del tono (ref2: living oscuro → amarillo pálido `#FBF49E`, sacado de la luz cálida de las lámparas).
4. Comprobar el contraste: texto contra fondo de 4,5:1 o más. Si no llega, oscurecer o aclarar más; no agregar contorno.
5. Un color por frase, alternando (nunca el mismo dos frases seguidas). Blanco o el tono más neutro para palabras sueltas de transición.

Antes de renderizar, anotar en el `config.json` de cada video de qué objeto sale cada color.

## Títulos fijos
- No hay. El texto cinético cumple esa función.

## Imágenes, gráficos y b-roll
- **Memes y recortes (ref2)**: personajes de películas o series, fotos o reacciones **sin fondo (recortados)**, que remiten al chiste o a la persona a la que se le habla (ref2: chicas de oficina de películas al decir "godín / trabajo de 9 a 5")
  - Van en la **franja de abajo** (desde ~60 % de la altura hacia abajo), varios superpuestos, **nunca tapan la cara**
  - Duran lo que dura la frase del chiste (~2–3 s), entran y salen **en seco**
  - Siempre preguntarle al usuario qué meme o personaje usar; no elegir caras por cuenta propia
- **Gráficos (ref2)**: cuando se plantea la solución, tarjeta simple con los pasos o la lista ("3 formas de…"), con los colores del entorno
- **Insertos (ref1)**: detalle del producto u objeto a pantalla completa, 2–4 s, en seco. Durante el inserto el texto se pausa

## Marca
- Colores: *(pendiente de confirmar por el usuario)* · Tipografía: Archivo Expanded Black · Logo: *(pendiente)*

## Audio
- Voz normalizada a -14 LUFS · Efectos: no
- **Música de fondo: la agrega el usuario en Instagram al publicar** (16/11/2026). El MP4 se entrega **solo con la voz**, sin música.
  - Como después se suma música, la voz va limpia y normalizada a -14 LUFS, sin silencios largos

## Estructura
- **Gancho (0–3 s)**: el problema o la situación, dicho a alguien puntual (ref2: "Si yo fuera godín o tuviera un trabajo de 9 a 5…"; ref1: "les tengo un hack increíble"). Texto armado grande + meme
- **A quién le habla (3–6 s)**: nombra al público ("Amigas, yo sé que muchas aquí son godines…")
- **Solución**: pasos concretos ("veo 3 formas…"), con gráfico o lista en pantalla, texto palabra a palabra
- **Chistes**: reacciones exageradas o comparaciones, reforzadas con meme o con texto apilado ("NO NO NO", "LO NECESITO" ×3)
- **Remate**: frase corta repetida o llamado a la acción

## Correcciones del usuario
<!-- Una regla por línea, con fecha -->
- 16/11/2026: no copiar los colores exactos de las referencias; la regla es sacar los colores del entorno de cada video
- 16/11/2026: no meter música en el render; la pone el usuario en Instagram
