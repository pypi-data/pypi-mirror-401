from .core.cpp_api import CppApi
from .core import cssl_bridge as CSSL
import warnings
import os
import sys
from pathlib import Path

__version__ = "4.7.2"
__all__ = ["CppApi", "CSSL"]

# Module-level cache for C++ modules
_api_instance = None
_loaded_modules = {}
_frozen_api = None  # Cached API module for frozen (PyInstaller) mode

def _is_frozen():
    """Check if running in a frozen PyInstaller bundle."""
    return getattr(sys, 'frozen', False)

def _get_frozen_api():
    """Get the bundled API module when running frozen."""
    global _frozen_api
    if _frozen_api is None:
        try:
            # In PyInstaller, sys._MEIPASS is the temp extraction directory
            if hasattr(sys, '_MEIPASS'):
                meipass = sys._MEIPASS
                if meipass not in sys.path:
                    sys.path.insert(0, meipass)

                # Try to load api.pyd directly using importlib
                import importlib.util
                ext = '.pyd' if sys.platform == 'win32' else '.so'
                api_path = os.path.join(meipass, f'api{ext}')

                if os.path.exists(api_path):
                    spec = importlib.util.spec_from_file_location('api', api_path)
                    if spec and spec.loader:
                        api_module = importlib.util.module_from_spec(spec)
                        sys.modules['api'] = api_module
                        spec.loader.exec_module(api_module)
                        _frozen_api = api_module
                        return _frozen_api

            # Fallback to regular import
            import api
            _frozen_api = api
        except Exception:
            _frozen_api = False
    return _frozen_api if _frozen_api else None

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

    # In frozen mode (PyInstaller), try to get module from bundled api
    if _is_frozen():
        frozen_api = _get_frozen_api()
        if frozen_api and hasattr(frozen_api, name):
            module = getattr(frozen_api, name)
            _loaded_modules[name] = module
            return module
        # If not found in frozen api, raise helpful error
        raise AttributeError(
            f"Module '{name}' not found in bundled executable. "
            f"Ensure it was included during build with 'includecpp --make-exe'."
        )

    # Normal mode: use CppApi
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
