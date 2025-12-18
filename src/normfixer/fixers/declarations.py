import re

def fix_declarations(lines):
    """
    Sépare les déclarations des assignations et les place AU DÉBUT
    """
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Détecter ouverture de fonction
        if '{' in line and i > 0:
            # Trouver toutes les déclarations dans la fonction
            declarations = []
            assignments = []
            body = []
            
            # Ajouter la ligne avec '{'
            result.append(line)
            i += 1
            
            # Parser le corps de la fonction
            while i < len(lines):
                curr_line = lines[i]
                curr_stripped = curr_line.strip()
                
                # Fin de fonction
                if curr_stripped == '}':
                    # ORDRE CORRECT : déclarations -> ligne vide -> assignations -> body
                    for decl in declarations:
                        result.append(decl)
                    
                    if declarations:
                        result.append('\n')
                    
                    for assign in assignments:
                        result.append(assign)
                    
                    for body_line in body:
                        result.append(body_line)
                    
                    result.append(curr_line)
                    i += 1
                    break
                
                # Détecter déclaration + assignation : int a = 0;
                match = re.match(r'^\s*(int|char|float|double|long|short|unsigned|void|size_t|t_\w+)\s+(\w+)\s*=\s*(.+);', curr_stripped)
                
                if match:
                    type_name, var_name, value = match.groups()
                    declarations.append(f"\t{type_name}\t{var_name};\n")
                    assignments.append(f"\t{var_name} = {value};\n")
                else:
                    # Ligne normale du body
                    body.append(curr_line)
                
                i += 1
            
            continue
        
        result.append(line)
        i += 1
    
    return result
