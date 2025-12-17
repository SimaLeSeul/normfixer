def fix_indentation(content: str) -> str:
    fixed_lines = []

    for line in content.splitlines():
        stripped = line.lstrip(" ")
        space_count = len(line) - len(stripped)

        if space_count > 0:
            tabs = space_count // 4
            line = ("\t" * tabs) + stripped

        fixed_lines.append(line)

    return "\n".join(fixed_lines) + "\n"
