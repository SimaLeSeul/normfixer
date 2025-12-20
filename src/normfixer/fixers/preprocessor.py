def fix_preprocessor(lines):
    """Ajoute une ligne vide après les directives préprocesseur"""
    fixed = []
    last_was_preprocessor = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("#"):
            fixed.append(line)
            last_was_preprocessor = True
        else:
            if last_was_preprocessor and stripped:
                fixed.append("")  # ✅ Ligne vide (pas \n)
            
            fixed.append(line)
            last_was_preprocessor = False
    
    return fixed
