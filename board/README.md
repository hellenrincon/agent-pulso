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
| `medios/{id}` | Fotos y videos reales | Archivos que sube la fundadora desde las pestañas Contenido o Estratega. Cada documento guarda el id del archivo (`asset`), `tipo` (foto o video), `categoria`, `descripcion`, `subido` y `usado_en` (posts donde se usó). El archivo se ve en `/_blob/{asset}` |

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
