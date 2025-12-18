import re

def fix_declaration_assign(lines):
    fixed = []
    pattern = re.compile(r"^(.*\b(?:int|char|float|double|long|short)\b\s+\w+)\s*=\s*(.+);$")

    for line in lines:
        stripped = line.strip()
        match = pattern.match(stripped)
        if match:
            before, value = match.groups()
            line = f"{before} = {value};"
        fixed.append(line)
    return fixed
