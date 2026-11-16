# Biblioteca de PULSO

Todo el material para crear, revisar y publicar está en **tres carpetas**. Tienen los mismos nombres en el Centro de mando (Crear → Biblioteca y herramientas) y en este repo.

| Carpeta | Qué va | Quién lo sube | Quién lo usa |
| --- | --- | --- | --- |
| **Brutos** | Fotos y tomas tal como salen del celular, sin editar | La fundadora | Contenido y Editor de vídeo: lo cortan, lo ajustan y lo montan en los posts |
| **Referencias** | Ideas para inspirarse: Reels o TikToks (archivo o enlace), capturas, el manual de marca, vasos y empaques reales | La fundadora y los agentes | Todos los agentes, para copiar ritmo y estilo. **Nunca se publica** |
| **Terminados** | Piezas listas: posts exportados de Canva y Reels editados, cada una con su post | Los agentes, o la fundadora si la hizo por fuera | La fundadora las revisa en su post; lo aprobado se programa en Metricool |

## Dónde vive cada cosa

- **Centro de mando (lo principal):** colección `medios`, con el campo `etapa` = `bruto`, `referencia` o `terminado`. Los archivos están en la biblioteca del artifact (`/_blob/{asset}`). Una referencia puede ser solo un enlace (`enlace`, `tipo: "enlace"`).
- **Este repo:** copias que conviene conservar con el código.
  - `brutos/`: vacío a propósito. Los brutos pesan mucho y viven en el Centro de mando.
  - `referencias/`: `manual-marca/` (versiones vino y petróleo) y `vasos-fundadora.png`.
  - `terminados/`: `posts-v2/`, con las versiones de los posts exportadas de Canva.
- **Vídeo (Editor de vídeo):** su área de trabajo es `videos/`. Los nombres equivalen así: `crudos/` son los brutos, `referencias/` son las referencias, `trabajo/` son cortes intermedios y `salida/` son los terminados. Lo aprobado vuelve al Centro de mando como `terminado`.

## Flujo

1. La fundadora sube a **Brutos** lo que graba, o lo sube directo en el post ("Tu material para este post"), y queda como bruto de ese post.
2. Contenido (y Editor de vídeo para los Reels) toma el bruto, sigue las **Referencias** y la línea de marca, y prepara la pieza en una copia de Canva.
3. La pieza queda en **Terminados**, con `propuesta` = id del post, y como versión nueva del post para que la fundadora compare y elija con dos clics.
4. La fundadora aprueba el post. Solo entonces la revisión programada lo envía a Metricool.
5. Si la fundadora sube algo a Terminados y elige el post, el tablero crea un pedido (`solicitudes`, `tipo: "material"`, `terminado: true`). Contenido lo agrega como versión del post **sin cambiarlo**.

Nada se publica sin la aprobación de la fundadora.

## Solo lo terminado se aprueba (16 nov 2026)
Crear → Por revisar muestra únicamente los posts con una pieza en Terminados. Al aprobar se guarda esa pieza en `propuestas.pieza` y es la que se publica. Si la fundadora borra una pieza de Terminados, el post vuelve a "En preparación".
