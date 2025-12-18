import argparse
import sys
import os
from .fixer_pipeline import process_file, process_path

def main():
    parser = argparse.ArgumentParser(description="NormFixer – Auto-fix Norminette")
    parser.add_argument("path", help="Fichier ou dossier à corriger")
    parser.add_argument("-v", "--verbose", action="store_true", help="Afficher les changements")
    parser.add_argument("--dry-run", action="store_true", help="Ne pas écrire, juste afficher")
    args = parser.parse_args()

    path = args.path

    if not os.path.exists(path):
        print(f"Erreur : '{path}' n'existe pas.")
        sys.exit(1)

    if os.path.isfile(path):
        process_file(path, verbose=args.verbose, dry_run=args.dry_run)
    else:
        process_path(path, verbose=args.verbose, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
