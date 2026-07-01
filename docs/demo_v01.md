# Demo v0.1: Simon en el campo

Esta demo muestra a Simon en un campo verde con cielo de dia, nubes en movimiento y notas musicales cuando canta.

## Resolucion

- Landscape: 480x320
- FPS objetivo: 30
- Tecnologia: Python + pygame-ce

## Assets usados

La demo busca estos archivos:

- `assets/images/field_day_480x320.png`
- `assets/sprites/simon/idle.png`
- `assets/sprites/simon/blink.png`
- `assets/sprites/simon/sing1.png`
- `assets/sprites/simon/sing2.png`
- `assets/sprites/simon/happy.png`
- `assets/sounds/simon_sing_lalala.wav`

Tambien acepta variantes como `simon_idle.png` o `idle_01.png`.

Si algun asset no existe, la demo usa un fallback dibujado por codigo para que la Raspberry pueda probar rendimiento e interaccion sin crashear.

## Interacciones

- Tocar/clickear a Simon: Simon canta, cambia animacion y salen notas musicales.
- Tocar/clickear fuera de Simon: Simon hace una reaccion happy corta.
- Tecla `ESC`: salir.
- `Ctrl+C` desde terminal: salir.

## Problemas conocidos

- Si no hay dispositivo de audio, la demo imprime un warning y continua sin sonido.
- Si `sprunkies_assets_v01.zip` no esta presente, se usan assets fallback temporales.
- Fullscreen se activa automaticamente en Raspberry Pi; usar `SPRUNKIES_WINDOWED=1` para probar en ventana.

## Proximos pasos

- Copiar y descomprimir `sprunkies_assets_v01.zip` dentro de `~/sprunkies`.
- Ajustar tamano exacto de Simon contra los sprites finales.
- Crear mas animaciones suaves para respirar, mirar y cantar.
- Mantener esta fase sin logica de Simon Says.

## Servicio systemd

La demo puede arrancar automaticamente con:

```sh
cd ~/sprunkies
sudo ./scripts/install_demo_service.sh
```

Esto instala `config/sprunkies-demo.service` en `/etc/systemd/system/`, habilita el servicio y lo arranca. El servicio corre como usuario `pi`, usa `DISPLAY=:0` y espera unos segundos despues de `lightdm` para que el escritorio este disponible.

Para detenerlo y quitarlo del arranque:

```sh
cd ~/sprunkies
sudo ./scripts/stop_demo_service.sh
```
