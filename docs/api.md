---
title: Referencia de la API
nav_order: 90
---

# MCUIK · Referencia de la API

> Generado automáticamente desde el código (`tools/gen_api_docs.py`). No editar a mano.

## MCUIK_IconNames.c

> Generado por tools/gen_icons.py: nombres de los iconos del atlas de MCUIK

### `MCUIK_Icon`

| Constante | Tipo | Valor |
|---|---|---|
| `MONEY` | `string` | `"money"` |
| `MATERIALS` | `string` | `"materials"` |
| `SUPPORT` | `string` | `"support"` |
| `RECRUIT` | `string` | `"recruit"` |
| `PEOPLE` | `string` | `"people"` |
| `ZONE` | `string` | `"zone"` |
| `TIME` | `string` | `"time"` |
| `STAR` | `string` | `"star"` |
| `OBJECTIVE` | `string` | `"objective"` |
| `RADIO` | `string` | `"radio"` |
| `JOURNAL` | `string` | `"journal"` |
| `INTEL` | `string` | `"intel"` |
| `PHONE` | `string` | `"phone"` |
| `CHAT` | `string` | `"chat"` |
| `MAP` | `string` | `"map"` |
| `PIN` | `string` | `"pin"` |
| `SHOP` | `string` | `"shop"` |
| `GARAGE` | `string` | `"garage"` |
| `VEHICLE` | `string` | `"vehicle"` |
| `WEAPON` | `string` | `"weapon"` |
| `AMMO` | `string` | `"ammo"` |
| `MEDICAL` | `string` | `"medical"` |
| `EXPLOSIVE` | `string` | `"explosive"` |
| `CLOTHING` | `string` | `"clothing"` |
| `TOOL` | `string` | `"tool"` |
| `BUILD` | `string` | `"build"` |
| `STORAGE` | `string` | `"storage"` |
| `COVER_CIVIL` | `string` | `"cover_civil"` |
| `COVER_MILITARY` | `string` | `"cover_military"` |
| `COVER_WATCHED` | `string` | `"cover_watched"` |
| `COVER_HIDDEN` | `string` | `"cover_hidden"` |
| `COVER_DISGUISED` | `string` | `"cover_disguised"` |
| `ALERT` | `string` | `"alert"` |
| `THREAT` | `string` | `"threat"` |
| `TOWN` | `string` | `"town"` |
| `BASE` | `string` | `"base"` |
| `OUTPOST` | `string` | `"outpost"` |
| `AIRFIELD` | `string` | `"airfield"` |
| `PORT` | `string` | `"port"` |
| `FACTORY` | `string` | `"factory"` |
| `RESOURCE` | `string` | `"resource"` |
| `CAMP` | `string` | `"camp"` |
| `FACTION_SPAIN` | `string` | `"faction_spain"` |
| `FACTION_TRUMPET` | `string` | `"faction_trumpet"` |
| `FACTION_PUTONCIN` | `string` | `"faction_putoncin"` |
| `FACTION_CIVIL` | `string` | `"faction_civil"` |
| `CHECK` | `string` | `"check"` |
| `CLOSE` | `string` | `"close"` |
| `PLUS` | `string` | `"plus"` |
| `MINUS` | `string` | `"minus"` |
| `ARROW` | `string` | `"arrow"` |
| `CHEVRON` | `string` | `"chevron"` |
| `INFO` | `string` | `"info"` |
| `LOCK` | `string` | `"lock"` |
| `KEY` | `string` | `"key"` |
| `NIGHT` | `string` | `"night"` |
| `DOT` | `string` | `"dot"` |
| `RING` | `string` | `"ring"` |
| `DIAMOND` | `string` | `"diamond"` |
| `HEX` | `string` | `"hex"` |


## MCUIK_Notify.c

> MCUIK - avisos animados:
> * Toast: tarjeta a la derecha (entra deslizando, se apila, se desvanece); hasta 4 a la vez.
> * Dialogo: quien habla y que dice, abajo en el centro, de uno en uno (cola). Al mostrarse cada
> linea se llama a OnDialogueShown(tag) para que la mision ponga la voz si la tiene.
> Solo en clientes con interfaz. Se anima solo (bucle propio en la cola de llamadas).

