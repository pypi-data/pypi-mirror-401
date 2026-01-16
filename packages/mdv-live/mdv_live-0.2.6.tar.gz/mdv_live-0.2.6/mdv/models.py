"""
リクエスト/レスポンスモデル
"""

from pydantic import BaseModel


class SaveFileRequest(BaseModel):
    """ファイル保存リクエスト"""
    path: str
    content: str


class CreateDirectoryRequest(BaseModel):
    """フォルダ作成リクエスト"""
    path: str


class MoveItemRequest(BaseModel):
    """ファイル/フォルダ移動リクエスト"""
    source: str
    destination: str
