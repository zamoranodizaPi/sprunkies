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
