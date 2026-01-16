"""
MDV - Markdown Viewer Server
ファイルツリー表示 + マークダウンプレビュー + ホットリロード
"""

from __future__ import annotations

import asyncio
import json
import mimetypes
import os
import re
import shutil
import socket
import webbrowser
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Set

from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse as FastAPIFileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from .file_types import (
    FILE_TYPES,
    SUPPORTED_EXTENSIONS,
    SKIP_DIRECTORIES,
    SKIP_FILES,
    get_file_type,
    FileTypeInfo,
)
from .models import SaveFileRequest, CreateDirectoryRequest, MoveItemRequest


# === Application State ===

@dataclass
class AppState:
    """アプリケーション状態を管理"""
    root_path: Path = field(default_factory=Path.cwd)
    connected_clients: Set[WebSocket] = field(default_factory=set)
    current_watching_file: Optional[str] = None
    last_mtime: float = 0
    # ディレクトリmtime監視用（外部からのファイル追加検知）
    dir_mtimes: dict = field(default_factory=dict)

    def set_root_path(self, path: str | Path) -> None:
        self.root_path = Path(path).resolve()
        # ルートディレクトリのmtimeを初期化
        self._update_dir_mtimes()

    def add_client(self, client: WebSocket) -> None:
        self.connected_clients.add(client)

    def remove_client(self, client: WebSocket) -> None:
        self.connected_clients.discard(client)

    def set_watching_file(self, path: str) -> None:
        self.current_watching_file = path
        # 監視ファイル変更時にmtimeをリセット
        try:
            self.last_mtime = os.path.getmtime(path)
        except OSError:
            self.last_mtime = 0

    def _update_dir_mtimes(self) -> None:
        """監視対象ディレクトリのmtimeを更新"""
        self.dir_mtimes = {}
        try:
            # ルートディレクトリ
            self.dir_mtimes[str(self.root_path)] = os.path.getmtime(self.root_path)
            # 直下のサブディレクトリ（1階層のみ）
            for entry in self.root_path.iterdir():
                if entry.is_dir() and entry.name not in SKIP_DIRECTORIES:
                    try:
                        self.dir_mtimes[str(entry)] = os.path.getmtime(entry)
                    except OSError:
                        pass
        except OSError:
            pass

    def check_dir_changes(self) -> bool:
        """ディレクトリのmtime変更をチェック（変更があればTrue）"""
        changed = False
        try:
            # ルートディレクトリをチェック
            current_mtime = os.path.getmtime(self.root_path)
            if self.dir_mtimes.get(str(self.root_path)) != current_mtime:
                changed = True

            # 直下のサブディレクトリをチェック
            for entry in self.root_path.iterdir():
                if entry.is_dir() and entry.name not in SKIP_DIRECTORIES:
                    try:
                        current = os.path.getmtime(entry)
                        path_str = str(entry)
                        if path_str not in self.dir_mtimes or self.dir_mtimes[path_str] != current:
                            changed = True
                            break
                    except OSError:
                        pass
        except OSError:
            pass

        if changed:
            self._update_dir_mtimes()
        return changed


# シングルトンインスタンス
state = AppState()


# === Rendering Functions ===

def escape_html(text: str) -> str:
    """HTMLエスケープ"""
    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# YAMLフロントマターのパターン（ファイル先頭の---で囲まれた部分）
_FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*(\n|$)', re.DOTALL)

# 見出し後のYAMLメタデータブロック（---で囲まれたkey: value形式）
# 例: # Title\n\n---\nname: foo\n---
_YAML_BLOCK_PATTERN = re.compile(
    r'(^|\n)(#{1,6}\s+[^\n]+)\n+---\s*\n((?:[a-zA-Z_][a-zA-Z0-9_]*:\s*[^\n]*\n?)+)---\s*(\n|$)',
    re.MULTILINE
)

# Mermaidコードブロックのパターン
_MERMAID_PATTERN = re.compile(r'```mermaid\s*\n(.*?)\n```', re.DOTALL)


