# Auto-generated __init__.py for libint2 package
import os as _os
from pathlib import Path as _Path

# Set LIBINT_DATA_PATH to the bundled basis files location
# This overrides the hardcoded build-time path
_pkg_dir = _Path(__file__).parent
_data_path = _pkg_dir / "share" / "libint"
if _data_path.exists():
    _os.environ.setdefault("LIBINT_DATA_PATH", str(_data_path))

# Re-export everything from the C++ extension module
from .libint2 import *
