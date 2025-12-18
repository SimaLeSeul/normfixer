from normfixer.fixers.preprocessor import fix_preprocessor
from normfixer.fixers.indentation import fix_indentation
from normfixer.fixers.assignments import fix_assignments
from normfixer.fixers.operators import fix_operators
from normfixer.fixers.empty_lines import fix_empty_lines

def apply_all_fixes(content):
    """Applique tous les fixers dans l'ordre correct"""
    lines = content.splitlines(keepends=True)
    
    # 1. Préprocesseur (ajoute newlines après #include)
    lines = fix_preprocessor(lines)
    
    # 2. Séparation déclarations/assignations
    lines = fix_assignments(lines)
    
    # 3. Indentation (remplace espaces par tabs)
    lines = fix_indentation(lines)
    
    # 4. Opérateurs
    lines = fix_operators(lines)
    
    # 5. Lignes vides dans fonctions
    lines = fix_empty_lines(lines)
    
    return ''.join(lines)
