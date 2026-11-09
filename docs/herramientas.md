---
title: Herramientas
nav_order: 7
---

# Herramientas (`tools/`)

Todo el contenido del kit se **genera** con Python 3. Se necesitan `pillow` y `resvg-py` (`pip install pillow resvg-py`).

```
python tools/build.py
```

Lo que hace `build.py`, en orden:

| Paso | Script | Resultado |
|---|---|---|
| 1 | `gen_icons.py` | Dibuja los iconos (SVG → PNG) en `UI/Textures/MCUIK/MCUIK_Icons.png`. Genera el `.imageset`, `MCUIK_IconNames.c` y la hoja `tools/icons_preview.png`. |
| 2 | `png2edds.py` | Convierte el PNG en `.edds` (RGBA8 con mipmaps), la textura que entiende el motor. **No necesita Workbench.** |
| 3 | `gen_layouts.py` | Escribe todos los `.layout` desde una descripción en Python (`W`, `img`, `text`, `sized`, `overlay`, `hbox`, `vbox`, `button`…). |
| 4 | `metas.py` | Crea el `.meta` de cada recurso con un GUID estable sacado de su ruta. |
| 5 | — | Escribe `Configs/MCUIK/MCUIK_Dialogs.conf` y `Scripts/Game/MCUIK/MCUIK_Res.c` (constantes con cada recurso). |
| — | `gen_api_docs.py` | Regenera `docs/api.md` desde el código. |

Después de añadir archivos nuevos, **abre el proyecto en Workbench una vez** para que los registre en `resourceDatabase.rdb`. Hasta entonces los prefabs y layouts nuevos no se replican bien.

## Formato `.edds` (por si lo necesitas en otro mod)

Es una cabecera DDS con extensión DX10, seguida de:
- la marca `ENF1` en `reserved1[1]`;
- una tabla de bloques `COPY`+tamaño (o `LZ4 `), uno por mip, del más pequeño al más grande;
- los datos en ese mismo orden.

`png2edds.py` escribe `R8G8B8A8_UNORM` sin comprimir. Así se reproducen bien los iconos con transparencia.

Uso: `python tools/png2edds.py entrada.png salida.edds` (lados múltiplos de 4).

## Generador de layouts en otro mod

MCES usa el generador de MCUIK:

```python
sys.path.insert(0, "<ruta>/MCUIK/tools")
import gen_layouts as L
L.save("MiPanel", L.sized("Root", 300, None, None, [L.overlay("Ov", [L.img("Bg", L.PANEL), ...])]), None, mi_carpeta)
```

Mira `MCES/tools/build.py` como ejemplo completo: ventana, tarjetas y pestañas.
