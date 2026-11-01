# Conexiones de PULSO

Cuentas y herramientas conectadas. La fundadora es dueña de todas; los agentes entran por autorización (conector), nunca con contraseña.

Fuente: configuración hecha por la fundadora el 25 de octubre de 2026, verificada por el agente con las herramientas de cada conector.

| Herramienta | Para qué | Estado | Datos de conexión |
| --- | --- | --- | --- |
| Centro de mando | Tablero compartido de agentes + dashboard de la fundadora | Activo | https://claude.ai/artifact/FxKr6SJtAyL8FHPLYy43jq · código en `dashboard/index.html` |
| Canva | Diseño de posts (plan gratis) | Conectado | Carpeta de posts: https://www.canva.com/folder/FAHY-7Plibw |
| Metricool | Programar y publicar en Instagram lo que la fundadora aprueba | Conectado | Marca (blogId) `7638555` · Instagram `pulso.coffee.co` · zona horaria `America/Bogota` |
| Instagram | Red principal | Conectado vía Metricool | `@pulso.coffee.co` (cuenta profesional) |
| Claude Design | Storyboards y mockups | Activo | Ver `board/conexion.md` |

## Canva: diseños hechos

| Post | Diseño | Id |
| --- | --- | --- |
| 1 · Hola, somos PULSO | https://canva.link/x254ajw4awat0bg | DAHY-z6winI |
| 2 · RUN • RIDE • SWIM | https://www.canva.com/d/oBTfNv2YJQKYwes (v2, fotos reales Unsplash; v1: https://canva.link/fz05yoctupq3z7t) | DAHZKyn9PY0 |
| 3 · Detrás de PULSO | https://canva.link/qv4psihcr5jsc3n | DAHY-1Rdlcs |
| 4 · Tu matcha sabe amargo | https://canva.link/2dcq8zfijt9zzy8 | DAHY-8FwRt0 |
| 5 · Cold brew en casa | https://canva.link/0f3obzp9902tl16 | DAHY-6qjApk |

- Posts 6 a 9: pendientes. El plan gratis de Canva se quedó sin créditos de IA el 25 de octubre de 2026.
- Post 3: la persona de la foto la generó la IA de Canva. Hay que reemplazarla por una foto real de la fundadora antes de publicar.
- Las miniaturas de los 5 diseños se publican junto al dashboard en `dashboard/canva/postN.png` y cada propuesta las enlaza con el campo `img`.

## Flujo de publicación (Metricool)

1. Contenido propone el post en `propuestas` (imagen, caption, fecha).
2. La fundadora lo aprueba en el Centro de mando (`propuestas/{id}.revision.estado = "aprobado"`).
3. Solo entonces Contenido lo programa en Metricool con `createScheduledPost` (blogId `7638555`, red `instagram`, zona `America/Bogota`), en la fecha del calendario.
4. Contenido guarda en la propuesta `metricool: { id, uuid, fecha, plannerUrl }` y deja una fila en `actividad`.
5. La fundadora puede ver, cambiar o borrar el post en el planificador de Metricool antes de que salga.

Reglas:
- Nunca se programa un post sin revisión `aprobado`. Un post con cambios pedidos vuelve a revisión.
- Instagram exige imagen o video en cada post; un Reel exige video.
- Imágenes: se exporta el diseño con `export-design` de Canva (jpg) y se pasa esa URL en `media`. Metricool copia el archivo a su servidor al programar. Probado el 25 de octubre de 2026 con el post 1 como borrador (draft) para el 27 de octubre, 6 pm.
- Fotos y videos de la biblioteca del Centro de mando todavía no se pueden pasar a Metricool ni a Canva: falta habilitar `www.canva.com` en la red del entorno.
- Programación automática: activa. Tarea cada hora de 7 am a 10 pm (Bogotá). Lo que la fundadora aprueba en el Centro de mando pasa solo a Metricool, sin que escriba nada. El flujo de "Enviar a revisión" de Metricool no está disponible en el plan gratis (error 403, 27 oct 2026), así que se aprueba en el tablero.
- Si la imagen la generó la IA, se marca `isAiGenerated: true`, como pide Instagram.

## Pedidos de ajuste al agente

La fundadora pide ajustes desde el Centro de mando ("Pedir ajuste al agente" en cada foto o video, o "Pedir cambio" en un post). Quedan en `solicitudes`. Contenido los hace en Canva, muestra el resultado y la fundadora lo aprueba.

Límite actual (25 de octubre de 2026): la red del entorno de los agentes bloquea `www.canva.com` y `export-download.canva.com`. Por eso el agente puede cambiar textos, colores y orden en los diseños de Canva, pero todavía no puede subir a Canva las fotos y videos de la fundadora. Se arregla agregando esos dominios en la configuración del entorno (Project settings → Cloud environment → Network access).

