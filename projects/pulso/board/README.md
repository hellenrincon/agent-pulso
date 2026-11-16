# Tablero compartido PULSO

El tablero es el **único canal** entre agentes. Vive en la base de datos del **Centro de mando PULSO** (una página de Claude con base de datos compartida). El dashboard (`dashboard/index.html`) es la vista de ese tablero.

- **Los agentes** leen y escriben con la herramienta `ArtifactData` sobre la URL del Centro de mando (ver `board/conexion.md`).
- **La fundadora** aprueba, rechaza o comenta desde las tarjetas del dashboard. Sus respuestas quedan en el mismo tablero.
- **Respaldo:** `board/exportes/` guarda copias JSON fechadas del tablero (para auditar quién hizo qué).

## Colecciones

| Colección | Elemento del documento maestro | Qué guarda |
| --- | --- | --- |
| `tareas/{id}` | Tareas | Qué hay que hacer, agente responsable, estado y a quién pasa después |
| `mensajes/{id}` | Mensajes | Notas entre agentes sobre una tarea |
| `decisiones/{id}` | Decisiones pendientes | Tarjetas que esperan la aprobación de la fundadora |
| `marca/documento` | Documento de marca | Resumen de `knowledge/marca.md`. Solo lectura salvo aprobación |
| `calendario/{id}` | Datos: calendario de contenido | Publicaciones planeadas |
| `menu/{id}` y `cupos/{fecha}` | Datos: menú y costos | Bebidas, costos, precios, cupos del día |
| `numeros/{id}` | Datos: métricas | Números clave con fuente y fecha |
| `actividad/{id}` | Registro | Qué hizo cada agente y a quién se lo pasó |
| `agentes/{id}` | Estado de los agentes | Activo, inactivo o modo eventos |
| `semana/actual` | Resumen del Estratega | Las 3 prioridades de la semana |
| `solicitudes/{id}` | Pedidos de ajuste de la fundadora | Lo que pide cambiar sobre una foto/video (`medio`) o un post (`propuesta`): `texto`, `agente`, `estado` (pendiente, en_curso, listo, no_se_pudo), `respuesta` y `enlace` al resultado |
| `medios/{id}` | Biblioteca: brutos, referencias y terminados | Archivos de la sección Crear → Biblioteca. Cada documento guarda `etapa` (`bruto`, `referencia` o `terminado`; si falta, lo que subió la fundadora es bruto y lo que subió un agente es referencia), el id del archivo (`asset`), `tipo` (foto, video o enlace), `enlace` (solo referencias guardadas como link), `categoria`, `descripcion`, `propuesta` (post al que pertenece), `por` (fundadora o agente), `subido` y `usado_en`. El archivo se ve en `/_blob/{asset}`. Ver `library/README.md` |
| `marca/board` | Branding board | Imágenes aprobadas para las casillas del tablero de marca: `logo`, `submarca`, `logo_secundario`, `tipografia`, `mockup1`, `mockup2` (id de archivo de la biblioteca). Solo el agente Marca e identidad la escribe, y solo con lo que la fundadora aprobó. Si una casilla está vacía, el Centro de mando dibuja la versión actual de la marca |
| `historial/{id}` | Historial de decisiones | Una entrada por cada vez que la fundadora aprueba, comenta o rechaza (decisiones y posts): `fecha`, `proyecto`, `agente`, `tipo`, `ref`, `titulo`, `resultado` (aprobada, con_cambios, rechazada, reabierta), `nota`, `opcion`, `opcion_titulo`. **No se edita ni se borra**; reabrir crea una entrada nueva. Los agentes lo leen antes de proponer algo parecido |
| `recetas/{id}` y `proveedores/{id}` | Menú y producto | Recetas con ingredientes y pasos; proveedores con fuente y estado |

## Campos

### `tareas/{id}`
```json
{
  "titulo": "Guion del Reel 3",
  "agente": "contenido",
  "estado": "pendiente | en_curso | esperando_aprobacion | hecha",
  "pasa_a": "estratega",
  "prioridad": 1,
  "detalle": "texto corto",
  "decision": "id de decisión (opcional)",
  "enlaces": [{ "titulo": "Storyboard", "url": "https://..." }],
  "fuente": "knowledge/... o enlace",
  "creada": "2026-10-25T09:00:00-05:00",
  "actualizada": "2026-10-25T09:00:00-05:00"
}
```

