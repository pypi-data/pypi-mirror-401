"""
Template export primitives.
"""

import typing as _typing


class Exporter:
    _available_exporters: _typing.Final = {}

    def __init_subclass__(cls, *, alias=None, **kwargs):
        assert alias not in cls._available_exporters, (
            f"Shadowing existing alias: '{alias}'"
        )
        super().__init_subclass__(**kwargs)
        if alias is not None:
            cls._available_exporters[alias] = cls

    @classmethod
    def factory(cls, alias):
        try:
            return cls._available_exporters[alias]
        except KeyError:
            err_msg = f"Unknown Backend alias: '{alias}'"
            raise KeyError(err_msg) from None

    def write(self, template, *, output, color=True, complete_flow=False, scale=1.0):
        raise NotImplementedError


# Subclasses of Export need to be imported to trigger registration in
# Exporter._available_exporters, even though the class are unused.
# The imports need to be done Exporter definition.
from ._svg import SVGExporter  # noqa: E402, F401
