# Plantilla de prompts de marca para Ideogram

Copia este archivo a `projects/<proyecto>/knowledge/prompts-ideogram.md` y reemplaza cada `{{…}}` con la marca del proyecto. El agente Marca e identidad lo llena; la fundadora aprueba antes de usarlo.

## Espacios a llenar

| Espacio | Qué va | Ejemplo (PULSO) |
| --- | --- | --- |
| `{{MARCA}}` | Nombre exacto como se escribe en el logo | PULSO Coffee & More |
| `{{RUBRO}}` | Qué es, en pocas palabras | marca de café y comunidad deportiva de Bogotá |
| `{{ESTILO}}` | 3 o 4 adjetivos | moderno, natural, elegante y energético |
| `{{TRANSMITE}}` | Lo que debe sentir quien la ve | bienestar, vitalidad y confianza |
| `{{ELEMENTOS}}` | Ideas para el símbolo (dejar que la IA proponga) | café, rutas marcadas o una figura abstracta de energía |
| `{{COLORES}}` | Colores en palabras (y hex si ya están aprobados) | vinotinto, café, marfil, verde esmeralda, blanco y gris claro |
| `{{SENSACION_COLOR}}` | Qué deben reflejar los colores | salud, frescura y pureza |
| `{{TIPOGRAFIA}}` | Cómo debe verse la letra | fuerte, moderna y ligeramente redondeada |
| `{{APLICACIONES}}` | Dónde se usará | camiseta, taza, termo, papelería y app móvil |

## Cómo usarlos

- Ideogram entiende español; si un resultado sale raro, prueba el mismo texto en inglés.
- **Magic Prompt encendido** para explorar ideas; **apagado** cuando ya sabes exactamente lo que quieres.
- Genera 4 opciones, quédate con 1 o 2 y súbelas a Crear → Biblioteca.

## 1. Logo (exploración abierta)

```
Diseño de logo profesional para la marca "{{MARCA}}", {{RUBRO}}. Estilo {{ESTILO}}, que transmita {{TRANSMITE}}.

El logo debe incluir elementos orgánicos y dinámicos, como {{ELEMENTOS}}. Propón tú la mejor forma de combinarlos.

Usa colores como {{COLORES}}, que reflejen {{SENSACION_COLOR}}.

La tipografía debe verse {{TIPOGRAFIA}}.

Fondo blanco, composición centrada, estilo vectorial limpio y de alta calidad.
```

## 2. Manual de marca / branding board

```
Manual de marca completo para "{{MARCA}}", con estilo {{ESTILO}}. Presentación tipo branding board, profesional y con fondo limpio.

Muestra el logo principal y sus versiones, e incluye mockups de {{APLICACIONES}}.

Incluye secciones completas de colores (con sus códigos), tipografía y aplicaciones de marca. Usa colores como {{COLORES}} y una tipografía {{TIPOGRAFIA}}.
```

## 3. Paleta

```
Tablero de paleta de colores para la marca "{{MARCA}}": muestras de color planas una al lado de otra, cada una con su nombre y código debajo. Colores: {{COLORES}}. Debe reflejar {{SENSACION_COLOR}}. Fondo limpio, mucho espacio en blanco, estilo profesional.
```

## 4. Aplicaciones sueltas

```
Mockup profesional de {{APLICACION}} con el logo de "{{MARCA}}", estilo {{ESTILO}}, colores {{COLORES}}, fondo limpio y luz natural.
```

## Reglas

- Lo que sale de Ideogram es exploración. El logo elegido se redibuja en vector antes de imprimir.
- Las imágenes con IA no se publican como producto real.
- Nada se publica, se paga ni se registra sin aprobación de la fundadora.
