import pytest
from text_extensions import TEXT_EXTENSIONS
from ._data import TEXT_EXAMPLES


def test_text_extensions_type_and_content():
    """Check TEXT_EXTENSIONS is a non-empty frozenset"""
    assert isinstance(TEXT_EXTENSIONS, frozenset)
    assert len(TEXT_EXTENSIONS) > 0


@pytest.mark.parametrize("ext", TEXT_EXAMPLES)
def test_common_text_extensions_present(ext):
    """Check that common text extensions are present in TEXT_EXTENSIONS"""
    assert ext in TEXT_EXTENSIONS

