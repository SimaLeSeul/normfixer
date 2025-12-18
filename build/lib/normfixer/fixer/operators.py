import re

# Patterns pour les opérateurs binaires simples
BINARY_OPS = ["=", r"\+", "-", r"\*", "/", "%", "==", "!=", "<", ">", "<=", ">="]

# Regex pour espaces autour des opérateurs binaires
BINARY_REGEX = re.compile(
    r"\s*(" + "|".join(BINARY_OPS) + r")\s*"
)

def fix_operator_spacing(content: str, track=False):
    """
    Ajoute des espaces autour des opérateurs binaires simples.
    Exemple : c=0 -> c = 0
    """
    fixed = []
    changes = []

    for lineno, line in enumerate(content.splitlines(), start=1):

        # Skip lignes vides ou commentaires
        stripped = line.strip()
        if not stripped or stripped.startswith("//") or stripped.startswith("/*"):
            fixed.append(line)
            continue

        new_line = line

        # Corrige les opérateurs binaires
        def repl(match):
            return f" {match.group(1)} "

        updated = BINARY_REGEX.sub(repl, new_line)

        # Fix pour éviter des doubles espaces (ex : "a  =  b")
        updated = re.sub(r"\s{2,}", " ", updated)

        # Si modifié
        if updated != new_line and track:
            changes.append(f"Line {lineno}: fixed operator spacing")

        fixed.append(updated)

    result = "\n".join(fixed) + "\n"
    return (result, changes) if track else result
