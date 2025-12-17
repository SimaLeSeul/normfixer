from .indentation import fix_indentation
from .whitespace import fix_whitespace
from .operators import fix_operator_spacing
from .parentheses import fix_parentheses_spacing

def fix_file(filepath: str, report: bool = True) -> bool:
    """
    Fix simple norm errors in a file.
    Prints changes if report=True.
    Returns True if file was modified.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()
    except OSError:
        return False

    changes = []
    content = original

    # --- Fix whitespace ---
    new_content, ws_changes = fix_whitespace(content, track=True)
    if ws_changes:
        changes.extend(ws_changes)
    content = new_content

	# --- Fix operator spacing ---
    new_content, op_changes = fix_operator_spacing(content, track=True)
    if op_changes:
        changes.extend(op_changes)
    content = new_content
	# --- Fix parentheses spacing ---
    new_content, par_changes = fix_parentheses_spacing(content, track=True)
    if par_changes:
        changes.extend(par_changes)
    content = new_content

    # --- Fix indentation ---
    new_content, ind_changes = fix_indentation(content, track=True)
    if ind_changes:
        changes.extend(ind_changes)
    content = new_content

    # Write file if changed
    modified = content != original
    if modified:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # Print changes
    if report and changes:
        print(f"[{filepath}]")
        for c in changes:
            print("  - " + c)

    return modified
