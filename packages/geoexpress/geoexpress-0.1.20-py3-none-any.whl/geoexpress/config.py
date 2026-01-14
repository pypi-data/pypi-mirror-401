import os
from pathlib import Path
from geoexpress.exceptions import GeoExpressNotInstalled


def find_geoexpress_bin() -> Path:
    candidates = []

    if os.name == "nt":
        candidates.append(Path("C:/Program Files/LizardTech/GeoExpress/bin"))
    else:
        candidates.append(Path("/usr/local/LizardTech/GeoExpress/bin"))

    for path in candidates:
        if path.exists():
            return path

    raise GeoExpressNotInstalled(
        "GeoExpress not installed.\n"
        "Please download and install GeoExpress from Extensis."
    )


GEOEXPRESS_BIN = find_geoexpress_bin()
