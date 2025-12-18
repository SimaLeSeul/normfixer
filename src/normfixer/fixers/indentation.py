def fix_indentation(content: str, track=False):
    lines = content.splitlines()
    fixed = []
    changes = []

    indent_level = 0
    next_line_extra_indent = 0  # pour les if sans {}

    for lineno, line in enumerate(lines, start=1):
        stripped = line.lstrip()

        if stripped == "":
            fixed.append("")
            continue

        # Si la ligne commence par '}', on réduit avant
        if stripped.startswith("}"):
            indent_level = max(0, indent_level - 1)

        # Appliquer indentation classique + indentation spéciale
        new_line = ("\t" * (indent_level + next_line_extra_indent)) + stripped

        if new_line != line and track:
            changes.append(f"Line {lineno}: fixed indentation")

        fixed.append(new_line)

        # Reset après l'utilisation
        next_line_extra_indent = 0

        # Si ligne finit par '{' → indentation classique
        if stripped.endswith("{"):
            indent_level += 1
            continue

        # 🔥 Cas spécial : if/while/for SANS '{'
        if (
            (stripped.startswith("if ") or stripped.startswith("if(")) or
            (stripped.startswith("while ") or stripped.startswith("while(")) or
            (stripped.startswith("for ") or stripped.startswith("for("))
        ) and not stripped.endswith("{"):
            next_line_extra_indent = 1

    result = "\n".join(fixed) + "\n"
    return (result, changes) if track else result
