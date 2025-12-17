from fixer.indentation import fix_indentation
from fixer.whitespace import fix_whitespace


def fix_file(filepath: str) -> bool:
    """
    Fix simple norm errors in a file.
    Returns True if file was modified.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()
    except OSError:
        return False

    content = original
    content = fix_whitespace(content)
    content = fix_indentation(content)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    return False
