# Hardware

## Equipo base

- Raspberry Pi 3
- Raspberry Pi OS Bookworm 32 bits
- Escritorio grafico de Raspberry Pi OS

## Pantalla

- TFT SPI touch de 3.5"
- Referencia: Hosyond 3.5" TFT touch SPI, compatible tipo Waveshare-like
- Resolucion del panel: 480x320 o 320x480 segun rotacion
- Orientacion objetivo inicial: horizontal 480x320

## Touch

- Controlador esperado: XPT2046 o compatible
- Confirmacion pendiente mediante `/dev/input/event*`, `xinput list` y, si esta disponible, `evtest`

## Pendiente

- Bocina/audio para una etapa posterior
- Validacion final de rotacion y calibracion touch en escritorio