### `MCUIK_ToastItem`


### `MCUIK_DialogueItem`


### `MCUIK_Notify`

| Constante | Tipo | Valor |
|---|---|---|
| `MAX_TOASTS` | `int` | `4` |
| `TOAST_IN` | `float` | `0.35` |
| `TOAST_OUT` | `float` | `0.4` |
| `SLIDE` | `float` | `80` |
| `GAP` | `float` | `10` |

- `static ScriptInvoker OnDialogueShown()`
  — Se llama con el tag de cada linea de dialogo al empezar a mostrarse
- `static void Reset()`
  — Partida nueva (o recarga en Workbench): se rehace todo
- `static void Toast(string icon, string title, string body, Color accent = null, float seconds = 0)`
  — Aviso lateral. seconds <= 0: segun lo largo que sea el texto
- `static void Dialogue(string icon, string speaker, string line, Color accent = null, float seconds = 0, int tag = -1)`
  — Linea de dialogo (cola). tag: lo que quiera la mision (p. ej. el numero de la voz)
- `static float ReadTime(string txt)`
  — Lo que se tarda en leer un texto con calma (13 letras por segundo, entre 5 y 26 s)
- `static void SetHidden(bool hidden)`
  — Oculta los avisos (por ejemplo con un menu abierto); siguen contando el tiempo
- `static int CountToasts()`
- `static string CurrentDialogue()`
- `static int QueuedDialogues()`

## MCUIK_Res.c

> Generado por tools/build.py: recursos del kit (no editar a mano)

### `MCUIK_Res`

| Constante | Tipo | Valor |
|---|---|---|
| `C_DIALOGS` | `ResourceName` | `"{757EA30DCE5EF939}Configs/MCUIK/MCUIK_Dialogs.conf"` |
| `ICONS` | `ResourceName` | `"{3BA4B2A75ED412DC}UI/Textures/MCUIK/MCUIK_Icons.imageset"` |
| `L_BAR` | `ResourceName` | `"{10D8CD1CE0343988}UI/layouts/MCUIK/MCUIK_Bar.layout"` |
| `L_CHIP` | `ResourceName` | `"{17B838C08CA9ED58}UI/layouts/MCUIK/MCUIK_Chip.layout"` |
| `L_DIALOGUE` | `ResourceName` | `"{EA9911095ADD9CCD}UI/layouts/MCUIK/MCUIK_Dialogue.layout"` |
| `L_DIVIDER` | `ResourceName` | `"{6D75511B9731A5A9}UI/layouts/MCUIK/MCUIK_Divider.layout"` |
| `L_EVENTCONTENT` | `ResourceName` | `"{B5B3998C39D3F128}UI/layouts/MCUIK/MCUIK_EventContent.layout"` |
| `L_HBOX` | `ResourceName` | `"{B398025C19E5DCAA}UI/layouts/MCUIK/MCUIK_HBox.layout"` |
| `L_ICON` | `ResourceName` | `"{8CD549298FCAB10E}UI/layouts/MCUIK/MCUIK_Icon.layout"` |
| `L_LISTCONTENT` | `ResourceName` | `"{3FF1CD16CBB6FB97}UI/layouts/MCUIK/MCUIK_ListContent.layout"` |
| `L_LISTROW` | `ResourceName` | `"{1C646CF8921747ED}UI/layouts/MCUIK/MCUIK_ListRow.layout"` |
| `L_PANEL` | `ResourceName` | `"{55ECE5D23E2BA2C7}UI/layouts/MCUIK/MCUIK_Panel.layout"` |
| `L_ROW` | `ResourceName` | `"{83A21D70082F201A}UI/layouts/MCUIK/MCUIK_Row.layout"` |
| `L_SPACER` | `ResourceName` | `"{843B3AE9A5C8DF20}UI/layouts/MCUIK/MCUIK_Spacer.layout"` |
| `L_TEXT` | `ResourceName` | `"{79015F9C3A8CAAC3}UI/layouts/MCUIK/MCUIK_Text.layout"` |
| `L_TITLE` | `ResourceName` | `"{3A3A3049DB0E0A49}UI/layouts/MCUIK/MCUIK_Title.layout"` |
| `L_TOAST` | `ResourceName` | `"{1E935E61E354B0F7}UI/layouts/MCUIK/MCUIK_Toast.layout"` |
| `L_VBOX` | `ResourceName` | `"{7AC394336033B66B}UI/layouts/MCUIK/MCUIK_VBox.layout"` |


