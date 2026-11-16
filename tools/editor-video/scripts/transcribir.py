#!/usr/bin/env python3
"""Saca los subtítulos de un vídeo o audio con Whisper (faster-whisper), sin internet
una vez bajado el modelo.

Uso:
    python3 transcribir.py VIDEO [--modelo small] [--idioma es] [--salida carpeta]

Escribe en la carpeta de salida (por defecto, junto al vídeo):
    <nombre>.palabras.json  lista de palabras con su tiempo, en el formato que usa
                            HyperFrames: [{"id": "w0", "text": "Hola", "start": 0.1, "end": 0.4}]
    <nombre>.srt            subtítulos por frases, para Instagram, CapCut o cualquier editor
"""
import argparse
import json
import os
import sys
from pathlib import Path


def tiempo_srt(segundos: float) -> str:
    ms = int(round(segundos * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    p = argparse.ArgumentParser(description="Subtítulos con Whisper local")
    p.add_argument("video")
    p.add_argument("--modelo", default=os.environ.get("WHISPER_MODELO", "small"),
                   help="tiny, base, small (por defecto), medium o large-v3")
    p.add_argument("--idioma", default="es", help="código de idioma; 'auto' para detectarlo")
    p.add_argument("--salida", default=None, help="carpeta de salida")
    a = p.parse_args()

    from faster_whisper import WhisperModel

    video = Path(a.video)
    if not video.exists():
        print(f"No encuentro el archivo: {video}", file=sys.stderr)
        return 1
    salida = Path(a.salida) if a.salida else video.parent
    salida.mkdir(parents=True, exist_ok=True)

    modelo = WhisperModel(a.modelo, device="cpu", compute_type="int8")
    idioma = None if a.idioma == "auto" else a.idioma
    segmentos, info = modelo.transcribe(
        str(video), language=idioma, word_timestamps=True, vad_filter=True
    )

    palabras, frases = [], []
    for seg in segmentos:
        frases.append((seg.start, seg.end, seg.text.strip()))
        for w in seg.words or []:
            texto = w.word.strip()
            if texto:
                palabras.append({"id": f"w{len(palabras)}", "text": texto,
                                 "start": round(w.start, 3), "end": round(w.end, 3)})

    base = salida / video.stem
    Path(f"{base}.palabras.json").write_text(
        json.dumps(palabras, ensure_ascii=False, indent=1), encoding="utf-8")
    with open(f"{base}.srt", "w", encoding="utf-8") as f:
        for i, (ini, fin, texto) in enumerate(frases, 1):
            f.write(f"{i}\n{tiempo_srt(ini)} --> {tiempo_srt(fin)}\n{texto}\n\n")

    print(f"Idioma: {info.language} · {len(palabras)} palabras · {len(frases)} frases")
    print(f"Listo: {base}.palabras.json y {base}.srt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
