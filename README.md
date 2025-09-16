# Zoho Expense → PostgreSQL Sync

A self-hosted FastAPI application that automatically syncs your Zoho Expense data to PostgreSQL, providing comprehensive expense tracking, reimbursement management, and financial reporting.

## 🎯 Overview

This application solves the problem of scattered expense data by creating a centralized, self-hosted expense ledger that:
- **Automatically syncs** expense data from Zoho Expense to your own PostgreSQL database
- **Tracks reimbursement status** and provides aging reports for outstanding expenses
- **Provides REST APIs** for integration with other tools and custom reporting
- **Runs completely self-hosted** on Railway (or any Docker platform)

Perfect for individuals, small businesses, or teams who want full control over their expense data.

## ✨ Key Features

### 📊 **Automated Data Sync**
- **Incremental sync** from Zoho Expense every 15 minutes (configurable)
- **Manual sync trigger** with simple URL parameter authentication
- **Secure OAuth integration** with encrypted token storage
- **Handles attachments** and receipt data

### 💰 **Expense Management**
- **Complete expense tracking** with merchant, amount, date, category
- **Reimbursement status management** (Reimbursed/Not Reimbursed)
- **Bulk status updates** via API endpoints
- **Notes and custom fields** support

### 📈 **Financial Reporting**
- **Summary reports** with date range filtering
- **Outstanding expenses** tracking for cash flow management
- **Aging reports** to identify overdue reimbursements
- **Export capabilities** for external analysis

### 🔐 **Security & Privacy**
- **Self-hosted** - your data stays on your infrastructure
- **Encrypted token storage** using Fernet encryption
- **Simple phrase-based authentication** for personal use
- **Environment-based configuration** for secure deployment

## 🚀 Quick Start

### Prerequisites
- **Zoho Expense account** with API access
- **Railway account** (or any Docker hosting platform)
- **5 minutes** for setup

### 1. Zoho OAuth Setup
Create a Zoho OAuth app at [Zoho API Console](https://api-console.zoho.com/):
- **Application Type**: Server-based Application
- **Redirect URI**: `https://your-app.railway.app/oauth/zoho/callback`
- **Scopes**: `ZohoExpense.expenses.READ,ZohoExpense.reports.READ,ZohoExpense.files.READ`

Save your `Client ID` and `Client Secret`.

### 2. Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/new)

1. **Connect this GitHub repository** to Railway
2. **Add PostgreSQL service** (Railway will auto-provide `DATABASE_URL`)
3. **Set environment variables**:

```bash
# Required - Your Zoho OAuth credentials
ZOHO_CLIENT_ID=your_zoho_client_id
ZOHO_CLIENT_SECRET=your_zoho_client_secret

# Required - Generate encryption key
ENCRYPTION_KEY=<run: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">

# Required - Your simple admin phrase
ADMIN_TOKEN=sync my expenses please

# Auto-configured by Railway
APP_BASE_URL=https://your-app.railway.app
DATABASE_URL=<auto-provided>

# Optional (defaults shown)
SYNC_INTERVAL_MINUTES=15
ENVIRONMENT=production
```

### 3. Initial Setup
After deployment:

1. **Authorize Zoho**: Visit `https://your-app.railway.app/oauth/zoho/login`
2. **Test sync**: `POST https://your-app.railway.app/admin/sync?secret=sync my expenses please`
3. **View data**: `https://your-app.railway.app/reports/summary`

That's it! Your expenses will now sync automatically every 15 minutes.

## 📋 API Endpoints

### Authentication & Setup
- `GET /health` - Health check
- `GET /oauth/zoho/login` - Start Zoho OAuth flow
- `GET /oauth/zoho/callback` - Complete OAuth (automatic)

### Data Management
- `GET /expenses` - List expenses with filtering
- `POST /expenses/mark-reimbursed` - Mark expenses as reimbursed
- `POST /admin/sync?secret=your-phrase` - Manual sync trigger

### Reporting
- `GET /reports/summary` - Financial summary with date filtering
- `GET /reports/outstanding` - Outstanding reimbursements
- `GET /reports/ageing` - Aging analysis for overdue expenses

### Example Usage

```bash
# Get summary for last 30 days
curl "https://your-app.railway.app/reports/summary?from=2024-01-01&to=2024-01-31"

# List unreimbursed expenses
curl "https://your-app.railway.app/expenses?status=Not%20Reimbursed&limit=50"

# Trigger manual sync
curl -X POST "https://your-app.railway.app/admin/sync?secret=sync my expenses please"

# Mark expenses as reimbursed
curl -X POST "https://your-app.railway.app/expenses/mark-reimbursed" \
  -H "Content-Type: application/json" \
  -d '{"expense_ids": ["exp_123", "exp_456"]}'
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

## 🗄️ Database Schema

The application creates these main tables:

- **`expenses`** - Core expense data synced from Zoho
- **`oauth_tokens`** - Encrypted OAuth tokens for Zoho API access

Key fields in `expenses` table:
- Basic info: `expense_id`, `merchant`, `amount`, `date`, `category`
- Status: `reimbursement_status`, `approval_status`
- Metadata: `created_at`, `updated_at`, `last_synced`

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
    DATE_TRUNC('month', date) as month,
    category,
    SUM(amount) as total
FROM expenses
GROUP BY month, category
ORDER BY month DESC, total DESC;
```

## 🛠️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Scheduling**: APScheduler for background sync
- **Security**: Fernet encryption for sensitive data
- **Deployment**: Docker on Railway

### Data Flow
1. **OAuth Setup** → Secure token storage
2. **Scheduled Sync** → Incremental data fetch from Zoho
3. **API Access** → RESTful endpoints for data access
4. **Reporting** → SQL-based analysis and summaries

## 🚧 Roadmap

### Phase 1: Stabilization (Current)
- [x] Core sync functionality
- [x] Basic reporting endpoints
- [x] Railway deployment
- [ ] Enhanced error handling and logging
- [ ] Comprehensive test suite

### Phase 2: Reconciliation
- [ ] CSV upload for company reports
- [ ] Fuzzy matching logic for expense reconciliation
- [ ] External reference tracking
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