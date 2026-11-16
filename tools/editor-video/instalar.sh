#!/usr/bin/env bash
# Instala las herramientas del agente editor de vídeos. Se puede correr varias veces sin problema.
#   bash tools/editor-video/instalar.sh            instala todo
#   bash tools/editor-video/instalar.sh --skills   además actualiza las skills de HyperFrames en .claude/skills
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$(cd "$AQUI/../.." && pwd)"
export HYPERFRAMES_NO_TELEMETRY=1 HYPERFRAMES_NO_UPDATE_CHECK=1

paso() { printf '\n== %s ==\n' "$*"; }

paso "1/4 FFmpeg (cortar, unir y arreglar el sonido)"
if ! command -v ffmpeg >/dev/null; then
  if command -v apt-get >/dev/null; then
    SUDO=""; [ "$(id -u)" -ne 0 ] && SUDO="sudo"
    $SUDO apt-get update -qq && $SUDO apt-get install -y -qq ffmpeg
  elif command -v brew >/dev/null; then
    brew install ffmpeg
  else
    echo "Instala FFmpeg a mano: https://ffmpeg.org/download.html" >&2; exit 1
  fi
fi
ffmpeg -version | head -1

paso "2/4 Node.js 22 o más nuevo (lo necesita HyperFrames)"
command -v node >/dev/null || { echo "Falta Node.js 22+: https://nodejs.org" >&2; exit 1; }
NODE_MAYOR="$(node -p 'process.versions.node.split(".")[0]')"
[ "$NODE_MAYOR" -ge 22 ] || { echo "Node.js $NODE_MAYOR es viejo: hace falta 22 o más" >&2; exit 1; }
node -v

paso "3/4 Whisper y yt-dlp (Python)"
python3 -m pip install -q --upgrade -r "$AQUI/requirements.txt"
python3 -c "import faster_whisper; print('faster-whisper', faster_whisper.__version__)"
yt-dlp --version | sed 's/^/yt-dlp /'

paso "4/4 HyperFrames, GSAP y la letra Caveat"
(cd "$AQUI" && npm install --no-audit --no-fund --loglevel=error)
"$AQUI/node_modules/.bin/hyperframes" --version | sed 's/^/hyperframes /'

if [ "${1:-}" = "--skills" ]; then
  paso "Skills de HyperFrames para Claude Code"
  (cd "$RAIZ" && npx -y skills add heygen-com/hyperframes \
     --skill hyperframes --skill hyperframes-cli --skill hyperframes-registry --skill media-use \
     -a claude-code -y)
fi

printf '\nListo. Para probar todo: bash %s/probar.sh\n' "tools/editor-video"
