import pytest
from text_extensions import is_text_path
from ._data import TEXT_PATHS, NON_TEXT_PATHS, HIDDEN_TEXT_PATHS, HIDDEN_NON_TEXT_PATHS


@pytest.mark.parametrize("path", TEXT_PATHS + HIDDEN_TEXT_PATHS)
def test_text_paths_true(path):
    """Paths with known text extensions should return True"""
    assert is_text_path(path)


@pytest.mark.parametrize("path", NON_TEXT_PATHS + HIDDEN_NON_TEXT_PATHS)
def test_non_text_paths_false(path):
    """Paths without known text extensions should return False"""
    assert not is_text_path(path)


@pytest.mark.parametrize("path", ["", ".", "..", "file", "path/to/file", "file.name.png"])
def test_paths_without_extension_false(path):
    """Paths without extensions or with non-text extensions should return False"""
    assert not is_text_path(path)


@pytest.mark.parametrize(
    "path,expected",
    [
        ("file.backup.txt", True),
        ("archive.tar.gz", False),  # .gz is typically binary
        ("file.name.txt", True),
        ("C:\\Users\\file.txt", True),
        ("/path/to/document.txt", True),
        ("SCRIPT.PY", True),
        ("Document.MD", True),
        ("config.JSON", True),
        ("file.PNG", False),
        ("/path/to/script.py", True),
        ("folder/subfolder/file.js", True),
        ("file.", False),
    ]
)
def test_paths_various(path, expected):
    """Edge cases: multiple dots, OS paths, case insensitivity, directories"""
    assert is_text_path(path) == expected

