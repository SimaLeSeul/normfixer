def fix_indentation(lines):
    """Remplace les espaces par des tabulations"""
    result = []
    indent_level = 0
    next_line_extra_indent = 0
    
    for line in lines:
        stripped = line.lstrip()
        
        # Ligne vide
        if not stripped:
            result.append('')
            continue
        
        # Ajuster niveau d'indentation
        if '}' in stripped:
            indent_level = max(0, indent_level - 1)
        
        # Calculer indentation
        total_indent = indent_level + next_line_extra_indent
        new_line = '\t' * total_indent + stripped
        
        result.append(new_line)
        
        # Reset extra indent
        next_line_extra_indent = 0
        
        # Incrémenter pour le prochain bloc
        if '{' in stripped:
            indent_level += 1
        
        # Détecter if/while/for sans accolades
        if any(kw in stripped for kw in ['if ', 'while ', 'for ', 'else']) and '{' not in stripped:
            next_line_extra_indent = 1
    
    return result