def _preprocess_markdown(content: str) -> tuple[str, list[str]]:
    """マークダウンの前処理（YAMLフロントマター変換、Mermaid保護）"""
    # YAMLフロントマターをコードブロックに変換（ファイル先頭）
    frontmatter_match = _FRONTMATTER_PATTERN.match(content)
    if frontmatter_match:
        frontmatter_content = frontmatter_match.group(1)
        rest_of_content = content[frontmatter_match.end():]
        content = f"```yaml\n{frontmatter_content}\n```\n{rest_of_content}"

    # 見出し後のYAMLメタデータブロックをコードブロックに変換
    def replace_yaml_block(match: re.Match) -> str:
        prefix = match.group(1)  # 先頭の改行または空文字
        heading = match.group(2)  # 見出し
        yaml_content = match.group(3).rstrip('\n')  # YAMLコンテンツ
        suffix = match.group(4)  # 末尾の改行または空文字
        return f"{prefix}{heading}\n\n```yaml\n{yaml_content}\n```{suffix}"

    content = _YAML_BLOCK_PATTERN.sub(replace_yaml_block, content)

    # Mermaidコードブロックを保護
    mermaid_blocks: list[str] = []

    def replace_mermaid(match: re.Match) -> str:
        mermaid_blocks.append(match.group(1))
        return f"<!--MERMAID_PLACEHOLDER_{len(mermaid_blocks) - 1}-->"

    content = _MERMAID_PATTERN.sub(replace_mermaid, content)

    return content, mermaid_blocks


def _postprocess_markdown(html: str, mermaid_blocks: list[str]) -> str:
    """マークダウンの後処理（Mermaid復元）"""
    # Mermaidコードブロックを復元
    for i, mermaid_code in enumerate(mermaid_blocks):
        placeholder = f"<!--MERMAID_PLACEHOLDER_{i}-->"
        escaped_code = escape_html(mermaid_code)
        mermaid_html = f'<pre><code class="language-mermaid">{escaped_code}</code></pre>'
        html = html.replace(f"<p>{placeholder}</p>", mermaid_html)
        html = html.replace(placeholder, mermaid_html)

    return html


# markdown-it-pyのインスタンスを作成（シングルトン）
_md_parser: Optional[MarkdownIt] = None


def _get_md_parser() -> MarkdownIt:
    """markdown-it-pyパーサーを取得（遅延初期化）"""
    global _md_parser
    if _md_parser is None:
        _md_parser = MarkdownIt("commonmark", {"html": True, "typographer": True, "breaks": True})
        _md_parser.enable("table")
        _md_parser.enable("strikethrough")
        _md_parser.use(tasklists_plugin)
    return _md_parser


def render_markdown(content: str) -> str:
    """マークダウンをHTMLに変換（markdown-it-py使用、行番号付き）"""
    content, mermaid_blocks = _preprocess_markdown(content)
    md = _get_md_parser()

    # トークンを取得して data-line 属性を追加
    tokens = md.parse(content)
    for token in tokens:
        if token.map and len(token.map) >= 1:
            # _open トークンに data-line を追加
            if token.attrs is None:
                token.attrs = {}
            token.attrs["data-line"] = str(token.map[0])

    html = md.renderer.render(tokens, md.options, {})
    return _postprocess_markdown(html, mermaid_blocks)


def render_code(content: str, lang: Optional[str] = None) -> str:
    """コードをシンタックスハイライト用HTMLに変換"""
    escaped = escape_html(content)
    lang_class = f"language-{lang}" if lang else ""
    return f'<pre><code class="{lang_class}">{escaped}</code></pre>'


def render_text(content: str) -> str:
    """プレーンテキストをHTMLに変換"""
    escaped = escape_html(content)
    return f'<pre class="plain-text">{escaped}</pre>'


