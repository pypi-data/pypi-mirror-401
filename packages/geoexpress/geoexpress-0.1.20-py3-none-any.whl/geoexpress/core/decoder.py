from geoexpress.core.base import GeoExpressCommand

_decoder = GeoExpressCommand("mrsidgeodecode")


def decode(input: str, output: str, options: dict = None):
    args = ["-i", input, "-o", output]

    if options:
        for k, v in options.items():
            args.extend([f"-{k}", str(v)])

    return _decoder.run(args)
