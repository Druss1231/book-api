import uuid
from sqlalchemy import Column, String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Book(Base):
    """
    書籍を表すORMモデル。

    - Author と 多対1 の関係を持つ
    - 書籍は必ず既存の著者に紐づく前提の設計
    - 著者削除時のデータ整合性を考慮し、CASCADE を採用
    """

    __tablename__ = "books"

    # 主キー
    # Author と同様に UUID を採用し、
    # 外部API公開や将来的な分散構成でも安全に扱えるようにする
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # 書籍タイトル
    # 現要件では最大100文字とし、
    # 要件変更時に影響範囲が分かりやすいようモデル側で制約を定義
    title = Column(
        String(100),
        nullable=False
    )

    # 著者ID（外部キー）
    # Book は必ず Author に属するため nullable=False
    # ondelete="CASCADE" により、著者削除時に
    # 孤立した書籍レコードが残らないようにする
    author_id = Column(
        UUID(as_uuid=True),
        ForeignKey("authors.id", ondelete="CASCADE"),
        nullable=False,
    )

    # インデックス定義
    # 著者IDでの検索（例: 著者ごとの書籍一覧取得）を
    # 高頻度で行うことを想定し、パフォーマンス向上のために付与
    __table_args__ = (
        Index("idx_books_author_id", "author_id"),
    )

    # 著者とのORMリレーション
    # back_populates により Author.books と双方向に関連付け
    # JOINを明示せずとも author.name などにアクセス可能
    author = relationship(
        "Author",
        back_populates="books"
    )