## Fotos y videos reales

La fundadora los sube en las pestañas Contenido o Estratega. Quedan en la colección `medios` del tablero (ver `board/README.md`). Se usan antes que cualquier imagen generada.


## Material por post (desde 26 oct 2026)
En "Revisión de posts", cada post tiene "Tu material para este post": la fundadora sube ahí la foto o el video según "Cómo hacer la foto o el video".
- Cada archivo se guarda en `medios` con `propuesta` = id del post.
- Se crea una solicitud `tipo: "material"` con `medios` (ids) para Contenido.
- La revisión programada (cada hora) la atiende: monta el material en una copia del diseño de Canva. Mientras canva.com siga bloqueado en esta sesión, Contenido prepara la versión ajustada con ffmpeg y la muestra en el tablero (`resultado`), y el paso a Canva lo hace la fundadora arrastrando el archivo.
- Nada se programa sin que la fundadora apruebe el post.

## Calendario de publicación (27 oct 2026)
Cada propuesta lleva `publicar {fecha, motivo, fuente, estado}`, una fecha y hora propuestas que la fundadora ve antes de aprobar. La colección `calendario` enlaza cada fila con su `propuesta` y tiene `hora`.
Horas: según Metricool (mejor hora Instagram, Bogotá, consultado 27 oct 2026), los picos son 10 am y 6 pm entre semana, y 10 am los fines de semana.

| Fecha | Hora | Post |
|---|---|---|
| Lun 2 nov | 6:00 / 6:15 / 6:30 pm | 1 Hola, 2 Pilares, 3 Detrás de PULSO (lanzamiento, fijados) |
| Mar 3 nov | 6:00 pm | 4 Matcha (Reel), más la Story "abrimos la cuenta" |
| Jue 5 nov | 6:00 pm | 10 Espresso (Reel) |
| Sáb 7 nov | 10:00 am | 5 Cold brew (Reel) |
| Dom 8 nov | 10:00 am | 6 Ciclovía |
| Mar 10 nov | 6:00 pm | 7 Dirty matcha (Reel) |
| Dom 15 nov | 10:00 am | 8 Espresso tonic (Reel) |
| Por confirmar | | 9 Lista de espera (cuando exista el formulario) |

Al aprobar, la revisión programada usa esa fecha. Si ya pasó, toma la siguiente franja libre y actualiza el calendario.

## Fotos libres en Canva (27 oct 2026)
`upload-asset-from-url` de Canva funciona con URLs públicas como images.unsplash.com, porque Canva las baja desde sus propios servidores. Así se pueden poner fotos reales de banco libre, con crédito, aunque esta sesión no llegue a esos dominios. Post 2 v2: Venti Views (correr), Anvesh Vatsavai (bici), Omar Abozeid (natación), con licencia Unsplash.

## Botón "ahora" (27 oct 2026)
El Centro de mando tiene permiso `mcp` sobre el conector Claude Code Remote (solo `fire_trigger`). Lo usan "Aprobar", "Pedir cambio ahora" y subir material en un post: disparan la revisión programada al instante. "Pedir cambio en la próxima revisión" espera a la vuelta de cada hora (7 am a 10 pm). La primera vez, el navegador pide permiso para usar el conector.

## Fotos de la fundadora a Canva (27 oct 2026)

Mientras la red bloquee `www.canva.com` y `export-download.canva.com`, el flujo es: la fundadora sube la foto final a su Canva (carpeta "PULSO · Posts de arranque" o Subidos), el agente la busca con `list-folder-items` (ordenado por fecha), copia el diseño, cambia la foto con `update_fill` + `crop_media`, exporta y programa. Así se hizo el post 2 (Canva DAHZLG-wFJQ, foto MAHZLO1mDM4, Metricool 407423102, 2 nov 6:15 pm). Arreglo definitivo: agregar esos dos dominios en Project settings → Cloud environment → Network access → Allowed domains.

## Canva · cuenta nueva (1 nov 2026)

- Carpeta: "PULSO · Contenido Instagram" (FAHZs3Q24F8).
- Diseño "PULSO · Contenido Instagram" (DAHZs0HU44c, https://canva.link/bmgu4im889w52v3): portada + posts 1 a 5 (páginas 2 a 6). Son las imágenes finales subidas como foto, no las capas editables: para editar texto o foto, se rehace la página o se comparte el diseño original desde la cuenta anterior.
- Manual de marca: DAHZspdIvP4.
- Pendiente: el video del post 10 (la subida desde el agente no acepta MP4; súbelo a mano en Canva). Posts 6 a 9 aún no tienen diseño.
- Cada propuesta guarda `canva` (nuevo), `canva_pagina` y `canva_anterior`.
