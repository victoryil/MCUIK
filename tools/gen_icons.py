# Genera el atlas de iconos de MCUIK (dibujados aqui en SVG, propios).
#   UI/Textures/MCUIK/MCUIK_Icons.png      atlas 1024x1024, celdas de 128 px, iconos blancos (se tinen por codigo)
#   UI/Textures/MCUIK/MCUIK_Icons.imageset  definicion de cada icono por nombre
#   Scripts/Game/MCUIK/MCUIK_IconNames.c   constantes con los nombres
#   tools/icons_preview.png            hoja de muestra para revisarlos a ojo
# Uso: python tools/gen_icons.py
import io, os, resvg_py
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CELL = 128
COLS = 8
S = 'fill="none" stroke="#fff" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
F = 'fill="#fff"'

# viewBox 0 0 24 24. Trazo redondeado de 1.9; los rellenos se usan para dar peso.
ICONS = {
	# ---- recursos
	"money": f'<circle cx="12" cy="12" r="9.2" {S}/><path d="M15.6 8.4a4.6 4.6 0 1 0 0 7.2" {S}/><path d="M7.2 10.8h6M7.2 13.4h6" {S}/>',
	"materials": f'<path d="M3.5 7.5 12 3.5l8.5 4v9L12 20.5l-8.5-4z" {S}/><path d="M3.5 7.5 12 11.5l8.5-4M12 11.5v9" {S}/><path d="m7.8 5.5 8.4 4" {S}/>',
	"support": f'<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z" {S}/>',
	"recruit": f'<circle cx="9.5" cy="8" r="3.6" {S}/><path d="M3 20c.6-3.6 3.2-5.6 6.5-5.6s5.9 2 6.5 5.6" {S}/><path d="M19 8v6M16 11h6" {S}/>',
	"people": f'<circle cx="8" cy="8.5" r="3.2" {S}/><circle cx="16.5" cy="9.5" r="2.6" {S}/><path d="M2.5 19.5c.5-3.3 2.7-5 5.5-5s5 1.7 5.5 5" {S}/><path d="M14.5 14.6c.6-.2 1.3-.3 2-.3 2.4 0 4.2 1.5 4.7 4.4" {S}/>',
	"zone": f'<path d="M5 21V3.8" {S}/><path d="M5 4.5c4-2 6.5 1.8 10.5 0l3.5-1v9l-3.5 1c-4 1.8-6.5-2-10.5 0" {S}/>',
	"time": f'<circle cx="12" cy="12" r="9" {S}/><path d="M12 7v5l3.2 2.2" {S}/>',
	"star": f'<path d="m12 3 2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8l-5.4 2.9 1.1-6.1-4.5-4.2 6.1-.8z" {S}/>',
	# ---- misiones e historia
	"objective": f'<circle cx="12" cy="12" r="8" {S}/><circle cx="12" cy="12" r="3.2" {S}/><path d="M12 1.8v4M12 18.2v4M1.8 12h4M18.2 12h4" {S}/>',
	"radio": f'<rect x="4" y="8" width="16" height="12.5" rx="2" {S}/><path d="M7 8 16.5 3" {S}/><circle cx="15.2" cy="14.2" r="2.6" {S}/><path d="M7.2 12h3M7.2 15h3M7.2 18h3" {S}/>',
	"journal": f'<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5z" {S}/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19v-3" {S}/><path d="M9 7.5h6M9 11h4" {S}/>',
	"intel": f'<path d="M3.5 6.5a1.5 1.5 0 0 1 1.5-1.5h4.2l2 2.2H19a1.5 1.5 0 0 1 1.5 1.5v9.3A1.5 1.5 0 0 1 19 19.5H5a1.5 1.5 0 0 1-1.5-1.5z" {S}/><path d="M8 13h8M8 16h5" {S}/>',
	"phone": f'<path d="M6.6 3.5h2.6l1.4 4.1-2 1.3a10.5 10.5 0 0 0 6.5 6.5l1.3-2 4.1 1.4v2.6a2 2 0 0 1-2.2 2A16.6 16.6 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2z" {S}/>',
	"chat": f'<path d="M4 5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5v9a1.5 1.5 0 0 1-1.5 1.5H10l-4.5 4V16h0A1.5 1.5 0 0 1 4 14.5z" {S}/><path d="M8 9h8M8 12h5" {S}/>',
	"map": f'<path d="m3.5 6 5.5-2.5 6 2.5 5.5-2.5v14.5L15 20.5 9 18l-5.5 2.5z" {S}/><path d="M9 3.5V18M15 6v14.5" {S}/>',
	"pin": f'<path d="M12 21.5s6.5-6.2 6.5-11.4a6.5 6.5 0 0 0-13 0c0 5.2 6.5 11.4 6.5 11.4z" {S}/><circle cx="12" cy="10" r="2.4" {S}/>',
	# ---- servicios
	"shop": f'<path d="M3 4h2.6l2.1 10.6a1.5 1.5 0 0 0 1.5 1.2h8.3a1.5 1.5 0 0 0 1.5-1.1L20.8 8H6.4" {S}/><circle cx="9.5" cy="19.8" r="1.4" {F}/><circle cx="17" cy="19.8" r="1.4" {F}/>',
	"garage": f'<path d="M5.5 15.5h13M4.5 15.5v-3l2-4.8A1.5 1.5 0 0 1 7.9 6.8h8.2a1.5 1.5 0 0 1 1.4.9l2 4.8v3" {S}/><path d="M4.5 15.5v2.3M19.5 15.5v2.3M4.5 12.5h15" {S}/><circle cx="8" cy="14" r=".9" {F}/><circle cx="16" cy="14" r=".9" {F}/>',
	"vehicle": f'<path d="M2.5 16.5V7.5A1.5 1.5 0 0 1 4 6h9.5v10.5" {S}/><path d="M13.5 9.5h4l3.5 3.8v3.2h-2" {S}/><circle cx="7" cy="17.5" r="2" {S}/><circle cx="16.5" cy="17.5" r="2" {S}/><path d="M9 17.5h5.5" {S}/>',
	"weapon": f'<path d="M1.8 9.5h13.7l1.5-1.3h5.2v2.6l-4.2.9-.9 1.6h-3.4l-1.1 2.2-1.6 3.6H7.4l1.5-4.6-2.3-1.2H1.8z" {S}/><path d="M11.8 13.2l-.6 2" {S}/>',
	"ammo": f'<path d="M6 21V10.5c0-2.5 1-5 2.2-6.5 1.2 1.5 2.2 4 2.2 6.5V21zM13.6 21V10.5c0-2.5 1-5 2.2-6.5 1.2 1.5 2.2 4 2.2 6.5V21z" {S}/><path d="M6 17.5h4.4M13.6 17.5H18" {S}/>',
	"medical": f'<rect x="3.5" y="3.5" width="17" height="17" rx="3" {S}/><path d="M12 7.5v9M7.5 12h9" stroke="#fff" stroke-width="3" stroke-linecap="round"/>',
	"explosive": f'<circle cx="10.5" cy="14" r="6.5" {S}/><path d="M15 9.5l2-2M17.5 4.5l.8-1.5M20 7l1.5-.6M19.5 4.8" {S}/><path d="M7.5 13a3 3 0 0 1 3-3" {S}/>',
	"clothing": f'<path d="M8.5 3.5 4 6l-1.5 4.5 3 1.2L7 10v10.5h10V10l1.5 1.7 3-1.2L20 6l-4.5-2.5c-.4 1.5-1.8 2.5-3.5 2.5s-3.1-1-3.5-2.5z" {S}/>',
	"tool": f'<path d="M14.5 4.2a5 5 0 0 0-5.8 6.6L3.5 16a2.1 2.1 0 0 0 3 3l5.2-5.2a5 5 0 0 0 6.6-5.8l-3 3-3-.6-.6-3z" {S}/>',
	"build": f'<path d="M3 21h18M5 21V10l7-5 7 5v11" {S}/><path d="M9.5 21v-6h5v6" {S}/>',
	"storage": f'<rect x="4" y="3" width="16" height="18" rx="1.5" {S}/><path d="M12 3v18M9.5 11v2M14.5 11v2" {S}/>',
	# ---- incognito
	"cover_civil": f'<circle cx="12" cy="7.5" r="3.6" {S}/><path d="M4.5 21c.6-4.2 3.5-6.8 7.5-6.8s6.9 2.6 7.5 6.8" {S}/><path d="M7.5 5.2c1.2-1.9 7.8-1.9 9 0" {S}/>',
	"cover_military": f'<path d="M3.5 15.5c0-5 3.8-9 8.5-9s8.5 4 8.5 9z" {S}/><path d="M2 15.5h20M8 10.5c1-1 2.5-1.6 4-1.6" {S}/><path d="M6 18.5h12" {S}/>',
	"cover_watched": f'<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z" {S}/><circle cx="12" cy="12" r="3.2" {S}/><circle cx="12" cy="12" r="1.2" {F}/>',
	"cover_hidden": f'<path d="M3.5 3.5l17 17" {S}/><path d="M9.6 5.8A9.5 9.5 0 0 1 12 5.5c6.4 0 10 6.5 10 6.5a17 17 0 0 1-2.7 3.4M14.1 14.3a3.2 3.2 0 0 1-4.4-4.4M6.4 7.6A16.6 16.6 0 0 0 2 12s3.6 6.5 10 6.5a9.6 9.6 0 0 0 4.3-1" {S}/>',
	"cover_disguised": f'<path d="M3 7.5c3-1.8 6-1.8 9 0 3-1.8 6-1.8 9 0v3c0 4-2.5 6.5-5 6.5-1.5 0-3-1.5-4-3-1 1.5-2.5 3-4 3-2.5 0-5-2.5-5-6.5z" {S}/><path d="M6.5 11h3M14.5 11h3" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
	"alert": f'<path d="M12 3.2 2.5 20h19z" {S}/><path d="M12 9.5v5" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="17.3" r="1.2" {F}/>',
	"threat": f'<path d="M12 3c-4.6 0-8 3.2-8 7.6 0 2.6 1.2 4.3 3 5.4V19a1.5 1.5 0 0 0 1.5 1.5h7A1.5 1.5 0 0 0 17 19v-3c1.8-1.1 3-2.8 3-5.4C20 6.2 16.6 3 12 3z" {S}/><circle cx="9" cy="11" r="1.8" {F}/><circle cx="15" cy="11" r="1.8" {F}/><path d="M10.5 20.5v-2.5M13.5 20.5v-2.5" {S}/>',
	# ---- tipos de zona
	"town": f'<path d="M3 21V11l5-4 5 4v10M13 21V8.5l4-3 4 3V21M2 21h20" {S}/><path d="M6.5 21v-4h3v4M16 12h2M16 15.5h2" {S}/>',
	"base": f'<path d="M4 21V8h3v2.5h3V8h4v2.5h3V8h3v13z" {S}/><path d="M10 21v-5a2 2 0 0 1 4 0v5" {S}/><path d="M12 8V3l3.5 1.5L12 6" {S}/>',
	"outpost": f'<path d="M6 21 8 9h8l2 12M8 9 7 5h10l-1 4M12 5V2.5" {S}/><path d="M7.3 15h9.4M9 21l3-6 3 6" {S}/>',
	"airfield": f'<path d="M12 2.8c.9 0 1.5.8 1.5 1.8v5l7.5 4.5v2l-7.5-2.3v4.2l2.3 1.8v1.7L12 20.4l-3.8 1.1v-1.7l2.3-1.8v-4.2L3 16.1v-2l7.5-4.5v-5c0-1 .6-1.8 1.5-1.8z" {S}/>',
	"port": f'<circle cx="12" cy="5" r="2" {S}/><path d="M12 7v14M8 10.5h8" {S}/><path d="M4 13.5c0 4.2 3.6 7.5 8 7.5s8-3.3 8-7.5M4 13.5l-1.5 1.5M20 13.5l1.5 1.5" {S}/>',
	"factory": f'<path d="M2.5 21V11l5 3V11l5 3V11l5 3V4h3.5v17z" {S}/><path d="M6.5 17.5h2M11.5 17.5h2" {S}/>',
	"resource": f'<path d="M4 20.5 13.5 11" {S}/><path d="M7.5 6c4.5-3.2 9.8-3 13.5.5-3.5-.8-6.3-.3-8.5 1.5-2-1.5-3.3-1.9-5-2z" {S}/><path d="m12.5 8 3.5 3.5" {S}/>',
	"camp": f'<path d="M2.5 20h19M5 20l7-14 7 14" {S}/><path d="M12 20l-2.5-5h5z" {S}/><path d="M12 6V3" {S}/>',
	# ---- facciones
	"faction_spain": f'<path d="M12 2.8 4.5 5.5v6c0 4.5 3.2 8.4 7.5 9.7 4.3-1.3 7.5-5.2 7.5-9.7v-6z" {S}/><path d="M5 10h14M5.6 14.5h12.8" {S}/>',
	"faction_trumpet": f'<path d="M12 2.8 4.5 5.5v6c0 4.5 3.2 8.4 7.5 9.7 4.3-1.3 7.5-5.2 7.5-9.7v-6z" {S}/><path d="m12 7.5 1.3 2.8 3 .4-2.2 2 .6 3-2.7-1.5-2.7 1.5.6-3-2.2-2 3-.4z" {F}/>',
	"faction_putoncin": f'<path d="M12 2.8 4.5 5.5v6c0 4.5 3.2 8.4 7.5 9.7 4.3-1.3 7.5-5.2 7.5-9.7v-6z" {S}/><circle cx="9" cy="8.6" r="1.6" {F}/><circle cx="15" cy="8.6" r="1.6" {F}/><path d="M8 13c0-2 1.8-3.4 4-3.4s4 1.4 4 3.4-1.8 3.5-4 3.5-4-1.5-4-3.5z" {F}/>',
	"faction_civil": f'<path d="M12 2.8 4.5 5.5v6c0 4.5 3.2 8.4 7.5 9.7 4.3-1.3 7.5-5.2 7.5-9.7v-6z" {S}/><circle cx="12" cy="10" r="2.4" {S}/><path d="M8 16.5c.6-1.8 2.1-2.8 4-2.8s3.4 1 4 2.8" {S}/>',
	# ---- controles
	"check": f'<path d="m4.5 12.5 4.8 4.8L19.5 7" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
	"close": f'<path d="M6 6l12 12M18 6 6 18" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
	"plus": f'<path d="M12 5v14M5 12h14" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
	"minus": f'<path d="M5 12h14" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round"/>',
	"arrow": f'<path d="M5 12h13M13 6.5l5.5 5.5-5.5 5.5" stroke="#fff" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
	"chevron": f'<path d="m9 5.5 6.5 6.5L9 18.5" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
	"info": f'<circle cx="12" cy="12" r="9" {S}/><path d="M12 11v6" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="7.6" r="1.25" {F}/>',
	"lock": f'<rect x="4.5" y="10.5" width="15" height="10.5" rx="2" {S}/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" {S}/><circle cx="12" cy="15.7" r="1.4" {F}/>',
	"key": f'<circle cx="7.5" cy="15.5" r="4" {S}/><path d="m10.5 12.5 9-9M16 7l2.5 2.5M18.5 4.5 21 7" {S}/>',
	"night": f'<path d="M19.5 14.8A8 8 0 0 1 9.2 4.5 8 8 0 1 0 19.5 14.8z" {S}/>',
	# ---- formas para fondos
	"dot": f'<circle cx="12" cy="12" r="5" {F}/>',
	"ring": f'<circle cx="12" cy="12" r="8.5" fill="none" stroke="#fff" stroke-width="2.6"/>',
	"diamond": f'<path d="M12 2.5 21.5 12 12 21.5 2.5 12z" {F}/>',
	"hex": f'<path d="M12 2.2 20.5 7v10L12 21.8 3.5 17V7z" {F}/>',
}


