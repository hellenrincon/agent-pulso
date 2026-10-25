# Skill: prioridades de la semana

**Quién la usa:** Estratega, cada lunes.

1. Lee `actividad` de la semana anterior, `decisiones` respondidas, `calendario`, `menu` y los pendientes de la fundadora del documento maestro.
2. Lista candidatos y puntúa cada uno: ¿desbloquea vender por la web? (3), ¿gana seguidores? (2), ¿prepara el carrito? (1). Resta 1 si pide más de 3 h de la fundadora en la semana o si cuesta dinero.
3. Quédate con **3**. Ni más ni menos.
4. Para cada una: título de 6 palabras máximo, por qué en una línea, agente responsable, tiempo de la fundadora.
5. Escribe `semana/actual`:
```json
{ "semana": "2026-10-26", "frase": "frase manuscrita corta",
  "prioridades": [{ "orden": 1, "titulo": "...", "porque": "...", "agente": "contenido", "tiempo_fundadora": "2 h", "tarea": "id" }],
  "actualizada": "ISO" }
```
6. Crea las tareas y deja una fila en `actividad`.
