import os
import io

from .fixers.whitespace import fix_whitespace
from .fixers.parentheses import fix_parentheses_spacing
from .fixers.operators import fix_operator_spacing
from .fixers.indentation import fix_indentation
from .fixers.fixer import (
    fix_newline_after_preproc,
    fix_space_before_func,
    fix_space_after_keyword,
    replace_tabs,
)
from .fixers.declaration_assign import fix_declaration_assign, add_empty_line_after_declarations
from .fixers.empty_line import fix_empty_line


# ----------------------------------------------------
# Helpers
# ----------------------------------------------------

def normalize_to_str(lines):
    """Convertit une liste de lignes → string"""
    if isinstance(lines, str):
        return lines
    return "".join(lines)


def normalize_to_lines(content):
    """Convertit string → liste de lignes"""
    if isinstance(content, list):
        return content
    return content.splitlines(keepends=True)


# ----------------------------------------------------
# Pipeline ordonné
# ----------------------------------------------------

STRING_FIXERS = [
    replace_tabs,
    fix_newline_after_preproc,
    fix_space_before_func,
    fix_whitespace,
    fix_operator_spacing,
    fix_parentheses_spacing,
    fix_space_after_keyword,
    fix_indentation,
]

LINE_FIXERS = [
    fix_declaration_assign,
    add_empty_line_after_declarations,
    fix_empty_line,
]


# ----------------------------------------------------
# Application
# ----------------------------------------------------

def apply_string_fixers(content):
    changes_all = []

    for fixer in STRING_FIXERS:
        try:
            result = fixer(content, track=True)
            # chaque fixer renvoie (content, changes)
            content, changes = result
            changes_all.extend(changes)
        except Exception as e:
            print(f"[ERROR] Fixer {fixer.__name__} failed: {e}")

    return content, changes_all


def apply_line_fixers(lines):
    changes_all = []

    # 1) fix_declaration_assign → renvoie juste une liste de lignes
    lines = fix_declaration_assign(lines)

    # 2) add_empty_line_after_declarations
    #    Ici tu as besoin de decl_lines,
    #    mais ta version actuelle ne les retourne pas.
    #    On doit donc recalculer les lignes de déclarations.

    decl_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.endswith(";") and (
            stripped.startswith("int ") or
            stripped.startswith("char ") or
            stripped.startswith("float ") or
            stripped.startswith("double ") or
            stripped.startswith("long ") or
            stripped.startswith("short ") or
            stripped.startswith("unsigned ") or
            stripped.startswith("size_t ") or
            stripped.startswith("const ")
        ):
            decl_lines.append(i)

    # appliquer l'ajout de ligne vide
    updated = add_empty_line_after_declarations(lines, decl_lines)
    lines = updated
    # Après fix_declaration_assign + add_empty_line_after_declarations
	# Ré‑indenter correctement
    content = normalize_to_str(lines)
    content, ch = fix_indentation(content, track=True)
    changes_all.extend(ch)
    lines = normalize_to_lines(content)


    # 3) fixer empty_line (ne change rien)
    lines = fix_empty_line(lines)

    return lines, changes_all



# ----------------------------------------------------
# Main entry
# ----------------------------------------------------

def process_file(path, verbose=False):
    try:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except OSError:
        return

    content = original
    all_changes = []

    # -------- STRING FIXERS --------
    content, ch = apply_string_fixers(content)
    all_changes.extend(ch)

    # convert → lignes
    lines = normalize_to_lines(content)

    # -------- LINE FIXERS --------
def apply_line_fixers(lines):
    changes_all = []

    # 1) split déclaration + assign
    lines = fix_declaration_assign(lines)

        # 2) Séparer toutes les déclarations AU DÉBUT du bloc
    declarations = []
    instructions = []

    found_assignment = False

    for line in lines:
        stripped = line.strip()

        is_decl = (
            stripped.endswith(";")
            and (
                stripped.startswith("int ")
                or stripped.startswith("char ")
                or stripped.startswith("float ")
                or stripped.startswith("double ")
                or stripped.startswith("long ")
                or stripped.startswith("short ")
                or stripped.startswith("unsigned ")
                or stripped.startswith("size_t ")
                or stripped.startswith("const ")
            )
        )

        is_assign = "=" in stripped and stripped.endswith(";")

        # si on voit une assignation → fin définitive du bloc déclarations
        if is_assign:
            found_assignment = True

        # tant qu'on n'a pas vu d'assignation, les déclarations vont en haut
        if is_decl and not found_assignment:
            declarations.append(line)
        else:
            instructions.append(line)


    # 3) reconstruire : déclarations + ligne vide + instructions
    rebuilt = []
    rebuilt.extend(declarations)

    # ligne vide obligatoire uniquement si on a des instructions
    if instructions and declarations:
        rebuilt.append("\n")

    rebuilt.extend(instructions)

    # 4) ré‑indentation globale
    content = "".join(rebuilt)
    content, ch = fix_indentation(content, track=True)
    changes_all.extend(ch)

    # 5) retour en liste
    lines = content.splitlines(keepends=True)

    return lines, changes_all

def process_path(path, verbose=False):
    if os.path.isfile(path):
        process_file(path, verbose)
        return

    for root, _, files in os.walk(path):
        for name in files:
            if name.endswith(".c") or name.endswith(".h"):
                process_file(os.path.join(root, name), verbose)
