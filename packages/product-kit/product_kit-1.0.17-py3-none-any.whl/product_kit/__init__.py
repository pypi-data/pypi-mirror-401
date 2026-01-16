"""Product Kit - CLI to scaffold Product Kit framework."""

from importlib.metadata import PackageNotFoundError, version


try:
    __version__ = version("product-kit")
except PackageNotFoundError:
    __version__ = "0.0.0"
