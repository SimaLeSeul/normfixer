import os

from .fixers.whitespace import fix_whitespace
from .fixers.assignments import fix_assignments
from .fixers.operators import fix_operators
from .fixers.indentation import fix_indentation
from .fixers.empty_lines import fix_empty_lines


def apply_fixers(lines):
    """Applique tous les fixers dans l'ordre optimal"""
    # 1. Nettoyer whitespace AVANT tout
    lines = fix_whitespace(lines)
    
    # 2. Séparer déclarations/assignations
    lines = fix_assignments(lines)
    
    # 3. Fixer les opérateurs
    lines = fix_operators(lines)
    
    # 4. Réindenter TOUT le code
    lines = fix_indentation(lines)
    
    # 5. Nettoyer lignes vides EN DERNIER
    lines = fix_empty_lines(lines)
    
    return lines


def process_file(filepath, verbose=False, dry_run=False):
    """Traite un fichier C/H"""
    if not os.path.isfile(filepath):
        print(f"[ERR] Not a file: {filepath}")
        return

    if verbose:
        print(f"\n{'='*60}")
        print(f"Processing: {filepath}")
        print(f"{'='*60}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if verbose:
        print("\n--- BEFORE ---")
        print(content)

    lines = content.splitlines(keepends=True)
    new_lines = apply_fixers(lines)
    new_content = "".join(new_lines)

    if verbose:
        print("\n--- AFTER ---")
        print(new_content)
        print(f"{'='*60}\n")

    if not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        if verbose:
            print(f"✓ File saved: {filepath}")

    return new_lines


def process_path(path, verbose=False, dry_run=False):
    """Traite récursivement un dossier"""
    if os.path.isfile(path):
        return process_file(path, verbose=verbose, dry_run=dry_run)

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith((".c", ".h")):
                process_file(
                    os.path.join(root, file),
                    verbose=verbose,
                    dry_run=dry_run
                )
