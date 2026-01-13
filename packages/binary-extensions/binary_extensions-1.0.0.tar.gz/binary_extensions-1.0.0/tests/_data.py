# Binary extensions used for tests
BINARY_EXAMPLES = ["png", "jpg", "gif", "pdf", "zip", "mp3", "mp4", "exe", "dll"]
NON_BINARY_EXAMPLES = ["txt", "md", "py", "js", "html", "css", "json", "xml"]

# Paths for testing is_binary_path
BINARY_PATHS = [
    "image.png",
    "photo.jpg",
    "document.pdf",
    "archive.zip",
    "video.mp4",
    "audio.mp3",
    "program.exe",
]

NON_BINARY_PATHS = [
    "readme.txt",
    "script.py",
    "style.css",
    "index.html",
    "data.json",
    "config.xml",
]

HIDDEN_BINARY_PATHS = [".hidden.png", ".config.jpg"]
HIDDEN_NON_BINARY_PATHS = [".gitignore"]

