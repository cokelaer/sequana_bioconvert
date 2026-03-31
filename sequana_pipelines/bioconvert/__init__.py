from importlib.metadata import PackageNotFoundError, version

try:
    version = version("sequana-bioconvert")
except PackageNotFoundError:
    version = "unknown"
