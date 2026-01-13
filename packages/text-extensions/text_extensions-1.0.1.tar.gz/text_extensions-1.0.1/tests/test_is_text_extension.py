import pytest
from text_extensions import is_text_extension
from ._data import TEXT_EXAMPLES, NON_TEXT_EXAMPLES


@pytest.mark.parametrize("ext", TEXT_EXAMPLES)
def test_text_extensions_true(ext):
    """Known text extensions should return True"""
    assert is_text_extension(ext)
    assert is_text_extension(f".{ext}")
    assert is_text_extension(ext.upper())
    assert is_text_extension(ext.title())


@pytest.mark.parametrize("ext", NON_TEXT_EXAMPLES)
def test_non_text_extensions_false(ext):
    """Non-text extensions should return False"""
    assert not is_text_extension(ext)


@pytest.mark.parametrize("ext", ["", ".", "unknown", "xyz"])
def test_edge_cases_false(ext):
    """Edge cases should return False"""
    assert not is_text_extension(ext)

