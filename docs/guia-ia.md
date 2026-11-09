---
title: Guía para IA
nav_order: 8
---

# Guía para un asistente de IA

Esta página está pensada para que un asistente (Claude, GPT, Copilot…) configure y use MCUIK en una misión de Arma Reforger sin romper nada. Una persona también puede usarla como lista de comprobación.

## Contexto que debes saber

- El lenguaje es **Enforce Script** (parecido a C#/C++, motor Enfusion). No es C#: no hay `var`, ni lambdas, ni LINQ, ni `using`.
- El código va en `Scripts/Game/**.c`. Las clases son globales; no hay espacios de nombres.
- La interfaz **solo existe en clientes**. En servidores dedicados `System.IsConsoleApp()` es `true`: no crees widgets ahí.
- Las piezas del kit se identifican **por nombre de widget** dentro de cada layout (`Icon`, `Value`, `Label`, `Content`, `Name`, `Price`…). Las tienes en [Piezas](piezas.md) y [Ventanas](ventanas.md).
- Para encontrar recursos usa `MCUIK_Res` (layouts, imageset y presets) y `MCUIK_Icon` (nombres de iconos). **No inventes GUIDs**: cópialos de ahí.

## Receta: añadir el kit a una misión

1. Añade `"B8DFCB8639E9DA37"` a `Dependencies` en el `addon.gproj` de la misión.
2. Crea una clase de HUD **solo de cliente**:
   - en el `OnPostInit` del modo de juego, si `!System.IsConsoleApp()`, llama a `MCUIK_Notify.Reset()` y crea tu HUD;
   - actualízalo desde un `EOnFrame` o desde un `CallLater` repetido cada 0,5 s.
3. Crea las piezas **una vez** y actualízalas con `MCUIK.Set*`. Para listas que cambian, `MCUIK.Clear(contenedor)` y vuelve a crearlas, pero solo cuando cambie su contenido: compara una firma en texto.
4. Coloca con `MCUIK.Place`. Para varias cajas en una columna usa un `MCUIK.VBox` colocado una vez y mete los paneles dentro.
5. Los avisos van con `MCUIK_Notify.Toast` y lo que dice un personaje con `MCUIK_Notify.Dialogue`. La voz se engancha a `OnDialogueShown()`.
6. Los mensajes que vienen del servidor llegan por un RPC al dueño (`RplRcver.Owner`), y en el cliente llamas a `MCUIK_Notify`.

## Reglas que evitan errores reales

| Regla | Por qué |
|---|---|
| Un `Color` por defecto se asigna a una **variable local**, nunca reasignando el parámetro (`Color c = color; if (!c) c = MCUIK_Theme.Accent();`). | Si guardas un objeto nuevo solo en un parámetro, se libera al momento. El error es «NULL pointer to instance. Variable 'c'». |
| No uses `out`, `debug`, `auto`, `class`, `ref`, `null`… como nombres de variable. | Son palabras reservadas: «Expected name, not a keyword». |
| En `string.Format`, el porcentaje se escribe `%` suelto (`"%1 %"`), no `%%`. | Se imprimiría `%%`. |
| `ToUpper()` modifica la cadena **en sitio**, no devuelve otra, y no convierte tildes. Usa `MCUIK.Upper(s)`. | Si no, sale «CAPITáN». |
| No multipliques un `bool` por un `float` (`0.12 * on`). Usa un `if`. | No compila. |
| Llama a `MCUIK_Notify.Reset()` y borra tus capas al empezar partida. | Los estáticos sobreviven a «Reload Game». |
| Para que un texto largo salte de línea dentro de una fila (`HBox`), aplica `MCUIK.Fill(texto)`. | Sin eso, la fila crece sin límite. |
| No abras ventanas si `GetGame().GetMenuManager().IsAnyDialogOpen()`. | Interrumpirías otra ventana. |

## Cómo comprobar que funciona

- **Compila:** arranca un servidor dedicado con el proyecto y busca en `console.log` «Can't compile» o «Virtual Machine Exception».
- **Se ve:** la interfaz solo se ve en un cliente. Lanza el juego con `-window` y tu misión, escribe una marca en el log cuando la pantalla esté lista (`Print("CAPTURA_HUD")`) y haz una captura de la ventana del juego.
- **Pruebas automáticas:** `MCUIK_Notify.CountToasts()` y `CurrentDialogue()` sirven para comprobar desde script que los avisos han salido.

## Archivos clave

| Archivo | Qué es |
|---|---|
| `Scripts/Game/MCUIK/MCUIK_Theme.c` | `MCUIK_Theme` (colores) y `MCUIK` (crear, colocar y rellenar piezas). |
| `Scripts/Game/MCUIK/MCUIK_Notify.c` | Avisos y diálogos animados. |
| `Scripts/Game/MCUIK/MCUIK_Res.c` | GUIDs de todos los recursos (generado). |
| `Scripts/Game/MCUIK/MCUIK_IconNames.c` | Nombres de iconos (generado). |
| `UI/layouts/MCUIK/*.layout` | Piezas (generadas por `tools/gen_layouts.py`). |
| `Configs/MCUIK/MCUIK_Dialogs.conf` | Presets de ventana `mcuik_list` y `mcuik_event`. |
| `llms.txt` (raíz) | Resumen de esta documentación para modelos de lenguaje. |
