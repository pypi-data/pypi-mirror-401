"""
PyTilsX\n
By XXHieXX
"""

import inspect
from .number import *
from .boolean import *
from .list import *
from .all import *
from .other import *

__version__ = "1.0.0"
__author__ = "XXHieXX"
_modules = [number, boolean, list, all, other]

__all__ = []
for module in _modules:
    for name in dir(module):
        if not name.startswith("_"):
            obj = getattr(module, name)
            if inspect.isfunction(obj) or inspect.isclass(obj):
                __all__.append(name)