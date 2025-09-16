
# Expense Tracking Patches — What & Why

This bundle contains patches and new files to harden the `expense-tracking` project.

## Changes made

1. **README cleanup (patches/README.patch)**
   - Removed insecure query-string `?secret=` for admin sync.
   - Updated docs to use `x-admin-token` header instead.
   - Reason: prevents leaking secrets into logs and browser history.

2. **app/main.py (patches/app_main.patch)**
   - Added CORS middleware for cross-origin safety.
   - Added Strict-Transport-Security (HSTS) header in `/health` (production HTTPS).
   - Extended `/health` to show last sync status and cursor.
   - Reason: improve observability & enforce secure defaults.

3. **app/routers/expenses.py (patches/app_routers_expenses.patch)**
   - Changed admin sync endpoint to require header token instead of query param.
   - Returns structured response with `ok` and `message`.
   - Reason: aligns with security best practices.

4. **app/sync.py (new_files/app/sync.py)**
   - Scaffold for sync engine with Postgres advisory lock (`pg_try_advisory_lock`).
   - Cursor persistence in `sync_state` table.
   - Async wrappers to call Zoho list APIs incrementally.
   - Reason: ensures idempotent, safe sync without race conditions.

5. **app/routers/recon.py (new_files/app/routers/recon.py)**
   - New endpoint `/recon/upload` to accept CSV (company T&E report).
   - Currently stubbed; parses CSV, returns row count; ready for fuzzy matching extension.
   - Reason: sets foundation for reconciliation workflow.

6. **CI (new_files/.github/workflows/ci.yml)**
   - GitHub Actions workflow for linting (`ruff`) and tests (`pytest`).
   - Reason: adds automated checks on pushes/PRs.

7. **Makefile (new_files/Makefile)**
   - Simple targets for `dev`, `migrate`, `run`, `lint`, `test`.
   - Reason: improve developer ergonomics.

## How to apply

Unzip into your repo root, then apply patches and copy new files:

```bash
unzip expense-tracking-patches2.zip -d patches

# apply README and code patches
git apply patches/patches/README.patch
git apply patches/patches/app_main.patch
git apply patches/patches/app_routers_expenses.patch

# copy in new files
cp -r patches/new_files/* .

# add patch notes
git add .
git commit -m "Apply security & sync hardening patches (admin header auth, sync scaffold, recon stub, CI, Makefile)"
git push origin <branch>
```

Then open a PR with the branch you pushed.
