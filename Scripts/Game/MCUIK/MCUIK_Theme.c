// MCUIK - tema visual: colores, plantillas y utilidades para montar piezas desde script.
// Mod independiente: no sabe nada de ninguna mision. Cualquiera puede usarlo poniendolo de dependencia.

class MCUIK_Theme
{
	static Color Rgb(int r, int g, int b, float a = 1)
	{
		return Color.FromRGBA(r, g, b, Math.Round(a * 255));
	}

	static Color Accent(float a = 1)  { return Rgb(255, 199, 44, a); }    // amarillo canario
	static Color Info(float a = 1)    { return Rgb(46, 139, 255, a); }    // azul atlantico
	static Color Danger(float a = 1)  { return Rgb(255, 77, 61, a); }
	static Color Warning(float a = 1) { return Rgb(255, 150, 40, a); }
	static Color Success(float a = 1) { return Rgb(61, 220, 132, a); }
	static Color Text(float a = 1)    { return Rgb(232, 237, 240, a); }
	static Color Muted(float a = 1)   { return Rgb(143, 161, 173, a); }
	static Color Panel(float a = 0.9) { return Rgb(14, 20, 25, a); }

	//! Color en formato de etiqueta de texto enriquecido: <color rgba="r,g,b,a">
	static string Tag(Color c)
	{
		return string.Format("<color rgba=\"%1,%2,%3,%4\">", Math.Round(c.R() * 255), Math.Round(c.G() * 255), Math.Round(c.B() * 255), Math.Round(c.A() * 255));
	}

	static string Paint(string txt, Color c)
	{
		return Tag(c) + txt + "</color>";
	}
}

class MCUIK
{

	// ------------------------------------------------------------------ crear y colocar

	static Widget Create(ResourceName layout, Widget parent = null)
	{
		WorkspaceWidget ws = GetGame().GetWorkspace();
		if (!ws)
			return null;
		return ws.CreateWidgets(layout, parent);
	}

	//! Capa a pantalla completa que no roba el raton (para colgar el HUD)
	static Widget CreateLayer(int z = 2)
	{
		WorkspaceWidget ws = GetGame().GetWorkspace();
		if (!ws)
			return null;
		Widget w = ws.CreateWidget(WidgetType.FrameWidgetTypeID, WidgetFlags.VISIBLE | WidgetFlags.IGNORE_CURSOR | WidgetFlags.NOFOCUS, Color.FromInt(Color.WHITE), z);
		if (!w)
			return null;
		FrameSlot.SetAnchorMin(w, 0, 0);
		FrameSlot.SetAnchorMax(w, 1, 1);
		FrameSlot.SetOffsets(w, 0, 0, 0, 0);
		return w;
	}

	//! Coloca un widget de una capa: ancla (0-1), alineacion propia (0-1) y desplazamiento en pixeles de 1080p
	static void Place(Widget w, float ax, float ay, float alx, float aly, float x, float y)
	{
		if (!w)
			return;
		FrameSlot.SetAnchorMin(w, ax, ay);
		FrameSlot.SetAnchorMax(w, ax, ay);
		FrameSlot.SetAlignment(w, alx, aly);
		FrameSlot.SetPos(w, x, y);
		FrameSlot.SetSizeToContent(w, true);
	}

	// ------------------------------------------------------------------ rellenar por nombre

	static void SetText(Widget root, string name, string txt)
	{
		if (!root)
			return;
		Widget w = root;
		if (root.GetName() != name)
			w = root.FindAnyWidget(name);
		TextWidget t = TextWidget.Cast(w);
		if (t)
		{
			t.SetText(txt);
			return;
		}
		RichTextWidget r = RichTextWidget.Cast(w);
		if (r)
			r.SetText(txt);
	}

	static void SetColor(Widget root, string name, Color c)
	{
		if (!root)
			return;
		Widget w = root;
		if (root.GetName() != name)
			w = root.FindAnyWidget(name);
		if (w)
			w.SetColor(c);
	}

