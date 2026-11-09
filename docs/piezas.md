---
title: Piezas
nav_order: 3
---

# Piezas

Todas se crean con `MCUIK.<Pieza>(padre, …)` y devuelven el `Widget` raíz. Para cambiarlas después se usa `MCUIK.Set<Pieza>(widget, …)`.

Así no hay que reconstruirlas: créalas una vez y actualiza los valores, por ejemplo cada 0,5 s.

## Colocar en pantalla

| Función | Qué hace |
|---|---|
| `MCUIK.CreateLayer(z = 2)` | Capa a pantalla completa que no roba el ratón ni el foco. Cuelga de ella tus piezas. |
| `MCUIK.Place(w, ax, ay, alx, aly, x, y)` | Coloca `w` en su capa:<br>- **Ancla** `ax, ay` (0–1): punto de la pantalla.<br>- **Alineación** `alx, aly` (0–1): qué punto del widget se pega al ancla.<br>- **Desplazamiento** `x, y`: en píxeles de referencia 1080p.<br>El tamaño se ajusta al contenido. |

Ejemplos de anclas:
- Arriba a la derecha: `Place(w, 1, 0, 1, 0, -18, 18)`.
- Abajo en el centro: `Place(w, 0.5, 1, 0.5, 1, 0, -120)`.
- Centro: `Place(w, 0.5, 0.5, 0.5, 0.5, 0, 0)`.

## Panel

Caja con cabecera (icono, título y un dato a la derecha), una línea de color y una columna `Content` para meter piezas.

```c
Widget p = MCUIK.Panel(layer, "objective", "OPERACIONES", 316);
MCUIK.SetPanel(p, "objective", "OPERACIONES", "2", 316, MCUIK_Theme.Info()); // icono, título, dato derecha, ancho, color
Widget c = MCUIK.Content(p);   // aquí van las piezas
```

Las partes con nombre (para `SetText`, `SetColor`, `SetIcon` y `SetVisible`) son `HeaderIcon`, `HeaderTitle`, `HeaderRight`, `Accent` y `Content`.

## Chip

Icono, número grande y etiqueta pequeña. Sirve para recursos y contadores.

```c
Widget chip = MCUIK.Chip(c, "money", "1.600 €", "FONDOS");
MCUIK.SetChip(chip, "money", "1.450 €", "FONDOS", MCUIK_Theme.Accent());
```

## Fila

Icono, etiqueta a la izquierda y valor a la derecha.

```c
Widget r = MCUIK.Row(c, "support", "Apoyo de los canarios", "45 %", MCUIK_Theme.Success());
MCUIK.SetRow(r, "support", "Apoyo de los canarios", "50 %", MCUIK_Theme.Success());
```

## Barra

Una barra que se llena según el valor.

```c
Widget b = MCUIK.Bar(c, 0.45, 292, MCUIK_Theme.Success(), 5);  // fracción 0–1, ancho px, color, alto
MCUIK.SetBar(b, 0.6, 292, MCUIK_Theme.Warning());
```

El ancho se pasa en píxeles: usa el ancho del panel menos 24 (los márgenes del contenido).

## Texto, título, separador y hueco

```c
MCUIK.Title(c, "OBJETIVO");                                   // mayúsculas pequeñas en color de acento
MCUIK.Text(c, "Libera <b>Agüimes</b>.", 16, MCUIK_Theme.Text()); // texto enriquecido con salto de línea
MCUIK.Divider(c);                                             // línea fina
MCUIK.Spacer(c, 10);                                          // hueco vertical
```

El texto admite `<b>`, `<i>`, `<br/>` y `<color rgba="r,g,b,a">`. Para colorear con el tema usa `MCUIK_Theme.Paint("texto", MCUIK_Theme.Danger())`.

## Cajas para componer

```c
Widget fila = MCUIK.HBox(c);           // fila horizontal
MCUIK.Chip(fila, "zone", "3/24", "ZONAS");
MCUIK.Pad(ultimoChip, 0, 4, 26, 4);    // márgenes: izquierda, arriba, derecha, abajo
MCUIK.Fill(textoLargo);                // ocupa lo que sobre en la fila (necesario para que un texto largo salte de línea)
Widget col = MCUIK.VBox(capa);         // columna: apila paneles y se reajusta sola si uno se oculta
```

Patrón recomendado para una columna de paneles: un `VBox` colocado con `Place`, con los paneles y `Spacer` dentro. Si ocultas un panel con `SetVisible(false)`, los de debajo suben solos.

## Utilidades

| Función | Resultado |
|---|---|
| `MCUIK.Thousands(12500)` | `12.500` |
| `MCUIK.Distance(1234)` | `1,2 km` (y `340 m` por debajo de 1 km) |
| `MCUIK.Upper("Capitán")` | `CAPITÁN` (respeta tildes y eñes, al contrario que `ToUpper`) |
| `MCUIK.Clear(contenedor)` | Quita todos los hijos (para rehacer una lista) |
| `MCUIK.EaseOut(t)` | Suavizado 0–1 para animaciones propias |
| `MCUIK.SetText/SetColor/SetIcon/SetVisible/SetWidth(root, "Nombre", …)` | Cambia un hijo por su nombre (o la propia raíz si se llama así) |
