from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from sqlalchemy import text

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/summary")
def summary(from_: str | None = None, to: str | None = None, db: Session = Depends(get_db)):
    # Simple totals
    q = """
    SELECT currency, SUM(amount) AS total_amount, COUNT(*) AS n
    FROM expenses
    GROUP BY currency
    """
    rows = list(db.execute(text(q)))
    return {"by_currency": [dict(r._mapping) for r in rows]}

@router.get("/outstanding")
def outstanding(db: Session = Depends(get_db)):
    q = """
    SELECT category_id, SUM(amount_home) AS total_outstanding
    FROM expenses
    WHERE (reimbursable IS TRUE) AND (reimbursement_status != 'Reimbursed')
    GROUP BY category_id
    """
    rows = list(db.execute(text(q)))
    return {"outstanding": [dict(r._mapping) for r in rows]}

@router.get("/ageing")
def ageing(db: Session = Depends(get_db)):
    q = """
    SELECT 
      CASE 
        WHEN CURRENT_DATE - txn_date <= 30 THEN '0-30'
        WHEN CURRENT_DATE - txn_date <= 60 THEN '31-60'
        WHEN CURRENT_DATE - txn_date <= 90 THEN '61-90'
        ELSE '90+'
      END AS bucket,
      SUM(amount_home) AS total
    FROM expenses
    WHERE (reimbursement_status != 'Reimbursed' OR reimbursement_status IS NULL)
    GROUP BY 1
    ORDER BY 1
    """
    rows = list(db.execute(text(q)))
    return {"ageing": [dict(r._mapping) for r in rows]}
