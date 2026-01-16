"""Core functionality for the Gesttalt Python binding."""

import ctypes
import json
import platform
from pathlib import Path
from typing import Any, Dict, Optional


class GesttaltError(Exception):
    """Base exception for Gesttalt errors."""
    pass


class SnippetError(GesttaltError):
    """Exception raised for snippet CRUD errors."""
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


ERROR_MESSAGES = {
    1: "Invalid timestamp",
    2: "Duplicate snippet",
    3: "Snippet not found",
    4: "Invalid extension",
    5: "Invalid description",
    6: "Invalid filename",
    7: "Parse error",
    8: "I/O error",
    9: "Out of memory",
    100: "Unknown error",
}


def _find_library() -> Path:
    system = platform.system()

    if system == "Darwin":
        dylib_name = "libgesttalt_ffi.dylib"
    elif system == "Windows":
        dylib_name = "gesttalt_ffi.dll"
    else:
        dylib_name = "libgesttalt_ffi.so"

    search_paths = [
        Path(__file__).parent / "lib",
        Path(__file__).parent.parent.parent.parent / "zig-out" / "lib",
        Path("/usr/local/lib"),
        Path("/usr/lib"),
    ]

    for search_path in search_paths:
        dylib_path = search_path / dylib_name
        if dylib_path.exists():
            return dylib_path

    raise GesttaltError(
        f"Could not find gesttalt library ({dylib_name}). "
        f"System: {system}. "
        "Make sure to install the correct platform-specific package."
    )


def _get_library():
    lib_path = _find_library()
    lib = ctypes.CDLL(str(lib_path))

    lib.gesttalt_snippet_create.argtypes = [
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(ctypes.c_char_p),
    ]
    lib.gesttalt_snippet_create.restype = ctypes.c_int

    lib.gesttalt_snippet_read.argtypes = [
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_char_p),
    ]
    lib.gesttalt_snippet_read.restype = ctypes.c_int

    lib.gesttalt_snippet_update.argtypes = [
        ctypes.c_char_p,
        ctypes.c_longlong,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.c_char_p,
    ]
    lib.gesttalt_snippet_update.restype = ctypes.c_int

    lib.gesttalt_snippet_delete.argtypes = [
        ctypes.c_char_p,
        ctypes.c_longlong,
    ]
    lib.gesttalt_snippet_delete.restype = ctypes.c_int

    lib.gesttalt_free.argtypes = [ctypes.c_char_p]
    lib.gesttalt_free.restype = None

    return lib


_lib: Optional[ctypes.CDLL] = None


def _ensure_library():
    global _lib
    if _lib is None:
        _lib = _get_library()
    return _lib


def _raise_for_code(code: int):
    if code == 0:
        return
    message = ERROR_MESSAGES.get(code, ERROR_MESSAGES[100])
    raise SnippetError(code, message)


def _encode_optional(value: Optional[str]) -> Optional[bytes]:
    if value is None:
        return None
    return value.encode("utf-8")


def create_snippet(
    project_dir: str,
    timestamp: int,
    description: str,
    body: str,
    filename: str,
) -> str:
    lib = _ensure_library()

    out_ptr = ctypes.c_char_p()
    result = lib.gesttalt_snippet_create(
        project_dir.encode("utf-8"),
        int(timestamp),
        description.encode("utf-8"),
        body.encode("utf-8"),
        filename.encode("utf-8"),
        ctypes.byref(out_ptr),
    )
    _raise_for_code(result)

    path = ctypes.string_at(out_ptr).decode("utf-8") if out_ptr.value else ""
    if out_ptr.value:
        lib.gesttalt_free(out_ptr)
    return path


def read_snippet(project_dir: str, timestamp: int) -> Optional[Dict[str, Any]]:
    lib = _ensure_library()

    out_ptr = ctypes.c_char_p()
    result = lib.gesttalt_snippet_read(
        project_dir.encode("utf-8"),
        int(timestamp),
        ctypes.byref(out_ptr),
    )
    _raise_for_code(result)

    if not out_ptr.value:
        return None
    raw = ctypes.string_at(out_ptr).decode("utf-8")
    lib.gesttalt_free(out_ptr)
    return json.loads(raw)


def update_snippet(
    project_dir: str,
    timestamp: int,
    description: Optional[str] = None,
    body: Optional[str] = None,
    filename: Optional[str] = None,
) -> None:
    lib = _ensure_library()

    result = lib.gesttalt_snippet_update(
        project_dir.encode("utf-8"),
        int(timestamp),
        _encode_optional(description),
        _encode_optional(body),
        _encode_optional(filename),
    )
    _raise_for_code(result)


def delete_snippet(project_dir: str, timestamp: int) -> None:
    lib = _ensure_library()

    result = lib.gesttalt_snippet_delete(
        project_dir.encode("utf-8"),
        int(timestamp),
    )
    _raise_for_code(result)
