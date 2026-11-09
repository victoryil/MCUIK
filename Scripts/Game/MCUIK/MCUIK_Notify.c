// MCUIK - avisos animados:
//  * Toast: tarjeta a la derecha (entra deslizando, se apila, se desvanece); hasta 4 a la vez.
//  * Dialogo: quien habla y que dice, abajo en el centro, de uno en uno (cola). Al mostrarse cada
//    linea se llama a OnDialogueShown(tag) para que la mision ponga la voz si la tiene.
// Solo en clientes con interfaz. Se anima solo (bucle propio en la cola de llamadas).

class MCUIK_ToastItem
{
	Widget m_wRoot;
	float m_fAge;
	float m_fLife;
	float m_fY;          // posicion vertical actual (sube suave al quitarse otros)
	bool m_bLeaving;
	float m_fLeave;
}

class MCUIK_DialogueItem
{
	string m_sIcon;
	string m_sSpeaker;
	string m_sLine;
	ref Color m_Color;
	float m_fLife;
	int m_iTag;
}

class MCUIK_Notify
{
	static const int MAX_TOASTS = 4;
	static const float TOAST_IN = 0.35;
	static const float TOAST_OUT = 0.4;
	static const float SLIDE = 80;
	static const float GAP = 10;

	// donde van: abajo a la derecha (los toasts) y abajo en el centro (dialogo); se pueden mover
	static float s_fToastRight = 24;
	static float s_fToastBottom = 190;
	static float s_fDialogueBottom = 120;

	protected static ref MCUIK_Notify s_Instance;
	protected static ref ScriptInvoker s_OnDialogueShown;

	protected Widget m_wLayer;
	protected ref array<ref MCUIK_ToastItem> m_aToasts = {};
	protected ref array<ref MCUIK_DialogueItem> m_aQueue = {};
	protected Widget m_wDialogue;
	protected float m_fDlgAge;
	protected float m_fDlgLife;
	protected string m_sDlgText;
	protected int m_iLastTick;
	protected bool m_bHidden;

	//! Se llama con el tag de cada linea de dialogo al empezar a mostrarse
	static ScriptInvoker OnDialogueShown()
	{
		if (!s_OnDialogueShown)
			s_OnDialogueShown = new ScriptInvoker();
		return s_OnDialogueShown;
	}

	protected static MCUIK_Notify Get()
	{
		if (System.IsConsoleApp())
			return null;
		if (!s_Instance)
		{
			s_Instance = new MCUIK_Notify();
			if (!s_Instance.Init())
				s_Instance = null;
		}
		return s_Instance;
	}

	//! Partida nueva (o recarga en Workbench): se rehace todo
	static void Reset()
	{
		if (s_Instance)
		{
			GetGame().GetCallqueue().Remove(s_Instance.Tick);
			if (s_Instance.m_wLayer)
				s_Instance.m_wLayer.RemoveFromHierarchy();
		}
		s_Instance = null;
	}

	protected bool Init()
	{
		m_wLayer = MCUIK.CreateLayer(5);
		if (!m_wLayer)
			return false;
		m_iLastTick = System.GetTickCount();
		GetGame().GetCallqueue().CallLater(Tick, 0, true);
		return true;
	}

	// ------------------------------------------------------------------ entrada

	//! Aviso lateral. seconds <= 0: segun lo largo que sea el texto
	static void Toast(string icon, string title, string body, Color accent = null, float seconds = 0)
	{
		MCUIK_Notify n = Get();
		if (n)
			n.AddToast(icon, title, body, accent, seconds);
	}

	//! Linea de dialogo (cola). tag: lo que quiera la mision (p. ej. el numero de la voz)
	static void Dialogue(string icon, string speaker, string line, Color accent = null, float seconds = 0, int tag = -1)
	{
		MCUIK_Notify n = Get();
		if (!n)
			return;
		MCUIK_DialogueItem d = new MCUIK_DialogueItem();
		d.m_sIcon = icon;
		d.m_sSpeaker = speaker;
		d.m_sLine = line;
		d.m_Color = accent;
		if (!d.m_Color)
			d.m_Color = MCUIK_Theme.Accent();
		if (seconds <= 0)
			seconds = ReadTime(line);
		d.m_fLife = seconds;
		d.m_iTag = tag;
		n.m_aQueue.Insert(d);
		// si se acumulan muchas, se tiran las mas viejas
		while (n.m_aQueue.Count() > 6)
			n.m_aQueue.RemoveOrdered(0);
	}

