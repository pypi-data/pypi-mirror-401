import os.path
from text_extensions._data import TEXT_EXTENSIONS, TEXT_EXTENSIONS_LOWER

__all__ = ["TEXT_EXTENSIONS", "TEXT_EXTENSIONS_LOWER", "is_text_extension", "is_text_path"]

def is_text_extension(ext: str) -> bool:
    """
    Return True if the given file extension is known to be text.

    Examples:
        >>> is_text_extension("txt")
        True
        >>> is_text_extension(".png")
        False
    """
    return ext.lower().lstrip(".") in TEXT_EXTENSIONS_LOWER

def is_text_path(file_path: str) -> bool:
    """
    Return True if the file path has a text file extension.

    Examples:
        >>> is_text_path("document.txt")
        True
        >>> is_text_path("image.png")
        False
        >>> is_text_path("/path/to/file.PY")
        True
        >>> is_text_path(".gitignore")
        True
    """
    basename = os.path.basename(file_path)
    _, ext = os.path.splitext(file_path)
    
    # Handle dotfiles (files starting with a dot that have no extension)
    # e.g., .gitignore, .bashrc, .vimrc
    if not ext and basename.startswith(".") and len(basename) > 1:
        # Treat the entire filename (without leading dot) as the extension
        ext = basename[1:]
    else:
        ext = ext.lstrip(".")
    
    return ext.lower() in TEXT_EXTENSIONS_LOWER

