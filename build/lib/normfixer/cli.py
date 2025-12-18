import argparse
from .fixer_pipeline import process_path

def main():
    parser = argparse.ArgumentParser(description="Auto-fixer for common Norminette issues.")
    parser.add_argument("path", help="File or directory to fix")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show details of applied fixes")

    args = parser.parse_args()
    process_path(args.path, verbose=args.verbose)
