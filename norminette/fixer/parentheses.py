import re

def fix_parentheses_spacing(content: str, track=False):
    fixed = []
    changes = []

    for lineno, line in enumerate(content.splitlines(), start=1):
        new_line = line

        # Supprime les espaces avant ')'
        updated = re.sub(r"\s+\)", ")", new_line)

        if updated != new_line and track:
            changes.append(f"Line {lineno}: removed space before ')'")

        fixed.append(updated)

    result = "\n".join(fixed) + "\n"
    return (result, changes) if track else result
