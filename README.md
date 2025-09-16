# Zoho Expense → PostgreSQL Sync

A self-hosted FastAPI application that automatically syncs your Zoho Expense data to PostgreSQL, providing comprehensive expense tracking, reimbursement management, and financial reporting.

## 🎯 Overview

This application solves the problem of scattered expense data by creating a centralized, self-hosted expense ledger that:
- **Automatically syncs** expense data from Zoho Expense to your own PostgreSQL database
- **Tracks reimbursement status** and provides aging reports for outstanding expenses
- **Provides REST APIs** for integration with other tools and custom reporting
- **Runs completely self-hosted** on Railway (or any Docker platform)

Perfect for individuals, small businesses, or teams who want full control over their expense data.

## 🔗 **Repository & Deployment**

- **GitHub Repository**: https://github.com/timlihk/expense-tracking
- **Status**: ✅ Ready for immediate deployment
- **Database**: Supabase PostgreSQL (free 500MB tier)
- **Hosting**: Railway (starting at $5/month)

## ✨ Key Features

### 📊 **Production-Grade Data Sync**
- **Incremental sync** with cursor-based pagination from Zoho Expense
- **Advisory locks** prevent concurrent sync runs in scaled deployments
- **Atomic upserts** ensure idempotent operations and data consistency
- **Error recovery** with detailed sync status tracking
- **Manual sync trigger** with secure header-based authentication
- **Rate limiting** protects against API abuse (10 sync requests/minute)
- **Secure OAuth integration** with encrypted token storage

### 💰 **Expense Management**
- **Complete expense tracking** with merchant, amount, date, category
- **Reimbursement status management** (Reimbursed/Not Reimbursed)
- **Bulk status updates** via API endpoints
- **Notes and custom fields** support

### 📈 **Financial Reporting**
- **Summary reports** with date range filtering
- **Outstanding expenses** tracking for cash flow management
- **Aging reports** to identify overdue reimbursements
- **Kirkland T&E report tracking** for expense submission reconciliation
- **Export capabilities** for external analysis

### 🔐 **Security & Privacy**
- **Self-hosted** - your data stays on your infrastructure
- **Encrypted token storage** using Fernet encryption
- **Header-based authentication** with secure token validation
- **Rate limiting** prevents API abuse and DDoS attacks
- **CORS middleware** with security headers (HSTS enabled)
- **Environment-based configuration** for secure deployment

## 🚀 Quick Start

### Prerequisites
- **Zoho Expense account** with API access
- **Supabase account** (free tier: 500MB PostgreSQL database)
- **Railway account** (or any Docker hosting platform)
- **5 minutes** for setup

