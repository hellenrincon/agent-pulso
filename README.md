# PULSO Coffee & More: sistema de agentes

Nueve agentes de IA que trabajan para la fundadora y se comunican **solo** por un tablero compartido. La fundadora decide todo en el **Centro de mando**: https://claude.ai/artifact/FxKr6SJtAyL8FHPLYy43jq

Fuente de verdad: *PULSO - Documento maestro de agentes* (20 oct 2026).

El repo está organizado por proyecto. Cada proyecto tiene su carpeta independiente y lo único compartido son las plantillas de agentes.

```
templates/agents/          # plantillas de agentes (único contenido compartido)
templates/prompts/         # plantillas de prompts con espacios {{…}} para cada marca
projects/
  pulso/                   # knowledge/, agents/, skills/, board/, decisions/, library/, videos/, web/
dashboard/                 # código del Centro de mando (multiproyecto)
tools/editor-video/        # FFmpeg, Whisper, yt-dlp y HyperFrames para el Editor de vídeos
.claude/skills/            # skills de HyperFrames para Claude Code
docs/                      # notas de montaje
```

## Agentes

| # | Agente | Estado | Ficha |
| --- | --- | --- | --- |
| 1 | Estratega | Activo | `projects/pulso/agents/estratega.md` |
| 2 | Contenido | Activo | `projects/pulso/agents/contenido.md` |
| 3 | Producto y operaciones | Activo | por escribir |
| 4 | Comunidad y ventas | Activo | por escribir |
| 5 | Datos | Inactivo (fase 2) | por escribir |
| 6 | Alianzas y eventos | Modo eventos | por escribir |
| 7 | Anuncios y SEO | Inactivo (fase 3) | por escribir |
| 8 | Marca e identidad | Activo | `projects/pulso/agents/marca.md` (plantilla en `templates/agents/marca.md`) |
| 9 | Editor de vídeos | Activo | `projects/pulso/agents/editor-video.md` (plantilla en `templates/agents/editor-video.md`) |

## Reglas que no se negocian

Nada se publica, se envía a clientes ni se paga sin la aprobación de la fundadora. Los agentes nunca reciben contraseñas. Todo sigue la línea gráfica de PULSO. Lo no confirmado se marca "por confirmar" y cada dato lleva su fuente. Detalle en `projects/pulso/knowledge/reglas.md`.
