# Skill: tarjeta de decisión

**Quién la usa:** todos los agentes. Es la única forma de pedir aprobación a la fundadora.

## Cuándo crear una
Siempre que algo se vaya a publicar, enviar a clientes, pagar, contactar a alguien externo, cambiar un precio o tocar la marca.

## Cómo
1. Escribe en `decisiones/{id}` con los campos de `board/README.md`.
2. `propuesta`: vista rápida, máximo 5 líneas. Qué se decide y por qué ahora.
3. `opciones`: 2 o 3, cada una con título corto y una línea de consecuencia.
4. `recomendada` + `porque`: una razón concreta (marca, presupuesto, tiempo de la fundadora).
5. `visual`: enlace a la pieza en Claude Design (storyboard, mockup, tarjeta) cuando exista. Si se puede mostrar, no se describe.
6. `fuentes`: de dónde sale cada dato. Lo no confirmado, "por confirmar".
7. Pasa la tarea a `esperando_aprobacion` y deja una fila en `actividad`.
8. **Nunca** cambies `estado` ni `respuesta`: eso lo hace la fundadora desde el dashboard.

## Después
Lee la respuesta: `aprobada` → ejecuta solo lo aprobado; `rechazada` → cierra o replantea; `comentada` → ajusta según el comentario y crea una tarjeta nueva.