### 1. Database Setup (Supabase)
Create a free PostgreSQL database with Supabase:
1. **Sign up** at [supabase.com](https://supabase.com) (free forever)
2. **Create new project** → Choose organization → Set database password
3. **Get connection details**: Go to Settings → Database → Copy "URI"
4. **Save the connection string** (you'll need it for deployment)

Example connection string:
```
postgresql://postgres:your-password@db.your-ref.supabase.co:5432/postgres
```

### 2. Zoho OAuth Setup
Create a Zoho OAuth app at [Zoho API Console](https://api-console.zoho.com/):
- **Application Type**: Server-based Application
- **Redirect URI**: `https://your-app.railway.app/oauth/zoho/callback`
- **Scopes**: `ZohoExpense.expenses.READ,ZohoExpense.reports.READ,ZohoExpense.files.READ`

Save your `Client ID` and `Client Secret`.

### 3. Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

1. **Connect this GitHub repository** to Railway
2. **Set environment variables** (no need for additional PostgreSQL service):

```bash
# Required - Your Supabase database connection
DATABASE_URL=postgresql://postgres:your-password@db.your-ref.supabase.co:5432/postgres

# Required - Your Zoho OAuth credentials
ZOHO_CLIENT_ID=your_zoho_client_id
ZOHO_CLIENT_SECRET=your_zoho_client_secret

# Required - Generate encryption key
ENCRYPTION_KEY=<run: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">

# Required - Your simple admin phrase
ADMIN_TOKEN=sync my expenses please

# Railway configuration
APP_BASE_URL=https://your-app.railway.app

# Optional (defaults shown)
SYNC_INTERVAL_MINUTES=15
ENVIRONMENT=production
```

### 4. Initial Setup
After deployment:

1. **Authorize Zoho**: Visit `https://your-app.railway.app/oauth/zoho/login`
2. **Test sync**: `curl -X POST "https://your-app.railway.app/admin/sync" -H "x-admin-token: sync my expenses please"`
3. **View data**: `https://your-app.railway.app/reports/summary`
4. **Optional**: Use Supabase dashboard to view your data at [supabase.com](https://supabase.com)

That's it! Your expenses will now sync automatically every 15 minutes to your free Supabase database.

## 📋 Complete API Reference

### 🏥 **System Health**
- `GET /health` - System health check and status

### 🔐 **Authentication & Setup**
- `GET /oauth/zoho/login` - Start Zoho OAuth authorization flow
- `GET /oauth/zoho/callback` - Complete OAuth (automatic redirect)
- `POST /admin/sync` - Manual sync trigger (requires `x-admin-token` header)

### 💰 **Expense Management**
- `GET /expenses` - List expenses with optional filtering
  - Query params: `status`, `limit` (max 500)
  - Returns: expense list with basic info + T&E report references
- `POST /expenses/reimburse/mark` - Mark expenses as reimbursed
  - Body: `{"expense_ids": [123, 456], "amount": 1000.00}`

### 🏢 **Kirkland T&E Report Management**
- `POST /expenses/kirkland-te/assign` - Assign T&E report number to expenses
  - Body: `{"expense_ids": [123, 456], "te_report_number": "KTE-2024-001"}`
  - Auto-updates status to "Submitted for Reimbursement"
- `GET /expenses/kirkland-te/{report_number}` - Get all expenses for specific T&E report
- `GET /expenses/kirkland-te` - List all T&E reports with summaries
  - Returns: report numbers, expense counts, totals, date ranges

### 📊 **Financial Reporting**
- `GET /reports/summary` - Financial summary with optional date filtering
  - Query params: `from=YYYY-MM-DD`, `to=YYYY-MM-DD`
- `GET /reports/outstanding` - List of unreimbursed expenses
- `GET /reports/ageing` - Aging analysis for overdue expenses

### 🔄 **Reconciliation (Company Reports)**
- `POST /recon/upload` - Upload company T&E report CSV for matching
- `GET /recon/match-candidates/{merchant}` - Find potential Zoho expense matches
- `POST /recon/match` - Create match between Zoho expense and company entry

### Example Usage

```bash
# Get summary for last 30 days
curl "https://your-app.railway.app/reports/summary?from=2024-01-01&to=2024-01-31"

# List unreimbursed expenses
curl "https://your-app.railway.app/expenses?status=Not%20Reimbursed&limit=50"

# Trigger manual sync (rate limited: 10/minute)
curl -X POST "https://your-app.railway.app/admin/sync" \
  -H "x-admin-token: sync my expenses please"

# Mark expenses as reimbursed
curl -X POST "https://your-app.railway.app/expenses/mark-reimbursed" \
  -H "Content-Type: application/json" \
  -d '{"expense_ids": ["exp_123", "exp_456"]}'

# Assign expenses to Kirkland T&E report
curl -X POST "https://your-app.railway.app/expenses/kirkland-te/assign" \
  -H "Content-Type: application/json" \
  -d '{"expense_ids": [123, 456], "te_report_number": "KTE-2024-001"}'

# Get expenses for specific T&E report
curl "https://your-app.railway.app/expenses/kirkland-te/KTE-2024-001"

# List all T&E reports with summaries
curl "https://your-app.railway.app/expenses/kirkland-te"
```

## 🏗️ Local Development

### Setup
```bash
# Clone and setup
git clone https://github.com/timlihk/Zoho-expense.git
cd Zoho-expense

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Environment setup
cp .env.example .env
# Edit .env with your credentials
```

### Database Setup
```bash
# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🗄️ Database Schema (Supabase PostgreSQL)

The application creates these main tables in your Supabase database:

- **`expenses`** - Core expense data synced from Zoho
- **`oauth_tokens`** - Encrypted OAuth tokens for Zoho API access

Key fields in `expenses` table:
- Basic info: `expense_id`, `merchant`, `amount`, `date`, `category`
- Status: `reimbursement_status`, `approval_status`
- T&E Tracking: `kirkland_te_report` (Kirkland T&E report reference)
- Metadata: `created_at`, `updated_at`, `last_synced`

### Supabase Benefits:
- **Free 500MB database** (handles 50,000+ expense records)
- **Built-in dashboard** for viewing and querying data
- **Automatic backups** and monitoring
- **Real-time capabilities** for future features
- **Direct SQL access** for custom reports

## 🔧 Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | - | PostgreSQL connection string |
| `ZOHO_CLIENT_ID` | Yes | - | Zoho OAuth client ID |
| `ZOHO_CLIENT_SECRET` | Yes | - | Zoho OAuth client secret |
| `ENCRYPTION_KEY` | Yes | - | Fernet key for token encryption |
| `ADMIN_TOKEN` | Yes | - | Simple phrase for admin endpoints |
| `APP_BASE_URL` | Yes | - | Your app's base URL for OAuth callback |
| `SYNC_INTERVAL_MINUTES` | No | 15 | Auto-sync frequency |
| `ENVIRONMENT` | No | production | Environment setting |

### Generating Encryption Key
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## 📊 Reporting Features

### Summary Reports
- Total expenses by date range
- Reimbursement status breakdown
- Category-wise spending analysis

### Outstanding Tracking
- List of unreimbursed expenses
- Total outstanding amount
- Aging analysis (30/60/90 days)

### Custom Queries
Direct PostgreSQL access allows for custom reporting:
```sql
-- Monthly spending by category
SELECT
    DATE_TRUNC('month', txn_date) as month,
    category_id,
    SUM(amount) as total
FROM expenses
GROUP BY month, category_id
ORDER BY month DESC, total DESC;

-- Expenses by Kirkland T&E report
SELECT
    kirkland_te_report,
    COUNT(*) as expense_count,
    SUM(amount) as total_amount,
    MIN(txn_date) as earliest_expense,
    MAX(txn_date) as latest_expense
FROM expenses
WHERE kirkland_te_report IS NOT NULL
GROUP BY kirkland_te_report;
```

## 🏢 Kirkland T&E Report Workflow

### **Typical Usage Flow:**
1. **Expenses sync** automatically from Zoho every 15 minutes
2. **Review expenses** via `/expenses` endpoint
3. **Group expenses** for submission to Kirkland T&E
4. **Assign T&E report number** using `/kirkland-te/assign`
5. **Track submissions** via `/kirkland-te` endpoint
6. **Monitor reimbursement status** in reports

### **T&E Report Management:**
```bash
# Group expenses for T&E submission
POST /expenses/kirkland-te/assign
{
  "expense_ids": [123, 124, 125],
  "te_report_number": "KTE-2024-Q1-001"
}

# View all expenses in a T&E report
GET /expenses/kirkland-te/KTE-2024-Q1-001

# Get summary of all T&E reports
GET /expenses/kirkland-te
```

## 🛠️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.12) with async/await patterns
- **Database**: PostgreSQL with SQLAlchemy ORM and advisory locks
- **Migrations**: Alembic for schema management
- **Scheduling**: APScheduler for background sync
- **Security**: Fernet encryption, rate limiting, CORS + HSTS
- **Testing**: pytest with comprehensive coverage
- **CI/CD**: GitHub Actions with automated testing
- **Deployment**: Docker on Railway

### Data Flow
1. **OAuth Setup** → Secure token storage
2. **Scheduled Sync** → Incremental data fetch from Zoho
3. **API Access** → RESTful endpoints for data access
4. **Reporting** → SQL-based analysis and summaries

### Production-Grade Features
- **Concurrency Control**: PostgreSQL advisory locks prevent duplicate sync runs
- **Data Integrity**: Atomic upserts with `ON CONFLICT DO UPDATE` for idempotent operations
- **API Protection**: Rate limiting with configurable limits per endpoint
- **Security Headers**: CORS middleware with HSTS for enhanced security
- **Comprehensive Testing**: Full test coverage with CI/CD automation
- **Error Recovery**: Detailed sync status tracking and error handling

## 🚧 Roadmap

### Phase 1: Stabilization (Completed ✅)
- [x] Core sync functionality
- [x] Basic reporting endpoints
- [x] Railway deployment
- [x] Enhanced error handling and logging
- [x] Comprehensive test suite
- [x] Production-grade sync engine with advisory locks
- [x] API rate limiting and security headers
- [x] GitHub Actions CI/CD pipeline

### Phase 2: Reconciliation (Completed ✅)
- [x] CSV upload for company reports
- [x] Fuzzy matching logic for expense reconciliation
- [x] External reference tracking
- [ ] Reconciliation dashboard

### Phase 3: Frontend
- [ ] Web dashboard for expense management
- [ ] Interactive reconciliation interface
- [ ] Advanced filtering and search

### Phase 4: Integrations
- [ ] Notion/Airtable integration
- [ ] Receipt storage (S3-compatible)
- [ ] Slack/email notifications
- [ ] Advanced analytics

## 🤝 Contributing

This is a personal project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - feel free to use this for your own expense tracking needs!

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/timlihk/Zoho-expense/issues)
- **Documentation**: This README + `/docs` endpoint
- **API Docs**: Visit `/docs` on your deployed app

---

**Ready to take control of your expense data?** Deploy in 5 minutes and start syncing! 🚀