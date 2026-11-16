# Herramientas del editor de vídeos

Todo lo que usa el agente **Editor de vídeos** (`templates/agents/editor-video.md`) para cortar, subtitular, animar y exportar Reels de Instagram. Funciona en la sesión de Claude en la nube donde viven los agentes, no en el ordenador de la fundadora.

## Las 4 herramientas, en palabras sencillas

| Herramienta | Para qué sirve | Dónde está |
| --- | --- | --- |
| **FFmpeg** | La "tijera" y la "mesa de sonido": corta, une, cambia el tamaño a 9:16 y deja el volumen al nivel que pide Instagram. | Programa del sistema |
| **Whisper** (faster-whisper) | Escucha el vídeo y escribe lo que se dice, palabra por palabra y con su tiempo. Así salen los subtítulos. Trabaja dentro de la sesión: el vídeo no se manda a ningún servicio. | `requirements.txt` |
| **yt-dlp** | Baja un vídeo de Instagram o TikTok con su enlace, para estudiar referencias (ritmo, cortes, ganchos). | `requirements.txt` |
| **HyperFrames** | El "editor": arma el vídeo como una página web (vídeo de fondo, textos, animaciones, música) y lo exporta a MP4. Trae 4 skills para Claude Code. | `package.json` y `.claude/skills/` |

Las 4 skills de HyperFrames están guardadas en el repo (`.claude/skills/`), así que cualquier sesión de Claude que abra el repo ya las tiene:

- `hyperframes`: las reglas para escribir el vídeo y el ciclo de trabajo (planear, escribir, revisar, exportar). Subtítulos, animaciones y motion graphics.
- `hyperframes-cli`: los comandos (`check`, `snapshot`, `render`, `audio`…).
- `hyperframes-registry`: unos 450 bloques listos (transiciones, títulos, estilos de subtítulos).
- `media-use`: música, efectos de sonido, imágenes y voz. Lo gratis de HeyGen pide iniciar sesión; sin sesión se usan solo archivos propios.

## Lo que hace falta además (y para qué)

| Qué | Para qué | Ya está en la nube |
| --- | --- | --- |
| **Node.js 22+** | Hace funcionar HyperFrames. | Sí |
| **Python 3.10+** y `pip` | Hace funcionar Whisper y yt-dlp. | Sí |
| **Chrome sin ventana** | HyperFrames "fotografía" cada cuadro del vídeo con él. Lo trae solo la primera vez si no lo encuentra. | Sí |
| **GSAP** | La librería de animaciones que usa HyperFrames. Va en `package.json`. | Se instala |
| **Letra Caveat** | La frase manuscrita del manual de marca. Montserrat ya viene con HyperFrames. | Se instala |
| **Permisos de red** | `huggingface.co` y `us.aws.cdn.hf.co` (bajar el modelo de Whisper la primera vez), `www.instagram.com` y `www.tiktok.com` (yt-dlp). | Permitidos el 16 nov 2026 |

**Pendiente de red:** los vídeos de Instagram y TikTok se bajan de servidores que cambian de nombre (`scontent-xxx.cdninstagram.com`, `v19-webapp-prime.us.tiktok.com`…). yt-dlp ya **lee** los datos del vídeo, pero para **bajarlo** hay que permitir esos dominios con comodín (`*.cdninstagram.com`, `*.fbcdn.net`, `*.tiktok.com`, `*.tiktokcdn.com`, `*.tiktokcdn-us.com`) en Configuración del proyecto → Entorno en la nube → Acceso a la red. Mientras tanto, la fundadora puede subir el vídeo de referencia a la biblioteca.

Instagram a veces pide iniciar sesión para ver un Reel. **Nunca** se le da la contraseña al agente (`knowledge/reglas.md`): si un Reel lo pide, se usa otro enlace o la fundadora sube el vídeo.

## Instalar y probar

```bash
bash tools/editor-video/instalar.sh     # instala lo que falte (se puede repetir)
bash tools/editor-video/probar.sh       # prueba las 4 herramientas con un vídeo de ejemplo
```

Resultado de la prueba del 16 nov 2026 (sesión en la nube): FFmpeg 6.1.1 ✓, faster-whisper 1.2.1 con modelo `small` ✓, yt-dlp 2026.10.26 ✓ (lee TikTok e Instagram), HyperFrames 0.9.56 ✓ (Reel 1080×1920 exportado en unos 25 s).

## Scripts

| Script | Qué hace |
| --- | --- |
| `scripts/bajar-video.sh "<enlace>"` | Baja un vídeo de referencia a `projects/pulso/videos/referencias/` y lista duración, tamaño y cortes de escena. |
| `scripts/transcribir.py VIDEO --idioma es` | Escribe `VIDEO.palabras.json` (para HyperFrames) y `VIDEO.srt` (para Instagram o cualquier editor). Modelo `small` por defecto; `--modelo medium` si hay música fuerte. |
| `scripts/armar-reel.py VIDEO --palabras VIDEO.palabras.json --gancho "…"` | Arma el proyecto HyperFrames con la línea PULSO: gancho en Caveat sobre crema, línea de pulso dorada, subtítulos en Montserrat que entran palabra por palabra y música opcional (`--musica pista.mp3`). |

Después de armar: `npx hyperframes check` (revisa errores y contraste), `npx hyperframes snapshot` (fotos de prueba) y `npx hyperframes render -o reel.mp4`.

## Notas

- `instalar.sh` y `probar.sh` apagan la telemetría de HyperFrames (`HYPERFRAMES_NO_TELEMETRY=1`). La skill `media-use` pide mandar un aviso de uso al empezar; con esa variable no se envía.
- `av` va limitado a menos de 16 porque faster-whisper 1.2.1 falla con las versiones nuevas.
- Para actualizar las skills: `bash tools/editor-video/instalar.sh --skills` (quedan registradas en `skills-lock.json`).
- Los vídeos de trabajo no se suben al repo (`.gitignore`); los aprobados van a la biblioteca del Centro de mando.
