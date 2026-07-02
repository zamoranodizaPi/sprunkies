# Demo v0.3: SSH Actions

Esta version agrega cinco acciones animadas de Simon sobre la demo v0.2. La mascota sigue cantando al tocarla cuando esta idle, y ahora tambien puede ejecutar acciones por teclado, touch o comandos enviados desde SSH.

## Acciones

- `soccer`: Simon juega futbol durante 4 segundos.
- `dance`: Simon baila durante 5 segundos.
- `joke`: Simon cuenta un chiste durante 6.5 segundos.
- `wave`: Simon saluda durante 3 segundos.
- `sleep`: Simon se duerme y despierta durante 6 segundos.

## Teclas

- `1`: futbol.
- `2`: baile.
- `3`: chiste.
- `4`: saludo.
- `5`: dormir/despertar.
- `ESC`: salir.

Los controles de desarrollo de v0.2 siguen disponibles: `S`, `H`, `D` y `Z`.

## Touch

La parte inferior de la pantalla tiene una barra con 5 zonas grandes:

- `1 Futbol`
- `2 Baila`
- `3 Chiste`
- `4 Hola`
- `5 Dormir`

Fuera de la barra, tocar a Simon en idle conserva el canto normal.

## Comandos SSH

La demo revisa aproximadamente cada 0.2 segundos:

```text
/tmp/sprunkies_command.txt
```

Ejemplos:

```sh
echo soccer > /tmp/sprunkies_command.txt
echo dance > /tmp/sprunkies_command.txt
echo joke > /tmp/sprunkies_command.txt
echo wave > /tmp/sprunkies_command.txt
echo sleep > /tmp/sprunkies_command.txt
```

Tambien acepta:

```sh
echo 1 > /tmp/sprunkies_command.txt
echo 2 > /tmp/sprunkies_command.txt
echo 3 > /tmp/sprunkies_command.txt
echo 4 > /tmp/sprunkies_command.txt
echo 5 > /tmp/sprunkies_command.txt
```

## Assets agregados

- `assets/sprites/simon_actions/simon_soccer_sheet.png`
- `assets/sprites/simon_actions/simon_dance_sheet.png`
- `assets/sprites/simon_actions/simon_joke_sheet.png`
- `assets/sprites/simon_actions/simon_wave_sheet.png`
- `assets/sprites/simon_actions/simon_sleep_wake_sheet.png`
- `assets/sounds/actions/action_1_soccer.wav`
- `assets/sounds/actions/action_2_dance_loop.wav`
- `assets/sounds/actions/action_3_joke_laugh.wav`
- `assets/sounds/actions/action_4_wave_hello.wav`
- `assets/sounds/actions/action_5_sleep_wake.wav`
- `asset_manifest_interactions_v03.json`

## Limitaciones

- Los sprite sheets usan fondo blanco; se aplica colorkey blanco simple.
- La barra inferior reduce un poco el espacio vertical para Simon.
- El comando por archivo es intencionalmente simple y local; no agrega servidor ni red extra.

## Proximos pasos

- Crear sprites finales con transparencia real.
- Afinar duraciones contra audio final.
- Mantener Simon Says, microfono y logica de juego para una fase posterior.
