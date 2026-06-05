from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, Integer, String, Numeric
from sqlalchemy.orm import DeclarativeBase, Session
from prometheus_flask_exporter import PrometheusMetrics

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Prometheus metrics (exposes /metrics automatically)
metrics = PrometheusMetrics(app)
metrics.info("app_info", "Book API", version="1.0.0")

# Config
FLASK_HOST   = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT   = int(os.getenv("FLASK_PORT", 5001))
FLASK_DEBUG  = os.getenv("FLASK_DEBUG", "False").lower() == "true"
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:8080,http://localhost:5173").split(",")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bookuser:bookpass@db:5432/bookdb")
SECRET_KEY   = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

app.secret_key = SECRET_KEY

CORS(
    app,
    origins=CORS_ORIGINS,
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True,
)

# ─── SQLAlchemy setup ─────────────────────────────────────────────────────────

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id     = Column(Integer, primary_key=True, autoincrement=True)
    title  = Column(String, nullable=False)
    author = Column(String, nullable=False)
    cover  = Column(String, default="")
    rating = Column(Numeric(3, 1), default=0)
    pages  = Column(Integer, default=0)
    genre  = Column(String, default="")
    status = Column(String, default="want-to-read")

    def to_dict(self):
        return {
            "id":     self.id,
            "title":  self.title,
            "author": self.author,
            "cover":  self.cover,
            "rating": float(self.rating) if self.rating is not None else 0,
            "pages":  self.pages,
            "genre":  self.genre,
            "status": self.status,
        }


# Create tables at startup
with app.app_context():
    Base.metadata.create_all(engine)


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "db": "reachable"}), 200
    except Exception as e:
        return jsonify({"status": "error", "db": str(e)}), 503


@app.route("/api/test", methods=["GET", "OPTIONS"])
def test_cors():
    return jsonify({"message": "CORS is working!"})


@app.route("/api/books", methods=["GET", "OPTIONS"])
def get_books():
    if request.method == "OPTIONS":
        return _cors_preflight()
    with Session(engine) as session:
        books = session.query(Book).order_by(Book.id).all()
    return jsonify([b.to_dict() for b in books])


@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.json
    book = Book(
        title=data.get("title"),
        author=data.get("author"),
        cover=data.get("cover", ""),
        rating=data.get("rating", 0),
        pages=data.get("pages", 0),
        genre=data.get("genre", ""),
        status=data.get("status", "want-to-read"),
    )
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return jsonify(book.to_dict()), 201


@app.route("/api/books/<int:book_id>", methods=["PUT", "OPTIONS"])
def update_book(book_id):
    if request.method == "OPTIONS":
        return _cors_preflight()
    data = request.json
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        for field in ("title", "author", "cover", "rating", "pages", "genre", "status"):
            if field in data:
                setattr(book, field, data[field])
        session.commit()
        session.refresh(book)
        return jsonify(book.to_dict())


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        session.delete(book)
        session.commit()
        return jsonify(book.to_dict())


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _cors_preflight():
    resp = jsonify({})
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE,OPTIONS"
    return resp


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting Flask server on http://{FLASK_HOST}:{FLASK_PORT}")
    print(f"Allowed origins: {CORS_ORIGINS}")
    app.run(debug=FLASK_DEBUG, port=FLASK_PORT, host=FLASK_HOST)