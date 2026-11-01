# Historial de decisiones de PULSO

Cada vez que la fundadora aprueba, rechaza o comenta en el Centro de mando, se guarda una entrada en la colección `historial` del tablero (proyecto `pulso`). Aquí se exportan como respaldo, una por archivo JSON.

Campos: `fecha`, `proyecto`, `agente`, `tipo` (decision o post), `ref` (id de la pieza), `titulo`, `resultado` (aprobada, con_cambios, rechazada o reabierta), `nota`, `opcion`, `opcion_titulo`, `por`.

Reglas:
- El historial no se edita ni se borra.
- Reabrir una decisión crea una entrada nueva; la anterior se queda.
- Los agentes lo leen antes de proponer algo parecido, para no repetir lo que ya se rechazó.
