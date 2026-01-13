"""
Standard library module detection.

Detects whether a module is part of Python's standard library.
"""

from __future__ import annotations

import sys

# Minimal fallback list for Python < 3.10
# This covers the most common standard library modules
_STDLIB_FALLBACK = frozenset({
    # Built-in modules
    '__future__', '__main__', '_thread', 'abc', 'aifc', 'argparse', 'array',
    'ast', 'asynchat', 'asyncio', 'asyncore', 'atexit', 'audioop', 'base64',
    'bdb', 'binascii', 'binhex', 'bisect', 'builtins', 'bz2', 'calendar',
    'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop',
    'collections', 'colorsys', 'compileall', 'concurrent', 'configparser',
    'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt',
    'csv', 'ctypes', 'curses', 'dataclasses', 'datetime', 'dbm', 'decimal',
    'difflib', 'dis', 'distutils', 'doctest', 'email', 'encodings', 'enum',
    'errno', 'faulthandler', 'fcntl', 'filecmp', 'fileinput', 'fnmatch',
    'formatter', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass',
    'gettext', 'glob', 'graphlib', 'grp', 'gzip', 'hashlib', 'heapq', 'hmac',
    'html', 'http', 'imaplib', 'imghdr', 'imp', 'importlib', 'inspect', 'io',
    'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache',
    'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math',
    'mimetypes', 'mmap', 'modulefinder', 'msilib', 'msvcrt', 'multiprocessing',
    'netrc', 'nis', 'nntplib', 'numbers', 'operator', 'optparse', 'os',
    'ossaudiodev', 'parser', 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes',
    'pkgutil', 'platform', 'plistlib', 'poplib', 'posix', 'posixpath', 'pprint',
    'profile', 'pstats', 'pty', 'pwd', 'py_compile', 'pyclbr', 'pydoc', 'queue',
    'quopri', 'random', 're', 'readline', 'reprlib', 'resource', 'rlcompleter',
    'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex',
    'shutil', 'signal', 'site', 'smtpd', 'smtplib', 'sndhdr', 'socket',
    'socketserver', 'spwd', 'sqlite3', 'ssl', 'stat', 'statistics', 'string',
    'stringprep', 'struct', 'subprocess', 'sunau', 'symbol', 'symtable', 'sys',
    'sysconfig', 'syslog', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile',
    'termios', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter',
    'token', 'tokenize', 'tomllib', 'trace', 'traceback', 'tracemalloc', 'tty',
    'turtle', 'turtledemo', 'types', 'typing', 'typing_extensions', 'unicodedata',
    'unittest', 'urllib', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref',
    'webbrowser', 'winreg', 'winsound', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc',
    'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo',
})


def is_stdlib(module: str) -> bool:
    """
    Check if a module is part of Python's standard library.

    Uses sys.stdlib_module_names for Python 3.10+, falls back to
    a curated list for older versions.

    Args:
        module: Top-level module name (e.g., 'os', 'requests')

    Returns:
        True if the module is in the standard library, False otherwise

    Examples:
        >>> is_stdlib('os')
        True
        >>> is_stdlib('sys')
        True
        >>> is_stdlib('requests')
        False
        >>> is_stdlib('numpy')
        False
    """
    # Normalize module name
    module = module.lower()

    # Python 3.10+ has a built-in set of stdlib module names
    if hasattr(sys, 'stdlib_module_names'):
        return module in sys.stdlib_module_names

    # Fallback for older Python versions
    return module in _STDLIB_FALLBACK


def get_stdlib_modules() -> set[str]:
    """
    Get the set of all standard library module names.

    Returns:
        Set of stdlib module names

    Example:
        >>> stdlib = get_stdlib_modules()
        >>> 'os' in stdlib
        True
        >>> len(stdlib) > 100
        True
    """
    if hasattr(sys, 'stdlib_module_names'):
        return set(sys.stdlib_module_names)

    return set(_STDLIB_FALLBACK)


def filter_stdlib_modules(modules: list[str]) -> list[str]:
    """
    Filter out standard library modules from a list.

    Args:
        modules: List of module names

    Returns:
        List of modules that are NOT in stdlib (i.e., third-party)

    Example:
        >>> filter_stdlib_modules(['os', 'requests', 'sys', 'numpy'])
        ['requests', 'numpy']
    """
    return [m for m in modules if not is_stdlib(m)]


def separate_stdlib_and_third_party(
    modules: list[str]
) -> tuple[list[str], list[str]]:
    """
    Separate modules into stdlib and third-party lists.

    Args:
        modules: List of module names

    Returns:
        Tuple of (stdlib_modules, third_party_modules)

    Example:
        >>> separate_stdlib_and_third_party(['os', 'requests', 'sys', 'numpy'])
        (['os', 'sys'], ['requests', 'numpy'])
    """
    stdlib_modules = []
    third_party_modules = []

    for module in modules:
        if is_stdlib(module):
            stdlib_modules.append(module)
        else:
            third_party_modules.append(module)

    return stdlib_modules, third_party_modules

