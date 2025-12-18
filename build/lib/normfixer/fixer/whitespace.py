import re

def fix_whitespace(content: str, track=False):
    lines = content.splitlines()
    fixed = []
    empty_count = 0
    changes = []

    for i, line in enumerate(lines, start=1):

        # Remove trailing whitespace
        new_line = re.sub(r"[ \t]+$", "", line)
        if new_line != line and track:
            changes.append(f"Line {i}: removed trailing whitespace")

        # Remove excessive empty lines
        if new_line == "":
            empty_count += 1
            if empty_count > 1:
                if track:
                    changes.append(f"Line {i}: removed extra empty line")
                continue
        else:
            empty_count = 0

        fixed.append(new_line)

    result = "\n".join(fixed) + "\n"
    return (result, changes) if track else result