	static void SetIcon(Widget root, string name, string icon, Color c = null)
	{
		if (!root)
			return;
		Widget w = root;
		if (root.GetName() != name)
			w = root.FindAnyWidget(name);
		ImageWidget img = ImageWidget.Cast(w);
		if (!img)
			return;
		img.LoadImageFromSet(0, MCUIK_Res.ICONS, icon);
		if (c)
			img.SetColor(c);
	}

	static void SetVisible(Widget root, string name, bool v)
	{
		if (!root)
			return;
		Widget w = root.FindAnyWidget(name);
		if (w)
			w.SetVisible(v);
	}

	static void SetWidth(Widget root, string name, float width)
	{
		if (!root)
			return;
		Widget w = root;
		if (root.GetName() != name)
			w = root.FindAnyWidget(name);
		SizeLayoutWidget s = SizeLayoutWidget.Cast(w);
		if (s)
			s.SetWidthOverride(width);
	}

	// ------------------------------------------------------------------ piezas

	//! Chip: icono + numero grande + etiqueta
	static Widget Chip(Widget parent, string icon, string value, string label, Color c = null)
	{
		Widget w = Create(MCUIK_Res.L_CHIP, parent);
		SetChip(w, icon, value, label, c);
		return w;
	}

	static void SetChip(Widget chip, string icon, string value, string label, Color color = null)
	{
		if (!chip)
			return;
		// local: un objeto nuevo guardado solo en un parametro se libera al momento
		Color c = color;
		if (!c)
			c = MCUIK_Theme.Accent();
		SetIcon(chip, "Icon", icon, c);
		SetText(chip, "Value", value);
		SetText(chip, "Label", label);
		SetVisible(chip, "Label", !label.IsEmpty());
	}

	//! Fila: icono, etiqueta y valor
	static Widget Row(Widget parent, string icon, string label, string value, Color iconColor = null)
	{
		Widget w = Create(MCUIK_Res.L_ROW, parent);
		SetRow(w, icon, label, value, iconColor);
		return w;
	}

	static void SetRow(Widget row, string icon, string label, string value, Color color = null)
	{
		if (!row)
			return;
		Color iconColor = color;
		if (!iconColor)
			iconColor = MCUIK_Theme.Muted();
		SetIcon(row, "Icon", icon, iconColor);
		SetText(row, "Label", label);
		SetText(row, "Value", value);
	}

	//! Barra: frac 0-1 con el ancho total en pixeles
	static Widget Bar(Widget parent, float frac, float width, Color c = null, float height = 6)
	{
		Widget w = Create(MCUIK_Res.L_BAR, parent);
		SizeLayoutWidget s = SizeLayoutWidget.Cast(w);
		if (s)
			s.SetHeightOverride(height);
		SetBar(w, frac, width, c);
		return w;
	}

	static void SetBar(Widget bar, float frac, float width, Color c = null)
	{
		if (!bar)
			return;
		SizeLayoutWidget s = SizeLayoutWidget.Cast(bar);
		if (s)
			s.SetWidthOverride(width);
		SetWidth(bar, "FillSize", Math.Clamp(frac, 0, 1) * width);
		if (c)
			SetColor(bar, "Fill", c);
	}

	//! Panel con cabecera: devuelve la raiz; el contenido se cuelga de Content(panel)
	static Widget Panel(Widget parent, string icon, string title, float width, Color accent = null)
	{
		Widget w = Create(MCUIK_Res.L_PANEL, parent);
		SetPanel(w, icon, title, "", width, accent);
		return w;
	}

