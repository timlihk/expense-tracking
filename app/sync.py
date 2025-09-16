from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import SyncState, Vendor, Category, ExpenseReport, Expense, Attachment
from app.zoho import list_expenses, list_reports

def get_cursor(db: Session) -> datetime | None:
    row = db.query(SyncState).filter_by(provider="zoho_expense").first()
    if row and row.cursor:
        try:
            return datetime.fromisoformat(row.cursor)
        except Exception:
            return None
    return None

def set_cursor(db: Session, ts: datetime):
    row = db.query(SyncState).filter_by(provider="zoho_expense").first()
    if not row:
        row = SyncState(provider="zoho_expense")
        db.add(row)
    row.cursor = ts.isoformat()
    row.last_run_at = datetime.utcnow()
    row.status = "success"
    db.commit()

def upsert_report(db: Session, item: dict) -> int | None:
    zoho_id = str(item.get("report_id") or item.get("id") or "")
    if not zoho_id:
        return None
    obj = db.query(ExpenseReport).filter_by(zoho_report_id=zoho_id).first()
    if not obj:
        obj = ExpenseReport(zoho_report_id=zoho_id)
        db.add(obj)
    obj.title = item.get("title")
    obj.report_number = item.get("report_number")
    obj.status = item.get("status")
    obj.total_amount = item.get("total")
    obj.currency = (item.get("currency") or {}).get("code") if isinstance(item.get("currency"), dict) else item.get("currency")
    db.commit()
    return obj.id

def upsert_expense(db: Session, item: dict, report_map: dict[str,int]):
    zoho_id = str(item.get("expense_id") or item.get("id") or "")
    if not zoho_id:
        return
    obj = db.query(Expense).filter_by(zoho_expense_id=zoho_id).first()
    if not obj:
        obj = Expense(zoho_expense_id=zoho_id)
        db.add(obj)
    # vendor & category
    vendor_name = (item.get("merchant") or item.get("vendor") or "").strip() or None
    if vendor_name:
        v = db.query(Vendor).filter_by(name=vendor_name).first()
        if not v:
            v = Vendor(name=vendor_name); db.add(v); db.flush()
        obj.vendor_id = v.id
        obj.merchant = vendor_name
    cat_name = (item.get("category_name") or (item.get("category") or {}).get("name") if isinstance(item.get("category"), dict) else item.get("category")) or None
    if cat_name:
        c = db.query(Category).filter_by(name=cat_name).first()
        if not c:
            c = Category(name=cat_name); db.add(c); db.flush()
        obj.category_id = c.id

    obj.txn_date = (item.get("date") or item.get("txn_date"))
    obj.description = item.get("description")
    obj.amount = item.get("amount")
    curr = item.get("currency")
    obj.currency = curr.get("code") if isinstance(curr, dict) else curr
    obj.exchange_rate = item.get("exchange_rate")
    obj.amount_home = item.get("amount_home") or item.get("converted_amount")
    obj.payment_mode = item.get("payment_mode")
    # Map report
    rid = item.get("report_id")
    if rid and str(rid) in report_map:
        obj.report_id = report_map[str(rid)]
    db.commit()

def run_sync(db: Session):
    # Pull reports first to map report IDs
    since = get_cursor(db)
    report_map: dict[str,int] = {}
    page = 1
    while True:
        data = asyncio_run(list_reports(db, since, page))
        items = data.get("reports") or data.get("data") or []
        for it in items:
            rid = upsert_report(db, it)
            if rid:
                report_map[str(it.get("report_id") or it.get("id"))] = rid
        if not data or not data.get("has_more"):
            break
        page += 1

    # Expenses
    page = 1
    last_ts = datetime.utcnow()
    while True:
        data = asyncio_run(list_expenses(db, since, page))
        items = data.get("expenses") or data.get("data") or []
        for it in items:
            upsert_expense(db, it, report_map)
        if not data or not data.get("has_more"):
            break
        page += 1

    set_cursor(db, last_ts)

def asyncio_run(coro):
    # simple compatibility helper to run async coroutines inside sync context
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run(coro)  # fallback
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)
