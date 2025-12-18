import re

def fix_indentation(lines):
    fixed = []
    indent_level = 0

    for line in lines:
        stripped = line.lstrip()

        # Si ligne vide → garder vide
        if stripped == "":
            fixed.append("")
            continue

        # Réduire indentation si '}' au début
        if stripped.startswith("}"):
            indent_level = max(0, indent_level - 1)

        # Ajouter indentation correcte (4 espaces)
        new_line = " " * (indent_level * 4) + stripped
        fixed.append(new_line)

        # Augmenter indentation si '{' à la fin
        if stripped.endswith("{"):
            indent_level += 1

    return fixed
