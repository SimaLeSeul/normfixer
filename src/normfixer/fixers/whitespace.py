import re

def fix_whitespace(lines):
    """
    - Supprime espaces/tabs en fin de ligne
    - Remplace tabs par 4 espaces
    - Préserve les newlines
    """
    fixed = []
    for line in lines:
        # Remplacer tabs par espaces
        line = line.replace("\t", "    ")
        
        # Supprimer trailing whitespace (garder \n)
        if line.endswith("\n"):
            line = line.rstrip() + "\n"
        else:
            line = line.rstrip()
        
        fixed.append(line)
    return fixed
