# Sprunkies interactions v0.3

Este paquete agrega 5 acciones por comando SSH, teclado y touch:

1. `soccer` / comando `1`: Simon juega futbol.
2. `dance` / comando `2`: Simon baila en el patio.
3. `joke` / comando `3`: Simon cuenta un chiste y se rie.
4. `wave` / comando `4`: Simon saluda.
5. `sleep` / comando `5`: Simon se duerme y despierta.

Las imagenes son sprite sheets de 8 frames en arreglo 4x2. La demo las recorta automaticamente con `src/sprite_sheet.py`.

Las hojas no son PNG transparentes finales. Para esta version se aplica colorkey blanco simple; si algun borde blanco queda visible, se documenta como pendiente para sprites finales.

Comandos recomendados:

```sh
echo soccer > /tmp/sprunkies_command.txt
echo dance > /tmp/sprunkies_command.txt
echo joke > /tmp/sprunkies_command.txt
echo wave > /tmp/sprunkies_command.txt
echo sleep > /tmp/sprunkies_command.txt
```
