import re

def fix_operators(lines):
    fixed = []
    for line in lines:
        line = re.sub(r"\s*([<>!=]=)\s*", r" \1 ", line)
        line = re.sub(r"\s*([+\-*/%])\s*", r" \1 ", line)
        line = re.sub(r"\s*(&&|\|\|)\s*", r" \1 ", line)
        line = re.sub(r"\s+", " ", line)
        fixed.append(line)
    return fixed
