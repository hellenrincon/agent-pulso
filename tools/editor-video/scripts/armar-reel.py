#!/usr/bin/env python3
"""Arma un proyecto HyperFrames de Reel 9:16 con la línea gráfica de PULSO.

Pone el vídeo de fondo, el gancho animado en los primeros segundos, los subtítulos
palabra por palabra (de transcribir.py), la línea de pulso dorada y, si se pide,
una música de fondo más baja que la voz.

Uso:
    python3 armar-reel.py VIDEO --palabras VIDEO.palabras.json --gancho "Tu matcha sabe amargo por esto" \
        [--textos textos.json] [--cierre "Etiqueta a quien lo tomaría contigo"] \
        [--musica pista.mp3 --volumen-musica 0.14] [--salida carpeta]

--palabras  subtítulos de lo que se dice (de transcribir.py). Opcional si el vídeo no tiene voz.
--textos    textos en pantalla con su tiempo, para vídeos sin voz:
            [{"text": "1 · Moler", "start": 2.0, "end": 5.6}]
--cierre    añade al final una tarjeta crema con la firma PULSO, el lema y esta frase (llamado a la acción).
--titulo, --mano, --pilar   franja de título arriba en el color del pilar (run vino, ride oliva, swim petróleo,
            cafe café): título en mayúscula espaciada y la frase en Caveat. Tapa textos viejos del vídeo.
--firma X,Y,ANCHO           pone la firma sutil crema (sin círculo) sobre el vídeo en esa posición.

Regla de la línea gráfica: una sola frase en Caveat por pieza. Si hay --mano, el gancho va en Montserrat.

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

# Manual de marca versión Vino (projects/pulso/knowledge/marca.md y knowledge/linea-grafica.md)
VINO, CREMA, DORADO = "#5A1A28", "#F3E8D6", "#B8913F"
PILARES = {"run": "#5A1A28", "ride": "#4A4B25", "swim": "#17293A", "cafe": "#5B3522"}
MARCA = Path(__file__).resolve().parents[3] / "projects/pulso/library/manual-marca/vino"


def duracion(ruta: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ruta)],
        capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


def tiene_audio(ruta: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                          "-of", "csv=p=0", str(ruta)], capture_output=True, text=True, check=True)
    return bool(out.stdout.strip())


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
    p.add_argument("--palabras")
    p.add_argument("--textos")
    p.add_argument("--gancho", default="")
    p.add_argument("--gancho-seg", type=float, default=3.0, help="segundos que dura el gancho")
    p.add_argument("--gancho-top", type=int, default=300, help="distancia del gancho al borde de arriba, en px. Instagram tapa lo que quede fuera de 270 a 1248 px")
    p.add_argument("--cierre", default="")
    p.add_argument("--cierre-seg", type=float, default=3.0)
    p.add_argument("--lema", default="Good Coffee, Better Movement")
    p.add_argument("--titulo", default="")
    p.add_argument("--mano", default="")
    p.add_argument("--pilar", choices=sorted(PILARES), default="run")
    p.add_argument("--banda-top", type=int, default=230)
    p.add_argument("--banda-alto", type=int, default=300)
    p.add_argument("--firma", default="", help="X,Y,ANCHO en px de la firma sutil crema sobre el vídeo")
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
    largo_video = round(duracion(video), 3)
    total = round(largo_video + (a.cierre_seg if a.cierre else 0), 3)

    palabras = json.loads(Path(a.palabras).read_text(encoding="utf-8")) if a.palabras else []
    palabras = [w for w in palabras if w["text"].strip() and w["start"] < largo_video]
    bloques = grupos(palabras)

    capas, js = [], []
    for i, g in enumerate(bloques):
        ini = max(0.1, g[0]["start"] - 0.05)
        fin = min(largo_video, g[-1]["end"] + 0.1)
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

    textos = json.loads(Path(a.textos).read_text(encoding="utf-8")) if a.textos else []
    for k, t in enumerate(textos):
        ini, fin = max(0.1, float(t["start"])), min(largo_video, float(t["end"]))
        capas.append(f'<div class="grupo rotulo" id="t{k}"><span class="w">{html.escape(t["text"])}</span><div class="pulso corto"></div></div>')
        js.append(f'tl.set("#t{k}", {{opacity: 1, visibility: "visible"}}, {ini:.3f});')
        js.append(f'tl.from("#t{k} .w", {{y: 30, opacity: 0, duration: 0.3, ease: "power3.out"}}, {ini:.3f});')
        js.append(f'tl.from("#t{k} .pulso", {{scaleX: 0, duration: 0.4, ease: "power2.inOut"}}, {ini + 0.1:.3f});')
        js.append(f'tl.to("#t{k}", {{opacity: 0, duration: 0.15, ease: "power2.in"}}, {fin - 0.15:.3f});')
        js.append(f'tl.set("#t{k}", {{opacity: 0, visibility: "hidden"}}, {fin:.3f});')

    cierre = ""
    if a.cierre:
        firma = MARCA / "firma_sutil_vino.png"
        logo = ""
        if firma.exists():
            shutil.copy(firma, salida / "assets/firma_sutil_vino.png")
            logo = '<img class="firma" src="assets/firma_sutil_vino.png" alt="PULSO">'
        cierre = f'''<div id="cierre" class="clip" data-start="{largo_video}" data-duration="{a.cierre_seg}" data-track-index="4">
        {logo}<div class="lema">{html.escape(a.lema)}</div><div class="pulso"></div><div class="cta">{html.escape(a.cierre)}</div></div>'''
        js.append(f'tl.from("#cierre", {{opacity: 0, duration: 0.35, ease: "power2.out"}}, {largo_video:.3f});')
        js.append(f'tl.from("#cierre .firma", {{scale: 0.92, opacity: 0, duration: 0.5, ease: "power3.out"}}, {largo_video + 0.15:.3f});')
        js.append(f'tl.from("#cierre .pulso", {{scaleX: 0, duration: 0.5, ease: "power2.inOut"}}, {largo_video + 0.4:.3f});')
        js.append(f'tl.from("#cierre .cta", {{y: 24, opacity: 0, duration: 0.4, ease: "power3.out"}}, {largo_video + 0.6:.3f});')

    banda = ""
    if a.titulo or a.mano:
        banda = f'''<div id="banda" class="clip" data-start="0" data-duration="{largo_video}" data-track-index="1">
        <div class="titulo">{html.escape(a.titulo)}</div>{f'<div class="mano">{html.escape(a.mano)}</div>' if a.mano else ''}<div class="pulso"></div></div>'''
        js.insert(0, 'tl.from("#banda .titulo", {y: 20, opacity: 0, duration: 0.45, ease: "power3.out"}, 0.1);'
                     'tl.from("#banda .mano", {y: 16, opacity: 0, duration: 0.45, ease: "power3.out"}, 0.3);'
                     'tl.from("#banda .pulso", {scaleX: 0, duration: 0.6, ease: "power2.inOut"}, 0.45);')

    marca_video = ""
    if a.firma:
        fx, fy, fw = (int(v) for v in a.firma.split(","))
        shutil.copy(MARCA / "firma_sutil_crema.png", salida / "assets/firma_sutil_crema.png")
        marca_video = (f'<img id="firma-video" class="clip" src="assets/firma_sutil_crema.png" alt="PULSO" data-start="0" '
                       f'data-duration="{largo_video}" data-track-index="6" '
                       f'style="position:absolute; left:{fx}px; top:{fy}px; width:{fw}px; opacity:.92">')

    gancho = ""
    if a.gancho:
        gancho = f'''<div id="gancho" class="clip" data-start="0" data-duration="{min(a.gancho_seg, largo_video)}" data-track-index="2">
        <div class="gancho-texto{' recto' if a.mano else ''}">{html.escape(a.gancho)}</div><div class="pulso"></div></div>'''
        js.insert(0, 'tl.from("#gancho .gancho-texto", {y: 40, opacity: 0, duration: 0.5, ease: "power3.out"}, 0.15);'
                     'tl.from("#gancho .pulso", {scaleX: 0, transformOrigin: "left center", duration: 0.6, ease: "power2.inOut"}, 0.35);')

    musica = ""
    if a.musica:
        m = Path(a.musica).resolve()
        shutil.copy(m, salida / "assets" / m.name)
        musica = (f'<audio id="musica" class="clip" src="assets/{m.name}" data-start="0" '
                  f'data-duration="{largo_video}" data-track-index="5" data-volume="{a.volumen_musica}"></audio>')

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
#gancho {{ position: absolute; left: 0; right: 0; top: {a.gancho_top}px; text-align: center; padding: 0 90px; }}
.gancho-texto {{ display: inline-block; background: {CREMA}; color: {VINO}; font-family: "Caveat", cursive;
  font-size: 92px; line-height: 1.05; padding: 22px 40px; }}
.pulso {{ height: 4px; background: {DORADO}; margin: 26px auto 0; width: 520px; }}
.pulso.corto {{ width: 220px; margin-top: 18px; }}
.gancho-texto.recto {{ font-family: "Montserrat", sans-serif; font-weight: 400; font-size: 54px; text-transform: uppercase;
  letter-spacing: 0.08em; line-height: 1.25; }}
#banda {{ position: absolute; left: 0; right: 0; top: {a.banda_top}px; min-height: {a.banda_alto}px; background: {PILARES[a.pilar]};
  display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 30px 90px; }}
#banda .titulo {{ color: {CREMA}; font-weight: 300; font-size: 66px; letter-spacing: 0.2em; text-transform: uppercase; }}
#banda .mano {{ color: {CREMA}; font-family: "Caveat", cursive; font-size: 74px; line-height: 1; margin-top: 8px; }}
#banda .pulso {{ width: 360px; margin-top: 18px; height: 3px; }}
#cierre {{ position: absolute; inset: 0; background: {CREMA}; display: flex; flex-direction: column;
  align-items: center; justify-content: flex-start; text-align: center; padding: 330px 110px 0; }}
#cierre .firma {{ width: 380px; height: auto; }}
#cierre .lema {{ color: {VINO}; font-weight: 300; font-size: 36px; letter-spacing: 0.16em; white-space: nowrap; text-transform: uppercase; margin-top: 30px; }}
#cierre .cta {{ color: {VINO}; font-weight: 400; font-size: 50px; line-height: 1.3; margin-top: 34px; }}
#subtitulos {{ position: absolute; left: 0; right: 0; bottom: 720px; height: 200px; }}
.grupo {{ position: absolute; left: 0; right: 0; bottom: 0; text-align: center; padding: 0 90px;
  opacity: 0; visibility: hidden; overflow: visible; }}
.w {{ display: inline-block; color: {CREMA}; font-weight: 700; font-size: 78px; text-transform: uppercase;
  letter-spacing: 0.04em; text-shadow: 0 4px 18px rgba(0,0,0,.55);
  background: rgba(40,12,20,.42); padding: 4px 16px; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1080" data-height="1920">
  <video id="a-roll" class="clip" src="assets/{video.name}" playsinline data-start="0" data-duration="{largo_video}"
    data-track-index="0"{' data-has-audio="true"' if tiene_audio(video) else ' muted'} style="position:absolute; inset:0; width:100%; height:100%; object-fit:cover"></video>
  {banda}
  {marca_video}
  {gancho}
  <div id="subtitulos" class="clip" data-start="0" data-duration="{largo_video}" data-track-index="3" data-track-kind="captions">
    {chr(10).join(capas)}
  </div>
  {cierre}
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
    print(f"Proyecto listo en {salida} ({total} s, {len(bloques)} grupos de subtítulos, {len(textos)} textos)")
    print(f"Siguiente: cd {salida} && npx hyperframes check && npx hyperframes render -o reel.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
