#!/usr/bin/env python3
"""Arma un proyecto HyperFrames de Reel 9:16 con la línea gráfica de PULSO.

Pone el vídeo de fondo, el gancho animado en los primeros segundos, los subtítulos
palabra por palabra (de transcribir.py), la línea de pulso dorada y, si se pide,
una música de fondo más baja que la voz.

Uso:
    python3 armar-reel.py VIDEO --palabras VIDEO.palabras.json --gancho "Tu matcha sabe amargo por esto" \
        [--musica pista.mp3 --volumen-musica 0.14] [--salida carpeta]

Después:
    cd <carpeta> && npx hyperframes check && npx hyperframes render -o reel.mp4
"""
import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
HERRAMIENTAS = AQUI.parent
MODULOS = HERRAMIENTAS / "node_modules"

# Manual de marca versión Vino (projects/pulso/knowledge/marca.md)
VINO, CREMA, DORADO = "#5A1A28", "#F3E8D6", "#B8913F"


def duracion(ruta: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def grupos(palabras, maximo=3, pausa=0.15):
    """Junta palabras en grupos cortos (2-3 palabras: ritmo de Reel)."""
    actual, todos = [], []
    for w in palabras:
        if actual and (len(actual) >= maximo or w["start"] - actual[-1]["end"] >= pausa
                       or actual[-1]["text"][-1:] in ".?!,"):
            todos.append(actual)
            actual = []
        actual.append(w)
    if actual:
        todos.append(actual)
    return todos


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("--palabras", required=True)
    p.add_argument("--gancho", default="")
    p.add_argument("--musica")
    p.add_argument("--volumen-musica", type=float, default=0.14)
    p.add_argument("--salida")
    a = p.parse_args()

    video = Path(a.video).resolve()
    salida = Path(a.salida or video.with_suffix("")).resolve()
    (salida / "assets" / "fonts").mkdir(parents=True, exist_ok=True)
    if not (MODULOS / "gsap").exists():
        print("Falta instalar: corre primero tools/editor-video/instalar.sh", file=sys.stderr)
        return 1

    shutil.copy(video, salida / "assets" / video.name)
    shutil.copy(MODULOS / "gsap/dist/gsap.min.js", salida / "assets/gsap.min.js")
    shutil.copy(MODULOS / "@fontsource/caveat/files/caveat-latin-400-normal.woff2",
                salida / "assets/fonts/caveat-400.woff2")
    total = round(duracion(video), 3)

    palabras = json.loads(Path(a.palabras).read_text(encoding="utf-8"))
    palabras = [w for w in palabras if w["text"].strip() and w["start"] < total]
    bloques = grupos(palabras)

    capas, js = [], []
    for i, g in enumerate(bloques):
        ini = max(0.1, g[0]["start"] - 0.05)
        fin = min(total, g[-1]["end"] + 0.1)
        if i + 1 < len(bloques):
            fin = min(fin, bloques[i + 1][0]["start"] - 0.02)
        spans = " ".join(f'<span class="w" id="g{i}w{j}">{html.escape(w["text"])}</span>'
                         for j, w in enumerate(g))
        capas.append(f'<div class="grupo" id="g{i}">{spans}</div>')
        js.append(f'tl.set("#g{i}", {{opacity: 1, visibility: "visible"}}, {ini:.3f});')
        for j, w in enumerate(g):
            js.append(f'tl.from("#g{i}w{j}", {{y: 30, opacity: 0, duration: 0.18, ease: "power3.out"}}, {w["start"]:.3f});')
        js.append(f'tl.to("#g{i}", {{opacity: 0, duration: 0.1, ease: "power2.in"}}, {fin - 0.1:.3f});')
        js.append(f'tl.set("#g{i}", {{opacity: 0, visibility: "hidden"}}, {fin:.3f});')

    gancho = ""
    if a.gancho:
        gancho = f'''<div id="gancho" class="clip" data-start="0" data-duration="{min(3, total)}" data-track-index="2">
        <div class="gancho-texto">{html.escape(a.gancho)}</div><div class="pulso"></div></div>'''
        js.insert(0, 'tl.from("#gancho .gancho-texto", {y: 40, opacity: 0, duration: 0.5, ease: "power3.out"}, 0.15);'
                     'tl.from("#gancho .pulso", {scaleX: 0, transformOrigin: "left center", duration: 0.6, ease: "power2.inOut"}, 0.35);')

    musica = ""
    if a.musica:
        m = Path(a.musica).resolve()
        shutil.copy(m, salida / "assets" / m.name)
        musica = (f'<audio id="musica" class="clip" src="assets/{m.name}" data-start="0" '
                  f'data-duration="{total}" data-track-index="5" data-volume="{a.volumen_musica}"></audio>')

    doc = f'''<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
@font-face {{ font-family: "Caveat"; src: url("assets/fonts/caveat-400.woff2") format("woff2"); font-weight: 400; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
body {{ font-family: "Montserrat", sans-serif; }}
#gancho {{ position: absolute; left: 0; right: 0; top: 300px; text-align: center; padding: 0 90px; }}
.gancho-texto {{ display: inline-block; background: {CREMA}; color: {VINO}; font-family: "Caveat", cursive;
  font-size: 92px; line-height: 1.05; padding: 22px 40px; }}
.pulso {{ height: 4px; background: {DORADO}; margin: 26px auto 0; width: 520px; }}
#subtitulos {{ position: absolute; left: 0; right: 0; bottom: 640px; height: 200px; }}
.grupo {{ position: absolute; left: 0; right: 0; bottom: 0; text-align: center; padding: 0 90px;
  opacity: 0; visibility: hidden; overflow: visible; }}
.w {{ display: inline-block; color: {CREMA}; font-weight: 700; font-size: 78px; text-transform: uppercase;
  letter-spacing: 0.04em; text-shadow: 0 4px 18px rgba(0,0,0,.55); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
  <video id="a-roll" class="clip" src="assets/{video.name}" playsinline data-start="0" data-duration="{total}"
    data-track-index="0" data-has-audio="true" style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
  {gancho}
  <div id="subtitulos" class="clip" data-start="0" data-duration="{total}" data-track-index="3" data-track-kind="captions">
    {chr(10).join(capas)}
  </div>
  {musica}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''
    (salida / "index.html").write_text(doc, encoding="utf-8")
    (salida / "hyperframes.json").write_text(json.dumps({
        "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
        "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
        "media": {"autoProxy": True}}, indent=2) + "\n", encoding="utf-8")
    print(f"Proyecto listo en {salida} ({total} s, {len(bloques)} grupos de subtítulos)")
    print(f"Siguiente: cd {salida} && npx hyperframes check && npx hyperframes render -o reel.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
