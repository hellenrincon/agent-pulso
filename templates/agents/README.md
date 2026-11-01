# Plantillas de agentes

Contenido compartido entre proyectos, junto con `templates/prompts/`. Cada proyecto copia estas fichas a `projects/<proyecto>/agents/` y las ajusta a su marca.

Reglas:
- Un agente solo lee y escribe dentro de `projects/<su-proyecto>/` y en el espacio de datos de su proyecto en el Centro de mando.
- Toda consulta y escritura lleva el identificador del proyecto. Sin proyecto activo no se hace nada.
- Copiar algo de un proyecto a otro solo ocurre si la fundadora lo aprueba, pieza por pieza.
- Antes de proponer algo, el agente lee el historial de decisiones de su proyecto (`historial` en el tablero y `projects/<proyecto>/decisions/`) para no repetir lo que ya se rechazó.

## Orden al crear un proyecto

1. **Marca e identidad** (`marca.md`): brief, rutas visuales, logo, paleta, tipografía, manual y prompts del proyecto.
2. **Estratega**: prioridades con la marca aprobada.
3. **Contenido** y el resto, ya con `marca.md` y los prompts listos.
