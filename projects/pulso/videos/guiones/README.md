# Cómo se armaron los Reels terminados (16 nov 2026)

Textos en pantalla de cada Reel (`*-textos.json`) y el comando exacto, para repetirlos o ajustarlos.

```bash
S=tools/editor-video/scripts
# Post 10, espresso (vídeo de la fundadora): sonido nivelado y textos por paso
ffmpeg -i espresso.mp4 -af "loudnorm=I=-16:TP=-1.5" -c:v copy -c:a aac espresso-sonido.mp4
python3 $S/armar-reel.py espresso-sonido.mp4 --textos projects/pulso/videos/guiones/espresso-textos.json \
  --gancho "Así nace un espresso" --gancho-seg 2.9 --pilar cafe --firma 880,280,130 \
  --cierre "¿Solo, con leche o con hielo?"

# Post 7 (RUN): se borra el emblema viejo y la franja vino tapa el título viejo
ffmpeg -i reel7.mp4 -vf "delogo=x=40:y=1480:w=170:h=180" -c:v libx264 -crf 16 reel7-limpio.mp4
python3 $S/armar-reel.py reel7-limpio.mp4 --pilar run --titulo "Verde + negro" --mano "Dirty Matcha" \
  --banda-top 220 --banda-alto 310 --firma 50,1485,165 --textos projects/pulso/videos/guiones/reel7-textos.json \
  --gancho "Verde o negro: ¿por qué no los dos?" --gancho-seg 3.4 --gancho-top 820 \
  --cierre "Etiqueta a quien lo tomaría contigo"

# Post 8 (RIDE): igual, franja oliva
ffmpeg -i reel8.mp4 -vf "delogo=x=870:y=1495:w=208:h=215" -c:v libx264 -crf 16 reel8-limpio.mp4
python3 $S/armar-reel.py reel8-limpio.mp4 --pilar ride --titulo "El café que te refresca" --mano "después de pedalear" \
  --banda-top 120 --banda-alto 360 --firma 893,1520,165 --textos projects/pulso/videos/guiones/reel8-textos.json \
  --gancho "Lo que pide el cuerpo después de pedalear" --gancho-seg 3.4 --gancho-top 820 \
  --cierre "¿Lo probarías en la ciclovía?"
```

Después, en cada carpeta: `npx hyperframes check`, `npx hyperframes render -o reel.mp4` y
`ffmpeg -i reel.mp4 -c:v libx264 -preset slow -crf 23 -pix_fmt yuv420p -movflags +faststart -c:a aac final.mp4`
para que pese menos de 20 MB (límite de la biblioteca).
