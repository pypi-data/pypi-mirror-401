"""Constants for the Simforge SDK."""

from pathlib import Path

# Default service URL for Simforge API
DEFAULT_SERVICE_URL = "https://simforge.goharvest.ai"

# Get SDK version from pyproject.toml
try:
    # Find pyproject.toml relative to this file
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        # Try Python 3.11+ built-in tomllib first
        try:
            import tomllib
        except ImportError:
            # Fall back to tomli for older Python versions
            try:
                import tomli as tomllib
            except ImportError:
                tomllib = None

        if tomllib:
            with open(pyproject_path, "rb") as f:
                pyproject = tomllib.load(f)
                __version__ = (
                    pyproject.get("tool", {})
                    .get("poetry", {})
                    .get("version", "unknown")
                )
        else:
            # Fallback: simple regex parse if no TOML library available
            import re

            content = pyproject_path.read_text()
            match = re.search(r'version\s*=\s*"([^"]+)"', content)
            __version__ = match.group(1) if match else "unknown"
    else:
        __version__ = "unknown"
except Exception:
    __version__ = "unknown"
