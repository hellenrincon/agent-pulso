# Skill: editar un Reel

**Quién la usa:** Editor de vídeos. **Entrega:** MP4 9:16 + `.srt` + 3 fotogramas + tarjeta de decisión.
**Herramientas:** `tools/editor-video/` (instalar con `bash tools/editor-video/instalar.sh`).

## Entrada
- Vídeos crudos de la fundadora (`medios`, `tipo: "video"`, `etapa: "bruto"`), guardados en `videos/crudos/`.
- Guion aprobado (skill `guion-de-reel`): gancho, escenas, segundos, texto en pantalla, cierre.
- Música (campo `musica` de la propuesta) o "sonido original".

## Pasos

1. **Juntar y cortar (FFmpeg).**
   - Ver duración y tamaño: `ffprobe -v error -show_entries format=duration:stream=width,height -of default=nw=1 toma.mp4`
   - Cortar un trozo: `ffmpeg -ss 2.5 -to 6.0 -i toma.mp4 -c:v libx264 -crf 18 -c:a aac trozo1.mp4`
   - Pasar a 9:16 si viene horizontal: `-vf "crop=ih*9/16:ih,scale=1080:1920"`
   - Unir trozos en orden: lista en `lista.txt` (`file 'trozo1.mp4'`…) y `ffmpeg -f concat -safe 0 -i lista.txt -c copy unido.mp4`
   - Nivelar sonido para Instagram: `-af "loudnorm=I=-14:TP=-1.5"`
   - Quitar silencios largos: buscar con `-af silencedetect=noise=-35dB:d=0.6` y cortar ahí.
2. **Subtítulos (Whisper).** `python3 tools/editor-video/scripts/transcribir.py videos/trabajo/unido.mp4 --idioma es`. Leer el `.srt` y corregir a mano palabras mal oídas en el `.palabras.json` (mismo orden, mismos tiempos). Si hay música fuerte, `--modelo medium`.
3. **Armar (HyperFrames).** `python3 tools/editor-video/scripts/armar-reel.py videos/trabajo/unido.mp4 --palabras videos/trabajo/unido.palabras.json --gancho "<gancho del guion>" [--musica pista.mp3] --salida videos/trabajo/<reel>`.
   Para algo más (títulos por escena, transiciones, cierre con emblema), leer primero la skill `hyperframes` y buscar bloques con `npx hyperframes catalog`.
4. **Revisar.** Dentro de la carpeta del proyecto: `npx hyperframes check` (0 errores), `npx hyperframes snapshot` en el gancho, el momento clave y el cierre, y `npx hyperframes audio reel.mp4 --json` después de exportar.
5. **Exportar.** `npx hyperframes render -o ../../salida/<reel>.mp4`.
6. **Entregar.** Subir MP4 y `.srt` a `medios` (`etapa: "terminado"`, `categoria: "reel-editado"`, `propuesta` = id del post), tarjeta de decisión con los 3 fotogramas y una línea de qué cambió frente al guion.

## Lista de control antes de la tarjeta
- [ ] 1080×1920, 15 a 30 s, gancho legible en los primeros 2 s.
- [ ] Subtítulos sin errores en nombres (PULSO, matcha, cold brew, RUN, RIDE).
- [ ] Nada tapa la cara, el vaso ni el logo; textos dentro del 80 % central (Instagram tapa los bordes).
- [ ] Colores y letras del manual versión Vino.
- [ ] Sonido entre −16 y −14 LUFS, sin saturar.
- [ ] Música con licencia comercial o sonido original.

## Analizar una referencia (Instagram o TikTok)
1. `bash tools/editor-video/scripts/bajar-video.sh "<enlace>"` (guarda en `videos/referencias/` y lista los cortes).
2. `transcribir.py` sobre el vídeo bajado para ver el texto y el ritmo de la voz.
3. Tarjeta con: duración, número de cortes, segundos del gancho, estilo de subtítulos, qué tomar para PULSO y qué no. **No se republica el vídeo.**
