# Book API

FastAPI + SQLAlchemy + PostgreSQL を用いた、著者と書籍を管理するシンプルな REST API です。
Docker Compose を利用してローカル環境への影響を最小限に抑えつつ開発できる構成になっています。

---

## 開発環境のセットアップ手順

### 前提条件

- Docker
- Docker Compose

（ローカルに Python や PostgreSQL をインストールする必要はありません）

---

### 起動手順

リポジトリのルートディレクトリで以下を実行します。

```bash
docker compose up --build -d
docker compose exec api alembic upgrade head
```

起動後、以下の URL で API にアクセスできます。

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

---

### 停止手順

```bash
docker compose down
```

---

## 実装した API エンドポイント一覧

### 著者（Author）

#### 著者一覧取得

```http
GET /authors
```

```bash
curl http://localhost:8000/authors
```

---

#### 著者登録

```http
POST /authors
```

```bash
curl -X POST http://localhost:8000/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "Yamada Taro"}'
```

---

#### 著者削除

```http
DELETE /authors/{author_id}
```

```bash
curl -X DELETE http://localhost:8000/authors/<AUTHOR_ID>
```

---

### 書籍（Book）

#### 書籍一覧取得（著者名含む）

```http
GET /books
```

```bash
curl http://localhost:8000/books
```

---

#### 書籍単体取得（著者名含む）

```http
GET /books/{book_id}
```

```bash
curl http://localhost:8000/books/<BOOK_ID>
```

---

#### 書籍登録（既存著者ID指定必須）

```http
POST /books
```

```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI入門",
    "author_id": "<AUTHOR_ID>"
  }'
```

※ 指定した著者IDが存在しない場合は 400 エラーを返します。

---

## アーキテクチャ・設計で意識した点

### 1. レイヤ分離

責務を明確にするため、以下のようにディレクトリを分割しています。

- `models/` : SQLAlchemy ORM モデル（DB構造）
- `schemas/` : Pydantic スキーマ（APIの入出力）
- `db/` : DB接続・セッション管理
- `alembic/` : マイグレーション管理

これにより、
- DB構造の変更
- APIレスポンス形式の変更

を独立して行える構成にしています。

---

### 2. ORM の relationship を活用

SQL の JOIN を直接書かず、SQLAlchemy の `relationship` を使って

- 書籍 → 著者

をオブジェクトとして扱えるようにしています。

これにより、FastAPI + Pydantic の機能を活かし、
「モデルを返すだけで著者名を含んだレスポンスを生成」できるようにしています。

---

### 3. Docker による環境分離

- ローカル環境を汚さない
- DB の再現性を担保

するため、アプリケーション・DB ともに Docker コンテナで構成しています。

---

### 4. データ整合性の担保

- 書籍登録時に著者の存在チェックを必須化
- 存在しないリソースには 404 / 400 を返却

といった形で、APIレベルでの基本的なバリデーションを実装しています。

---

## 補足

- マイグレーション管理には Alembic を使用
- Swagger UI を用いてブラウザから API の動作確認が可能

---

以上

