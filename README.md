# MCUIK – Modern Common UI Kit

Kit de interfaz para misiones y mods de Arma Reforger:
- iconos propios;
- tema de colores;
- piezas listas para componer HUDs y ventanas;
- avisos animados.

No depende de ninguna misión. Ponlo de dependencia (`B8DFCB8639E9DA37`) y úsalo desde tu script.

## Qué trae

| Pieza | Para qué |
|---|---|
| `MCUIK_Notify.Toast(icon, title, body, color)` | Tarjeta lateral que entra deslizando, se apila (hasta 4) y se desvanece. |
| `MCUIK_Notify.Dialogue(icon, speaker, line, color, seconds, tag)` | Quién habla y qué dice, abajo en el centro, en cola. `OnDialogueShown()` te avisa con el `tag` para poner la voz. |
| `MCUIK.Panel(parent, icon, title, width, color)` | Panel con cabecera (icono, título y dato a la derecha) y una columna `Content`. |
| `MCUIK.Chip(parent, icon, value, label)` | Icono, número grande y etiqueta pequeña. |
| `MCUIK.Row(parent, icon, label, value)` | Fila con etiqueta a la izquierda y valor a la derecha. |
| `MCUIK.Bar(parent, frac, width, color)` | Barra de progreso. |
| `MCUIK.Text / Title / Divider / Spacer / HBox / VBox` | Para componer. `Pad()` pone márgenes y `Fill()` reparte el espacio. |
| `MCUIK.CreateLayer()` + `MCUIK.Place(w, ancla…, alineación…, x, y)` | Capa a pantalla completa y colocación por anclas. |
| Ventanas `mcuik_list` y `mcuik_event` (`MCUIK_Res.C_DIALOGS`) | Lista con filas pulsables (`MCUIK_Res.L_LISTROW`) y ventana de evento con insignia. |
| `MCUIK_Theme` | Colores: `Accent`, `Info`, `Danger`, `Warning`, `Success`, `Text`, `Muted` y `Panel`. `Paint()` sirve para texto enriquecido. |

### Iconos

Son 60 iconos en blanco dentro de `UI/Textures/MCUIK/MCUIK_Icons.imageset`, para teñirlos por código. Los nombres están en `MCUIK_Icon`:
- dinero, material, apoyo, reclutas, objetivo, radio, diario, tienda, garaje, vehículo, arma, munición, médico, ropa…;
- estados de incógnito;
- tipos de zona;
- facciones;
- controles.

Hay una hoja de muestra en `tools/icons_preview.png`.

## Ejemplo

```c
Widget layer = MCUIK.CreateLayer();
Widget panel = MCUIK.Panel(layer, "money", "TESORERÍA", 300);
MCUIK.Place(panel, 1, 0, 1, 0, -18, 18);
Widget c = MCUIK.Content(panel);
MCUIK.Chip(c, "money", "12.500 €", "FONDOS");
MCUIK.Row(c, "support", "Apoyo", "45 %", MCUIK_Theme.Success());
MCUIK.Bar(c, 0.45, 276, MCUIK_Theme.Success());

MCUIK_Notify.Toast("zone", "Zona liberada", "Agüimes vuelve a ser vuestra.", MCUIK_Theme.Success());
```

## Cuidado con Enforce Script

Un color nuevo guardado solo en un **parámetro** de función se libera al momento. Guárdalo en una variable local:

```c
Color c = color;
if (!c)
    c = MCUIK_Theme.Accent();
```

## Herramientas (`tools/`)

`python tools/build.py` rehace todo:
- el atlas de iconos (`gen_icons.py`, dibujados en SVG);
- su textura `.edds` (`png2edds.py`, sin Workbench);
- los layouts (`gen_layouts.py`);
- los `.meta`;
- las constantes de `MCUIK_Res.c`.

Después hay que abrir el proyecto en Workbench una vez para que registre los recursos nuevos.
