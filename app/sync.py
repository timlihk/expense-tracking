# Production-grade sync engine with advisory locks and cursor persistence
import asyncio
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import text, select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models import Expense, ExpenseReport, Vendor, Category
from app.zoho import list_expenses, list_reports

LOCK_KEY = 812739  # stable across deployments

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _get_cursor(db: Session) -> Optional[datetime]:
    row = db.execute(
        text("SELECT cursor FROM sync_state WHERE provider='zoho_expense' ORDER BY id DESC LIMIT 1")
    ).first()
    if not row or not row[0]:
        return None
    try:
        return datetime.fromisoformat(row[0])
    except Exception:
        return None

def _set_sync_state(db: Session, status: str, cursor: Optional[datetime], message: Optional[str] = None):
    db.execute(
        text(
            "INSERT INTO sync_state(provider, cursor, last_run_at, status, message) "
            "VALUES (:p, :c, now(), :s, :m)"
        ),
        {
            "p": "zoho_expense",
            "c": cursor.isoformat() if cursor else None,
            "s": status,
            "m": message,
        },
    )
    db.commit()

def _try_lock(db: Session) -> bool:
    row = db.execute(text("SELECT pg_try_advisory_lock(:k)"), {"k": LOCK_KEY}).first()
    return bool(row and row[0])

def _unlock(db: Session):
    db.execute(text("SELECT pg_advisory_unlock(:k)"), {"k": LOCK_KEY})
    db.commit()

def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # nested: rarely happens in uvicorn main thread, but guard anyway
            return asyncio.run(coro)
        return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)

# ---------- Upsert helpers with ON CONFLICT ----------

def upsert_vendor(db: Session, name: Optional[str]) -> Optional[int]:
    if not name:
        return None
    stmt = insert(Vendor).values(name=name).on_conflict_do_nothing(index_elements=["name"]).returning(Vendor.id)
    row = db.execute(stmt).first()
    if row:
        db.commit()
        return row[0]
    # Already exists — fetch id
    vid = db.execute(text("SELECT id FROM vendors WHERE name=:n"), {"n": name}).scalar()
    db.commit()
    return vid

def upsert_category(db: Session, name: Optional[str]) -> Optional[int]:
    if not name:
        return None
    stmt = insert(Category).values(name=name).on_conflict_do_nothing(index_elements=["name"]).returning(Category.id)
    row = db.execute(stmt).first()
    if row:
        db.commit()
        return row[0]
    cid = db.execute(text("SELECT id FROM categories WHERE name=:n"), {"n": name}).scalar()
    db.commit()
    return cid

def upsert_report(db: Session, zoho: dict) -> Optional[int]:
    z_id = str(zoho.get("report_id") or zoho.get("id") or "")
    if not z_id:
        return None
    payload = {
        "zoho_report_id": z_id,
        "title": zoho.get("title"),
        "report_number": zoho.get("report_number"),
        "status": zoho.get("status"),
        "total_amount": zoho.get("total"),
        "currency": (zoho.get("currency") or {}).get("code") if isinstance(zoho.get("currency"), dict) else zoho.get("currency"),
    }
    stmt = insert(ExpenseReport).values(**payload).on_conflict_do_update(
        index_elements=["zoho_report_id"],
        set_=payload,
    ).returning(ExpenseReport.id)
    rid = db.execute(stmt).scalar()
    db.commit()
    return rid

def upsert_expense(db: Session, zoho: dict, report_map: dict[str, int]):
    z_id = str(zoho.get("expense_id") or zoho.get("id") or "")
    if not z_id:
        return
    vendor_name = (zoho.get("merchant") or zoho.get("vendor") or "") or None
    category_name = (
        zoho.get("category_name")
        or (zoho.get("category") or {}).get("name") if isinstance(zoho.get("category"), dict) else zoho.get("category")
    )
    vendor_id = upsert_vendor(db, vendor_name)
    category_id = upsert_category(db, category_name)

    rid = None
    raw_rid = zoho.get("report_id")
    if raw_rid and str(raw_rid) in report_map:
        rid = report_map[str(raw_rid)]

    payload = {
        "zoho_expense_id": z_id,
        "report_id": rid,
        "txn_date": zoho.get("date") or zoho.get("txn_date"),
        "merchant": vendor_name,
        "vendor_id": vendor_id,
        "category_id": category_id,
        "description": zoho.get("description"),
        "amount": zoho.get("amount"),
        "currency": (zoho.get("currency") or {}).get("code") if isinstance(zoho.get("currency"), dict) else zoho.get("currency"),
        "exchange_rate": zoho.get("exchange_rate"),
        "amount_home": zoho.get("amount_home") or zoho.get("converted_amount"),
        "payment_mode": zoho.get("payment_mode"),
    }
    stmt = insert(Expense).values(**payload).on_conflict_do_update(
        index_elements=["zoho_expense_id"],
        set_=payload,  # safe: only mutable fields are listed
    )
    db.execute(stmt)
    db.commit()

# ---------- Main sync with advisory lock ----------

def run_sync(db: Session):
    """
    Production-grade sync with PostgreSQL advisory lock to prevent concurrent runs.
    Uses cursor-based incremental sync and upserts for idempotent operations.
    """
    if not _try_lock(db):
        _set_sync_state(db, "skipped", _get_cursor(db), "Another sync is running")
        return {"status": "skipped", "message": "Another sync is running"}

    try:
        since = _get_cursor(db)
        report_map: dict[str, int] = {}

        # 1) Reports (build mapping for expense.report_id)
        page = 1
        reports_count = 0
        while True:
            data = _run_async(list_reports(db, since, page))
            items = (data.get("reports") or data.get("data") or [])
            for it in items:
                rid = upsert_report(db, it)
                if rid:
                    key = str(it.get("report_id") or it.get("id"))
                    if key:
                        report_map[key] = rid
                reports_count += 1
            if not data or not data.get("has_more"):
                break
            page += 1

        # 2) Expenses
        page = 1
        expenses_count = 0
        new_cursor = _now_utc()
        while True:
            data = _run_async(list_expenses(db, since, page))
            items = (data.get("expenses") or data.get("data") or [])
            for it in items:
                upsert_expense(db, it, report_map)
                expenses_count += 1
            if not data or not data.get("has_more"):
                break
            page += 1

        _set_sync_state(db, "success", new_cursor, f"Synced {reports_count} reports, {expenses_count} expenses")
        return {
            "status": "success",
            "reports_synced": reports_count,
            "expenses_synced": expenses_count,
            "cursor": new_cursor.isoformat()
        }

    except Exception as e:
        _set_sync_state(db, "error", _get_cursor(db), str(e))
        return {"status": "error", "message": str(e)}
    finally:
        _unlock(db)