def render(svg_inner, size):
	svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24">{svg_inner}</svg>'
	png = bytes(resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size))
	return Image.open(io.BytesIO(png)).convert("RGBA")


def main():
	names = list(ICONS.keys())
	rows = (len(names) + COLS - 1) // COLS
	atlas = Image.new("RGBA", (COLS * CELL, COLS * CELL), (255, 255, 255, 0))
	assert rows <= COLS, "no caben"
	pad = 8
	for i, n in enumerate(names):
		img = render(ICONS[n], CELL - 2 * pad)
		x, y = (i % COLS) * CELL, (i // COLS) * CELL
		atlas.alpha_composite(img, (x + pad, y + pad))
	# blanco puro en RGB para que al tenir salga el color exacto
	px = atlas.load()
	for yy in range(atlas.size[1]):
		for xx in range(atlas.size[0]):
			a = px[xx, yy][3]
			px[xx, yy] = (255, 255, 255, a)
	tex = os.path.join(ROOT, "UI", "Textures", "MCUIK")
	atlas.save(os.path.join(tex, "MCUIK_Icons.png"))

	# imageset
	lines = ["ImageSetClass {", f" RefSize {COLS * CELL} {COLS * CELL}", ' Textures {', '  ImageSetTextureClass {', '   mpix 1', '   path "{3A51A29D8F0C7E21}UI/Textures/MCUIK/MCUIK_Icons.edds"', '  }', ' }', ' Images {']
	for i, n in enumerate(names):
		x, y = (i % COLS) * CELL, (i // COLS) * CELL
		lines += [f'  ImageSetDefClass {n} {{', f'   Name "{n}"', f'   Pos {x} {y}', f'   Size {CELL} {CELL}', '   Flags 0', '  }']
	lines += [' }', '}']
	io.open(os.path.join(tex, "MCUIK_Icons.imageset"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")

	# constantes
	c = ["// Generado por tools/gen_icons.py: nombres de los iconos del atlas de MCUIK", "class MCUIK_Icon", "{"]
	for n in names:
		c.append(f'\tstatic const string {n.upper()} = "{n}";')
	c.append("}")
	io.open(os.path.join(ROOT, "Scripts", "Game", "MCUIK", "MCUIK_IconNames.c"), "w", encoding="utf-8", newline="\n").write("\n".join(c) + "\n")

	# hoja de muestra: cada icono tenido sobre el fondo del tema
	cw, ch = 150, 150
	sheet = Image.new("RGBA", (COLS * cw, rows * ch), (14, 20, 25, 255))
	d = ImageDraw.Draw(sheet)
	tints = [(255, 199, 44), (232, 237, 240), (46, 139, 255), (255, 77, 61), (61, 220, 132)]
	for i, n in enumerate(names):
		img = render(ICONS[n], 72)
		col = tints[i % len(tints)]
		r, g, b, a = img.split()
		tinted = Image.merge("RGBA", (r.point(lambda v: col[0]), g.point(lambda v: col[1]), b.point(lambda v: col[2]), a))
		x, y = (i % COLS) * cw, (i // COLS) * ch
		sheet.alpha_composite(tinted, (x + 39, y + 22))
		d.text((x + 8, y + 112), n, fill=(143, 161, 173, 255))
	sheet.save(os.path.join(ROOT, "tools", "icons_preview.png"))
	print(len(names), "iconos")


if __name__ == "__main__":
	main()
