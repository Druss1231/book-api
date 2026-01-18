from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.database import SessionLocal
from app.models.author import Author
from app.models.book import Book
from app.schemas.author import AuthorCreate, AuthorResponse
from app.schemas.book import BookCreate, BookResponse


# FastAPI アプリケーション本体
app = FastAPI()


def get_db():
    """
    DBセッションを提供する依存関数。

    - 各リクエストごとに新しいセッションを生成
    - リクエスト終了時に必ず close される
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===== 著者関連 API =====

@app.get("/authors", response_model=list[AuthorResponse])
def get_authors(db: Session = Depends(get_db)):
    """
    著者一覧を取得する。

    - 登録されているすべての著者を返却
    """
    return db.query(Author).all()


@app.post("/authors", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """
    新しい著者を登録する。
    """
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


# ===== 書籍関連 API =====

@app.post("/books", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    新しい書籍を登録する。

    - 既存の著者IDの指定が必須
    - 著者が存在しない場合は 400 エラーを返す
    """
    # 著者存在チェック（整合性担保）
    author = db.query(Author).filter(Author.id == book.author_id).first()
    if author is None:
        raise HTTPException(status_code=400, detail="Author does not exist")

    db_book = Book(
        title=book.title,
        author_id=book.author_id
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    """
    書籍一覧を取得する。

    - 各書籍に対応する著者情報も含めて返却
    """
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: UUID, db: Session = Depends(get_db)):
    """
    指定されたIDの書籍情報を取得する。

    - 書籍に対応する著者情報もレスポンスに含める
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: UUID, db: Session = Depends(get_db)):
    """
    指定されたIDの書籍を削除する。
    """
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
