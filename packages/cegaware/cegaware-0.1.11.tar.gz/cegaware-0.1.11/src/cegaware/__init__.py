from .Function import *
from .Enum import *
from .Struct import *

try:
    # Python 3.8+
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Pour Python <3.8
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("cegaware")
except PackageNotFoundError:
    # Version inconnue si package non installé
    __version__ = "0.0.0"