	//! Lo que se tarda en leer un texto con calma (13 letras por segundo, entre 5 y 26 s)
	static float ReadTime(string txt)
	{
		return Math.Clamp(3 + txt.Length() / 13.0, 5, 26);
	}

	//! Oculta los avisos (por ejemplo con un menu abierto); siguen contando el tiempo
	static void SetHidden(bool hidden)
	{
		MCUIK_Notify n = Get();
		if (n)
			n.m_bHidden = hidden;
	}

	static int CountToasts()
	{
		if (!s_Instance)
			return 0;
		return s_Instance.m_aToasts.Count();
	}

	static string CurrentDialogue()
	{
		if (!s_Instance)
			return "";
		return s_Instance.m_sDlgText;
	}

	static int QueuedDialogues()
	{
		if (!s_Instance)
			return 0;
		return s_Instance.m_aQueue.Count();
	}

	// ------------------------------------------------------------------ toasts

	protected void AddToast(string icon, string title, string body, Color color, float seconds)
	{
		Color accent = color;
		if (!accent)
			accent = MCUIK_Theme.Accent();
		if (seconds <= 0)
			seconds = Math.Clamp(ReadTime(title + body) * 0.8, 5, 16);
		Widget w = MCUIK.Create(MCUIK_Res.L_TOAST, m_wLayer);
		if (!w)
			return;
		MCUIK.SetIcon(w, "BadgeIcon", icon, accent);
		MCUIK.SetColor(w, "BadgeBg", Color.FromRGBA(Math.Round(accent.R() * 255), Math.Round(accent.G() * 255), Math.Round(accent.B() * 255), 46));
		MCUIK.SetColor(w, "Strip", accent);
		MCUIK.SetColor(w, "Time", Color.FromRGBA(Math.Round(accent.R() * 255), Math.Round(accent.G() * 255), Math.Round(accent.B() * 255), 170));
		MCUIK.SetText(w, "Title", title);
		MCUIK.SetColor(w, "Title", accent);
		MCUIK.SetText(w, "Body", body);
		MCUIK.Place(w, 1, 1, 1, 1, -s_fToastRight + SLIDE, -s_fToastBottom);
		w.SetOpacity(0);
		MCUIK_ToastItem t = new MCUIK_ToastItem();
		t.m_wRoot = w;
		t.m_fLife = seconds;
		t.m_fY = s_fToastBottom;
		m_aToasts.Insert(t);
		// demasiados: el mas viejo se va
		int alive = 0;
		foreach (MCUIK_ToastItem o : m_aToasts)
		{
			if (!o.m_bLeaving)
				alive++;
		}
		if (alive > MAX_TOASTS)
		{
			foreach (MCUIK_ToastItem o2 : m_aToasts)
			{
				if (!o2.m_bLeaving)
				{
					o2.m_bLeaving = true;
					break;
				}
			}
		}
	}

	protected void Tick()
	{
		int now = System.GetTickCount();
		float dt = Math.Clamp((now - m_iLastTick) / 1000.0, 0, 0.25);
		m_iLastTick = now;
		if (!m_wLayer)
			return;
		MenuManager mm = GetGame().GetMenuManager();
		bool hide = m_bHidden || (mm && mm.IsAnyDialogOpen());
		m_wLayer.SetVisible(!hide);
		TickToasts(dt);
		TickDialogue(dt);
	}

