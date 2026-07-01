# Display y touch setup

Este documento registra el procedimiento inicial para preparar la pantalla TFT SPI touch de 3.5" en Raspberry Pi OS Bookworm 32 bits.

## Estado de inspeccion desde este equipo

- Workspace local creado en `C:\Users\zamor\Documents\sprunkies`.
- No se pudo inspeccionar la Raspberry Pi por SSH:
  - `ssh pi@192.168.1.50 "uname -a"` respondio `Connection refused`.
  - `ssh raspberrypi.local "uname -a"` no resolvio el host.
- Por lo anterior, no se modifico `/boot/firmware/config.txt` todavia.

## Estado aplicado en Raspberry Pi 192.168.1.120

Fecha de trabajo: 2026-07-01.

Detectado:

- OS: Raspbian GNU/Linux 12 Bookworm.
- Arquitectura: `armhf` / kernel `armv7l`.
- Modelo: Raspberry Pi 3 Model B Plus Rev 1.4.
- SPI estaba habilitado antes del driver.
- Despues de instalar el driver de pantalla aparecieron:
  - `/dev/fb0`
  - `/dev/fb1`
  - `/dev/input/event0`
  - touch `ADS7846 Touchscreen`
- `xinput list` detecta `ADS7846 Touchscreen` bajo Xorg.

Cambios aplicados:

- Se clono el proyecto en `/home/pi/sprunkies`.
- Se creo backup de `/boot/firmware/config.txt` en:
  - `/home/pi/sprunkies/config/backups/config.txt.20260701-150659.bak`
- Se instalo el driver usado previamente en el proyecto de gases:
  - repo: `https://github.com/goodtft/LCD-show.git`
  - ruta: `/opt/LCD-show`
  - comando: `sudo ./LCD35-show 0`
- El instalador agrego/configuro en `/boot/firmware/config.txt`:

```ini
[all]
hdmi_force_hotplug=1
dtparam=i2c_arm=on
dtparam=spi=on
enable_uart=1
dtoverlay=tft35a:rotate=90
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt 480 320 60 6 0 0 0
hdmi_drive=2
```

- El instalador dejo `fbcp` corriendo para copiar el framebuffer principal a la TFT.
- Se restauro `graphical.target`, porque el instalador dejo el sistema en `multi-user.target`.
- Se creo `/etc/X11/xorg.conf.d/10-fbdev.conf` para que Xorg use framebuffer:

```conf
Section "Device"
    Identifier "FramebufferDevice"
    Driver "fbdev"
    Option "fbdev" "/dev/fb0"
EndSection

Section "Screen"
    Identifier "FramebufferScreen"
    Device "FramebufferDevice"
EndSection
```

- Se ajusto LightDM porque la unidad esperaba dispositivos `/dev/dri/*`, pero el driver LCD deshabilito KMS:
  - backup: `/etc/systemd/system/lightdm.service.sprunkies-20260701-1523.bak`
  - unidad local: `/etc/systemd/system/lightdm.service`
- Se ajusto `/etc/lightdm/lightdm.conf` para usar sesion `LXDE` en lugar de `LXDE-pi-x`:
  - backup: `/etc/lightdm/lightdm.conf.sprunkies-20260701-1521.bak`
- Se genero `assets/images/simon-start.png`.
- Se aplico Simon como fondo de escritorio con `pcmanfm`.

## Comandos de diagnostico a ejecutar en la Raspberry Pi

```sh
cd ~/sprunkies
sh scripts/check_system.sh
sh scripts/check_touch.sh
```

Los scripts revisan:

- version de OS
- arquitectura
- modelo de Raspberry Pi
- estado de SPI
- framebuffers `/dev/fb*`
- dispositivos input `/dev/input/event*`
- pantallas detectadas
- servicio grafico
- `xinput list` si esta disponible
- `evtest` si esta disponible

## Backup antes de cambiar config.txt

Ejecutar:

```sh
cd ~/sprunkies
sh scripts/backup_config.sh
```

Esto crea un respaldo en:

```text
config/backups/config.txt.YYYYMMDD-HHMMSS.bak
```

## Archivo correcto en Bookworm

El archivo correcto es:

```text
/boot/firmware/config.txt
```

No usar `/boot/config.txt` para este proyecto.

## Cambios propuestos para pantalla SPI

No aplicar estas lineas a ciegas. Primero confirmar con `scripts/check_system.sh` y hacer backup.

Bloque candidato para agregar al final de `/boot/firmware/config.txt`:

```ini
# sprunkies 3.5in SPI TFT touch display
dtparam=spi=on
# Candidate overlay for Waveshare/Hosyond-like 3.5in SPI TFT.
# Confirm exact overlay name with: ls /boot/firmware/overlays/*35*
# Example candidates often include waveshare35a or piscreen.
# dtoverlay=waveshare35a:rotate=90,speed=32000000,fps=20
```

Notas:

- HDMI no debe desactivarse permanentemente sin confirmacion.
- Si el overlay exacto no existe en la imagen actual, listar overlays disponibles:

```sh
ls /boot/firmware/overlays | grep -Ei 'waveshare|35|xpt|ads|ili|fb'
```

- La orientacion preferida es horizontal 480x320.
- Si la imagen aparece rotada, ajustar el parametro `rotate` del overlay probado.

## Touch y calibracion

Calibracion previa de referencia del proyecto anterior:

```text
screen_w=320
screen_h=480
rotation=90
swap_xy=True
invert_x=False
invert_y=True
```

Para `sprunkies` se prefiere horizontal 480x320 si es estable.

Proceso recomendado:

1. Confirmar dispositivo touch:

   ```sh
   ls -l /dev/input/event*
   xinput list
   ```

2. Si `evtest` esta instalado:

   ```sh
   sudo evtest
   ```

3. Tocar las cuatro esquinas y observar si los ejes coinciden con la pantalla.

4. Si el touch queda invertido o cruzado, documentar:

   - orientacion de pantalla activa
   - nombre exacto del dispositivo en `xinput list`
   - eventos crudos de `evtest`
   - si X/Y estan intercambiados
   - si X o Y estan invertidos

No usar offsets magicos sin registrar el motivo.

## Archivos modificados

Hasta ahora, desde este workspace:

- No se modifico `/boot/firmware/config.txt`.
- Solo se crearon archivos del proyecto `sprunkies`.

## Resultado de pruebas

Pendiente ejecutar en la Raspberry Pi:

- `scripts/check_system.sh`
- `scripts/check_touch.sh`
- `scripts/show_simon.sh /dev/fb1`
- prueba visual del escritorio en TFT
- prueba tactil sobre el escritorio

## Pantalla inicial de Simon

Cuando `/dev/fb1` existe, Simon puede mostrarse directamente en el framebuffer:

```sh
cd ~/sprunkies
sh scripts/show_simon.sh /dev/fb1
```

Esto no arranca todavia el juego. Solo dibuja el personaje inicial en pantalla negra para validar salida visual del proyecto.

Para dejarlo tambien como fondo del escritorio LXDE:

```sh
cd ~/sprunkies
sh scripts/set_simon_wallpaper.sh /dev/fb1
```

## Revertir cambios si algo sale mal

Si despues de editar `/boot/firmware/config.txt` la pantalla o arranque fallan:

1. Acceder por HDMI o montar la tarjeta SD en otra computadora.
2. Restaurar el backup:

   ```sh
   sudo cp ~/sprunkies/config/backups/config.txt.YYYYMMDD-HHMMSS.bak /boot/firmware/config.txt
   sudo reboot
   ```

3. Si se agrego un bloque `sprunkies`, tambien se puede comentar temporalmente con `#`.
