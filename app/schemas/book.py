from uuid import UUID
from pydantic import BaseModel
from app.schemas.author import AuthorResponse


class BookCreate(BaseModel):
    """
    書籍作成時に使用するリクエストスキーマ。

    - 書籍タイトルと既存の著者IDを受け取る
    - 著者の存在チェックはAPI層で行う
    """
    title: str
    author_id: UUID


class BookResponse(BaseModel):
    """
    書籍情報を返却するレスポンススキーマ。

    - 書籍自身の情報に加えて、対応する著者情報を含める
    - AuthorResponse をネストすることで
      「書籍 + 著者」の関係性を明確に表現している
    """
    id: UUID
    title: str
    author_id: UUID
    author: AuthorResponse

    class Config:
        # SQLAlchemy の ORM モデル(Book)から
        # 関連オブジェクト(author)を含めてレスポンスを生成可能にする
        from_attributes = True
