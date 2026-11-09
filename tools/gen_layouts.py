# Genera los .layout del kit MCUIK desde una descripcion en Python (mas facil de mantener que a mano).
# Uso: python tools/gen_layouts.py
import hashlib, io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "UI", "layouts", "MCUIK")
import metas
ICONS = "{" + metas.guid_for("UI/Textures/MCUIK/MCUIK_Icons.imageset") + "}UI/Textures/MCUIK/MCUIK_Icons.imageset"
BOLD = "{EABA4FE9D014CCEF}UI/Fonts/RobotoCondensed/RobotoCondensed_Bold.fnt"
REG = "{3E7733BAC8C831F6}UI/Fonts/RobotoCondensed/RobotoCondensed_Regular.fnt"

# colores del tema (r g b a, 0-1)
PANEL = "0.055 0.078 0.098 0.9"
PANEL_DARK = "0.03 0.045 0.058 0.95"
ACCENT = "1 0.78 0.17 1"
TEXT = "0.91 0.93 0.94 1"
MUTED = "0.56 0.63 0.68 1"

_counter = [0]


class W:
	def __init__(self, cls, name, slot=None, props=None, children=None):
		self.cls, self.name, self.slot, self.props, self.children = cls, name, slot or {}, props or [], children or []


def gid(seed):
	_counter[0] += 1
	return '"{' + hashlib.sha1(f"{seed}:{_counter[0]}".encode()).hexdigest()[:16].upper() + '}"'


def emit(w, slot_kind, depth, file_seed, root=False):
	ind = " " * depth
	head = f"{ind}{w.cls}Class" + ("" if root else " " + gid(file_seed + w.name)) + " {"
	out = [head, f'{ind} Name "{w.name}"']
	if w.slot and slot_kind:
		out.append(f"{ind} Slot {slot_kind} {gid(file_seed + w.name + 'slot')} {{")
		for k, v in w.slot.items():
			out.append(f"{ind}  {k} {v}")
		out.append(f"{ind} }}")
	for p in w.props:
		if isinstance(p, tuple) and p[0] == "font":
			_, font, outline = p
			out.append(f"{ind} FontProperties FontProperties {gid(file_seed + w.name + 'font')} {{")
			out.append(f'{ind}  Font "{font}"')
			if outline:
				out += [f"{ind}  OutlineSize 1", f"{ind}  OutlineColor 0 0 0 0.6"]
			out.append(f"{ind} }}")
		else:
			out.append(f"{ind} {p}")
	if w.children:
		kind = {"OverlayWidget": "OverlayWidgetSlot", "HorizontalLayoutWidget": "LayoutSlot", "VerticalLayoutWidget": "LayoutSlot",
			"SizeLayoutWidget": "AlignableSlot", "FrameWidget": "FrameWidgetSlot", "ButtonWidget": "ButtonWidgetSlot",
			"ScrollLayoutWidget": "AlignableSlot"}[w.cls]
		out.append(f"{ind} {{")
		for c in w.children:
			out += emit(c, kind, depth + 2, file_seed)
		out.append(f"{ind} }}")
	out.append(f"{ind}}}")
	return out


