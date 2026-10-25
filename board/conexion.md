# Conexión al tablero

| Qué | Valor |
| --- | --- |
| Centro de mando (tablero + dashboard) | https://claude.ai/artifact/FxKr6SJtAyL8FHPLYy43jq |
| Código del dashboard | `dashboard/index.html` |
| Herramienta de los agentes | `ArtifactData` (leer: `get`, `list`, `query`; escribir: `set`, `update`, `batch`) con `url` = la del Centro de mando |
| Dueña | La fundadora (el Centro de mando es privado; solo ella y quien ella invite lo abren) |

## Rutina mínima de un agente

1. `list` de `tareas` filtrando por `agente` = su id, y de `decisiones` propias ya respondidas.
2. Hacer el trabajo según su ficha en `agents/`.
3. Escribir en un solo `batch`: la tarea actualizada, la tarjeta en `decisiones` si pide aprobación, y una fila en `actividad`.
4. Toda escritura sobre un documento existente va con `if_version` (la versión leída), para no pisar cambios de la fundadora.

Ids de agente: `estratega`, `contenido`, `producto`, `comunidad`, `alianzas`, `datos`, `anuncios`. La fundadora aparece como `fundadora`.

## Piezas de Claude Design enlazadas

| Pieza | Tarea | Enlace |
| --- | --- | --- |
| Storyboard Reel 3 + mockup del post | `t-reel3` | https://claude.ai/artifact/JCtczJMzhyxjPUAHHwxh88 |