### `decisiones/{id}`
```json
{
  "titulo": "¿Publicamos el Reel 3 el lunes 26 oct?",
  "agente": "contenido",
  "tarea": "id de la tarea",
  "tipo": "publicacion | precio | gasto | alianza | contacto | marca | otro",
  "propuesta": "Vista rápida, máximo 5 líneas",
  "opciones": [
    { "id": "a", "titulo": "Publicar el lunes 26", "detalle": "..." },
    { "id": "b", "titulo": "Mover al miércoles 28", "detalle": "..." }
  ],
  "recomendada": "a",
  "porque": "Razón de la recomendación",
  "visual": { "titulo": "Storyboard en Claude Design", "url": "https://claude.ai/..." },
  "fuentes": ["pulso-base-de-conocimiento.md §8"],
  "estado": "pendiente | aprobada | rechazada | comentada",
  "respuesta": { "opcion": "a", "comentario": "", "fecha": "ISO" },
  "creada": "ISO"
}
```
Solo la fundadora cambia `estado` y `respuesta` (desde el dashboard). Un agente nunca marca su propia decisión como aprobada.

### `mensajes/{id}`
`{ "tarea": "id", "de": "estratega", "para": "contenido", "texto": "...", "fecha": "ISO" }`

### `actividad/{id}`
`{ "agente": "contenido", "accion": "Creó el calendario semanal", "pasa_a": "estratega", "tarea": "id", "fecha": "ISO" }`

### `calendario/{id}`
`{ "fecha": "2026-10-26", "formato": "Reel | Story | Post | Carrusel", "titulo": "...", "pilar": "RUN | RIDE | SWIM | CAFÉ", "estado": "idea | guion | grabado | editado | aprobado | publicado", "gancho": "...", "visual": "url", "tarea": "id", "fuente": "..." }`
Desde el 16 nov el calendario se arma **después** del contenido: solo lleva posts con contenido aprobado (`propuesta` = id). `estado`: `propuesto` (fecha propuesta por Contenido) → `aprobado` (la fundadora aprobó la fecha) → `programado` (ya en Metricool). La fecha aprobada vive también en `propuestas/{id}.publicar.estado = "aprobado"`.

### `menu/{id}`
`{ "nombre": "Cold Brew", "estado": "candidata | piloto | aprobada", "costo": null, "precio": null, "foto": "url o null", "fuente": "..." }`
`null` se muestra como "por confirmar".

### `cupos/{AAAA-MM-DD}`
`{ "total": null, "vendidos": 0, "fuente": "..." }`

### `numeros/{id}`
`{ "nombre": "Seguidores", "valor": 0, "unidad": "", "fuente": "Documento maestro", "fecha": "2026-10-17" }`

### `agentes/{id}`
`{ "nombre": "Estratega", "fase": 1, "estado": "activo | inactivo | modo_eventos", "objetivo": "...", "formato": "...", "ficha": "agents/estratega.md", "solicitud": null }`
Si la fundadora pide activar un agente desde el dashboard, se guarda `solicitud: "activar"`; Max conecta sus integraciones y cambia `estado`.

## Ciclo de una tarea

```
Pendiente → En curso → Esperando aprobación → Hecha
                         │
                         └─ crea decisiones/{id} → la fundadora responde → el agente lee la respuesta
```

## Reglas del tablero

1. Todo cambio deja una fila en `actividad`.
2. Ningún agente borra filas de otro agente.
3. Fechas en ISO 8601, zona horaria de Bogotá (`-05:00`).
4. Lo no confirmado va como `null` o como el texto "por confirmar". Nunca un número inventado.
5. Nada de contraseñas, tokens ni datos de pago en el tablero.

## Manual de marca (revisión en grande)

- `marca/manual` (doc): `{titulo, fuente, canva_id, canva_url, version, estado, paginas:[{n, titulo, asset}], versiones:[{etiqueta, nota, canva_id, canva_url, paginas:[{n, asset}]}], version_elegida}`. Las versiones completas se comparan lado a lado, página por página; elegir una pide dos clics y no aprueba páginas. Las páginas se muestran a ancho completo en Marca y conocimiento.
- `marca_comentarios` (colección, solo se agrega): `{pagina (0 = general), tipo: aprobado|cambios|comentario|deshecho, texto, por, fecha, version, proyecto}`. `deshecho` = la fundadora deshizo la aprobación de esa página: vuelve a "Por revisar" y no cuenta como aprobada. En posts, deshacer pone `revision: null` y deja en historial una entrada `reabierta`; el agente no programa un post sin `revision.estado = aprobado`.
- Pedir cambio crea una solicitud `{tipo:"marca", agente:"marca", alcance:"manual"|"pagina", pagina (null si es todo el manual), desde_pagina, version, canva_id, texto, estado:"pendiente"}`. Por defecto el alcance es todo el manual. La atiende el agente Marca e identidad: ajusta el diseño en Canva, exporta la página nueva y sube `version`.
- Aprobaciones y cambios quedan también en `historial` (`tipo:"marca"`).
