try:
    from importlib import metadata
except ImportError:  # pragma: no cover
    import importlib_metadata as metadata  # type: ignore

def get_version():
    """Retrieve installed binwalk version."""
    try:
        return metadata.version("binwalk")
    except Exception:
        return "0.0"

__version__ = get_version()
