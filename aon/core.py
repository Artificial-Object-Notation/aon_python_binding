"""
AON Python binding via ctypes.

Expects the shared library from the Rust core:
  - libaon_core.so   (Linux)
  - libaon_core.dylib (macOS)
  - aon_core.dll      (Windows)
"""

import ctypes
import os
import sys

if sys.platform.startswith("win"):
    LIB_NAME = "aon_core.dll"
elif sys.platform == "darwin":
    LIB_NAME = "libaon_core.dylib"
else:
    LIB_NAME = "libaon_core.so"

_here = os.path.dirname(__file__)

_candidates = [
    os.path.join(_here, LIB_NAME),
    os.path.join(os.getcwd(), LIB_NAME),
    LIB_NAME,
]

lib = None
for path in _candidates:
    try:
        lib = ctypes.CDLL(path)
        break
    except OSError:
        continue

if lib is None:
    raise RuntimeError(f"Não foi possível carregar {LIB_NAME}. Paths testadas: {_candidates}")

# Configure FFI signatures
lib.aon_json_to_aon.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
lib.aon_json_to_aon.restype  = ctypes.c_void_p

lib.aon_aon_to_json.argtypes = [ctypes.c_char_p]
lib.aon_aon_to_json.restype  = ctypes.c_void_p

lib.aon_last_error.argtypes = []
lib.aon_last_error.restype  = ctypes.c_void_p

lib.aon_free_string.argtypes = [ctypes.c_void_p]
lib.aon_free_string.restype  = None


def _get_last_error() -> str | None:
    """Retorna a última mensagem de erro da lib Rust, se existir."""
    err_ptr = lib.aon_last_error()
    if err_ptr:
        try:
            msg = ctypes.string_at(err_ptr).decode("utf-8", errors="ignore")
        except Exception:
            msg = "<erro ao decodificar mensagem de erro>"
        return msg
    return None


def json_to_aon(json_str: str, root: str) -> str:
    """
    Converte JSON (string) para AON (string), inferindo schema a partir do JSON.

    :param json_str: JSON em string.
    :param root: nome do schema raiz (ex: "users").
    """
    if not isinstance(json_str, str):
        raise TypeError("json_str deve ser string")
    if not isinstance(root, str):
        raise TypeError("root deve ser string")

    b_json = json_str.encode("utf-8")
    b_root = root.encode("utf-8")

    ptr = lib.aon_json_to_aon(b_json, b_root)
    if not ptr:
        err = _get_last_error()
        raise RuntimeError(f"AON error: {err}")

    try:
        result = ctypes.string_at(ptr).decode("utf-8")
    finally:
        lib.aon_free_string(ptr)

    return result


def aon_to_json(aon_str: str) -> str:
    """
    Converte AON (string) de volta para JSON (string).
    """
    if not isinstance(aon_str, str):
        raise TypeError("aon_str deve ser string")

    b_aon = aon_str.encode("utf-8")

    ptr = lib.aon_aon_to_json(b_aon)
    if not ptr:
        err = _get_last_error()
        raise RuntimeError(f"AON error: {err}")

    try:
        result = ctypes.string_at(ptr).decode("utf-8")
    finally:
        lib.aon_free_string(ptr)

    return result
