import os
from pathlib import Path
from normfixer.fixer import fix_file

def process_file(filepath, verbose=False, dry_run=False):
    """
    Traite un fichier C et applique toutes les corrections
    """
    # Lire le fichier
    with open(filepath, 'r') as f:
        original_content = f.read()
    
    if verbose:
        print("=" * 60)
        print(f"Processing: {filepath}")
        print("=" * 60)
        print("\n--- BEFORE ---")
        print(original_content)
    
    # Appliquer TOUTES les corrections via fix_file()
    fixed_content = fix_file(original_content)
    
    if verbose:
        print("\n--- AFTER ---")
        print(fixed_content)
        print("\n" + "=" * 60 + "\n")
    
    # Sauvegarder (sauf en dry-run)
    if not dry_run:
        with open(filepath, 'w') as f:
            f.write(fixed_content)
        
        if verbose:
            print(f"✓ File saved: {filepath}")
    else:
        if verbose:
            print(f"⚠ DRY RUN - File NOT saved: {filepath}")


def process_path(path, verbose=False, dry_run=False):
    """
    Traite un fichier ou un dossier (récursif)
    """
    path = Path(path)
    
    if path.is_file():
        if path.suffix in ['.c', '.h']:
            process_file(path, verbose=verbose, dry_run=dry_run)
        else:
            print(f"⚠ Skipping non-C file: {path}")
    
    elif path.is_dir():
        c_files = list(path.rglob('*.c')) + list(path.rglob('*.h'))
        
        if not c_files:
            print(f"⚠ No .c or .h files found in: {path}")
            return
        
        print(f"📂 Found {len(c_files)} files in {path}")
        
        for file in c_files:
            process_file(file, verbose=verbose, dry_run=dry_run)
    
    else:
        print(f"❌ Path not found: {path}")
