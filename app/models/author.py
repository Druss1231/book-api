import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Author(Base):
    """
    著者を表すORMモデル。

    - 書籍(Book)と 1対多 の関係を持つ
    - UUIDを主キーに採用し、将来的な分散環境や外部公開APIでも
      ID衝突を避けられる設計としている
    """

    __tablename__ = "authors"

    # 主キー
    # UUIDを使用することで、クライアント側でIDを扱っても
    # 連番推測などのリスクを避けられる
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 著者名
    # 現時点では最大50文字とし、要件変更時はここを起点に調整可能
    name = Column(
        String(50),
        nullable=False
    )

    # 著者に紐づく書籍一覧
    # relationship はORMレベルの関連付けであり、
    # 実際の外部キー制約は Book 側で定義する
    #
    # back_populates を使うことで、双方向参照が可能となり、
    # author.books / book.author の両方から自然にアクセスできる
    books = relationship(
        "Book",
        back_populates="author"
    )
