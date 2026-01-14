from geoexpress.core.base import GeoExpressCommand

_meta = GeoExpressCommand("mrsidgeometa")


def set_metadata(image: str, key: str, value: str) -> str:
    """
    Set a metadata key-value pair on a MrSID file.
    """
    return _meta.run([
        "-set", f"{key}={value}",
        image
    ])


def get_metadata(image: str) -> str:
    """
    Get all metadata from a MrSID file.
    """
    return _meta.run([image])
