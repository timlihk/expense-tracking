from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db import get_db
from app.models import Expense
from app.config import settings
from app.sync import run_sync

limiter = Limiter(key_func=get_remote_address)

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
        "kirkland_te_report": r.kirkland_te_report,
    } for r in rows]

@router.post("/reimburse/mark")
def mark_reimbursed(expense_ids: list[int], amount: float | None = None, db: Session = Depends(get_db)):
    rows = db.query(Expense).filter(Expense.id.in_(expense_ids)).all()
    for r in rows:
        r.reimbursement_status = "Reimbursed"
    db.commit()
    return {"updated": len(rows)}

class KirklandTERequest(BaseModel):
    expense_ids: list[int]
    te_report_number: str

@router.post("/kirkland-te/assign")
def assign_kirkland_te_report(request: KirklandTERequest, db: Session = Depends(get_db)):
    """Assign Kirkland T&E report number to expenses"""
    rows = db.query(Expense).filter(Expense.id.in_(request.expense_ids)).all()
    for r in rows:
        r.kirkland_te_report = request.te_report_number
        # Optionally mark as reimbursed when assigned to T&E report
        if r.reimbursement_status == "Not Reimbursed":
            r.reimbursement_status = "Submitted for Reimbursement"
    db.commit()
    return {"updated": len(rows), "te_report": request.te_report_number}

@router.get("/kirkland-te/{te_report_number}")
def get_expenses_by_te_report(te_report_number: str, db: Session = Depends(get_db)):
    """Get all expenses associated with a specific Kirkland T&E report"""
    rows = db.query(Expense).filter(Expense.kirkland_te_report == te_report_number).all()
    return [{
        "id": r.id,
        "date": r.txn_date,
        "merchant": r.merchant,
        "amount": float(r.amount) if r.amount is not None else None,
        "currency": r.currency,
        "status": r.reimbursement_status,
        "kirkland_te_report": r.kirkland_te_report,
    } for r in rows]

@router.get("/kirkland-te")
def list_te_reports(db: Session = Depends(get_db)):
    """List all Kirkland T&E report numbers with summary"""
    from sqlalchemy import func

    results = db.query(
        Expense.kirkland_te_report,
        func.count(Expense.id).label('expense_count'),
        func.sum(Expense.amount).label('total_amount'),
        func.min(Expense.txn_date).label('earliest_date'),
        func.max(Expense.txn_date).label('latest_date')
    ).filter(
        Expense.kirkland_te_report.isnot(None)
    ).group_by(
        Expense.kirkland_te_report
    ).all()

    return [{
        "te_report_number": r.kirkland_te_report,
        "expense_count": r.expense_count,
        "total_amount": float(r.total_amount) if r.total_amount else 0,
        "date_range": {
            "from": r.earliest_date,
            "to": r.latest_date
        }
    } for r in results]

@router.post("/admin/sync")
@limiter.limit("10/minute")  # Strict limit for admin operations
def admin_sync(request: Request, x_admin_token: str = Header(default=""), db: Session = Depends(get_db)):
    if x_admin_token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    run_sync(db)
    return {"ok": True, "message": "Sync started"}
