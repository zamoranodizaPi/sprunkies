# Demo v0.2: Simon Touch Pet

Esta version convierte la demo visual en una mascota virtual musical por touch. Simon sigue en el campo verde con cielo de dia y nubes lentas, pero ahora reacciona segun la zona tocada.

## Resolucion

- Landscape: 480x320
- FPS objetivo: 30
- Tecnologia: Python + pygame-ce
- Entrada: touch como mouse, con soporte adicional para `FINGERDOWN`

## Estados de Simon

- `idle`: animacion normal con rebote suave y parpadeo ocasional.
- `sing`: alterna `sing1` y `sing2`, reproduce el audio principal y genera notas.
- `happy`: usa `happy` si existe y muestra corazones o estrellas.
- `dance`: rebote mas marcado con alternancia simple entre `idle` y `happy`.
- `sleepy`: entra tras 45 segundos sin tocar, baja el movimiento y muestra `zzz`.
- `wake`: transicion corta al tocar a Simon mientras esta sleepy.

## Mapa de zonas tactiles

- Cielo: `y` de 0 a 150.
- Pasto: `y` de 235 a 320.
- Simon: rectangulo actual del sprite.
- Cabeza: parte superior del rectangulo de Simon.
- Cuerpo: parte inferior del rectangulo de Simon.

## Interacciones

- Simon general: canta, reproduce audio principal y salen notas musicales.
- Cabeza: reaccion happy con corazones/estrellas y sonido alegre.
- Cuerpo: baile/rebote con estrellas y sonido tipo boton/pop.
- Cielo o nubes: Simon reacciona feliz, la nube se resalta y salen notas/estrellas.
- Pasto: aparecen flores y Simon hace reaccion happy.
- Sleepy: tocar a Simon lo despierta.

## Audios usados

Audio principal, en orden de prioridad:

1. `assets/sounds/simon_theme.wav`
2. `assets/sounds/simon_signature_theme.wav`
3. `assets/sounds/Square1_then_Square2_louder.wav`
4. `assets/sounds/touch_demo.wav`
5. `assets/sounds/simon_sing_lalala.wav`

Efectos opcionales:

- `button_red_tom.wav`
- `button_blue_bell.wav`
- `button_yellow_la.wav`
- `button_green_pop.wav`
- `success_jingle.wav`
- `oops_soft.wav`
- `simon_signature_motif.wav`

Si falta un archivo de audio o no hay dispositivo disponible, la demo imprime un warning y continua sin sonido.

## Assets usados

- `assets/images/field_day_480x320.png`
- `assets/images/cloud_01.png`
- `assets/images/cloud_02.png`
- `assets/images/music_note_*.png`
- `assets/sprites/simon/idle*.png`
- `assets/sprites/simon/blink*.png`
- `assets/sprites/simon/sing1*.png`
- `assets/sprites/simon/sing2*.png`
- `assets/sprites/simon/happy*.png`

Si faltan imagenes, se usan fallbacks dibujados por codigo.

## Controles

- `ESC`: salir.
- `Ctrl+C`: salir desde terminal.
- `S`: forzar canto.
- `H`: forzar happy.
- `D`: forzar dance.
- `Z`: forzar sleepy.

## Problemas conocidos

- En Raspberry, el servicio actual usa `aplay` y `plughw:1,0`; si no se escucha, revisar salida de audio del sistema.
- La deteccion tactil es por rectangulos simples, no por mascara del sprite.
- El estado sleepy usa el sprite `blink` si no existe un sprite sleepy dedicado.

## Proximos pasos

- Afinar sprites dedicados para sleepy y wake.
- Ajustar sonidos cortos por zona segun pruebas con la pantalla real.
- Mantener esta etapa sin Simon Says, sin sensores, sin red y sin base de datos.
