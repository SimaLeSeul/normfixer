import re

def fix_function_declarations(lines):
    """
    Fixe le formatage des déclarations de fonctions :
    - TAB entre type de retour et nom de fonction
    - Espace avant parenthèse
    """
    fixed = []
    
    for line in lines:
        stripped = line.strip()
        
        # Détecter déclaration de fonction (type + nom + parenthèse)
        # Exemples: "int ft_isalpha(", "char *ft_strdup(", "void test("
        match = re.match(r'^([\w\s\*]+?)\s+(\w+)\s*\(', stripped)
        
        if match:
            return_type = match.group(1).strip()  # "int", "char *", etc.
            func_name = match.group(2)             # "ft_isalpha", etc.
            rest = stripped[match.end()-1:]        # "(int c)" etc.
            
            # Reformater : type + TAB + nom + reste
            new_line = f"{return_type}\t{func_name}{rest}\n"
            fixed.append(new_line)
        else:
            fixed.append(line)
    
    return fixed
