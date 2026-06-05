-- Tabel ini juga dibuat oleh app.py saat startup,
-- tapi init.sql ini berguna jika ingin seed data awal.

CREATE TABLE IF NOT EXISTS books (
    id         SERIAL PRIMARY KEY,
    title      TEXT NOT NULL,
    author     TEXT NOT NULL,
    cover      TEXT    DEFAULT '',
    rating     NUMERIC(3,1) DEFAULT 0,
    pages      INTEGER DEFAULT 0,
    genre      TEXT    DEFAULT '',
    status     TEXT    DEFAULT 'want-to-read',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Contoh seed data
INSERT INTO books (title, author, genre, pages, rating, status) VALUES
  ('Clean Code', 'Robert C. Martin', 'Technology', 431, 4.5, 'read'),
  ('The Pragmatic Programmer', 'Andrew Hunt', 'Technology', 352, 4.8, 'read'),
  ('Designing Data-Intensive Applications', 'Martin Kleppmann', 'Technology', 616, 4.9, 'reading')
ON CONFLICT DO NOTHING;
