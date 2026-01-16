from __future__ import annotations

from typing import TYPE_CHECKING

import pyarrow

from chalkdf._chalk_import import _get_lazy_frame_cls, has_chalk

if TYPE_CHECKING:
    from chalk.df.lazyframe import LazyFramePlaceholder


class DataFrameMeta(type):
    def __call__(cls, *args, **kwargs):
        # Intercept constructor: DataFrame(...)
        if has_chalk():
            try:
                LazyFrame: type[LazyFramePlaceholder] | None = _get_lazy_frame_cls()
            except ImportError:
                LazyFrame = None

            if LazyFrame is not None:
                # If args[0] is dict/arrow, return LazyFrame.
                # If args[0] is ChalkTable, return super().__call__.
                root = args[0] if args else kwargs.get("root")
                if isinstance(root, (dict, pyarrow.Table, pyarrow.RecordBatch)):
                    lf = LazyFrame()
                    if isinstance(root, dict):
                        return lf.from_dict(root)
                    else:
                        return lf.from_arrow(root)
        return super().__call__(*args, **kwargs)

    def __getattribute__(cls, name):
        # Intercept attribute access: DataFrame.scan
        # Note: __getattribute__ is called for EVERYTHING.

        # First, get the real attribute
        real_attr = super().__getattribute__(name)

        # If it's a private attribute or magic method, return it
        if name.startswith("_"):
            return real_attr

        if has_chalk():
            # Check condition
            try:
                LazyFrame: type[LazyFramePlaceholder] | None = _get_lazy_frame_cls()
            except ImportError:
                LazyFrame = None

            if LazyFrame is not None:
                if callable(real_attr):
                    # return a proxy wrapper
                    def proxy(*args, **kwargs):
                        # Create a fresh LazyFrame and call the method on it
                        # e.g. LazyFrame().scan(...)
                        return getattr(LazyFrame(), name)(*args, **kwargs)

                    return proxy

        return real_attr
