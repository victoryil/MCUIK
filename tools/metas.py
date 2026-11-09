# Crea el .meta de los recursos que no lo tienen (layouts, imagesets, configs, prefabs).
# El GUID sale del nombre del archivo (estable): asi el mismo archivo siempre tiene el mismo GUID.
# Uso: python tools/metas.py <carpeta del proyecto>   -> imprime "GUID ruta" de cada recurso
import hashlib, io, os, re, sys

KINDS = {".layout": "LayoutResourceClass", ".imageset": "ImageSetResourceClass", ".conf": "CONFResourceClass",
	".et": "EntityPrefabResourceClass", ".styles": "StylesResourceClass"}
PLATFORMS = ["XBOX_ONE", "XBOX_SERIES", "PS4", "PS5", "HEADLESS"]


def guid_for(rel):
	return hashlib.sha1(("MCUIK:" + rel).encode()).hexdigest()[:16].upper()


def main(root):
	for dp, dn, fn in os.walk(root):
		if ".git" in dp or "tools" in dp:
			continue
		for f in fn:
			ext = os.path.splitext(f)[1]
			if ext not in KINDS:
				continue
			p = os.path.join(dp, f)
			rel = os.path.relpath(p, root).replace("\\", "/")
			meta = p + ".meta"
			if os.path.exists(meta):
				g = re.search(r'Name "\{([0-9A-F]{16})\}', io.open(meta, encoding="utf-8").read()).group(1)
				print(g, rel)
				continue
			g = guid_for(rel)
			k = KINDS[ext]
			lines = ["MetaFileClass {", f' Name "{{{g}}}{rel}"', " Configurations {", f"  {k} PC {{", "  }"]
			for pl in PLATFORMS:
				lines += [f"  {k} {pl} : PC {{", "  }"]
			lines += [" }", "}"]
			io.open(meta, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
			print(g, rel, "(nuevo)")


if __name__ == "__main__":
	main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
