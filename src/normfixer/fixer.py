from normfixer.fixers.preprocessor import fix_preprocessor
from normfixer.fixers.spaces import fix_spacing
from normfixer.fixers.indentation import fix_indentation
from normfixer.fixers.declarations import fix_declarations
from normfixer.fixers.newlines import fix_newlines

def fix_file(content):
    """
    Applique tous les fixers dans l'ordre correct
    """
    # IMPORTANT : split() sans '\n' pour éviter les doublons
    lines = content.splitlines()
    
    # 1. Preprocesseur
    lines = fix_preprocessor(lines)
    
    # 2. Déclarations
    lines = fix_declarations(lines)
    
    # 3. Espaces
    lines = fix_spacing(lines)
    
    # 4. Indentation
    lines = fix_indentation(lines)
    
    # 5. Lignes vides - DEBUG
    print("🔍 AVANT fix_newlines:", len(lines), "lignes")
    for i, line in enumerate(lines):
        print(f"  [{i}] {repr(line)}")
    
    lines = fix_newlines(lines)
    
    print("\n🔍 APRÈS fix_newlines:", len(lines), "lignes")
    for i, line in enumerate(lines):
        print(f"  [{i}] {repr(line)}")
    
    # Rejoindre avec \n + TOUJOURS finir par \n
    return '\n'.join(lines) + '\n'
