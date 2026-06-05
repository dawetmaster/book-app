# DevOps Tasks (Mid-Level)

> **Level**: Mid-Level (2–5 years experience)

### 🔹 DevOps & Infrastructure Engineer

Use `backend/` or `frontend/` (or both) from this repo as the application you build the pipeline and infrastructure around.

- **Required:**
  1. **Container** — Multi-stage `Dockerfile` + `docker-compose.yml` that runs the app with at least one dependency or sidecar (e.g. database, reverse proxy, or log shipper)
  2. **CI/CD Pipeline** — GitHub Actions or GitLab CI workflow with distinct stages: lint → build → test → push image to a container registry (Docker Hub or GHCR)
  3. **Infrastructure as Code** — Terraform or Ansible to provision at least one real or simulated resource (e.g. cloud VM, S3 bucket, or a local environment via Ansible playbook)
  4. **Monitoring** — Docker Compose stack with Prometheus + Grafana (or Loki); include at least one working dashboard or alert rule targeting the app
  5. **README / Runbook** — Architecture diagram (ASCII or image), and step-by-step runbook covering: how to deploy, how to access monitoring, and how to roll back

- **Optional (nice to have):**
  - Kubernetes manifests: `Deployment`, `Service`, `ConfigMap`
  - Secrets management: GitHub Secrets wired into CI, or a Vault reference
  - Multi-environment config: separate staging and production env vars
  - Scripted health check in Bash or Python (e.g. polling `/health` until ready)

- **Bonus:**
  - GitOps setup with ArgoCD or Flux
  - Container image vulnerability scan (Trivy or Grype) integrated in CI pipeline
  - IaC for a networking resource (DNS record, load balancer rule, firewall)
  - On-call runbook for a simulated production incident (e.g. service down, high memory)
