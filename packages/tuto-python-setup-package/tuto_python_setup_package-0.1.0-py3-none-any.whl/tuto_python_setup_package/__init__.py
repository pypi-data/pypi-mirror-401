"""tuto-python-setup-package - Tutorial package for Python setup workflow"""

from tuto_python_setup_package._version import __version__

__all__ = ["__version__"]


def hello() -> str:
    """Return a greeting message."""
    return "Hello from tuto-python-setup-package!"
