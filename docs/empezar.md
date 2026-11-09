---
title: Empezar
nav_order: 2
---

# Empezar

## 1. Añadir la dependencia

En el `addon.gproj` de tu mod:

```
Dependencies {
 "58D0FB3206B6F859"
 "B8DFCB8639E9DA37"
}
```

En el Workshop, marca **MCUIK** como dependencia al publicar. Para probar sin publicar, pon la carpeta del proyecto MCUIK en una de las rutas de `-addonsDir`.

## 2. Pintar algo (solo en clientes)

La interfaz existe solo donde hay pantalla. En un servidor dedicado, `GetGame().GetWorkspace()` no sirve, así que comprueba antes `System.IsConsoleApp()`.

```c
class MiHud
{
    protected Widget m_wLayer;
    protected Widget m_wPanel;
    protected Widget m_wDinero;
    protected Widget m_wApoyo;

    void Crear()
    {
        if (System.IsConsoleApp())
            return;
        m_wLayer = MCUIK.CreateLayer();                                // capa a pantalla completa, no roba el ratón
        m_wPanel = MCUIK.Panel(m_wLayer, "faction_spain", "MI COMPAÑÍA", 300);
        MCUIK.Place(m_wPanel, 1, 0, 1, 0, -18, 18);                     // arriba a la derecha, 18 px del borde
        Widget c = MCUIK.Content(m_wPanel);
        m_wDinero = MCUIK.Chip(c, "money", "0 €", "FONDOS");
        m_wApoyo = MCUIK.Bar(c, 0, 276, MCUIK_Theme.Success());
    }

    void Actualizar(int dinero, float apoyo)
    {
        MCUIK.SetChip(m_wDinero, "money", MCUIK.Thousands(dinero) + " €", "FONDOS");
        MCUIK.SetBar(m_wApoyo, apoyo, 276, MCUIK_Theme.Success());
    }
}
```

## 3. Avisar al jugador

```c
MCUIK_Notify.Toast("alert", "Contraataque", "Dos grupos van hacia <b>Telde</b>.", MCUIK_Theme.Danger());
MCUIK_Notify.Dialogue("radio", "Capitán Lustre", "Buen trabajo, Carvos.", MCUIK_Theme.Accent());
```

## 4. Al empezar una partida nueva

Los datos estáticos de Enforce Script sobreviven a «Reload Game» en Workbench y a volver a entrar en partida. Al iniciar tu modo de juego (en clientes), llama a:

```c
MCUIK_Notify.Reset();
```

y quita tus capas antiguas con `RemoveFromHierarchy()`.

## Siguiente

- [Piezas](piezas.md): todo lo que puedes montar.
- [Guía para IA](guia-ia.md): si quien va a programar es un asistente.
