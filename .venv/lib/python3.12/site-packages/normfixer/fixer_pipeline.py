import os

from .fixers.whitespace import fix_whitespace
from .fixers.operators import fix_operators
from .fixers.assignments import fix_assignments
from .fixers.declaration_assign import fix_declaration_assign
from .fixers.indentation import fix_indentation
from .fixers.empty_lines import clean_empty_lines


def apply_fixers(lines):
    lines = fix_whitespace(lines)
    lines = fix_operators(lines)
    lines = fix_assignments(lines)
    lines = fix_declaration_assign(lines)
    lines = fix_indentation(lines)
    lines = clean_empty_lines(lines)
    return lines


def process_file(filepath, verbose=False, dry_run=False):
    if not os.path.isfile(filepath):
        print(f"[ERR] Not a file: {filepath}")
        return

    if verbose:
        print(f"[INFO] Processing {filepath}")

    with open(filepath, "r") as f:
        lines = f.readlines()

    new_lines = apply_fixers(lines)

    if dry_run:
        return new_lines

    with open(filepath, "w") as f:
        f.writelines(new_lines)

    return new_lines


def process_path(path, verbose=False, dry_run=False):
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
