import pytest


def dict_parametrize(argnames, paramsdict, indirect=False, scope=None):  # noqa: FBT002
    """Decorator to parametrize test functions from a (id, argvalue) dict."""
    ids, argvalues = zip(  # ensure id matches its argvalue
        *paramsdict.items(),
        strict=True,
    )
    return pytest.mark.parametrize(argnames, argvalues, indirect, ids, scope)
