from importlib.metadata import version

from roboswag.model import APIModel

try:
    __version__ = version("roboswag")
except Exception:  # pragma: no cover
    pass
