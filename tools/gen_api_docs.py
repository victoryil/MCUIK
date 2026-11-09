# Genera la referencia de la API (Markdown) a partir del codigo Enforce Script del mod.
# Lee clases, metodos publicos y sus comentarios "//!" que van justo encima.
# Uso: python tools/gen_api_docs.py <carpeta Scripts> <salida.md> "<titulo>"
import io, os, re, sys

CLASS_RE = re.compile(r"^(?:modded\s+)?class\s+(\w+)(?:\s*:\s*(\w+))?")
METHOD_RE = re.compile(r"^\s+((?:static\s+|override\s+|protected\s+|private\s+)*)([\w<>, ]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:\{.*)?$")
CONST_RE = re.compile(r"^\s+static\s+const\s+(\w+)\s+(\w+)\s*=\s*(.+);")
SKIP = {"if", "for", "while", "switch", "foreach", "return", "else"}


def parse(path):
	lines = io.open(path, encoding="utf-8").read().splitlines()
	header = []
	for l in lines:
		if l.startswith("//"):
			header.append(l.lstrip("/ ").rstrip())
		else:
			break
	classes = []
	cur = None
	doc = []
	depth = 0
	for l in lines:
		s = l.strip()
		m = CLASS_RE.match(l)
		if m and depth == 0:
			cur = {"name": m.group(1), "base": m.group(2), "doc": doc, "methods": [], "consts": [], "modded": l.startswith("modded")}
			classes.append(cur)
			doc = []
		elif cur and depth == 1:
			if s.startswith("//!"):
				doc.append(s[3:].strip())
			elif s.startswith("[") or s.startswith("//"):
				pass
			else:
				c = CONST_RE.match(l)
				mm = METHOD_RE.match(l)
				if c:
					cur["consts"].append((c.group(1), c.group(2), c.group(3), list(doc)))
				elif mm and mm.group(3) not in SKIP and "protected" not in mm.group(1) and "private" not in mm.group(1) and not mm.group(3).startswith("Rpc") and "Rpc" not in mm.group(3):
					cur["methods"].append({"mods": mm.group(1).strip(), "ret": mm.group(2).strip(), "name": mm.group(3), "args": mm.group(4).strip(), "doc": list(doc)})
				if s:
					doc = []
		elif depth == 0 and s.startswith("//!"):
			doc.append(s[3:].strip())
		depth += l.count("{") - l.count("}")
		if depth == 0 and s == "}":
			cur = None
	return header, classes


def main(scripts, out, title):
	md = ["---", f"title: Referencia de la API", "nav_order: 90", "---", "", f"# {title}", "", "> Generado automáticamente desde el código (`tools/gen_api_docs.py`). No editar a mano.", ""]
	for dp, dn, fn in sorted(os.walk(scripts)):
		for f in sorted(fn):
			if not f.endswith(".c"):
				continue
			header, classes = parse(os.path.join(dp, f))
			if not classes:
				continue
			md += [f"## {f}", ""]
			if header:
				md += ["> " + h for h in header if h] + [""]
			for c in classes:
				base = f" : `{c['base']}`" if c["base"] else ""
				mod = " *(modded)*" if c["modded"] else ""
				md += [f"### `{c['name']}`{base}{mod}", ""]
				if c["doc"]:
					md += [" ".join(c["doc"]), ""]
				if c["consts"] and len(c["consts"]) <= 80:
					md += ["| Constante | Tipo | Valor |", "|---|---|---|"]
					for t, n, v, d in c["consts"]:
						v = v.replace("|", "\\|")
						md.append(f"| `{n}` | `{t}` | `{v}` |")
					md.append("")
				for m in c["methods"]:
					sig = f"{m['mods']} {m['ret']} {m['name']}({m['args']})".strip()
					md.append(f"- `{sig}`")
					if m["doc"]:
						md.append(f"  — {' '.join(m['doc'])}")
				md.append("")
	os.makedirs(os.path.dirname(out), exist_ok=True)
	io.open(out, "w", encoding="utf-8", newline="\n").write("\n".join(md) + "\n")
	print("api ->", out)


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])
