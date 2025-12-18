import os

def is_c_file(path: str) -> bool:
    return path.endswith(".c") or path.endswith(".h")

def read_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path: str, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def list_c_files(root: str):
    for r, _, files in os.walk(root):
        for f in files:
            if is_c_file(f):
                yield os.path.join(r, f)
