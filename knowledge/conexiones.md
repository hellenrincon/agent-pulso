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
| 2 · RUN • RIDE • SWIM | https://canva.link/fz05yoctupq3z7t | DAHY-0aG-WE |
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
- Metricool necesita las imágenes en un enlace público (o Google Drive vinculado en Metricool). Los archivos del Centro de mando y los enlaces de Canva no son públicos: antes del primer post hay que definir cómo se entregan (por confirmar).
- Si la imagen la generó la IA, se marca `isAiGenerated: true`, como pide Instagram.

## Fotos y videos reales

La fundadora los sube en las pestañas Contenido o Estratega. Quedan en la colección `medios` del tablero (ver `board/README.md`). Se usan antes que cualquier imagen generada.
