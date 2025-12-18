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

def fix_decl_assign(content, track=False):
    params = extract_function_params(content)

    fixed = []
    changes = []
    decl_lines = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        m = DECL_ASSIGN_RE.match(stripped)
        if not m:
            fixed.append(line)
            continue

        ctype = m.group(1)
        varname = m.group(2).lstrip('*')
        value = m.group(3)

        # 🔥 SI C’EST UN PARAMÈTRE → NE PAS SPLITTER
        if varname in params:
            # On remplace uniquement "type" par rien
            fixed.append(f"{varname} = {value};")
            if track:
                changes.append(f"Line {lineno}: removed illegal redeclaration of parameter '{varname}'")
            continue

        # Split normal pour une vraie déclaration
        fixed.append(f"{ctype} {varname};")
        fixed.append(f"{varname} = {value};")

        decl_lines.append(len(fixed)-2)

        if track:
            changes.append(f"Line {lineno}: split declaration + assignment")

    result = "\n".join(fixed) + "\n"
    return (result, changes, decl_lines)

def add_empty_line_after_declarations(content: str, decl_lines, track=False):
    lines = content.splitlines()
    fixed = []
    changes = []

    last_decl = -1

    # trouve la dernière déclaration
    for d in decl_lines:
        if d > last_decl:
            last_decl = d

    for i, line in enumerate(lines):
        fixed.append(line)

        # si on est à la fin des déclarations
        if i == last_decl:
            # si la ligne suivante n'est PAS vide
            if i + 1 < len(lines) and lines[i+1].strip() != "":
                fixed.append("")  # ajoute une ligne vide
                if track:
                    changes.append(f"Inserted empty line after declarations (line {i+1})")

    result = "\n".join(fixed) + "\n"
    return (result, changes) if track else result
