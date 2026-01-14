from geoexpress.core.base import GeoExpressCommand

_echoid = GeoExpressCommand("echoid")


def locking_code():
    return _echoid.run([])
