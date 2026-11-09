---
title: Avisos y diálogos
nav_order: 4
---

# Avisos y diálogos (`MCUIK_Notify`)

Funciona solo en clientes. Se anima solo, con su propio bucle; no hay que llamarlo cada fotograma.

## Tarjetas laterales (toasts)

```c
MCUIK_Notify.Toast(string icon, string title, string body, Color accent = null, float seconds = 0);
```

- **Entrada:** deslizando desde la derecha.
- **Apilado:** los nuevos van abajo y como mucho hay **4** a la vez; si sale uno más, el más viejo se va.
- **Tiempo:** una línea fina abajo se vacía con el tiempo. Con `seconds <= 0` dura lo que se tarda en leerlo (entre 5 y 16 s).
- **Posición:** se cambia con `MCUIK_Notify.s_fToastRight` y `s_fToastBottom`, en píxeles desde la esquina de abajo a la derecha.

```c
MCUIK_Notify.Toast("zone", "Zona liberada", "<b>Agüimes</b> vuelve a ser española.", MCUIK_Theme.Success());
MCUIK_Notify.Toast("alert", "Contraataque", "Llegan en 6 minutos.", MCUIK_Theme.Danger());
```

## Diálogo (quién habla)

```c
MCUIK_Notify.Dialogue(string icon, string speaker, string line, Color accent = null, float seconds = 0, int tag = -1);
```

- Abajo en el centro, de uno en uno (cola de hasta 6).
- El nombre de quien habla sale en mayúsculas (con tildes), y hay una insignia con su icono y una línea de tiempo.
- Con `seconds <= 0` dura lo que se tarda en leer la línea (entre 5 y 26 s). Si hay voz, pasa su duración.
- Si se acumulan más de dos líneas sin voz, la que se muestra dura un 30 % menos.

### Voz

Cuando una línea empieza a verse se dispara `OnDialogueShown()` con su `tag`. Úsalo para reproducir la voz justo a la vez:

```c
MCUIK_Notify.OnDialogueShown().Insert(PonerVoz);   // una vez al iniciar (quítalo antes con Remove si reinicias)

static void PonerVoz(int tag)
{
    if (tag >= 0)
        MiSistemaDeVoces.Play(tag);
}

int voz = MiSistemaDeVoces.Find(texto);
MCUIK_Notify.Dialogue("radio", "Capitán Lustre", texto, MCUIK_Theme.Accent(), MiSistemaDeVoces.Duracion(voz) + 1.5, voz);
```

## Otras funciones

| Función | Para qué |
|---|---|
| `SetHidden(bool)` | Ocultar los avisos un rato (siguen contando el tiempo). Con un diálogo del juego abierto se ocultan solos. |
| `ReadTime(texto)` | Segundos que se tarda en leer un texto. |
| `CountToasts()`, `CurrentDialogue()`, `QueuedDialogues()` | Para pruebas automáticas. |
| `Reset()` | Al empezar una partida nueva. |
