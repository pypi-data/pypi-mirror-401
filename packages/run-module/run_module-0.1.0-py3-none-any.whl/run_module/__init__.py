import runpy
import sys


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: run-module <module_name> [args...]", file=sys.stderr)
        sys.exit(1)

    module_name = sys.argv[1]
    sys.argv = sys.argv[1:]  # Shift so module sees itself as argv[0]
    runpy.run_module(module_name, run_name="__main__", alter_sys=True)
