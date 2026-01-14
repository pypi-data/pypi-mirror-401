from geoexpress.core.base import GeoExpressCommand

_encoder = GeoExpressCommand("mrsidgeoencoder")


def encode(input: str, output: str, options: dict = None):
    args = ["-i", input, "-o", output]

    if options:
        for k, v in options.items():
            flag = f"-{k}"
            if isinstance(v, bool):
                if v:
                    args.append(flag)
            else:
                args.extend([flag, str(v)])

    return _encoder.run(args)
