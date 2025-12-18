from normfixer.fixers.spaces import fix_spacing
from normfixer.fixers.declarations import fix_declarations
from normfixer.fixers.blank_lines import fix_blank_lines

def apply_all_fixes(lines):
    """
    Applique toutes les corrections dans l'ordre approprié
    """
    # 1. Normaliser les espaces et opérateurs
    lines = fix_spacing(lines)
    
    # 2. Séparer déclarations et assignations
    lines = fix_declarations(lines)
    
    # 3. Gérer les lignes vides
    lines = fix_blank_lines(lines)
    
    # 4. Convertir espaces en tabs partout
    lines = convert_all_spaces_to_tabs(lines)
    
    return ''.join(lines)


def convert_all_spaces_to_tabs(lines):
    """
    Convertit TOUS les espaces d'indentation en tabs
    """
    result = []
    for line in lines:
        if not line.strip():
            result.append(line)
            continue
        
        # Compter espaces au début
        spaces = len(line) - len(line.lstrip())
        
        if spaces > 0:
            # 4 espaces = 1 tab (ou 8 selon ton école)
            tabs = '\t' * (spaces // 4)
            remaining = ' ' * (spaces % 4)
            
            # Si remaining > 0, convertir aussi en tab
            if remaining:
                tabs += '\t'
            
            result.append(tabs + line.lstrip())
        else:
            result.append(line)
    
    return result
