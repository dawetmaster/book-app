# Fullstack Tasks (Mid-Level)

> **Level**: Mid-Level (2–5 years experience)

### 🔹 Fullstack Developer

Use the `frontend/` and `backend/` from this repo as your starting point.

- **Required:**
  1. **Search & filter** — Implement server-side search by title/author and filter by genre on the backend (`GET /api/books?q=&genre=`); wire the Browse page to use query params instead of client-side filtering
  2. **Detail page** — Add a book detail page (`/books/:id`) with cover, title, author, genre, pages, rating, and status management (add to library / update status)
  3. **User library** — Implement "My Books" view with real data from the backend; support add, remove, and status updates (`want-to-read` → `reading` → `read`) persisted via API
  4. **Reading progress** — Allow users to update their current page on a book they are reading; display a progress bar on both the browse and detail pages
  5. **Input validation** — Validate all POST/PUT request bodies on the backend and return structured error responses (400 with field-level messages)

- **Optional (implement at least one):**
  - Pagination or infinite scroll on the Browse page (`GET /api/books?page=&limit=`)
  - Authentication — simple login/register flow (session or JWT); gate library mutations behind auth
  - Reading stats — surface aggregated stats on the Profile page (books read this month, pages this week, favourite genre) computed from real backend data

- **Bonus:**
  - Add more essential features you think the app is missing
  - Write at least one unit or integration test (frontend component test or backend route test)
