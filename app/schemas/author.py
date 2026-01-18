from pydantic import BaseModel
from uuid import UUID


class AuthorCreate(BaseModel):
    """
    著者作成時に使用するリクエストスキーマ。

    - クライアントから受け取る入力専用
    - IDはサーバー側で採番するため含めない
    """
    name: str


class AuthorResponse(BaseModel):
    """
    著者情報を返却するレスポンススキーマ。

    - DBモデル(Author)をそのまま返さず、
      APIとして公開する項目のみを定義
    """
    id: UUID
    name: str

    class Config:
        # SQLAlchemy ORM オブジェクトをそのまま返却できるようにする
        # FastAPI + SQLAlchemy の連携で必須
        from_attributes = True


class BookCreate(BaseModel):
    """
    書籍作成時に使用するリクエストスキーマ。

    - 既存の著者ID(author_id)の指定が必須
    - 著者の存在チェックはAPI側で行う
    """
    title: str
    author_id: UUID


class BookResponse(BaseModel):
    """
    書籍情報を返却するレスポンススキーマ。

    - author_id は内部参照用として保持
    - 著者名を含める場合は別スキーマを定義することで
      責務を分離できる設計
    """
    id: UUID
    title: str
    author_id: UUID

    class Config:
        # ORMモデルから直接レスポンスを生成するための設定
        from_attributes = True
