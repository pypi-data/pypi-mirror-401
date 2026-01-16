from __future__ import annotations

import importlib

from setuptools import setup


def _try_get_bdist_wheel():
    try:
        mod = importlib.import_module("wheel.bdist_wheel")
        return getattr(mod, "bdist_wheel", None)
    except Exception:  # pragma: no cover
        return None


_bdist_wheel = _try_get_bdist_wheel()


if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):  # type: ignore[misc]
        def finalize_options(self) -> None:
            super().finalize_options()
            # This package ships platform-specific shared libraries (ctypes).
            # Mark the wheel as non-pure so it gets a platform tag.
            self.root_is_pure = False


    setup(cmdclass={"bdist_wheel": bdist_wheel})
else:  # pragma: no cover
    setup()
