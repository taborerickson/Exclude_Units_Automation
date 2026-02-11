# tests/conftest.py
import sys
from pathlib import Path

# Adding project root to sys.path so imports works when ran
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))