def save(name, root):
	_counter[0] = 0
	lines = emit(root, None, 0, name, root=True)
	io.open(os.path.join(OUT, name + ".layout"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
	print("layout", name)


# ---------------------------------------------------------------- piezas

FILL = {"HorizontalAlign": 3, "VerticalAlign": 3}


def img(name, color, slot=None, image=None, size=None):
	props = []
	if image:
		props += [f'Texture "{ICONS}"', f'Image "{image}"']
	props.append(f"Color {color}")
	if size:
		props.append(f"Size {size} {size}")
	return W("ImageWidget", name, slot or dict(FILL), props)


def text(name, txt, size, font=REG, color=TEXT, slot=None, rich=False, wrap=False, extra=None, outline=False):
	props = [f"Color {color}", f'Text "{txt}"', f'"Font Size" {size}', f'"Min Font Size" {max(10, size - 6)}']
	if wrap:
		props.append("Wrap 1")
	props += extra or []
	props.append(("font", font, outline))
	return W("RichTextWidget" if rich else "TextWidget", name, slot or {}, props)


def sized(name, w=None, h=None, slot=None, children=None):
	props = []
	if w is not None:
		props += ["AllowWidthOverride 1", f"WidthOverride {w}"]
	if h is not None:
		props += ["AllowHeightOverride 1", f"HeightOverride {h}"]
	return W("SizeLayoutWidget", name, slot or {}, props, children)


def overlay(name, children, slot=None):
	return W("OverlayWidget", name, slot or dict(FILL), [], children)


def hbox(name, children, slot=None):
	return W("HorizontalLayoutWidget", name, slot or dict(FILL), [], children)


def vbox(name, children, slot=None):
	return W("VerticalLayoutWidget", name, slot or dict(FILL), [], children)


def icon_badge(prefix, box, icon, pad="0 0 0 0"):
	"""Icono sobre un hexagono tenido: el bloque de icono de avisos y cabeceras"""
	return sized(prefix + "Size", box, box, {"VerticalAlign": 1, "Padding": pad}, [
		overlay(prefix + "Ov", [
			img(prefix + "Bg", "1 0.78 0.17 0.2", dict(FILL), "hex"),
			img(prefix + "Icon", ACCENT, {"HorizontalAlign": 1, "VerticalAlign": 1}, icon, int(box * 0.56)),
		]),
	])


def time_line(prefix):
	"""Linea fina abajo que se va vaciando (tiempo que le queda al aviso)"""
	return sized(prefix + "Size", 0, 3, {"HorizontalAlign": 0, "VerticalAlign": 2}, [img(prefix, "1 0.78 0.17 0.7")])


def build():
	os.makedirs(OUT, exist_ok=True)

	# Aviso lateral (toast): franja de color, icono, titulo y texto; se vacia una linea con el tiempo
	save("MCUIK_Toast", sized("ToastRoot", 430, None, None, [
		overlay("Ov", [
			img("Bg", PANEL),
			hbox("Row", [
				sized("StripSize", 4, None, {"VerticalAlign": 3}, [img("Strip", ACCENT)]),
				icon_badge("Badge", 46, "info", "12 12 0 12"),
				vbox("Texts", [
					text("Title", "AVISO", 14, BOLD, ACCENT, {"Padding": "0 0 0 2"}, extra=['"Horizontal Alignment" Left']),
					text("Body", "Texto del aviso", 17, REG, TEXT, rich=True, wrap=True),
				], {"SizeMode": "Fill", "VerticalAlign": 1, "Padding": "12 11 16 13"}),
			]),
			time_line("Time"),
		]),
	]))

	# Dialogo (subtitulo con quien habla): abajo en el centro
	save("MCUIK_Dialogue", sized("DialogueRoot", 860, None, None, [
		overlay("Ov", [
			img("Bg", "0.03 0.045 0.058 0.86"),
			hbox("Row", [
				sized("StripSize", 4, None, {"VerticalAlign": 3}, [img("Strip", ACCENT)]),
				icon_badge("Portrait", 64, "radio", "16 14 0 14"),
				vbox("Texts", [
					text("Speaker", "Quien habla", 17, BOLD, ACCENT, {"Padding": "0 0 0 4"}),
					text("Line", "Lo que dice", 21, REG, TEXT, rich=True, wrap=True, outline=True),
				], {"SizeMode": "Fill", "VerticalAlign": 1, "Padding": "16 12 20 14"}),
			]),
			time_line("Time"),
		]),
	]))

	# Panel con cabecera (icono + titulo + dato a la derecha) y una columna de contenido
	save("MCUIK_Panel", sized("PanelRoot", 320, None, None, [
		overlay("Ov", [
			img("Bg", PANEL),
			vbox("Col", [
				overlay("Header", [
					img("HeaderBg", PANEL_DARK),
					hbox("HeaderRow", [
						W("ImageWidget", "HeaderIcon", {"VerticalAlign": 1, "Padding": "12 0 8 0"},
							[f'Texture "{ICONS}"', 'Image "star"', f"Color {ACCENT}", "Size 18 18"]),
						text("HeaderTitle", "TITULO", 15, BOLD, ACCENT, {"SizeMode": "Fill", "VerticalAlign": 1}),
						text("HeaderRight", "", 15, BOLD, MUTED, {"VerticalAlign": 1, "Padding": "8 0 12 0"}),
					], {"HorizontalAlign": 3, "VerticalAlign": 3, "Padding": "0 7 0 7"}),
				], {"HorizontalAlign": 3}),
				sized("AccentSize", None, 2, {"HorizontalAlign": 3}, [img("Accent", "1 0.78 0.17 0.85")]),
				vbox("Content", [], {"HorizontalAlign": 3, "Padding": "12 8 12 10"}),
			], dict(FILL)),
		]),
	]))

	# Chip: icono + numero grande + etiqueta pequena
	save("MCUIK_Chip", hbox("ChipRoot", [
		W("ImageWidget", "Icon", {"VerticalAlign": 1, "Padding": "0 0 7 0"}, [f'Texture "{ICONS}"', 'Image "money"', f"Color {ACCENT}", "Size 22 22"]),
		vbox("Texts", [
			text("Value", "0", 20, BOLD, TEXT),
			text("Label", "", 12, BOLD, MUTED),
		], {"VerticalAlign": 1}),
	], {}))

	# Fila: icono, etiqueta a la izquierda y valor a la derecha
	save("MCUIK_Row", hbox("RowRoot", [
		W("ImageWidget", "Icon", {"VerticalAlign": 1, "Padding": "0 0 8 0"}, [f'Texture "{ICONS}"', 'Image "dot"', f"Color {MUTED}", "Size 16 16"]),
		text("Label", "Etiqueta", 16, REG, MUTED, {"SizeMode": "Fill", "VerticalAlign": 1}),
		text("Value", "", 16, BOLD, TEXT, {"VerticalAlign": 1, "Padding": "8 0 0 0"}),
	], {"HorizontalAlign": 3, "Padding": "0 2 0 2"}))

	# Barra de progreso: pista y relleno (el ancho del relleno se pone por codigo)
	save("MCUIK_Bar", sized("BarRoot", 200, 6, None, [
		overlay("Ov", [
			img("Track", "1 1 1 0.12"),
			sized("FillSize", 0, None, {"HorizontalAlign": 0, "VerticalAlign": 3}, [img("Fill", ACCENT)]),
		]),
	]))

	# Texto suelto con estilo del kit (para meter en paneles)
	save("MCUIK_Text", text("Text", "", 16, REG, TEXT, rich=True, wrap=True))
	save("MCUIK_Title", text("Title", "", 14, BOLD, ACCENT))
	# Separador fino
	save("MCUIK_Divider", sized("DividerRoot", None, 1, {"HorizontalAlign": 3}, [img("Line", "1 1 1 0.1")]))
	# Hueco vertical
	save("MCUIK_Spacer", sized("SpacerRoot", None, 8, {}, []))
	# Contenedores para componer: fila y columna
	save("MCUIK_HBox", W("HorizontalLayoutWidget", "HBox", {}, [], []))
	save("MCUIK_VBox", W("VerticalLayoutWidget", "VBox", {}, [], []))
	save("MCUIK_Icon", W("ImageWidget", "Icon", {}, [f'Texture "{ICONS}"', 'Image "dot"', "Color 1 1 1 1", "Size 24 24"]))


if __name__ == "__main__":
	build()
