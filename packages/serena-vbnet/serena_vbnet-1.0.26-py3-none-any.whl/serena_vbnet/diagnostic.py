#!/usr/bin/env python3
"""
Diagnostic script to inspect Serena API compatibility.
Run this on any system to understand what Serena API methods are available.
"""

import sys
import json
import inspect


def inspect_serena_api():
    """Inspect the Serena API and report what's available."""

    results = {
        "python_version": sys.version,
        "serena_version": None,
        "errors": [],
        "api_info": {}
    }

    # Try importing serena
    try:
        import serena
        results["serena_version"] = getattr(serena, "__version__", "unknown")
    except ImportError as e:
        results["errors"].append(f"Cannot import serena: {e}")
        print(json.dumps(results, indent=2))
        return

    # Inspect SolidLanguageServer
    try:
        from serena.language_server import SolidLanguageServer
        init_sig = inspect.signature(SolidLanguageServer.__init__)
        results["api_info"]["SolidLanguageServer.__init__"] = {
            "parameters": [str(p) for p in init_sig.parameters.values()],
            "parameter_names": list(init_sig.parameters.keys())
        }
    except Exception as e:
        results["errors"].append(f"Cannot inspect SolidLanguageServer: {e}")

    # Inspect SolidLSPSettings
    try:
        from serena.config import SolidLSPSettings
        methods = [m for m in dir(SolidLSPSettings) if not m.startswith('_')]
        results["api_info"]["SolidLSPSettings"] = {
            "methods": methods,
            "has_get_ls_specific_settings": hasattr(SolidLSPSettings, 'get_ls_specific_settings')
        }
    except Exception as e:
        results["errors"].append(f"Cannot inspect SolidLSPSettings: {e}")

    # Inspect RuntimeDependencyCollection
    try:
        from serena.language_server.runtime_dependencies import RuntimeDependencyCollection

        # Get constructor signature
        init_sig = inspect.signature(RuntimeDependencyCollection.__init__)

        # Get all public methods
        methods = [m for m in dir(RuntimeDependencyCollection) if not m.startswith('_')]

        results["api_info"]["RuntimeDependencyCollection"] = {
            "init_parameters": [str(p) for p in init_sig.parameters.values()],
            "init_parameter_names": list(init_sig.parameters.keys()),
            "supports_overrides": "overrides" in init_sig.parameters,
            "all_methods": methods,
            "has_get_single_dep_for_current_platform": hasattr(RuntimeDependencyCollection, 'get_single_dep_for_current_platform'),
            "has_single_dep_for_current_platform": hasattr(RuntimeDependencyCollection, 'single_dep_for_current_platform'),
            "has_single_for_current_platform": hasattr(RuntimeDependencyCollection, 'single_for_current_platform'),
            "has_get_dependencies_for_current_platform": hasattr(RuntimeDependencyCollection, 'get_dependencies_for_current_platform')
        }

        # Try to get signatures of dependency methods
        for method_name in ['get_single_dep_for_current_platform', 'single_dep_for_current_platform', 'single_for_current_platform']:
            if hasattr(RuntimeDependencyCollection, method_name):
                method = getattr(RuntimeDependencyCollection, method_name)
                sig = inspect.signature(method)
                results["api_info"]["RuntimeDependencyCollection"][f"{method_name}_signature"] = {
                    "parameters": [str(p) for p in sig.parameters.values()],
                    "parameter_names": list(sig.parameters.keys())
                }

    except Exception as e:
        results["errors"].append(f"Cannot inspect RuntimeDependencyCollection: {e}")

    # Check for completions_available attribute
    try:
        from serena.language_server import SolidLanguageServer
        # This is tricky since it's an instance attribute, but we can check if __init__ sets it
        import dis
        bytecode = dis.Bytecode(SolidLanguageServer.__init__)
        instructions = list(bytecode)
        has_completions_available = any(
            instr.argval == 'completions_available'
            for instr in instructions
            if hasattr(instr, 'argval')
        )
        results["api_info"]["SolidLanguageServer"] = {
            "likely_has_completions_available": has_completions_available
        }
    except Exception as e:
        results["errors"].append(f"Cannot check completions_available: {e}")

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    inspect_serena_api()
