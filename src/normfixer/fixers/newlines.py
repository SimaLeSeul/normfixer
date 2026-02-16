def fix_newlines(lines):
    """
    Supprime les lignes vides dans les fonctions SAUF :
    - UNE ligne vide après TOUTES les déclarations
    """
    result = []
    in_function = False
    last_declaration_index = -1
    
    # ÉTAPE 1 : Trouver le dernier index de déclaration
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped == '{':
            in_function = True
            continue
        
        if stripped == '}':
            in_function = False
            # ❌ NE PAS RESET ICI
            continue
        
        if in_function and stripped:
            is_declaration = (
                ('\tint\t' in line or '\tchar\t' in line or '\tfloat\t' in line or 
                 '\tdouble\t' in line or '\tvoid\t' in line or '\tunsigned\t' in line or
                 '\tsize_t\t' in line or '\tt_' in line) and
                '=' not in line and
                ';' in line and
                'if' not in line and
                'while' not in line and
                'for' not in line and
                'return' not in line
            )
            
            if is_declaration:
                last_declaration_index = i
                print(f"🔍 Déclaration trouvée à l'index {i}: {line.strip()}")
    
    print(f"📍 Dernière déclaration à l'index: {last_declaration_index}")
    
    # ÉTAPE 2 : Reconstruire sans lignes vides sauf après la dernière déclaration
    in_function = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped == '{':
            in_function = True
            result.append(line)
            continue
        
        if stripped == '}':
            in_function = False
            result.append(line)
            continue
        
        if in_function:
            # Ignorer toutes les lignes vides existantes
            if not stripped:
                continue
            
            # Ajouter la ligne de code
            result.append(line)
            
            # ✅ AJOUTER UNE LIGNE VIDE APRÈS LA DERNIÈRE DÉCLARATION
            if i == last_declaration_index and last_declaration_index != -1:
                print(f"✅ Ajout ligne vide après index {i}")
                result.append('')
        else:
            result.append(line)
    
    return result
