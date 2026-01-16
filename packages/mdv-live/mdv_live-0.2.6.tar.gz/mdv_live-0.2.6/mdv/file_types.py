"""
ファイルタイプの定義
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class FileTypeInfo:
    """ファイルタイプ情報"""
    type: str  # 'markdown', 'text', 'code', 'image'
    icon: str
    lang: Optional[str] = None


# ファイル拡張子とタイプのマッピング
FILE_TYPES: Dict[str, FileTypeInfo] = {
    # Markdown
    ".md": FileTypeInfo("markdown", "markdown"),
    ".markdown": FileTypeInfo("markdown", "markdown"),

    # Text
    ".txt": FileTypeInfo("text", "text"),
    ".text": FileTypeInfo("text", "text"),
    ".rst": FileTypeInfo("text", "text"),
    ".log": FileTypeInfo("text", "text"),

    # Config files
    ".json": FileTypeInfo("code", "json", "json"),
    ".yaml": FileTypeInfo("code", "yaml", "yaml"),
    ".yml": FileTypeInfo("code", "yaml", "yaml"),
    ".toml": FileTypeInfo("code", "toml", "toml"),
    ".ini": FileTypeInfo("code", "config", "ini"),
    ".cfg": FileTypeInfo("code", "config", "ini"),
    ".conf": FileTypeInfo("code", "config", "ini"),
    ".env": FileTypeInfo("code", "config", "bash"),

    # Code files
    ".py": FileTypeInfo("code", "python", "python"),
    ".js": FileTypeInfo("code", "javascript", "javascript"),
    ".ts": FileTypeInfo("code", "typescript", "typescript"),
    ".jsx": FileTypeInfo("code", "react", "javascript"),
    ".tsx": FileTypeInfo("code", "react", "typescript"),
    ".html": FileTypeInfo("code", "html", "html"),
    ".css": FileTypeInfo("code", "css", "css"),
    ".scss": FileTypeInfo("code", "css", "scss"),
    ".less": FileTypeInfo("code", "css", "less"),
    ".java": FileTypeInfo("code", "java", "java"),
    ".c": FileTypeInfo("code", "c", "c"),
    ".cpp": FileTypeInfo("code", "cpp", "cpp"),
    ".h": FileTypeInfo("code", "c", "c"),
    ".hpp": FileTypeInfo("code", "cpp", "cpp"),
    ".go": FileTypeInfo("code", "go", "go"),
    ".rs": FileTypeInfo("code", "rust", "rust"),
    ".rb": FileTypeInfo("code", "ruby", "ruby"),
    ".php": FileTypeInfo("code", "php", "php"),
    ".swift": FileTypeInfo("code", "swift", "swift"),
    ".kt": FileTypeInfo("code", "kotlin", "kotlin"),
    ".sh": FileTypeInfo("code", "shell", "bash"),
    ".bash": FileTypeInfo("code", "shell", "bash"),
    ".zsh": FileTypeInfo("code", "shell", "bash"),
    ".sql": FileTypeInfo("code", "database", "sql"),
    ".xml": FileTypeInfo("code", "xml", "xml"),
    ".graphql": FileTypeInfo("code", "graphql", "graphql"),
    ".vue": FileTypeInfo("code", "vue", "html"),
    ".svelte": FileTypeInfo("code", "svelte", "html"),

    # Template files
    ".j2": FileTypeInfo("code", "jinja2", "django"),
    ".jinja": FileTypeInfo("code", "jinja2", "django"),
    ".jinja2": FileTypeInfo("code", "jinja2", "django"),

    # Images
    ".png": FileTypeInfo("image", "image"),
    ".jpg": FileTypeInfo("image", "image"),
    ".jpeg": FileTypeInfo("image", "image"),
    ".gif": FileTypeInfo("image", "image"),
    ".svg": FileTypeInfo("image", "image"),
    ".webp": FileTypeInfo("image", "image"),
    ".ico": FileTypeInfo("image", "image"),
    ".bmp": FileTypeInfo("image", "image"),

    # PDF
    ".pdf": FileTypeInfo("pdf", "pdf"),

    # Video
    ".mp4": FileTypeInfo("video", "video"),
    ".webm": FileTypeInfo("video", "video"),
    ".mov": FileTypeInfo("video", "video"),
    ".avi": FileTypeInfo("video", "video"),
    ".mkv": FileTypeInfo("video", "video"),
    ".m4v": FileTypeInfo("video", "video"),

    # Audio
    ".mp3": FileTypeInfo("audio", "audio"),
    ".wav": FileTypeInfo("audio", "audio"),
    ".ogg": FileTypeInfo("audio", "audio"),
    ".flac": FileTypeInfo("audio", "audio"),
    ".m4a": FileTypeInfo("audio", "audio"),
    ".aac": FileTypeInfo("audio", "audio"),
}

# サポートする拡張子のセット
SUPPORTED_EXTENSIONS = frozenset(FILE_TYPES.keys())

# スキップするディレクトリ
SKIP_DIRECTORIES = frozenset([
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    ".git",
    "dist",
    "build",
    ".next",
    ".nuxt",
    ".cache",
    "coverage",
    ".pytest_cache",
    ".mypy_cache",
    ".Trash",
    ".Trashes",
    "Library",
    "OneDrive",
    "Dropbox",
    "Google Drive",
    "iCloud Drive",
])

# スキップするファイル（ゴミファイル）
SKIP_FILES = frozenset([
    ".DS_Store",
    ".localized",
    "Thumbs.db",
    "desktop.ini",
])


def get_file_type(extension: str) -> Optional[FileTypeInfo]:
    """拡張子からファイルタイプ情報を取得"""
    return FILE_TYPES.get(extension.lower())
