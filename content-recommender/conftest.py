import sys
from pathlib import Path

# Ensure `import src.*` works when running `pytest` from the repository root.
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