	static void SetPanel(Widget panel, string icon, string title, string right, float width, Color color = null)
	{
		if (!panel)
			return;
		Color accent = color;
		if (!accent)
			accent = MCUIK_Theme.Accent();
		SetWidth(panel, "PanelRoot", width);
		SetIcon(panel, "HeaderIcon", icon, accent);
		SetText(panel, "HeaderTitle", title);
		SetColor(panel, "HeaderTitle", accent);
		SetText(panel, "HeaderRight", right);
		SetColor(panel, "Accent", accent);
	}

	static Widget Content(Widget panel)
	{
		if (!panel)
			return null;
		return panel.FindAnyWidget("Content");
	}

	static Widget Text(Widget parent, string txt, float size = 16, Color c = null)
	{
		Widget w = Create(MCUIK_Res.L_TEXT, parent);
		RichTextWidget r = RichTextWidget.Cast(w);
		if (r)
		{
			r.SetText(txt);
			r.SetDesiredFontSize(size);
			if (c)
				r.SetColor(c);
		}
		return w;
	}

	static Widget Title(Widget parent, string txt, Color c = null)
	{
		Widget w = Create(MCUIK_Res.L_TITLE, parent);
		SetText(w, "Title", txt);
		if (c && w)
			w.SetColor(c);
		return w;
	}

	static Widget Divider(Widget parent)
	{
		return Create(MCUIK_Res.L_DIVIDER, parent);
	}

	static Widget Spacer(Widget parent, float h = 8)
	{
		Widget w = Create(MCUIK_Res.L_SPACER, parent);
		SizeLayoutWidget s = SizeLayoutWidget.Cast(w);
		if (s)
			s.SetHeightOverride(h);
		return w;
	}

	static Widget HBox(Widget parent)
	{
		return Create(MCUIK_Res.L_HBOX, parent);
	}

	static Widget VBox(Widget parent)
	{
		return Create(MCUIK_Res.L_VBOX, parent);
	}

	//! Margen de un widget dentro de una fila o columna
	static void Pad(Widget w, float left, float top, float right, float bottom)
	{
		if (w)
			LayoutSlot.SetPadding(w, left, top, right, bottom);
	}

	//! Ocupa el espacio que sobre en su fila (para que un texto largo haga salto de linea)
	static void Fill(Widget w)
	{
		if (w)
			LayoutSlot.SetSizeMode(w, LayoutSizeMode.Fill);
	}

	//! Quita todos los hijos de un contenedor
	static void Clear(Widget container)
	{
		if (!container)
			return;
		Widget c = container.GetChildren();
		while (c)
		{
			Widget next = c.GetSibling();
			c.RemoveFromHierarchy();
			c = next;
		}
	}

	//! Mayusculas que respetan tildes y enes (ToUpper del motor no las convierte)
	static string Upper(string s)
	{
		string r = s;
		r.ToUpper();
		r.Replace("á", "Á");
		r.Replace("é", "É");
		r.Replace("í", "Í");
		r.Replace("ó", "Ó");
		r.Replace("ú", "Ú");
		r.Replace("ñ", "Ñ");
		r.Replace("ü", "Ü");
		return r;
	}

	//! Distancia legible: 340 m, 1,2 km
	static string Distance(float d)
	{
		if (d < 1000)
			return string.Format("%1 m", Math.Round(d / 10) * 10);
		string s = string.Format("%1 km", Math.Round(d / 100) / 10.0);
		s.Replace(".", ",");
		return s;
	}

	//! Cantidad con separador de miles: 12.500
	static string Thousands(int v)
	{
		string s = Math.AbsInt(v).ToString();
		string res;
		int n = s.Length();
		for (int i = 0; i < n; i++)
		{
			if (i > 0 && (n - i) % 3 == 0)
				res += ".";
			res += s.Get(i);
		}
		if (v < 0)
			return "-" + res;
		return res;
	}

	//! Suavizado para animaciones (sale rapido y frena al final)
	static float EaseOut(float t)
	{
		t = Math.Clamp(t, 0, 1);
		return 1 - (1 - t) * (1 - t) * (1 - t);
	}
}
