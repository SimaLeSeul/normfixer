import re

def fix_assignments(lines):
    """
    Sépare déclarations et assignations selon la norme 42:
    1. Toutes les déclarations groupées
    2. Ligne vide
    3. Toutes les assignations groupées
    4. Ligne vide
    5. Code
    """
    fixed = []
    in_function = False
    brace_count = 0
    
    # Pattern pour déclaration avec assignation
    decl_assign_pattern = re.compile(
        r'^(\s*)(int|char|float|double|long|short|unsigned\s+\w+|signed\s+\w+|size_t|void\s*\*)\s+'
        r'([a-zA-Z_]\w*)\s*=\s*(.+);?\s*$'
    )
    
    # Pattern pour déclaration simple
    decl_pattern = re.compile(
        r'^(\s*)(int|char|float|double|long|short|unsigned\s+\w+|signed\s+\w+|size_t|void\s*\*)\s+'
        r'([a-zA-Z_]\w*)\s*;?\s*$'
    )
    
    buffer = []
    declarations = []
    assignments = []
    collecting_declarations = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Suivre les accolades
        brace_count += stripped.count('{') - stripped.count('}')
        
        # Détecter début de fonction
        if '{' in stripped and not in_function:
            in_function = True
            fixed.append(line)
            collecting_declarations = True
            i += 1
            continue
        
        # Détecter fin de fonction
        if brace_count == 0 and '}' in stripped and in_function:
            in_function = False
            collecting_declarations = False
            
            # Flush les déclarations et assignations
            if declarations or assignments:
                for decl in declarations:
                    fixed.append(decl)
                if declarations:
                    fixed.append("\n")
                for assign in assignments:
                    fixed.append(assign)
                if assignments:
                    fixed.append("\n")
                declarations = []
                assignments = []
            
            fixed.append(line)
            i += 1
            continue
        
        # Collecter déclarations et assignations dans une fonction
        if in_function and collecting_declarations:
            # Ignorer lignes vides
            if stripped == "":
                i += 1
                continue
            
            # Détecter déclaration avec assignation
            match_assign = decl_assign_pattern.match(line)
            if match_assign:
                indent, type_, var, value = match_assign.groups()
                value = value.rstrip(';').strip()
                declarations.append(f"{indent}{type_} {var};\n")
                assignments.append(f"{indent}{var} = {value};\n")
                i += 1
                continue
            
            # Détecter déclaration simple
            match_decl = decl_pattern.match(line)
            if match_decl:
                indent, type_, var = match_decl.groups()
                declarations.append(f"{indent}{type_} {var};\n")
                i += 1
                continue
            
            # Si on arrive à une ligne qui n'est pas une déclaration
            # On arrête de collecter et on flush
            collecting_declarations = False
            
            # Flush déclarations et assignations
            if declarations or assignments:
                for decl in declarations:
                    fixed.append(decl)
                if declarations:
                    fixed.append("\n")
                for assign in assignments:
                    fixed.append(assign)
                if assignments:
                    fixed.append("\n")
                declarations = []
                assignments = []
            
            # Ajouter la ligne courante
            if line and not line.endswith("\n"):
                line += "\n"
            fixed.append(line)
            i += 1
            continue
        
        # Ligne normale hors fonction
        if line and not line.endswith("\n"):
            line += "\n"
        fixed.append(line)
        i += 1
    
    return fixed
