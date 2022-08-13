from importlib.metadata import version

try:
    __version__ = version("roboswag")
except Exception:  # pragma: no cover
    pass
