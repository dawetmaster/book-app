from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import psycopg2
import psycopg2.extras
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

# ─── DB helpers ───────────────────────────────────────────────────────────────

def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    """Create the books table if it doesn't exist."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS books (
                    id      SERIAL PRIMARY KEY,
                    title   TEXT NOT NULL,
                    author  TEXT NOT NULL,
                    cover   TEXT DEFAULT '',
                    rating  NUMERIC(3,1) DEFAULT 0,
                    pages   INTEGER DEFAULT 0,
                    genre   TEXT DEFAULT '',
                    status  TEXT DEFAULT 'want-to-read',
                    created_at TIMESTAMPTZ DEFAULT now()
                );
                """
            )
        conn.commit()


# Run once at startup
with app.app_context():
    init_db()


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
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
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM books ORDER BY id")
            books = cur.fetchall()
    return jsonify([dict(b) for b in books])


@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.json
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO books (title, author, cover, rating, pages, genre, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *
                """,
                (
                    data.get("title"),
                    data.get("author"),
                    data.get("cover", ""),
                    data.get("rating", 0),
                    data.get("pages", 0),
                    data.get("genre", ""),
                    data.get("status", "want-to-read"),
                ),
            )
            book = dict(cur.fetchone())
        conn.commit()
    return jsonify(book), 201


@app.route("/api/books/<int:book_id>", methods=["PUT", "OPTIONS"])
def update_book(book_id):
    if request.method == "OPTIONS":
        return _cors_preflight()
    data = request.json
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE books
                SET title  = COALESCE(%s, title),
                    author = COALESCE(%s, author),
                    cover  = COALESCE(%s, cover),
                    rating = COALESCE(%s, rating),
                    pages  = COALESCE(%s, pages),
                    genre  = COALESCE(%s, genre),
                    status = COALESCE(%s, status)
                WHERE id = %s
                RETURNING *
                """,
                (
                    data.get("title"),
                    data.get("author"),
                    data.get("cover"),
                    data.get("rating"),
                    data.get("pages"),
                    data.get("genre"),
                    data.get("status"),
                    book_id,
                ),
            )
            book = cur.fetchone()
        conn.commit()
    if book:
        return jsonify(dict(book))
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("DELETE FROM books WHERE id = %s RETURNING *", (book_id,))
            book = cur.fetchone()
        conn.commit()
    if book:
        return jsonify(dict(book))
    return jsonify({"error": "Book not found"}), 404


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
