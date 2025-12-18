import re

def fix_indentation(lines):
    """
    Convertit les espaces en tabulations pour l'indentation
    Gère l'indentation après les accolades ouvrantes
    """
    result = []
    indent_level = 0
    
    for line in lines:
        stripped = line.lstrip()
        
        # Ignorer les lignes vides et commentaires
        if not stripped or stripped.startswith(('/*', '*', '//')):
            result.append(line)
            continue
        
        # Gérer les accolades fermantes
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Appliquer l'indentation avec des tabs
        if stripped:
            indented_line = '\t' * indent_level + stripped
            result.append(indented_line)
        else:
            result.append(line)
        
        # Gérer les accolades ouvrantes
        if stripped.rstrip().endswith('{'):
            indent_level += 1
    
    return result