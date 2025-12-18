import os
from pathlib import Path

def process_file(filepath, verbose=False, dry_run=False):
    """
    Traite un fichier C pour corriger les erreurs de norme
    
    Args:
        filepath: Chemin du fichier à traiter
        verbose: Afficher les modifications
        dry_run: Ne pas sauvegarder les modifications
    """
    from normfixer.core.fixer import apply_all_fixes
    
    try:
        # Lire le fichier
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Appliquer les corrections
        lines = original_content.splitlines(keepends=True)
        fixed_content = apply_all_fixes(lines)
        
        # Affichage si verbose
        if verbose:
            print("=" * 60)
            print(f"Processing: {filepath}")
            print("=" * 60)
            print("\n--- BEFORE ---")
            print(original_content)
            print("\n--- AFTER ---")
            print(fixed_content)
            print("\n" + "=" * 60)
        
        # Sauvegarder si pas dry-run
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"\n✓ File saved: {filepath}")
        else:
            print(f"\n✓ Dry-run complete (no changes saved)")
            
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        raise


def process_path(path, verbose=False, dry_run=False):
    """
    Traite un fichier ou un dossier (récursivement)
    
    Args:
        path: Chemin du fichier ou dossier
        verbose: Afficher les modifications
        dry_run: Ne pas sauvegarder les modifications
    """
    path_obj = Path(path)
    
    if path_obj.is_file():
        if path_obj.suffix in ['.c', '.h']:
            process_file(str(path_obj), verbose=verbose, dry_run=dry_run)
        else:
            print(f"⚠️  Skipping non-C file: {path}")
    
    elif path_obj.is_dir():
        c_files = list(path_obj.rglob('*.c')) + list(path_obj.rglob('*.h'))
        
        if not c_files:
            print(f"⚠️  No C files found in: {path}")
            return
        
        print(f"📁 Found {len(c_files)} C file(s) in {path}")
        for file in c_files:
            process_file(str(file), verbose=verbose, dry_run=dry_run)
    
    else:
        print(f"❌ Error: Path not found: {path}")

def process_file(filepath, verbose=False, dry_run=False):
    """
    Traite un fichier C pour corriger les erreurs de norme
    
    Args:
        filepath: Chemin du fichier à traiter
        verbose: Afficher les modifications
        dry_run: Ne pas sauvegarder les modifications
    """
    from normfixer.core.fixer import apply_all_fixes
    
    try:
        # Lire le fichier
        with open(filepath, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Appliquer les corrections
        lines = original_content.splitlines(keepends=True)
        fixed_content = apply_all_fixes(lines)
        
        # Affichage si verbose
        if verbose:
            print("=" * 60)
            print(f"Processing: {filepath}")
            print("=" * 60)
            print("\n--- BEFORE ---")
            print(original_content)
            print("\n--- AFTER ---")
            print(fixed_content)
            print("\n" + "=" * 60)
        
        # Sauvegarder si pas dry-run
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print(f"\n✓ File saved: {filepath}")
        else:
            print(f"\n✓ Dry-run complete (no changes saved)")
            
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        raise
