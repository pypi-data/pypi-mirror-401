# # councillm/runtime.py

# _RUNTIME = {}


# def configure_runtime(generators, critics, chairman):
#     if not generators or not chairman:
#         raise ValueError("At least one generator and one chairman required")

#     _RUNTIME["generators"] = generators
#     _RUNTIME["critics"] = critics
#     _RUNTIME["chairman"] = chairman


# def get_runtime():
#     if not _RUNTIME:
#         raise RuntimeError("Council not configured yet")
#     return _RUNTIME

# councillm/runtime.py

_RUNTIME: dict = {}


def configure_runtime(*, generators, critics=None, chairman):
    """
    Configure the LLM Council roles at runtime.
    """
    if not generators:
        raise ValueError("At least one GENERATOR model is required")
    if not chairman:
        raise ValueError("A CHAIRMAN model is required")

    _RUNTIME.clear()
    _RUNTIME["generators"] = list(generators)
    _RUNTIME["critics"] = list(critics) if critics else []
    _RUNTIME["chairman"] = chairman


def is_configured() -> bool:
    return bool(_RUNTIME)


def get_runtime() -> dict:
    if not _RUNTIME:
        raise RuntimeError(
            "Council not configured. Run configuration before asking questions."
        )
    return _RUNTIME
