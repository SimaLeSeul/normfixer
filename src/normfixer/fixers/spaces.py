import re

def fix_spacing(lines):
    """
    Corrige les espaces autour des opérateurs et après les virgules
    """
    result = []
    for line in lines:
        # Ignorer les lignes vides, commentaires et preprocessor
        stripped = line.strip()
        if not stripped or stripped.startswith(('#', '/*', '*', '//')):
            result.append(line)
            continue
        
        # Espaces autour des opérateurs d'assignation
        line = re.sub(r'(\w)\s*=\s*(\w)', r'\1 = \2', line)
        
        # Espaces autour des opérateurs de comparaison
        line = re.sub(r'(\w)\s*(>=|<=|==|!=|>|<)\s*(\w)', r'\1 \2 \3', line)
        
        # Espaces autour des opérateurs logiques
        line = re.sub(r'\s*(&&|\|\|)\s*', r' \1 ', line)
        
        # Espaces après les virgules
        line = re.sub(r',(\S)', r', \1', line)
        
        # Espaces après les points-virgules (dans les for)
        line = re.sub(r';(\S)', r'; \1', line)
        
        result.append(line)
    
    return result