def render_file_content(content: str, file_info: FileTypeInfo) -> str:
    """ファイルタイプに応じてコンテンツをレンダリング"""
    if file_info.type == "markdown":
        return render_markdown(content)
    elif file_info.type == "code":
        return render_code(content, file_info.lang)
    else:
        return render_text(content)


# === WebSocket Broadcasting ===

async def broadcast_tree_update() -> None:
    """全クライアントにファイルツリー更新を通知"""
    if not state.connected_clients:
        return

    try:
        tree = get_file_tree(state.root_path)
        message = json.dumps({
            "type": "tree_update",
            "tree": tree,
        })

        disconnected = []
        for client in state.connected_clients:
            try:
                await client.send_text(message)
            except Exception:
                disconnected.append(client)

        for client in disconnected:
            state.remove_client(client)

    except Exception as e:
        print(f"Error broadcasting tree update: {e}")


async def broadcast_file_update(file_path: str) -> None:
    """全クライアントにファイル更新を通知"""
    if not state.connected_clients:
        return

    try:
        path = Path(file_path)
        file_info = get_file_type(path.suffix)

        if not file_info:
            return

        # メッセージ作成
        if file_info.type == "image":
            message = {
                "type": "file_update",
                "path": file_path,
                "fileType": "image",
                "reload": True,
            }
        else:
            content = path.read_text(encoding="utf-8")
            html_content = render_file_content(content, file_info)
            message = {
                "type": "file_update",
                "path": file_path,
                "content": html_content,
                "raw": content,
                "fileType": file_info.type,
            }

        message_json = json.dumps(message)

        # 全クライアントに送信
        disconnected = []
        for client in state.connected_clients:
            try:
                await client.send_text(message_json)
            except Exception:
                disconnected.append(client)

        # 切断されたクライアントを削除
        for client in disconnected:
            state.remove_client(client)

    except Exception as e:
        print(f"Error broadcasting update: {e}")


# === File Watcher (Polling) ===

async def file_watcher() -> None:
    """ファイル変更を監視（ポーリング方式、gripと同じアプローチ）"""
    dir_check_counter = 0
    while True:
        await asyncio.sleep(0.3)  # 0.3秒間隔でチェック

        if not state.connected_clients:
            continue

        # ファイル変更チェック
        if state.current_watching_file:
            try:
                mtime = os.path.getmtime(state.current_watching_file)
                if mtime != state.last_mtime:
                    state.last_mtime = mtime
                    await broadcast_file_update(state.current_watching_file)
            except OSError:
                pass  # ファイルが存在しない場合は無視

        # ディレクトリ変更チェック（3回に1回=約1秒間隔）
        # 外部からのファイル追加・削除を検知
        dir_check_counter += 1
        if dir_check_counter >= 3:
            dir_check_counter = 0
            if state.check_dir_changes():
                await broadcast_tree_update()


# === File Tree ===

def get_file_tree(root: Path, max_depth: int = 1, current_depth: int = 0) -> list:
    """ディレクトリツリーを取得（サポートするファイルタイプのみ）

    Args:
        root: 走査するディレクトリ
        max_depth: 最大深さ（1=直下のみ、0=無制限）
        current_depth: 現在の深さ（内部用）
    """
    items = []

    try:
        entries = sorted(
            root.iterdir(),
            key=lambda x: (not x.is_dir(), x.name.lower())
        )
    except (PermissionError, OSError, TimeoutError):
        # ネットワークドライブ等でタイムアウトする場合もスキップ
        return items

    for entry in entries:
        # 特定ディレクトリをスキップ
        if entry.name in SKIP_DIRECTORIES:
            continue
        # ゴミファイルをスキップ
        if entry.name in SKIP_FILES:
            continue

        rel_path = str(entry.relative_to(state.root_path))

        if entry.is_dir():
            # 深さ制限チェック（max_depth=0は無制限）
            if max_depth > 0 and current_depth >= max_depth:
                # 子要素は遅延読み込み（loaded=Falseで未読み込みを示す）
                items.append({
                    "name": entry.name,
                    "path": rel_path,
                    "type": "directory",
                    "children": [],
                    "loaded": False,
                })
            else:
                children = get_file_tree(entry, max_depth, current_depth + 1)
                items.append({
                    "name": entry.name,
                    "path": rel_path,
                    "type": "directory",
                    "children": children,
                    "loaded": True,
                })
        elif entry.suffix.lower() in SUPPORTED_EXTENSIONS:
            file_info = FILE_TYPES[entry.suffix.lower()]
            items.append({
                "name": entry.name,
                "path": rel_path,
                "type": "file",
                "fileType": file_info.type,
                "icon": file_info.icon,
                "lang": file_info.lang,
            })

    return items


