"""Root launch shim for the canonical app kept under the Hung codebase layout."""

from pathlib import Path
import sys


CODEBASE_DIR = Path(__file__).resolve().parent / "codebase"
if str(CODEBASE_DIR) not in sys.path:
    sys.path.insert(0, str(CODEBASE_DIR))

from codebase.app import main  # noqa: E402


if __name__ == "__main__":
    main()
