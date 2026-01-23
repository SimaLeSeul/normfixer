import re

def fix_spacing(lines):
    """
    Normalise les espaces selon la norme (opérateurs, parenthèses, etc.)
    """
    result = []
    
    for line in lines:
        stripped = line.strip()
        
        # Ligne vide ou préprocesseur : garder tel quel
        if not stripped or stripped.startswith('#'):
            result.append(line)
            continue
        
        # 1. SIGNATURE DE FONCTION : type TAB nom(args)
        # Détecte : int ft_xxx(...) ou void ft_xxx(...)
        func_match = re.match(
            r'^(\s*)(int|char|void|float|double|long|short|unsigned|size_t|t_\w+)\s+(\w+)\s*\(',
            line
        )
        if func_match:
            indent, ret_type, func_name = func_match.groups()
            rest = line[func_match.end()-1:]  # Garde "(args)..."
            line = f"{indent}{ret_type}\t{func_name}{rest}"
        
        # 2. Opérateurs : espaces autour de = + - * / etc.
        line = re.sub(r'(\w)\s*([+\-*/%]?=)\s*(\w)', r'\1 \2 \3', line)
        
        # 3. Comparateurs : espaces autour de == != <= >= < >
        line = re.sub(r'(\w|\))\s*([<>!=]=?)\s*(\w|\()', r'\1 \2 \3', line)
        
        # 4. Opérateurs logiques : espaces autour de && ||
        line = re.sub(r'(\)|\w)\s*(&&|\|\|)\s*(\(|\w)', r'\1 \2 \3', line)
        
        # 5. Virgules : espace après, pas avant
        line = re.sub(r'\s*,\s*', ', ', line)
        
        # 6. Parenthèses : pas d'espace après '(' ni avant ')'
        line = re.sub(r'\(\s+', '(', line)
        line = re.sub(r'\s+\)', ')', line)
        
        # 7. Mots-clés : espace après if/while/for/return
        line = re.sub(r'\b(if|while|for|return)\(', r'\1 (', line)
        
        result.append(line)
    
    return result
