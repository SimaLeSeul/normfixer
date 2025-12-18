import re

def extract_function_params(content):
    params = set()

    # match: return_type name(type a, type *b, ...)
    proto = re.search(r'\w[\w\s\*]*\s+\w+\s*\(([^)]*)\)', content)
    if not proto:
        return params

    raw = proto.group(1).strip()
    if not raw:
        return params

    for p in raw.split(','):
        p = p.strip()
        if not p:
            continue

        # dernier élément = nom du paramètre
        name = p.split()[-1].lstrip('*')
        params.add(name)

    return params


DECL_ASSIGN_RE = re.compile(
    r'^\s*(int|char|float|double|long|short|unsigned|size_t|const\s+\w+)\s+(\**\w+)\s*=\s*(.+);$'
)


def fix_declaration_assign(lines, track=False):
    content = "".join(lines)
    params = extract_function_params(content)

    fixed = []
    changes = []
    decl_lines = []

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()

        m = DECL_ASSIGN_RE.match(stripped)
        if not m:
            # 🔥 Toujours garantir un \n
            if not line.endswith("\n"):
                fixed.append(line + "\n")
            else:
                fixed.append(line)
            continue

        ctype = m.group(1)
        varname = m.group(2).lstrip('*')
        value = m.group(3)

        if varname in params:
            fixed.append(f"{varname} = {value};\n")
            if track:
                changes.append(
                    f"Line {lineno}: removed illegal redeclaration of parameter '{varname}'"
                )
            continue

        fixed.append(f"{ctype} {varname};\n")
        fixed.append(f"{varname} = {value};\n")

        decl_lines.append(len(fixed) - 2)

        if track:
            changes.append(f"Line {lineno}: split declaration + assignment")

    return fixed

def add_empty_line_after_declarations(lines, decl_lines, track=False):
    fixed = []
    changes = []

    last_decl = max(decl_lines) if decl_lines else -1

    for i, line in enumerate(lines):
        fixed.append(line)

        # ajoute une ligne vide après la dernière déclaration
        if i == last_decl:
            if i + 1 < len(lines) and lines[i+1].strip() != "":
                fixed.append("\n")
                if track:
                    changes.append(f"Inserted empty line after declarations (line {i+2})")

    return fixed if not track else (fixed, changes)
