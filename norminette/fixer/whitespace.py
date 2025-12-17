import re


def fix_whitespace(content: str) -> str:
    lines = content.splitlines()

    fixed = []
    empty_count = 0

    for line in lines:
        # Supprimer espaces en fin de ligne
        line = re.sub(r"[ \t]+$", "", line)

        if line == "":
            empty_count += 1
            if empty_count > 1:
                continue
        else:
            empty_count = 0

        fixed.append(line)

    return "\n".join(fixed) + "\n"
