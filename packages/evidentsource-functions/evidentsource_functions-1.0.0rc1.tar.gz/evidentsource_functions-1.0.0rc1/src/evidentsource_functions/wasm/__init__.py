"""WASM component bindings and adapters.

This module provides the bridge between componentize-py generated types
and the EvidentSource SDK types.
"""

from evidentsource_functions.wasm.adapters import (
    StateChangeAdapter,
    StateViewAdapter,
)

__all__ = [
    "StateChangeAdapter",
    "StateViewAdapter",
]