	protected void TickToasts(float dt)
	{
		WorkspaceWidget ws = GetGame().GetWorkspace();
		// de abajo arriba: el mas nuevo abajo del todo
		float y = s_fToastBottom;
		for (int i = m_aToasts.Count() - 1; i >= 0; i--)
		{
			MCUIK_ToastItem t = m_aToasts[i];
			if (!t.m_wRoot)
			{
				m_aToasts.Remove(i);
				continue;
			}
			t.m_fAge += dt;
			if (!t.m_bLeaving && t.m_fAge >= t.m_fLife)
				t.m_bLeaving = true;
			float alpha = MCUIK.EaseOut(t.m_fAge / TOAST_IN);
			float slide = (1 - MCUIK.EaseOut(t.m_fAge / TOAST_IN)) * SLIDE;
			if (t.m_bLeaving)
			{
				t.m_fLeave += dt;
				alpha = Math.Min(alpha, 1 - t.m_fLeave / TOAST_OUT);
				slide = MCUIK.EaseOut(t.m_fLeave / TOAST_OUT) * SLIDE * 0.6;
				if (t.m_fLeave >= TOAST_OUT)
				{
					t.m_wRoot.RemoveFromHierarchy();
					m_aToasts.RemoveOrdered(i);
					continue;
				}
			}
			// sube suave hasta su sitio en la pila
			t.m_fY += (y - t.m_fY) * Math.Clamp(dt * 12, 0, 1);
			t.m_wRoot.SetOpacity(Math.Clamp(alpha, 0, 1));
			FrameSlot.SetPos(t.m_wRoot, -s_fToastRight + slide, -t.m_fY);
			float frac = 1 - Math.Clamp(t.m_fAge / t.m_fLife, 0, 1);
			MCUIK.SetWidth(t.m_wRoot, "TimeSize", 430 * frac);
			float w, h;
			t.m_wRoot.GetScreenSize(w, h);
			if (ws)
				h = ws.DPIUnscale(h);
			if (h < 10)
				h = 80;
			y += h + GAP;
		}
	}

	// ------------------------------------------------------------------ dialogo

	protected void TickDialogue(float dt)
	{
		if (m_wDialogue)
		{
			m_fDlgAge += dt;
			float alpha = Math.Min(MCUIK.EaseOut(m_fDlgAge / 0.3), 1 - (m_fDlgAge - m_fDlgLife) / 0.35);
			m_wDialogue.SetOpacity(Math.Clamp(alpha, 0, 1));
			float rise = (1 - MCUIK.EaseOut(m_fDlgAge / 0.3)) * 24;
			FrameSlot.SetPos(m_wDialogue, 0, -s_fDialogueBottom + rise);
			MCUIK.SetWidth(m_wDialogue, "TimeSize", 860 * (1 - Math.Clamp(m_fDlgAge / m_fDlgLife, 0, 1)));
			// con cola esperando, se acelera un poco la salida
			if (m_fDlgAge < m_fDlgLife + 0.35)
				return;
			m_wDialogue.RemoveFromHierarchy();
			m_wDialogue = null;
			m_sDlgText = "";
		}
		if (m_aQueue.IsEmpty())
			return;
		MCUIK_DialogueItem d = m_aQueue[0];
		m_aQueue.RemoveOrdered(0);
		m_wDialogue = MCUIK.Create(MCUIK_Res.L_DIALOGUE, m_wLayer);
		if (!m_wDialogue)
			return;
		Color c = d.m_Color;
		MCUIK.SetIcon(m_wDialogue, "PortraitIcon", d.m_sIcon, c);
		MCUIK.SetColor(m_wDialogue, "PortraitBg", Color.FromRGBA(Math.Round(c.R() * 255), Math.Round(c.G() * 255), Math.Round(c.B() * 255), 46));
		MCUIK.SetColor(m_wDialogue, "Strip", c);
		MCUIK.SetColor(m_wDialogue, "Time", Color.FromRGBA(Math.Round(c.R() * 255), Math.Round(c.G() * 255), Math.Round(c.B() * 255), 150));
		MCUIK.SetText(m_wDialogue, "Speaker", MCUIK.Upper(d.m_sSpeaker));
		MCUIK.SetColor(m_wDialogue, "Speaker", c);
		MCUIK.SetText(m_wDialogue, "Line", d.m_sLine);
		MCUIK.Place(m_wDialogue, 0.5, 1, 0.5, 1, 0, -s_fDialogueBottom);
		m_wDialogue.SetOpacity(0);
		m_fDlgAge = 0;
		m_fDlgLife = d.m_fLife;
		if (m_aQueue.Count() > 2 && d.m_iTag < 0)
			m_fDlgLife = Math.Max(4, m_fDlgLife * 0.7);
		m_sDlgText = d.m_sSpeaker + ": " + d.m_sLine;
		if (s_OnDialogueShown)
			s_OnDialogueShown.Invoke(d.m_iTag);
	}
}
