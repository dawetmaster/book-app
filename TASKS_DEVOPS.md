# DevOps Tasks (Junior)

> **Level**: Junior (0–2 years experience)

### 🔹 DevOps
- Use `backend/` or `frontend/` as the app to containerize (your choice)
- **Required:**
  - `Dockerfile` that successfully builds and runs the chosen app
  - `README` section explaining how to build and run the container locally (`docker build`, `docker run`)
  - At least one GitHub Actions workflow (e.g. build image on every push to `main`)
- **Optional (implement at least one):**
  - `docker-compose.yml` — run the app alongside any dependency (e.g. a database or reverse proxy)
  - Multi-stage `Dockerfile` to reduce final image size
  - Environment variable handling via `.env` file (no hardcoded values in image)
  - Health check defined in `Dockerfile` or `docker-compose.yml`
- **Bonus:**
  - Dockerfile linting step in CI (e.g. `hadolint`)
  - Push built image to a container registry (Docker Hub or GHCR)
  - Brief comment in `README` explaining what each CI step does
