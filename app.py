"""Root launch shim for the canonical app kept under the Hung codebase layout."""

from pathlib import Path
import runpy
import sys


ROOT_DIR = Path(__file__).resolve().parent
CODEBASE_DIR = ROOT_DIR / "codebase"

if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))


def main() -> None:
    runpy.run_path(str(CODEBASE_DIR / "app.py"), run_name="__main__")


if __name__ == "__main__":
    main()

