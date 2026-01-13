import pytest
from text_extensions import TEXT_EXTENSIONS, is_text_extension, is_text_path
from ._data import TEXT_EXAMPLES, TEXT_PATHS


@pytest.mark.parametrize("ext,path,expected", [
    ("txt", "file.txt", True),
    ("py", "script.py", True),
    ("png", "image.png", False),
    ("json", "data.json", True),
    ("pdf", "document.pdf", False),
])
def test_consistency_between_functions(ext, path, expected):
    """Both functions return consistent results"""
    assert is_text_extension(ext) == expected
    assert is_text_path(path) == expected


def test_all_extensions_in_set():
    """Ensure all extensions in TEXT_EXTENSIONS are recognized"""
    for ext in TEXT_EXTENSIONS:
        assert is_text_extension(ext) is True
        assert is_text_path(f"file.{ext}") is True

