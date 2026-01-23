import re

def fix_declarations(lines):
    """Sépare les déclarations des assignations"""
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if '{' in line and i > 0:
            declarations = []
            assignments = []
            body = []
            
            result.append(line)
            i += 1
            
            while i < len(lines):
                curr_line = lines[i]
                curr_stripped = curr_line.strip()
                
                if curr_stripped == '}':
                    for decl in declarations:
                        result.append(decl)
                    
                    if declarations and assignments:
                        result.append("")  # ✅ Ligne vide
                    
                    for assign in assignments:
                        result.append(assign)
                    
                    if (declarations or assignments) and body:
                        result.append("")  # ✅ Ligne vide
                    
                    for body_line in body:
                        result.append(body_line)
                    
                    result.append(curr_line)
                    i += 1
                    break
                
                match = re.match(
                    r'^\s*(int|char|float|double|long|short|unsigned|void|size_t|t_\w+)\s+(\w+)\s*=\s*(.+);',
                    curr_stripped
                )
                
                if match:
                    type_name, var_name, value = match.groups()
                    declarations.append(f"\t{type_name}\t{var_name};")  # ✅ Sans \n
                    assignments.append(f"\t{var_name} = {value};")      # ✅ Sans \n
                else:
                    body.append(curr_line)
                
                i += 1
            
            continue
        
        result.append(line)
        i += 1
    
    return result
