import re

def fix_indentation(lines):
    """
    Fixe l'indentation à 1 TAB par niveau (norme 42)
    Remplace TOUS les espaces d'indentation par des TABs
    """
    fixed = []
    indent_level = 0
    next_line_extra_indent = False

    for i, line in enumerate(lines):
        # Préserver les lignes vides et préprocesseur
        if line.strip() == "":
            fixed.append("\n")
            continue
        
        if line.strip().startswith("#"):
            fixed.append(line)
            continue

        # Extraire contenu sans indentation
        stripped = line.strip()

        # Si la ligne précédente demandait une indentation temporaire
        if next_line_extra_indent:
            indented_line = ("\t" * (indent_level + 1)) + stripped
            next_line_extra_indent = False
        else:
            # Diminuer indentation AVANT si ligne commence par '}'
            if stripped.startswith("}"):
                indent_level = max(0, indent_level - 1)
            
            # Appliquer l'indentation avec TAB
            indented_line = ("\t" * indent_level) + stripped

        # Assurer le newline
        if not indented_line.endswith("\n"):
            indented_line += "\n"
        
        fixed.append(indented_line)

        # Augmenter indentation APRÈS si ligne se termine par '{'
        if stripped.endswith("{"):
            indent_level += 1
        # Détecter if/while/for/else sans accolades
        elif re.match(r'^(if|while|for|else(\s+if)?)\s*[\(]', stripped):
            if not stripped.endswith("{") and not stripped.endswith(";"):
                if i + 1 < len(lines):
                    next_stripped = lines[i + 1].strip()
                    if next_stripped and not next_stripped.startswith("{"):
                        next_line_extra_indent = True

    return fixed
