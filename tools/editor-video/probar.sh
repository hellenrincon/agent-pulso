#!/usr/bin/env bash
# Prueba rápida de las 4 herramientas. Crea todo en una carpeta temporal y no toca el repo.
# Necesita acceso a huggingface.co (modelo de Whisper, la primera vez) y a TikTok/Instagram (yt-dlp).
set -uo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1 PATH="$AQUI/node_modules/.bin:$PATH"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
OK=0; MAL=0
bien() { echo "  ✓ $*"; OK=$((OK+1)); }
mal()  { echo "  ✗ $*"; MAL=$((MAL+1)); }

echo "1. FFmpeg: crear un clip vertical de 4 s, cortarlo a 3 s y nivelar el sonido"
if ffmpeg -v error -f lavfi -i "color=c=0x5A1A28:s=1080x1920:d=4" -f lavfi -i "sine=f=440:d=4" \
     -shortest -c:v libx264 -c:a aac "$TMP/base.mp4" \
   && ffmpeg -v error -ss 0.5 -t 3 -i "$TMP/base.mp4" -af "loudnorm=I=-14:TP=-1.5" \
     -c:v libx264 -c:a aac "$TMP/corte.mp4"; then
  bien "corte de $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/corte.mp4") s"
else mal "FFmpeg no pudo cortar"; fi

echo "2. Whisper: sacar subtítulos de una muestra de voz"
if curl -fsSL -o "$TMP/voz.flac" https://huggingface.co/datasets/Narsil/asr_dummy/resolve/main/mlk.flac \
   && python3 -I "$AQUI/scripts/transcribir.py" "$TMP/voz.flac" --modelo "${WHISPER_MODELO:-small}" --idioma en \
   && grep -qi dream "$TMP/voz.srt"; then
  bien "subtítulos: $(sed -n 3p "$TMP/voz.srt")"
else mal "Whisper no transcribió (¿está permitido huggingface.co?)"; fi

echo "3. yt-dlp: leer los datos de un vídeo público de TikTok (sin bajarlo)"
if INFO="$(yt-dlp --skip-download --print '%(extractor)s %(duration)ss %(width)sx%(height)s' \
     'https://www.tiktok.com/@scout2015/video/6718335390845095173' 2>/dev/null)" && [ -n "$INFO" ]; then
  bien "$INFO"
else mal "yt-dlp no llegó a TikTok (¿está permitido tiktok.com?)"; fi

echo "4. HyperFrames: armar un Reel con gancho y subtítulos y exportarlo a MP4"
if [ -f "$TMP/voz.palabras.json" ] \
   && ffmpeg -v error -i "$TMP/corte.mp4" -i "$TMP/voz.flac" -map 0:v -map 1:a -t 3 -c:v copy -c:a aac "$TMP/clip.mp4" \
   && python3 -I "$AQUI/scripts/armar-reel.py" "$TMP/clip.mp4" --palabras "$TMP/voz.palabras.json" \
        --gancho "Prueba PULSO" --salida "$TMP/reel" >/dev/null \
   && (cd "$TMP/reel" && hyperframes check >/dev/null 2>&1 && hyperframes render -o reel.mp4 >/dev/null 2>&1) \
   && [ -s "$TMP/reel/reel.mp4" ]; then
  bien "Reel exportado: $(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=s=x:p=0 "$TMP/reel/reel.mp4")"
else mal "HyperFrames no exportó el Reel (corre 'npx hyperframes doctor' en tools/editor-video)"; fi

echo; echo "Resultado: $OK bien, $MAL con problemas"
[ "$MAL" -eq 0 ]
