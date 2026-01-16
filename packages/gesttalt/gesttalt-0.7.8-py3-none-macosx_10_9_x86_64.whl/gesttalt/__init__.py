"""
Gesttalt - Content CRUD bindings powered by Zig.

Example usage:
    >>> from gesttalt import create_snippet, create_post, create_note
    >>> create_snippet(".", 1735148400, "Example snippet", "const x = 1;", "example.zig")
    >>> create_post(".", "hello-world", "Hello", "My first post")
    >>> create_note(".", 1735148400, body="Quick update")
"""

from .core import (
    create_snippet,
    list_snippets,
    read_snippet,
    update_snippet,
    delete_snippet,
    create_post,
    list_posts,
    read_post,
    update_post,
    delete_post,
    create_note,
    list_notes,
    read_note,
    update_note,
    delete_note,
    GesttaltError,
    SnippetError,
)

__version__ = "0.7.5"
__all__ = [
    "create_snippet",
    "list_snippets",
    "read_snippet",
    "update_snippet",
    "delete_snippet",
    "create_post",
    "list_posts",
    "read_post",
    "update_post",
    "delete_post",
    "create_note",
    "list_notes",
    "read_note",
    "update_note",
    "delete_note",
    "GesttaltError",
    "SnippetError",
    "__version__",
]
