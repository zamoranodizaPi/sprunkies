# sprunkies

`sprunkies` es un proyecto de mascota virtual musical para nino en Raspberry Pi 3 con pantalla touch TFT SPI de 3.5".

El personaje inicial se llama **Simon**.

## Objetivo v0.1

Preparar el ambiente base del proyecto:

- confirmar Raspberry Pi OS Bookworm 32 bits
- dejar visible el escritorio grafico en la pantalla touch de 3.5"
- validar que el touch funcione sobre el escritorio
- crear la estructura inicial de archivos, documentacion y scripts de diagnostico

En esta fase todavia no se implementa el juego.

Este proyecto no tiene relacion con SCADA, Modbus, Nexus, sensores, gases ni proyectos industriales anteriores.

## Estructura

```text
sprunkies/
  README.md
  docs/
    hardware.md
    display_touch_setup.md
    game_idea.md
  assets/
    images/
    sounds/
    sprites/
  src/
  tools/
  scripts/
  config/
    backups/
```

## Uso inicial en Raspberry Pi

Desde la Raspberry Pi:

```sh
cd ~/sprunkies
sh scripts/check_system.sh
sh scripts/check_touch.sh
sh scripts/backup_config.sh
```

Para mostrar a Simon en la pantalla TFT ya expuesta como framebuffer:

```sh
cd ~/sprunkies
sh scripts/show_simon.sh /dev/fb1
```

Para generar la imagen de Simon y dejarla como fondo del escritorio LXDE:

```sh
cd ~/sprunkies
sh scripts/set_simon_wallpaper.sh /dev/fb1
```

Antes de modificar `/boot/firmware/config.txt`, revisar `docs/display_touch_setup.md` y hacer backup.

## Demo visual v0.2 - Simon Touch Pet

Instalar dependencias en la Raspberry:

```sh
cd ~/sprunkies
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Ejecutar la demo:

```sh
cd ~/sprunkies
./scripts/run_demo.sh
```

Debe verse un campo verde con cielo de dia, nubes lentas y Simon animado en landscape 480x320. Al tocar/clickear a Simon, canta y aparecen notas musicales. Para salir, presionar `ESC` o usar `Ctrl+C` desde la terminal.

La v0.2 convierte la demo en una mascota touch sencilla:

- Tocar a Simon en general: canta y salen notas musicales.
- Tocar cabeza: Simon se pone happy y aparecen corazones/estrellas.
- Tocar cuerpo: Simon baila con rebote mas marcado y estrellas.
- Tocar cielo o nubes: Simon reacciona feliz, una nube se resalta y salen notas/estrellas.
- Tocar pasto: salen flores pequenas desde el pasto.
- Sin tocar por 45 segundos: Simon entra en sleepy y muestra `zzz`.
- Tocar a Simon en sleepy: despierta con una reaccion happy.

Audios para canto principal, en orden:

1. `assets/sounds/simon_theme.wav`
2. `assets/sounds/simon_signature_theme.wav`
3. `assets/sounds/Square1_then_Square2_louder.wav`
4. `assets/sounds/touch_demo.wav`
5. `assets/sounds/simon_sing_lalala.wav`

Audios cortos opcionales para efectos: `button_red_tom.wav`, `button_blue_bell.wav`, `button_yellow_la.wav`, `button_green_pop.wav`, `success_jingle.wav`, `oops_soft.wav` y `simon_signature_motif.wav`. Si falta algun audio, la demo continua sin crashear.

Controles de desarrollo: `S` fuerza canto, `H` happy, `D` dance y `Z` sleepy.

Archivos principales:

- `src/main.py`
- `src/config.py`
- `src/asset_loader.py`
- `src/scene_simon_field.py`
- `src/simon_pet.py`
- `src/effects.py`
- `scripts/run_demo.sh`
- `docs/demo_v02_touch_pet.md`

## Arranque automatico

Para instalar la demo como servicio systemd en la Raspberry:

```sh
cd ~/sprunkies
sudo ./scripts/install_demo_service.sh
```

Servicio instalado:

```text
sprunkies-demo.service
```

Comandos utiles:

```sh
systemctl status sprunkies-demo.service
sudo systemctl restart sprunkies-demo.service
sudo ./scripts/stop_demo_service.sh
```
