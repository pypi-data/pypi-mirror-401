#!/usr/bin/env python3
"""
MDV - Markdown Viewer CLI
どこからでも呼び出せるマークダウンビューア
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional



@dataclass
class ProcessInfo:
    """プロセス情報"""
    pid: str
    port: str
    command: str


def get_mdv_processes() -> List[ProcessInfo]:
    """稼働中のMDVサーバープロセスを取得"""
    try:
        result = subprocess.run(
            ["lsof", "-i", "-P", "-n"],
            capture_output=True,
            text=True,
        )

        processes = []
        for line in result.stdout.strip().split("\n"):
            if "python" not in line.lower() or "LISTEN" not in line:
                continue

            parts = line.split()
            if len(parts) < 9:
                continue

            pid = parts[1]

            # プロセスのコマンドラインを確認
            try:
                cmd_result = subprocess.run(
                    ["ps", "-p", pid, "-o", "command="],
                    capture_output=True,
                    text=True,
                )
                cmd = cmd_result.stdout.strip()

                if "mdv" not in cmd.lower():
                    continue

                # ポート番号を抽出
                port_info = parts[8] if len(parts) > 8 else ""
                port = ""
                if ":" in port_info:
                    port = port_info.split(":")[-1].split("->")[0]

                # コマンドを短縮
                display_cmd = cmd[:80] + "..." if len(cmd) > 80 else cmd

                processes.append(ProcessInfo(
                    pid=pid,
                    port=port,
                    command=display_cmd,
                ))
            except subprocess.SubprocessError:
                pass

        return processes

    except Exception as e:
        print(f"Error getting processes: {e}")
        return []


def list_servers() -> int:
    """稼働中のMDVサーバーを一覧表示"""
    processes = get_mdv_processes()

    if not processes:
        print("稼働中のMDVサーバーはありません")
        return 0

    print(f"稼働中のMDVサーバー: {len(processes)}件")
    print("-" * 60)
    print(f"{'PID':<8} {'Port':<8} {'Command'}")
    print("-" * 60)

    for proc in processes:
        print(f"{proc.pid:<8} {proc.port:<8} {proc.command}")

    print("-" * 60)
    print("\n停止: mdv -k -a (全停止) / mdv -k <PID> (個別停止)")
    return 0


def kill_server_by_pid(pid: str) -> int:
    """特定のPIDのサーバーを停止"""
    try:
        subprocess.run(["kill", pid], check=True)
        print(f"PID {pid} を停止しました")
        return 0
    except ValueError:
        print(f"無効なPID: {pid}")
        return 1
    except subprocess.CalledProcessError:
        print(f"PID {pid} の停止に失敗しました")
        return 1


def kill_all_servers() -> int:
    """全サーバーを停止"""
    processes = get_mdv_processes()

    if not processes:
        print("稼働中のMDVサーバーはありません")
        return 0

    print(f"{len(processes)}件のMDVサーバーを停止します...")

    killed = 0
    for proc in processes:
        try:
            subprocess.run(["kill", proc.pid], check=True)
            print(f"  PID {proc.pid} (port {proc.port}) を停止")
            killed += 1
        except subprocess.CalledProcessError:
            print(f"  PID {proc.pid} の停止に失敗")

    print(f"\n完了: {killed}/{len(processes)} 件を停止しました")
    return 0 if killed == len(processes) else 1


def kill_servers(target: Optional[str] = None, kill_all: bool = False) -> int:
    """MDVサーバーを停止"""
    if target:
        return kill_server_by_pid(target)

    if not kill_all:
        print("全サーバーを停止するには -a オプションが必要です")
        print("   mdv -k -a     全サーバーを停止")
        print("   mdv -k <PID>  特定のサーバーを停止")
        return 1

    return kill_all_servers()


def convert_to_pdf(input_path: Path, output_path: Optional[Path] = None) -> int:
    """MarkdownファイルをPDFに変換（md-to-pdfを使用）"""
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1

    if not input_path.is_file():
        print(f"Error: Not a file: {input_path}")
        return 1

    if input_path.suffix.lower() not in [".md", ".markdown"]:
        print(f"Error: Not a markdown file: {input_path}")
        return 1

    # md-to-pdfコマンドを構築（最新版は--out-dirをサポートしない）
    cmd = ["npx", "md-to-pdf", str(input_path)]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(input_path.parent),
        )

        if result.returncode != 0:
            if "npx: command not found" in result.stderr or "not found" in result.stderr:
                print("Error: npx (Node.js) is required for PDF conversion")
                print("Install Node.js: https://nodejs.org/")
                return 1
            print(f"Error: {result.stderr}")
            return 1

        # 出力ファイルパスを特定（md-to-pdfは入力と同じディレクトリに生成）
        default_output = input_path.with_suffix(".pdf")
        if output_path and output_path != default_output:
            # 出力先が指定されている場合、生成後に移動
            if default_output.exists():
                import shutil
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(default_output), str(output_path))
                print(f"PDF saved: {output_path}")
            else:
                print(f"Warning: Expected PDF not found at {default_output}")
                return 1
        else:
            print(f"PDF saved: {default_output}")

        return 0

    except FileNotFoundError:
        print("Error: npx (Node.js) is required for PDF conversion")
        print("Install Node.js: https://nodejs.org/")
        return 1
    except Exception as e:
        print(f"Error creating PDF: {e}")
        return 1


def start_viewer(
    path: str = ".",
    port: int = 8642,
    open_browser: bool = True
) -> None:
    """MDVサーバーを起動"""
    target_path = Path(path).resolve()

    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}")
        sys.exit(1)

    # ファイルが指定された場合、親ディレクトリをルートにして、そのファイルを開く
    initial_file: Optional[str] = None
    if target_path.is_file():
        initial_file = target_path.name
        target_path = target_path.parent

    from .server import start_server
    start_server(
        root_path=str(target_path),
        port=port,
        open_browser=open_browser,
        initial_file=initial_file,
    )


def create_parser() -> argparse.ArgumentParser:
    """引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        prog="mdv",
        description="MDV - Markdown Viewer with file tree + live preview",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mdv                    Start viewer in current directory
  mdv /path/to/dir       Start viewer in specified directory
  mdv README.md          Open specific file
  mdv --pdf README.md    Convert markdown to PDF
  mdv -p 3000            Start on port 3000
  mdv -l                 List running servers
  mdv -k -a              Stop all servers
