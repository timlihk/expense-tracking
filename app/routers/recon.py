from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db import get_db
from app.models import Expense
import csv
import io
from typing import List, Dict, Any

limiter = Limiter(key_func=get_remote_address)

router = APIRouter(prefix="/recon", tags=["reconciliation"])

@router.post("/upload")
@limiter.limit("5/minute")  # Limited uploads to prevent abuse
async def upload_company_report(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload company T&E report CSV for reconciliation with Zoho expenses.

    Expected CSV columns: date, merchant, amount, reference
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV format")

    try:
        # Read CSV content
        content = await file.read()
        csv_content = content.decode('utf-8')

        # Parse CSV
        reader = csv.DictReader(io.StringIO(csv_content))
        rows = list(reader)

        # Basic validation
        required_columns = {'date', 'merchant', 'amount'}
        if not required_columns.issubset(set(reader.fieldnames or [])):
            raise HTTPException(
                status_code=400,
                detail=f"CSV must contain columns: {required_columns}"
            )

        # Process each row (stub for now)
        processed_rows = []
        for i, row in enumerate(rows):
            try:
                processed_row = {
                    'row_number': i + 1,
                    'date': row['date'],
                    'merchant': row['merchant'],
                    'amount': float(row['amount']),
                    'reference': row.get('reference', ''),
                    'status': 'ready_for_matching'
                }
                processed_rows.append(processed_row)
            except ValueError as e:
                processed_rows.append({
                    'row_number': i + 1,
                    'status': 'error',
                    'error': f"Invalid amount: {row.get('amount', 'missing')}"
                })

        # Return summary
        successful_rows = [r for r in processed_rows if r['status'] == 'ready_for_matching']
        error_rows = [r for r in processed_rows if r['status'] == 'error']

        return {
            'total_rows': len(rows),
            'successful_rows': len(successful_rows),
            'error_rows': len(error_rows),
            'errors': error_rows,
            'message': f"Processed {len(successful_rows)} rows ready for matching"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@router.get("/match-candidates/{merchant}")
async def get_match_candidates(
    merchant: str,
    amount: float = None,
    date_from: str = None,
    date_to: str = None,
    db: Session = Depends(get_db)
):
    """
    Get potential Zoho expense matches for a company report entry.

    This is a stub for fuzzy matching logic that would match by:
    - Merchant name similarity
    - Amount (with tolerance)
    - Date proximity
    """
    query = db.query(Expense).filter(Expense.merchant.ilike(f"%{merchant}%"))

    if amount:
        # Allow 5% tolerance on amount
        tolerance = amount * 0.05
        query = query.filter(
            Expense.amount >= amount - tolerance,
            Expense.amount <= amount + tolerance
        )

    if date_from:
        query = query.filter(Expense.txn_date >= date_from)

    if date_to:
        query = query.filter(Expense.txn_date <= date_to)

    # Limit to unmatched expenses
    query = query.filter(Expense.external_ref.is_(None))

    candidates = query.limit(10).all()

    return {
        'query': {
            'merchant': merchant,
            'amount': amount,
            'date_range': f"{date_from} to {date_to}" if date_from and date_to else "any"
        },
        'candidates': [{
            'id': c.id,
            'date': c.txn_date,
            'merchant': c.merchant,
            'amount': float(c.amount) if c.amount else None,
            'status': c.reimbursement_status,
            'te_report': c.kirkland_te_report,
        } for c in candidates],
        'count': len(candidates)
    }

@router.post("/match")
async def create_match(
    expense_id: int,
    company_reference: str,
    db: Session = Depends(get_db)
):
    """
    Create a match between Zoho expense and company report entry.
    """
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Update external reference
    expense.external_ref = company_reference
    expense.company_report_status = "Matched"

    db.commit()

    return {
        'expense_id': expense_id,
        'company_reference': company_reference,
        'status': 'matched',
        'message': 'Expense successfully matched to company report'
    }