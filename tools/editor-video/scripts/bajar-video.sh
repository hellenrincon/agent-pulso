#!/usr/bin/env bash
# Baja un vídeo de Instagram o TikTok (o de cualquier sitio que soporte yt-dlp) para analizarlo.
# Uso: bash bajar-video.sh "<enlace>" [carpeta]   (por defecto: projects/pulso/videos/referencias)
# Solo para estudiar referencias: no se republica contenido ajeno.
set -euo pipefail
ENLACE="${1:?Falta el enlace del vídeo}"
RAIZ="$(cd "$(dirname "$0")/../../.." && pwd)"
DESTINO="${2:-$RAIZ/projects/pulso/videos/referencias}"
mkdir -p "$DESTINO"
yt-dlp \
  -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b" \
  --merge-output-format mp4 \
  --write-info-json --no-playlist \
  -o "$DESTINO/%(extractor)s-%(uploader_id|autor)s-%(id)s.%(ext)s" \
  "$ENLACE"
# Resumen para el análisis: duración, tamaño y cortes de escena
ARCHIVO="$(ls -t "$DESTINO"/*.mp4 | head -1)"
echo "Bajado: $ARCHIVO"
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of default=nw=1 "$ARCHIVO"
echo "Cortes de escena (segundos):"
ffmpeg -hide_banner -i "$ARCHIVO" -filter:v "select='gt(scene,0.3)',showinfo" -f null - 2>&1 \
  | grep -o 'pts_time:[0-9.]*' | cut -d: -f2 | tr '\n' ' '; echo