""",
    )

    # サーバー管理オプション
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List running MDV servers",
    )
    parser.add_argument(
        "-k", "--kill",
        nargs="?",
        const="__no_pid__",
        metavar="PID",
        help="Stop server (-k -a for all, -k <PID> for specific)",
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Use with -k to stop all servers",
    )

    # ビューア起動オプション
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory or file path to view (default: current directory)",
    )
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=8642,
        help="Server port (default: 8642)",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't open browser automatically",
    )

    # PDF変換オプション
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Convert markdown file to PDF",
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        metavar="FILE",
        help="Output PDF file path (default: same name as input with .pdf extension)",
    )

    return parser


def main() -> None:
    """メインエントリーポイント"""
    parser = create_parser()
    args = parser.parse_args()

    # -l: サーバー一覧
    if args.list:
        sys.exit(list_servers())

    # -k: サーバー停止
    if args.kill is not None:
        if args.kill != "__no_pid__":
            sys.exit(kill_servers(target=args.kill))
        else:
            sys.exit(kill_servers(kill_all=args.all))

    # --pdf: PDF変換
    if args.pdf:
        input_path = Path(args.path).resolve()
        output_path = Path(args.output).resolve() if args.output else None
        sys.exit(convert_to_pdf(input_path, output_path))

    # デフォルト: ビューア起動
    start_viewer(args.path, args.port, not args.no_browser)


if __name__ == "__main__":
    main()
