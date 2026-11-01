# Plantillas de agentes

Único contenido compartido entre proyectos. Cada proyecto copia estas fichas a `projects/<proyecto>/agents/` y las ajusta a su marca.

Reglas:
- Un agente solo lee y escribe dentro de `projects/<su-proyecto>/` y en el espacio de datos de su proyecto en el Centro de mando.
- Toda consulta y escritura lleva el identificador del proyecto. Sin proyecto activo no se hace nada.
- Copiar algo de un proyecto a otro solo ocurre si la fundadora lo aprueba, pieza por pieza.
- Antes de proponer algo, el agente lee el historial de decisiones de su proyecto (`historial` en el tablero y `projects/<proyecto>/decisions/`) para no repetir lo que ya se rechazó.
