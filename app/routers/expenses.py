from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db import get_db
from app.models import Expense
from app.config import settings
from app.sync import run_sync

router = APIRouter(prefix="/expenses", tags=["expenses"])

@router.get("")
def list_expenses(status: str | None = None, limit: int = 100, db: Session = Depends(get_db)):
    q = db.query(Expense)
    if status:
        q = q.filter(Expense.reimbursement_status == status)
    q = q.order_by(Expense.txn_date.desc()).limit(min(limit, 500))
    rows = q.all()
    return [{
        "id": r.id,
        "date": r.txn_date,
        "merchant": r.merchant,
        "amount": float(r.amount) if r.amount is not None else None,
        "currency": r.currency,
        "status": r.reimbursement_status,
        "company_report_status": r.company_report_status,
    } for r in rows]

@router.post("/reimburse/mark")
def mark_reimbursed(expense_ids: list[int], amount: float | None = None, db: Session = Depends(get_db)):
    rows = db.query(Expense).filter(Expense.id.in_(expense_ids)).all()
    for r in rows:
        r.reimbursement_status = "Reimbursed"
    db.commit()
    return {"updated": len(rows)}

@router.post("/admin/sync")
def admin_sync(secret: str = "", db: Session = Depends(get_db)):
    if secret != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    run_sync(db)
    return {"ok": True}
