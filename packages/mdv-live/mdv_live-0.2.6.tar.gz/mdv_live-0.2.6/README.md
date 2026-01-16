# MDV - Markdown Viewer

ファイルツリー + ライブプレビュー + ファイルブラウザ機能付きマークダウンビューア

## Features

- 📁 左側にフォルダツリー表示
- 📄 マークダウンをHTMLでレンダリング
- 🔄 ファイル更新時に自動リロード（WebSocket）
- 🎨 シンタックスハイライト（highlight.js）
- 📊 Mermaid図のレンダリング対応
- 🌙 ダーク/ライトテーマ切り替え
- ✏️ インラインエディタ（Cmd+E）
- 📥 PDF出力（Cmd+P）
- 🎬 動画/音声プレビュー

### ファイルブラウザ機能

- 右クリックコンテキストメニュー
  - ファイル：開く、ダウンロード、名前変更、パスコピー、削除
  - フォルダ：新規フォルダ、アップロード、名前変更、パスコピー、削除
- ドラッグ&ドロップ
  - ファイル/フォルダをフォルダへ移動
  - 外部ファイルをドロップしてアップロード
- キーボードショートカット
  - Delete/Backspace：選択アイテムを削除
  - F2：名前変更

## Installation

```bash
# PyPIからインストール（推奨）
pip install mdv-live

# または開発版をインストール
git clone https://github.com/panhouse/mdv.git
cd mdv
pip install -e .
```

## Usage

```bash
# カレントディレクトリを表示
mdv

# 特定のディレクトリを表示
mdv ./project/

# 特定のファイルを開く
mdv README.md

# ポート指定
mdv -p 9000

# ブラウザを自動で開かない
mdv --no-browser

# MarkdownをPDFに変換
mdv --pdf README.md
mdv --pdf README.md -o output.pdf

# サーバー管理
mdv -l        # 稼働中のサーバー一覧
mdv -k -a     # 全サーバー停止
mdv -k <PID>  # 特定サーバー停止
```

## Keyboard Shortcuts

| ショートカット | 機能 |
|---------------|------|
| Cmd/Ctrl + B | サイドバー表示切替 |
| Cmd/Ctrl + E | 編集モード切替 |
| Cmd/Ctrl + S | 保存（編集モード時） |
| Cmd/Ctrl + P | PDF出力 |
| Cmd/Ctrl + W | タブを閉じる |
| Delete/Backspace | ファイル/フォルダ削除 |
| F2 | 名前変更 |

## Requirements

- Python 3.9+
- FastAPI
- uvicorn
- markdown-it-py
- python-multipart
