# Deployment Guide

**Repository**: https://github.com/timlihk/expense-tracking
**Status**: ✅ Ready for immediate deployment

Complete deployment guide for the Zoho Expense sync application with Supabase database.

## 🚀 Railway + Supabase Deployment (Recommended)

### 1. Prerequisites
- GitHub account with this repository
- Railway account ([railway.app](https://railway.app))
- Supabase account ([supabase.com](https://supabase.com)) - **FREE TIER**
- Zoho Expense account with admin access

### 2. Setup Supabase Database (FREE)

1. **Create Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Sign up (free forever)
   - Click "New Project"
   - Choose organization
   - Set project name: "expense-tracking"
   - Set database password (save this!)
   - Select region closest to you

2. **Get Connection String**:
   - In Supabase dashboard → Settings → Database
   - Copy the "URI" connection string
   - It looks like: `postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres`
   - Save this for step 4

### 3. Setup Zoho OAuth App

1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Create a new **Server-based Application**
3. Set these values:
   - **Application Name**: Expense Sync
   - **Homepage URL**: `https://your-app-name.up.railway.app`
   - **Authorized Redirect URI**: `https://your-app-name.up.railway.app/oauth/zoho/callback`
4. Set **Scopes**: `ZohoExpense.expenses.READ,ZohoExpense.reports.READ,ZohoExpense.files.READ`
5. Save your **Client ID** and **Client Secret**

### 4. Deploy to Railway

1. **Connect Repository**:
   - Login to Railway
   - Create new project from GitHub
   - Connect: `https://github.com/timlihk/expense-tracking`

2. **No PostgreSQL needed**:
   - Skip adding Railway PostgreSQL service
   - We're using Supabase instead (free!)

3. **Configure Environment Variables**:
   ```bash
   # Required - Your Supabase database (from step 2)
   DATABASE_URL=postgresql://postgres:your-password@db.your-ref.supabase.co:5432/postgres

   # Required - Your Zoho credentials (from step 3)
   ZOHO_CLIENT_ID=your_client_id_here
   ZOHO_CLIENT_SECRET=your_client_secret_here

   # Required - Generate these
   ENCRYPTION_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
   ADMIN_TOKEN=sync my expenses please

   # Railway configuration
   APP_BASE_URL=https://your-app-name.up.railway.app

   # Optional (defaults shown)
   SYNC_INTERVAL_MINUTES=15
   ENVIRONMENT=production
   ```

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for deployment to complete (2-3 minutes)

### 5. Initial Setup

1. **Test Health**: Visit `https://your-app-name.up.railway.app/health`
2. **Authorize Zoho**: Visit `https://your-app-name.up.railway.app/oauth/zoho/login`
3. **Test Sync**:
   ```bash
   curl -X POST "https://your-app-name.up.railway.app/admin/sync?secret=sync my expenses please"
   ```
4. **View Reports**: Visit `https://your-app-name.up.railway.app/reports/summary`
5. **Optional**: View data in Supabase dashboard → Table Editor

## 💰 Cost Breakdown

### Supabase (Database)
- **Free Tier**: 500MB database, unlimited API requests
- **Handles**: 50,000+ expense records easily
- **Cost**: $0/month forever

### Railway (Application Hosting)
- **Free Tier**: Limited usage
- **Hobby Plan**: $5/month for personal projects
- **Pro Plan**: $20/month for production use

**Total**: $0-5/month for personal expense tracking

## ✨ **What You Get After Deployment**

### 🔄 **Automatic Expense Sync**
- Syncs from Zoho Expense every 15 minutes
- Encrypted OAuth token storage
- Incremental updates (only new/changed expenses)

### 💰 **Complete Expense Management**
- List and filter expenses via REST API
- Mark expenses as reimbursed
- Track reimbursement status and amounts

### 🏢 **Kirkland T&E Report Integration**
- Assign expenses to T&E report numbers
- Track submission status
- Generate T&E report summaries
- Reconcile company reimbursements

### 📊 **Financial Reporting**
- Summary reports with date filtering
- Outstanding expense tracking
- Aging analysis for overdue reimbursements
- Direct Supabase dashboard access

### 🔧 **Developer-Friendly**
- Interactive API documentation at `/docs`
- RESTful endpoints for all operations
- Simple authentication for personal use
- Direct PostgreSQL access for custom queries

## 📚 **Post-Deployment Resources**

### 🔗 **Important URLs** (Replace `your-app` with your Railway app name)
- **Health Check**: `https://your-app.up.railway.app/health`
- **API Documentation**: `https://your-app.up.railway.app/docs`
- **Zoho Authorization**: `https://your-app.up.railway.app/oauth/zoho/login`
- **Reports Summary**: `https://your-app.up.railway.app/reports/summary`
- **Manual Sync**: `https://your-app.up.railway.app/admin/sync?secret=your-phrase`

### 📊 **Data Access**
- **Supabase Dashboard**: [supabase.com](https://supabase.com) → Your Project → Table Editor
- **Direct SQL**: Use Supabase SQL Editor for custom queries

## Alternative Deployment Options

### Docker (Self-hosted)

```bash
# Build and run
docker build -t zoho-expense .
docker run -p 8080:8080 --env-file .env zoho-expense
```

### Manual Server Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://..."
export ZOHO_CLIENT_ID="..."
# ... etc

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Troubleshooting

### Common Issues

1. **OAuth Error**: Ensure redirect URI matches exactly
2. **Database Connection**: Check `DATABASE_URL` format
3. **Sync Failing**: Verify Zoho API scopes are correct
4. **401 Unauthorized**: Check `ADMIN_TOKEN` matches your secret phrase

### Logs

View Railway logs in the dashboard under your service → "Deployments" → "View Logs"

### Support

- Check `/health` endpoint for service status
- View `/docs` for API documentation
- Review Railway logs for detailed error messages