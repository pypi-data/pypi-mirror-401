import io
from typing import Final

import helpers
import pytest

from cate import core


class TestFromJSON:
    VALID_INPUTS: Final = {
        'full': '[[1, 1], [1, 2]]',
    }
    MALFORMED_JSON_INPUTS: Final = {
        'empty': '',
        'missing_closing_bracket': '[',
        'extra_comma': '[[0, 0], [0, 0],]',
    }
    INVALID_INPUTS: Final = {
        'None': 'null',
        'boolean': 'true',
        'empty': '[]',
        'dict': '{"super": "matrix"}',
        'string_coeff': '[["1", 0], [0, 1]]',
        'float_coeff': '[[1.0, 0], [0, 1]]',
        'list_of_dict': '[{}]',
    }

    @helpers.dict_parametrize('input_', VALID_INPUTS)
    def test_valid_input(self, input_):
        fp = io.StringIO(input_)
        # check no exception is raised
        core.Template.from_json(fp)

    @helpers.dict_parametrize('input_', MALFORMED_JSON_INPUTS)
    def test_malformed_json(self, input_):
        fp = io.StringIO(input_)
        with pytest.raises(TypeError, match=r'^Malformed JSON$'):
            core.Template.from_json(fp)

    @helpers.dict_parametrize('input_', INVALID_INPUTS)
    def test_invalid_input(self, input_):
        fp = io.StringIO(input_)
        with pytest.raises(TypeError, match=r'^Invalid input structure$'):
            core.Template.from_json(fp)
