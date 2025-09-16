# Project Outline & Roadmap for T&E Master Ledger (Zoho Expense → Postgres)

This document briefs the Claude Code Agent on what has been built, current state, and the next development roadmap.

---

## 1. What Has Been Done ✅

- **Complete MVP Implementation** (FastAPI + Postgres + Railway ready)
  - Complete **FastAPI app** under `app/` with modern Python 3.12
  - **Postgres schema** modeled with SQLAlchemy & Alembic migrations
  - **OAuth flow** with Zoho Expense (login + callback, refresh handling)
  - **Incremental sync** job using APScheduler; can also be triggered manually via simple URL parameter
  - **Dockerfile & railway.toml** for seamless Railway deployment
  - **Requirements.txt** pinned with production-ready dependencies
  - **.env.example** for environment configuration (Zoho, DB, encryption, admin token, etc.)
  - **Comprehensive README.md** with setup, deployment, and endpoint usage instructions
  - **Simplified Authentication** - URL parameter instead of complex headers for personal use

- **Core Endpoints Available**:
  - `/health` → heartbeat and status check
  - `/oauth/zoho/login` + `/oauth/zoho/callback` → OAuth flow
  - `/expenses` → list, filter, mark reimbursed
  - `/admin/sync?secret=phrase` → manual sync trigger (simplified auth)
  - `/reports/summary`, `/reports/outstanding`, `/reports/ageing` → comprehensive reporting

- **Production Ready**
  - Deployed to GitHub at https://github.com/timlihk/Zoho-expense
  - Ready to deploy on Railway with PostgreSQL plugin
  - Alembic migrations run automatically in container startup
  - Encrypted token storage with Fernet encryption
  - Environment-based configuration for security

---

## 2. Current Architecture

- **Backend**: FastAPI (Python 3.12)
- **Database**: Postgres (on Railway)
- **ORM & Migrations**: SQLAlchemy + Alembic
- **Scheduler**: APScheduler for recurring Zoho sync
- **Auth**: Zoho OAuth 2.0 (encrypted tokens with Fernet)
- **Reports**: SQL views exposed via REST endpoints
- **Deployment Target**: Railway (Docker + Postgres plugin)

---

## 3. Roadmap / Next Steps

### Phase 1 (MVP stabilization)
- [ ] Confirm Zoho API responses → adjust field mappings in `app/zoho.py` and `app/sync.py`.
- [ ] Add logging and error handling for sync jobs.
- [ ] Unit tests for core modules (sync, OAuth, reports).
- [ ] GitHub Actions CI for linting, tests, Docker build.

### Phase 2 (Usability & Reconciliation)
- [ ] CSV upload endpoint for **company reports** (to reconcile Zoho vs company ledger).
- [ ] Matching logic: fuzzy match by merchant + date ±N days + amount tolerance.
- [ ] Update `company_report_status` and store external references.
- [ ] Export reconciled data to CSV.

### Phase 3 (Frontend / Dashboards)
- [ ] Simple React or Svelte frontend (served under `/ui`) for:
  - Dashboard summary (totals, outstanding, ageing)
  - Expense table with filters
  - CSV upload + reconciliation wizard
- [ ] Authentication for frontend (basic password or OAuth).

### Phase 4 (Integrations & Extras)
- [ ] Notion / Airtable integration (push summaries).
- [ ] S3-compatible storage for receipt attachments.
- [ ] Slack/email notifications for pending reimbursements.
- [ ] Advanced reporting: average reimbursement lag, category spend trends.

---

## 4. Deliverables for Claude Code Agent
- Maintain and extend the FastAPI backend.
- Improve sync reliability and add reconciliation logic.
- Scaffold frontend for dashboards and reconciliation.
- Add automated testing and CI/CD pipeline.
- Document deployment + operational playbooks.

---

This roadmap ensures the project grows from a basic ledger into a full self‑hosted reimbursement tracker and reporting tool integrated with Zoho Expense and company workflows.

