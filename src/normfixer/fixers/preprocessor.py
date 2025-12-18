import re

def fix_preprocessor(lines):
    """
    Ajoute une ligne vide après les directives préprocesseur
    (NL_AFTER_PREPROC)
    """
    fixed = []
    last_was_preprocessor = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Si c'est une directive préprocesseur
        if stripped.startswith("#"):
            fixed.append(line)
            last_was_preprocessor = True
        else:
            # Si la ligne précédente était un préprocesseur et que cette ligne n'est pas vide
            if last_was_preprocessor and stripped:
                # Ajouter une ligne vide
                fixed.append("\n")
            
            fixed.append(line)
            last_was_preprocessor = False
    
    return fixed
