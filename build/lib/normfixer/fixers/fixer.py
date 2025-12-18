from .indentation import fix_indentation
from .whitespace import fix_whitespace
from .operators import fix_operator_spacing
from .parentheses import fix_parentheses_spacing
from .declaration_assign import fix_declaration_assign, add_empty_line_after_declarations

import re


# -------------------------------------------------------
# NEW FIXERS (manquants)
# -------------------------------------------------------

def fix_newline_after_preproc(content, track=False):
    changes = []
    lines = content.splitlines()
    fixed = []

    for i, line in enumerate(lines):
        fixed.append(line)
        if line.strip().startswith("#"):
            if i + 1 < len(lines) and lines[i+1].strip() != "":
                fixed.append("")
                if track:
                    changes.append(f"Added newline after preprocessor at line {i+1}")

    return ("\n".join(fixed) + "\n", changes) if track else "\n".join(fixed) + "\n"


def fix_space_before_func(content, track=False):
    changes = []
    lines = content.splitlines()
    fixed = []

    for i, line in enumerate(lines):
        if " (" in line and re.match(r'^\s*\w', line):
            new = line.replace(" (", "(")
            if new != line and track:
                changes.append(f"Removed space before function name (line {i+1})")
            line = new
        fixed.append(line)

    return ("\n".join(fixed) + "\n", changes) if track else "\n".join(fixed) + "\n"


def replace_tabs(content, track=False):
    new = content.replace("\t", "    ")
    if track and new != content:
        return new, ["Replaced tabs by spaces"]
    return new, []


def fix_space_after_keyword(content, track=False):
    kw = r'\b(if|while|for|return)\('
    new = re.sub(kw, lambda m: m.group(0).replace("(", " ("), content)
    if track and new != content:
        return new, ["Added missing space after keyword"]
    return new, []

    

# -------------------------------------------------------
# MAIN FIXER FILE PIPELINE
# -------------------------------------------------------

def fix_file(filepath: str, report: bool = True) -> bool:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()
    except OSError:
        return False

    changes = []
    content = original

    # 0) Replace tabs
    content, ch = replace_tabs(content, track=True)
    changes.extend(ch)

    # 1) Newline after #include
    content, ch = fix_newline_after_preproc(content, track=True)
    changes.extend(ch)

    # 2) Remove space before function name
    content, ch = fix_space_before_func(content, track=True)
    changes.extend(ch)

    # 3) Whitespace fix
    content, ch = fix_whitespace(content, track=True)
    changes.extend(ch)

    # 4) Operator spacing
    content, ch = fix_operator_spacing(content, track=True)
    changes.extend(ch)

    # 5) Parentheses spacing
    content, ch = fix_parentheses_spacing(content, track=True)
    changes.extend(ch)

    # 6) Split declarations
    content, da_changes, decl_lines = fix_declaration_assign(content, track=True)
    changes.extend(da_changes)

    # 7) Add empty line after declarations
    content, space_changes = add_empty_line_after_declarations(content, decl_lines, track=True)
    changes.extend(space_changes)

    # 8) Missing space after keyword
    content, ch = fix_space_after_keyword(content, track=True)
    changes.extend(ch)

    # 9) Indentation
    content, ch = fix_indentation(content, track=True)
    changes.extend(ch)

    modified = content != original
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    if report and changes:
        print(f"[{filepath}]")
        for c in changes:
            print("  - " + c)

    return modified
