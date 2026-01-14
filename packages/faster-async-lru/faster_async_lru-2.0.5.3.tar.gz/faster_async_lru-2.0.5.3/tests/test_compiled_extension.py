import importlib.machinery

import faster_async_lru


def test_compiled_extension_loaded() -> None:
    origin = faster_async_lru.__spec__.origin  # type: ignore[union-attr]
    assert origin is not None
    assert origin.endswith(tuple(importlib.machinery.EXTENSION_SUFFIXES)), (
        "Expected faster_async_lru to be loaded from a compiled extension module, "
        f"got {origin!r}."
    )
