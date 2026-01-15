from .core.cpp_api import CppApi
from .core import cssl_bridge as CSSL
import warnings
import os
from pathlib import Path

__version__ = "4.6.8"
__all__ = ["CppApi", "CSSL"]

# Module-level cache for C++ modules
_api_instance = None
_loaded_modules = {}

def _get_api():
    """Get or create singleton CppApi instance.

    Checks INCLUDECPP_PROJECT env var for project path when running
    from a different directory (e.g., via 'includecpp server run').
    """
    global _api_instance
    if _api_instance is None:
        # Check for project path from environment (set by 'server run -p')
        project_path = os.environ.get('INCLUDECPP_PROJECT')
        if project_path:
            config_path = Path(project_path) / 'cpp.proj'
            if config_path.exists():
                _api_instance = CppApi(config_path=config_path)
            else:
                _api_instance = CppApi()
        else:
            _api_instance = CppApi()
    return _api_instance

def __getattr__(name: str):
    """Enable: from includecpp import fast_list

    This hook is called when Python cannot find an attribute in this module.
    It allows dynamic C++ module loading via the import system.
    """
    if name.startswith('_'):
        raise AttributeError(f"module 'includecpp' has no attribute '{name}'")

    if name in _loaded_modules:
        return _loaded_modules[name]

    api = _get_api()

    if name not in api.registry:
        available = list(api.registry.keys())
        raise AttributeError(
            f"Module '{name}' not found. "
            f"Available: {available}. "
            f"Run 'includecpp rebuild' first."
        )

    if api.need_update(name):
        warnings.warn(
            f"Module '{name}' source files changed. "
            f"Run 'includecpp rebuild' to update.",
            UserWarning
        )

    module = api.include(name)
    _loaded_modules[name] = module
    return module

def __dir__():
    """List available attributes including C++ modules."""
    base = ['CppApi', 'CSSL', '__version__']
    try:
        api = _get_api()
        return sorted(set(base + list(api.registry.keys())))
    except Exception:
        return base
