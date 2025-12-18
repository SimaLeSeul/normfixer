def clean_empty_lines(lines):
    fixed = []
    prev_empty = False

    for line in lines:
        if line.strip() == "":
            if prev_empty:
                continue
            prev_empty = True
        else:
            prev_empty = False
        fixed.append(line)
    return fixed
