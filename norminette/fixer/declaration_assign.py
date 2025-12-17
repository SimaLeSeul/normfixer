import re

DECL_ASSIGN_RE = re.compile(
    r'^\s*(int|char|float|double|long|short|unsigned|size_t|const\s+\w+)\s+(\**\w+)\s*=\s*(.+);$'
)

def extract_function_params(content):
    params = set()

    # capture ligne prototype: int func(type a, type b, ...)
    proto_re = re.compile(r'\w+\s+\w+\s*\(([^)]*)\)')
    match = proto_re.search(content)
    if not match:
        return params

    param_str = match.group(1)
    if not param_str.strip():
        return params

    for p in param_str.split(','):
        parts = p.strip().split()
        name = parts[-1] if parts else None
        if name:
            params.add(name.strip('*'))  # enlève les *
    return params

def fix_decl_assign(content: str, track=False):
    params = extract_function_params(content)   # 🔥 nouveau

    fixed = []
    changes = []
    decl_lines = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        stripped = line.strip()

        match = DECL_ASSIGN_RE.match(stripped)
        if match:
            ctype = match.group(1)
            varname = match.group(2).lstrip('*')

            # 🔥 NE PAS SPLITTER si c'est un paramètre
            if varname in params:
                fixed.append(line)
                continue

            value = match.group(3)

            fixed.append(f"{ctype} {varname};")
            fixed.append(f"{varname} = {value};")

            decl_lines.append(len(fixed)-2)

            if track:
                changes.append(f"Line {lineno}: split declaration + assignment")
        else:
            fixed.append(line)

    result = "\n".join(fixed) + "\n"
    return (result, changes, decl_lines) if track else result
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
