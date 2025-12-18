import re

def fix_keyword_spacing(content: str, track=False):
    """
    Corrige : if( → if (
    return( → return (
    while( → while (
    """
    kw = r'\b(if|while|for|return)\('
    changes = []
    new_content = re.sub(kw, lambda m: m.group(0).replace("(", " ("), content)

    if track and new_content != content:
        changes.append("Added missing space after keyword")

    return new_content, changes
