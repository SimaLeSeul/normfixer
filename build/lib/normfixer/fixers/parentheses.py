import re

def fix_parentheses_spacing(content: str, track=False):
    """
    Supprime espaces avant ')'
    """
    fixed = []
    changes = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        updated = re.sub(r"\s+\)", ")", line)

        if updated != line and track:
            changes.append(f"Line {lineno}: removed space before ')'")

        fixed.append(updated)

    return ("\n".join(fixed) + "\n", changes)
