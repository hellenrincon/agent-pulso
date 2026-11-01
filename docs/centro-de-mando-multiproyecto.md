# Centro de mando multiproyecto: qué se montó y respuestas a los puntos por confirmar

Fecha: 1 nov 2026. Fuente: `para-max-centro-de-mando.md` (enviado por Alexander Duque). El prototipo visual enlazado no se pudo abrir desde esta cuenta, así que el montaje sigue el documento.

## Qué quedó montado

| Punto del documento | Estado |
| --- | --- |
| Menú lateral fijo con las 10 secciones | Hecho |
| Selector de proyecto arriba del menú, lleva a Mis proyectos | Hecho |
| Barra inferior en celular: Inicio, Decisiones, Crear, Pedidos, Más | Hecho ("Más" abre el menú completo) |
| Inicio ("Hoy en PULSO"): 4 accesos, decisiones pendientes, cupos del día, agentes activos | Hecho |
| Decisiones con pestañas Pendientes / Historial | Hecho |
| Historial agrupado por día, con filtros por agente, resultado y fecha, y botón Reabrir | Hecho. Las 5 respuestas que ya existían (2 decisiones y 3 posts) se cargaron con su fecha real |
| Cada aprobación, comentario o rechazo queda guardado | Hecho: colección `historial`, la página nunca edita ni borra entradas |
| Reabrir crea entrada nueva y no borra la anterior | Hecho. Un post ya programado en Metricool no se reabre desde aquí: se cambia en Metricool |
| Crear: flujo de 5 pasos y herramientas creativas | Hecho. Muestra qué está conectado (Canva, Metricool) y qué está por confirmar |
| Marca y conocimiento: carpeta del proyecto e independencia | Hecho |
| Mis proyectos con tarjeta por proyecto y "Nuevo proyecto" | Hecho. Nuevo proyecto se pide en el chat (ver punto 5) |
| Repo por proyecto: `templates/agents/` + `projects/pulso/` | Hecho |
| Calendario, Ventas y pedidos, Menú y producto, Eventos, Agentes | Movidas al menú con el contenido que ya tenían; su diseño nuevo queda para la etapa 6 |

## Respuestas a "Por confirmar contigo"

1. **Claude Design desde los agentes.** En este entorno no hay conector de Claude Design para los agentes. Los posts se están haciendo en Canva, que sí está conectado (plan gratis): el agente copia el diseño, lo edita y lo exporta. Si se quiere Claude Design, hay que confirmar que exista un conector o API para él.
2. **Tablero y dashboard.** El Centro de mando es una página de Claude con base de datos compartida. El historial se guarda en la colección `historial` (una entrada por decisión, con fecha, agente, resultado, nota y opción elegida) y se respalda en `projects/pulso/decisions/`.
3. **Veo, Ideogram, Freepik y Lovable.** Ninguno está conectado hoy. Los cuatro necesitan una clave de API, y la clave tiene que vivir en un servidor, no en el navegador ni en los agentes. Hoy no hay ese servidor. Freepik tiene MCP oficial solo para imágenes e íconos; Lovable pide plan Business para su API (según el documento). Disponibilidad y precios: por confirmar antes de contratar.
4. **Redes de Metricool.** Hoy está en plan gratis con Instagram (`@pulso.coffee.co`, marca 7638555). Qué redes incluye el plan que se contrate: por confirmar con la página de planes de Metricool al momento de contratar.
5. **Aislar datos entre proyectos.** Ambos: carpeta propia en `projects/<id>/` y espacio de datos propio en el Centro de mando. PULSO usa las colecciones raíz (fue el primero); cada proyecto nuevo usa `proyectos/<id>/<colección>`. La página hace toda lectura y escritura a través del proyecto activo. Crear un proyecto nuevo requiere: nombre, `marca.md` y la aprobación de la fundadora; se copia `templates/agents/` y se registra en la lista de proyectos.

## Pendiente

- Tope de gasto mensual por proyecto: por confirmar (hoy no hay gastos).
- Etapas 4 a 6 del orden sugerido: conectar las herramientas creativas cuando haya claves y servidor, y diseñar Calendario, Ventas y pedidos, Menú y producto, Eventos y Agentes.
