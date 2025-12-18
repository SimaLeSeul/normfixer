import re

def fix_function_declaration_spacing(content: str, track=False):
    """
    Corrige : int main (...) → int main(...)
    """
    lines = content.splitlines()
    changes = []
    fixed = []

    for i, line in enumerate(lines, start=1):
        if " (" in line and re.match(r'^\s*\w', line):
            new_line = line.replace(" (", "(")
            if new_line != line and track:
                changes.append(f"Line {i}: removed space before function name")
            fixed.append(new_line)
        else:
            fixed.append(line)

    return ("\n".join(fixed) + "\n", changes)
