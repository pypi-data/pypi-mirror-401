# Text extensions used for tests
TEXT_EXAMPLES = ["txt", "md", "py", "js", "html", "css", "json", "xml", "yaml", "yml", "sh", "bat", "c", "cpp", "java", "go", "rs", "ts", "tsx", "jsx"]
NON_TEXT_EXAMPLES = ["png", "jpg", "gif", "pdf", "zip", "mp3", "mp4", "exe", "dll", "bin"]

# Paths for testing is_text_path
TEXT_PATHS = [
    "readme.txt",
    "script.py",
    "style.css",
    "index.html",
    "data.json",
    "config.xml",
    "document.md",
    "package.yaml",
    "script.sh",
    "main.c",
    "app.js",
]

NON_TEXT_PATHS = [
    "image.png",
    "photo.jpg",
    "document.pdf",
    "archive.zip",
    "video.mp4",
    "audio.mp3",
    "program.exe",
]

HIDDEN_TEXT_PATHS = [".gitignore", ".bashrc", ".vimrc", ".env"]
HIDDEN_NON_TEXT_PATHS = [".hidden.png", ".config.jpg"]