# === Security ===

def validate_path(requested_path: str) -> Path:
    """
    パスを検証してセキュアなPathオブジェクトを返す
    不正なパスの場合はHTTPExceptionを発生
    """
    file_path = state.root_path / requested_path

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # ROOT_PATH外へのアクセスを防ぐ
    try:
        file_path.resolve().relative_to(state.root_path.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    return file_path


def validate_path_for_write(requested_path: str) -> Path:
    """
    書き込み用のパス検証（ファイルが存在しなくてもOK）
    パストラバーサル防止 + ROOT_PATH内であることを確認
    """
    file_path = state.root_path / requested_path

    # ROOT_PATH外へのアクセスを防ぐ
    try:
        file_path.resolve().relative_to(state.root_path.resolve())
    except ValueError:
        raise HTTPException(status_code=403, detail="Access denied")

    return file_path


def sanitize_filename(filename: str) -> str:
    """ファイル名をサニタイズ（パス区切り文字を除去）"""
    return Path(filename).name


# === FastAPI Application ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクル管理"""
    # Startup
    asyncio.create_task(file_watcher())
    print("✅ File watcher started (polling mode)")
    yield
    # Shutdown
    print("👋 Server shutting down")


app = FastAPI(title="MDV - Markdown Viewer", lifespan=lifespan)


@app.get("/")
async def index() -> FastAPIFileResponse:
    """メインページ"""
    static_dir = Path(__file__).parent / "static"
    return FastAPIFileResponse(static_dir / "index.html")


@app.get("/api/tree")
async def get_tree() -> list:
    """ファイルツリーを取得（1階層のみ、遅延読み込み対応）"""
    return get_file_tree(state.root_path, max_depth=1)


@app.get("/api/tree/expand")
async def expand_tree(path: str = Query(...)) -> list:
    """指定ディレクトリの子要素を取得（遅延読み込み用）"""
    dir_path = validate_path(path)

    if not dir_path.is_dir():
        raise HTTPException(status_code=400, detail="Not a directory")

    # 指定ディレクトリの直下1階層のみ取得
    return get_file_tree(dir_path, max_depth=1)


@app.get("/api/info")
async def get_info() -> dict:
    """サーバー情報を取得"""
    return {
        "rootPath": str(state.root_path),
        "rootName": state.root_path.name or str(state.root_path)
    }


@app.get("/api/file")
async def get_file(path: str = Query(...)) -> dict:
    """ファイルを取得してレンダリング"""
    file_path = validate_path(path)

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    file_info = get_file_type(file_path.suffix)
    if not file_info:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # 監視対象を更新
    state.set_watching_file(str(file_path.resolve()))

    # 画像の場合
    if file_info.type == "image":
        return {
            "path": path,
            "name": file_path.name,
            "fileType": file_info.type,
            "imageUrl": f"/api/image?path={path}",
        }

    # PDFの場合
    if file_info.type == "pdf":
        return {
            "path": path,
            "name": file_path.name,
            "fileType": file_info.type,
            "pdfUrl": f"/api/pdf?path={path}",
        }

    # 動画の場合
    if file_info.type == "video":
        return {
            "path": path,
            "name": file_path.name,
            "fileType": file_info.type,
            "mediaUrl": f"/api/media?path={path}",
        }

    # 音声の場合
    if file_info.type == "audio":
        return {
            "path": path,
            "name": file_path.name,
            "fileType": file_info.type,
            "mediaUrl": f"/api/media?path={path}",
        }

    # テキスト系ファイルを読み込み
    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Cannot read binary file as text")

    html_content = render_file_content(content, file_info)

    return {
        "path": path,
        "name": file_path.name,
        "content": html_content,
        "raw": content,
        "fileType": file_info.type,
        "lang": file_info.lang,
    }


@app.get("/api/image")
async def get_image(path: str = Query(...)) -> FastAPIFileResponse:
    """画像ファイルを返す"""
    file_path = validate_path(path)

    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type or not mime_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Not an image file")

    return FastAPIFileResponse(file_path, media_type=mime_type)


@app.get("/api/pdf")
async def get_pdf(path: str = Query(...)) -> FastAPIFileResponse:
    """PDFファイルを返す"""
    file_path = validate_path(path)

    if not file_path.suffix.lower() == ".pdf":
        raise HTTPException(status_code=400, detail="Not a PDF file")

    return FastAPIFileResponse(file_path, media_type="application/pdf")


@app.post("/api/file")
async def save_file(request: SaveFileRequest) -> dict:
    """ファイルを保存"""
    file_path = validate_path(request.path)

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    file_info = get_file_type(file_path.suffix)
    if not file_info or file_info.type == "image":
        raise HTTPException(status_code=400, detail="Cannot edit this file type")

    try:
        file_path.write_text(request.content, encoding="utf-8")
        return {"success": True, "path": request.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save: {str(e)}")


@app.delete("/api/file")
async def delete_file(path: str = Query(...)) -> dict:
    """ファイルまたはフォルダを削除"""
    file_path = validate_path(path)

    try:
        if file_path.is_dir():
            shutil.rmtree(file_path)
        else:
            file_path.unlink()
        # ツリー更新を通知
        await broadcast_tree_update()
        return {"success": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete: {str(e)}")


@app.get("/api/download")
async def download_file(path: str = Query(...)) -> FastAPIFileResponse:
    """ファイルをダウンロード（Content-Disposition: attachment）"""
    file_path = validate_path(path)

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    mime_type, _ = mimetypes.guess_type(str(file_path))
    return FastAPIFileResponse(
        file_path,
        media_type=mime_type or "application/octet-stream",
        filename=file_path.name
    )


@app.get("/api/media")
async def get_media(path: str = Query(...), request: Request = None) -> StreamingResponse:
    """動画/音声ストリーミング（Range requests対応）"""
    file_path = validate_path(path)

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    file_size = file_path.stat().st_size
    mime_type, _ = mimetypes.guess_type(str(file_path))
    mime_type = mime_type or "application/octet-stream"

    range_header = request.headers.get("range") if request else None

    if range_header:
        # Range: bytes=0-1000 形式をパース
        match = re.match(r"bytes=(\d*)-(\d*)", range_header)
        if match:
            start = int(match.group(1)) if match.group(1) else 0
            end = int(match.group(2)) if match.group(2) else file_size - 1

            if start >= file_size:
                raise HTTPException(status_code=416, detail="Range not satisfiable")

            end = min(end, file_size - 1)
            content_length = end - start + 1

            def stream_range():
                with open(file_path, "rb") as f:
                    f.seek(start)
                    remaining = content_length
                    while remaining > 0:
                        chunk_size = min(1024 * 1024, remaining)
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break
                        remaining -= len(chunk)
                        yield chunk

            return StreamingResponse(
                stream_range(),
                status_code=206,
                media_type=mime_type,
                headers={
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                    "Accept-Ranges": "bytes",
                    "Content-Length": str(content_length),
                }
            )

    # Range指定なしの場合は全体を返す
    def stream_file():
        with open(file_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                yield chunk

    return StreamingResponse(
        stream_file(),
        media_type=mime_type,
        headers={
            "Accept-Ranges": "bytes",
            "Content-Length": str(file_size),
        }
    )


@app.post("/api/upload")
async def upload_files(
    path: str = Form(""),
    files: List[UploadFile] = File(...)
) -> dict:
    """ファイルをアップロード（複数ファイル対応）"""
    target_dir = validate_path_for_write(path) if path else state.root_path

    # ディレクトリが存在しない場合は作成
    target_dir.mkdir(parents=True, exist_ok=True)

    if not target_dir.is_dir():
        raise HTTPException(status_code=400, detail="Target is not a directory")

    uploaded = []
    for file in files:
        if not file.filename:
            continue

        filename = sanitize_filename(file.filename)
        dest_path = target_dir / filename

        try:
            with open(dest_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            uploaded.append(filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to upload {filename}: {str(e)}")

    # ツリー更新を通知
    if uploaded:
        await broadcast_tree_update()

    return {"success": True, "uploaded": uploaded}


@app.post("/api/mkdir")
async def create_directory(request: CreateDirectoryRequest) -> dict:
    """新規フォルダを作成"""
    dir_path = validate_path_for_write(request.path)

    if dir_path.exists():
        raise HTTPException(status_code=400, detail="Directory already exists")

    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        # ツリー更新を通知
        await broadcast_tree_update()
        return {"success": True, "path": request.path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create directory: {str(e)}")


@app.post("/api/move")
async def move_item(request: MoveItemRequest) -> dict:
    """ファイル/フォルダを移動またはリネーム"""
    source_path = validate_path(request.source)
    dest_path = validate_path_for_write(request.destination)

    if dest_path.exists():
        raise HTTPException(status_code=400, detail="Destination already exists")

    try:
        shutil.move(str(source_path), str(dest_path))
        # ツリー更新を通知
        await broadcast_tree_update()
        return {"success": True, "source": request.source, "destination": request.destination}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to move: {str(e)}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """WebSocket接続を管理"""
    await websocket.accept()
    state.add_client(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "watch":
                file_path = state.root_path / message.get("path", "")
                if file_path.exists():
                    state.set_watching_file(str(file_path.resolve()))

    except WebSocketDisconnect:
        state.remove_client(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        state.remove_client(websocket)


# 静的ファイルをマウント
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# === Server Startup ===

def find_available_port(start_port: int, max_attempts: int = 100) -> int:
    """利用可能なポートを探す"""
    for offset in range(max_attempts):
        port = start_port + offset
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue

    raise RuntimeError(
        f"No available port found in range {start_port}-{start_port + max_attempts}"
    )


def start_server(
    root_path: str = ".",
    port: int = 8642,
    open_browser: bool = True,
    initial_file: Optional[str] = None,
) -> None:
    """サーバーを起動"""
    state.set_root_path(root_path)

    if not state.root_path.exists():
        print(f"Error: Path does not exist: {state.root_path}")
        return

    # 利用可能なポートを探す
    try:
        actual_port = find_available_port(port)
        if actual_port != port:
            print(f"⚠️  Port {port} is in use, using {actual_port} instead")
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    print(f"📁 Serving: {state.root_path}")
    print(f"🌐 URL: http://localhost:{actual_port}")

    # ブラウザを開く（サーバー起動後に遅延して開く）
    if open_browser:
        import threading
        url = f"http://localhost:{actual_port}"
        if initial_file:
            from urllib.parse import quote
            url += f"?file={quote(initial_file)}"

        def open_browser_delayed():
            import time
            time.sleep(0.5)  # サーバー起動を待つ
            webbrowser.open(url)

        threading.Thread(target=open_browser_delayed, daemon=True).start()

    # サーバー起動
    try:
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=actual_port,
            log_level="warning"
        )
        server = uvicorn.Server(config)
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    start_server()
