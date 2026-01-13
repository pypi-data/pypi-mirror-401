# councillm/runtime.py

_RUNTIME = {}


def configure_runtime(generators, critics, chairman):
    if not generators or not chairman:
        raise ValueError("At least one generator and one chairman required")

    _RUNTIME["generators"] = generators
    _RUNTIME["critics"] = critics
    _RUNTIME["chairman"] = chairman


def get_runtime():
    if not _RUNTIME:
        raise RuntimeError("Council not configured yet")
    return _RUNTIME
