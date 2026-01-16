"""
Gesttalt - Snippets CRUD bindings powered by Zig.

Example usage:
    >>> from gesttalt import create_snippet
    >>> create_snippet(".", 1735148400, "Example snippet", "const x = 1;", "example.zig")
"""

from .core import (
    create_snippet,
    read_snippet,
    update_snippet,
    delete_snippet,
    GesttaltError,
    SnippetError,
)

__version__ = "0.1.0"
__all__ = [
    "create_snippet",
    "read_snippet",
    "update_snippet",
    "delete_snippet",
    "GesttaltError",
    "SnippetError",
    "__version__",
]
