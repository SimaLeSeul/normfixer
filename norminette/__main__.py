import argparse
import glob
import pathlib
import platform
import subprocess
import sys
try:
    from importlib.metadata import version
    pkg_version = version("norminette")
except Exception:
    pkg_version = "local"

version_text = f"norminette {pkg_version}"

from norminette.context import Context
from norminette.errors import formatters
from norminette.exceptions import CParsingError
from norminette.file import File
from norminette.lexer import Lexer
from norminette.registry import Registry
from norminette.tools.colors import colors

from norminette.fixer import fix_file

version_text += f", Python {platform.python_version()}"
version_text += f", {platform.platform()}"


def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "file",
        help="File(s) or folder(s) you wanna run the parser on. If no file provided, runs on current folder.",
        nargs="*",
    )
    parser.add_argument(
        "-d", "--debug",
        action="count",
        help="Debug output",
        default=0,
    )
    parser.add_argument(
        "-o", "--only-filename",
        action="store_true",
        help="Show only filename",
        default=False,
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=version_text,
    )
    parser.add_argument("--cfile", action="store")
    parser.add_argument("--hfile", action="store")
    parser.add_argument("--filename", action="store")
    parser.add_argument("--use-gitignore", action="store_true")

    parser.add_argument(
        "-r", "--repair",
        action="store_true",
        help="Fix your norm errors",
    )

    parser.add_argument(
        "-f", "--format",
        choices=[formatter.name for formatter in formatters],
        help="Formatting style for errors",
        default="humanized",
    )

    parser.add_argument("--no-colors", action="store_true")
    parser.add_argument("-R", nargs=1)

    args = parser.parse_args()

    registry = Registry()
    formatter = next(filter(lambda it: it.name == args.format, formatters))

    files = []
    debug = args.debug

    #
    # --- CASE: raw content provided with --cfile / --hfile
    #
    if args.cfile or args.hfile:
        file_name = args.filename or ("file.c" if args.cfile else "file.h")
        file_data = args.cfile if args.cfile else args.hfile
        files.append(File(file_name, file_data))

    #
    # --- CASE: normal files / directories
    #
    else:
        stack = []
        stack += args.file if args.file else glob.glob("**/*.[ch]", recursive=True)

        for item in stack:
            path = pathlib.Path(item)

            if not path.exists():
                print(f"Error: '{path!s}' no such file or directory")
                sys.exit(1)

            # File
            if path.is_file():
                if path.suffix not in (".c", ".h"):
                    print(f"Error: {path.name!r} is not valid C or C header file")
                    continue

                # Apply repair BEFORE parsing
                if args.repair:
                    fix_file(item)

                files.append(File(item))

            # Directory
            elif path.is_dir():
                stack += glob.glob(str(path) + "/**/*.[ch]", recursive=True)

        del stack

    #
    # --- Handle --use-gitignore
    #
    if args.use_gitignore:
        tmp_targets = []
        for target in files:
            exit_code = subprocess.run(
                ["git", "check-ignore", "-q", target.path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).returncode

            if exit_code == 0:
                continue
            elif exit_code == 1:
                tmp_targets.append(target)
            else:
                print(f"Error: something wrong with --use-gitignore option {target.path!r}")
                sys.exit(0)

        files = tmp_targets

    #
    # --- Parse files
    #
    for file in files:
        try:
            lexer = Lexer(file)
            tokens = list(lexer)
            context = Context(file, tokens, debug, args.R)
            registry.run(context)

        except CParsingError as e:
            print(file.path + f": Error!\n\t" + colors(e.msg, "red"))
            sys.exit(1)

        except KeyboardInterrupt:
            sys.exit(1)

    #
    # --- Print results
    #
    errors = formatter(files, use_colors=not args.no_colors)
    print(errors, end="")

    sys.exit(1 if any(len(it.errors) for it in files) else 0)


if __name__ == "__main__":
    main()
