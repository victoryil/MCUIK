# Rehace todo el kit: iconos (png + edds + imageset), layouts, metas y constantes de recursos.
# Uso: python tools/build.py
import io, os, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(T)
sys.path.insert(0, T)
import gen_icons, gen_layouts, metas, png2edds
gen_icons.main()
png2edds.write(os.path.join(ROOT, "UI/Textures/MCUIK/MCUIK_Icons.png"), os.path.join(ROOT, "UI/Textures/MCUIK/MCUIK_Icons.edds"))
gen_layouts.build()
out = io.StringIO()
old = sys.stdout
sys.stdout = out
metas.main(ROOT)
sys.stdout = old
lines = ["// Generado por tools/build.py: recursos del kit (no editar a mano)", "class MCUIK_Res", "{"]
for l in out.getvalue().splitlines():
	g, rel = l.split(" ")[0], l.split(" ")[1]
	name = os.path.splitext(os.path.basename(rel))[0].replace("MCUIK_", "").upper()
	kind = "L_" if rel.endswith(".layout") else ""
	lines.append(f'\tstatic const ResourceName {kind}{name} = "{{{g}}}{rel}";')
lines.append("}")
io.open(os.path.join(ROOT, "Scripts/Game/MCUIK/MCUIK_Res.c"), "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
print("\n".join(lines))
