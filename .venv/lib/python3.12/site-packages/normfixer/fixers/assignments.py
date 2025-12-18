import re

def fix_assignments(lines):
    fixed = []
    pattern = re.compile(r"^\s*(int|char|float|double|long)\s+([a-zA-Z_]\w*)\s*=\s*(.+);")

    for line in lines:
        match = pattern.match(line.strip())
        if match:
            type_, var, value = match.groups()
            fixed.append(f"{type_} {var};")
            fixed.append(f"{var} = {value};")
        else:
            fixed.append(line)
    return fixed
