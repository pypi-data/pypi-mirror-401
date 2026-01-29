from importlib.metadata import version, PackageNotFoundError


def get_version() -> str:
    try:
        return version("requestly")
    except PackageNotFoundError:
        return "0.0.0"