## MCUIK_Theme.c

> MCUIK - tema visual: colores, plantillas y utilidades para montar piezas desde script.
> Mod independiente: no sabe nada de ninguna mision. Cualquiera puede usarlo poniendolo de dependencia.

### `MCUIK_Theme`

- `static Color Rgb(int r, int g, int b, float a = 1)`
- `static Color Accent(float a = 1)`
- `static Color Info(float a = 1)`
- `static Color Danger(float a = 1)`
- `static Color Warning(float a = 1)`
- `static Color Success(float a = 1)`
- `static Color Text(float a = 1)`
- `static Color Muted(float a = 1)`
- `static Color Panel(float a = 0.9)`
- `static string Tag(Color c)`
  — Color en formato de etiqueta de texto enriquecido: <color rgba="r,g,b,a">
- `static string Paint(string txt, Color c)`

### `MCUIK`

- `static Widget Create(ResourceName layout, Widget parent = null)`
- `static Widget CreateLayer(int z = 2)`
  — Capa a pantalla completa que no roba el raton (para colgar el HUD)
- `static void Place(Widget w, float ax, float ay, float alx, float aly, float x, float y)`
  — Coloca un widget de una capa: ancla (0-1), alineacion propia (0-1) y desplazamiento en pixeles de 1080p
- `static void SetText(Widget root, string name, string txt)`
- `static void SetColor(Widget root, string name, Color c)`
- `static void SetIcon(Widget root, string name, string icon, Color c = null)`
- `static void SetVisible(Widget root, string name, bool v)`
- `static void SetWidth(Widget root, string name, float width)`
- `static Widget Chip(Widget parent, string icon, string value, string label, Color c = null)`
  — Chip: icono + numero grande + etiqueta
- `static void SetChip(Widget chip, string icon, string value, string label, Color color = null)`
- `static Widget Row(Widget parent, string icon, string label, string value, Color iconColor = null)`
  — Fila: icono, etiqueta y valor
- `static void SetRow(Widget row, string icon, string label, string value, Color color = null)`
- `static Widget Bar(Widget parent, float frac, float width, Color c = null, float height = 6)`
  — Barra: frac 0-1 con el ancho total en pixeles
- `static void SetBar(Widget bar, float frac, float width, Color c = null)`
- `static Widget Panel(Widget parent, string icon, string title, float width, Color accent = null)`
  — Panel con cabecera: devuelve la raiz; el contenido se cuelga de Content(panel)
- `static void SetPanel(Widget panel, string icon, string title, string right, float width, Color color = null)`
- `static Widget Content(Widget panel)`
- `static Widget Text(Widget parent, string txt, float size = 16, Color c = null)`
- `static Widget Title(Widget parent, string txt, Color c = null)`
- `static Widget Divider(Widget parent)`
- `static Widget Spacer(Widget parent, float h = 8)`
- `static Widget HBox(Widget parent)`
- `static Widget VBox(Widget parent)`
- `static void Pad(Widget w, float left, float top, float right, float bottom)`
  — Margen de un widget dentro de una fila o columna
- `static void Fill(Widget w)`
  — Ocupa el espacio que sobre en su fila (para que un texto largo haga salto de linea)
- `static void Clear(Widget container)`
  — Quita todos los hijos de un contenedor
- `static string Upper(string s)`
  — Mayusculas que respetan tildes y enes (ToUpper del motor no las convierte)
- `static string Distance(float d)`
  — Distancia legible: 340 m, 1,2 km
- `static string Thousands(int v)`
  — Cantidad con separador de miles: 12.500
- `static float EaseOut(float t)`
  — Suavizado para animaciones (sale rapido y frena al final)

