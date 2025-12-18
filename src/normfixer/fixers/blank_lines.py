def fix_blank_lines(lines):
    """
    Gère les lignes vides : une seule après #include
    """
    result = []
    prev_was_include = False
    
    for line in lines:
        stripped = line.strip()
        
        # Ligne vide après #include
        if stripped.startswith('#include'):
            result.append(line)
            prev_was_include = True
            continue
        
        # Ajouter UNE SEULE ligne vide après includes
        if prev_was_include and stripped and not stripped.startswith('#'):
            result.append('\n')
            prev_was_include = False
        
        result.append(line)
    
    return result
