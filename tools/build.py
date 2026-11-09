# Rehace todo el kit: iconos (png + edds + imageset), layouts, presets de ventanas, metas y constantes (MCUIK_Res.c).
# Uso: python tools/build.py
import io, os, sys

T = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(T)
sys.path.insert(0, T)
import gen_icons, gen_layouts, metas, png2edds


def run_metas():
	buf = io.StringIO()
	old = sys.stdout
	sys.stdout = buf
	metas.main(ROOT)
	sys.stdout = old
	return {l.split(" ")[1]: l.split(" ")[0] for l in buf.getvalue().splitlines() if l.strip()}


def ref(g, rel):
	return "{" + g[rel] + "}" + rel


gen_icons.main()
png2edds.write(os.path.join(ROOT, "UI/Textures/MCUIK/MCUIK_Icons.png"), os.path.join(ROOT, "UI/Textures/MCUIK/MCUIK_Icons.edds"))
gen_layouts.build()
conf = gen_layouts.build_windows()

# presets de ventanas: necesitan el GUID de sus layouts
g = run_metas()
conf = conf.replace("%LIST%", ref(g, "UI/layouts/MCUIK/MCUIK_ListContent.layout"))
conf = conf.replace("%EVENT%", ref(g, "UI/layouts/MCUIK/MCUIK_EventContent.layout"))
os.makedirs(os.path.join(ROOT, "Configs", "MCUIK"), exist_ok=True)
io.open(os.path.join(ROOT, "Configs", "MCUIK", "MCUIK_Dialogs.conf"), "w", encoding="utf-8", newline="\n").write(conf)

g = run_metas()
lines = ["// Generado por tools/build.py: recursos del kit (no editar a mano)", "class MCUIK_Res", "{"]
for rel in sorted(g):
	name = os.path.splitext(os.path.basename(rel))[0].replace("MCUIK_", "").upper()
	kind = "L_" if rel.endswith(".layout") else ("C_" if rel.endswith(".conf") else "")
	lines.append(f'\tstatic const ResourceName {kind}{name} = "{ref(g, rel)}";')
lines.append("}")
io.open(os.path.join(ROOT, "Scripts/Game/MCUIK/MCUIK_Res.c"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
