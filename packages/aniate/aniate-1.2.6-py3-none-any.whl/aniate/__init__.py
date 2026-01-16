"""
Aniate - Terminal Intelligence Layer
"""

__version__ = "1.2.1"
__author__ = "Kabir Murjani"

# Lazy imports - don't load at package import time
def __getattr__(name):
    if name == "app":
        from .cli import app
        return app
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["app"]
