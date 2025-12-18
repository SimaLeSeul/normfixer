def fix_empty_lines(lines):
    """
    Supprime les lignes vides à l'intérieur des fonctions
    (EMPTY_LINE_FUNCTION)
    Mais garde celles après déclarations et assignations
    """
    fixed = []
    in_function = False
    brace_count = 0
    prev_was_declaration_block = False
    prev_was_assignment_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Suivre les accolades
        brace_count += stripped.count('{') - stripped.count('}')
        
        # Détecter entrée dans fonction
        if '{' in stripped and not in_function:
            in_function = True
            fixed.append(line)
            continue
        
        # Détecter sortie de fonction
        if brace_count == 0 and in_function:
            in_function = False
            prev_was_declaration_block = False
            prev_was_assignment_block = False
        
        # Si ligne vide
        if stripped == "":
            # Garder si après bloc de déclarations
            if prev_was_declaration_block:
                fixed.append(line)
                prev_was_declaration_block = False
                continue
            
            # Garder si après bloc d'assignations
            if prev_was_assignment_block:
                fixed.append(line)
                prev_was_assignment_block = False
                continue
            
            # Supprimer si à l'intérieur d'une fonction
            if in_function:
                continue
            
            # Garder sinon
            fixed.append(line)
            continue
        
        # Détecter déclarations
        if in_function and (stripped.startswith(("int ", "char ", "float ", "double ", 
                                                 "long ", "short ", "unsigned ", "size_t "))):
            if "=" not in stripped:  # Déclaration pure
                prev_was_declaration_block = True
            else:  # Assignation
                prev_was_assignment_block = True
        else:
            # Reset si on rencontre du code
            if stripped and not stripped.startswith("//") and not stripped.startswith("/*"):
                prev_was_declaration_block = False
                prev_was_assignment_block = False
        
        fixed.append(line)
    
    return fixed
