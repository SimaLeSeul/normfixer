import re

def fix_operators(lines):
    """
    Ajoute espaces autour des opérateurs (norme 42)
    """
    fixed = []
    
    for line in lines:
        has_newline = line.endswith("\n")
        working_line = line.rstrip("\n")
        
        stripped = working_line.strip()
        
        # Ignorer préprocesseur, commentaires, lignes vides
        if not stripped or stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*"):
            fixed.append(line)
            continue
        
        # Sauvegarder l'indentation
        indent_match = re.match(r'^(\s*)', working_line)
        indent = indent_match.group(1) if indent_match else ""
        content = working_line[len(indent):]
        
        # FIX : return(0); → return (0);
        content = re.sub(r'\breturn\(', 'return (', content)
        
        # Opérateurs de comparaison: ==, !=, <=, >=
        content = re.sub(r'(\w)\s*([<>!=]=)\s*(\w)', r'\1 \2 \3', content)
        
        # Opérateurs logiques: &&, ||
        content = re.sub(r'(\))\s*(&&|\|\|)\s*(\()', r'\1 \2 \3', content)
        
        # Opérateurs arithmétiques (attention aux ++ et --)
        content = re.sub(r'(\w)\s*([+\-*/%])\s*(\w)', r'\1 \2 \3', content)
        
        # Nettoyer espaces multiples
        content = re.sub(r' {2,}', ' ', content)
        
        working_line = indent + content
        
        if has_newline:
            working_line += "\n"
        
        fixed.append(working_line)
    
    return fixed
