import re

def fix_whitespace(lines):
    fixed = []
    for line in lines:
        line = re.sub(r"[ \t]+$", "", line)
        line = line.replace("\t", "    ")
        fixed.append(line)
    return fixed
