# Deployment Guide

Quick deployment guide for the Zoho Expense sync application.

## Railway Deployment (Recommended)

### 1. Prerequisites
- GitHub account with this repository
- Railway account ([railway.app](https://railway.app))
- Zoho Expense account with admin access

### 2. Setup Zoho OAuth App

1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Create a new **Server-based Application**
3. Set these values:
   - **Application Name**: Expense Sync
   - **Homepage URL**: `https://your-app-name.up.railway.app`
   - **Authorized Redirect URI**: `https://your-app-name.up.railway.app/oauth/zoho/callback`
4. Set **Scopes**: `ZohoExpense.expenses.READ,ZohoExpense.reports.READ,ZohoExpense.files.READ`
5. Save your **Client ID** and **Client Secret**

### 3. Deploy to Railway

1. **Connect Repository**:
   - Login to Railway
   - Create new project
   - Connect this GitHub repository

2. **Add PostgreSQL**:
   - In Railway dashboard, click "New"
   - Select "Database" → "PostgreSQL"
   - This automatically provides `DATABASE_URL`

3. **Configure Environment Variables**:
   ```bash
   # Required - Your Zoho credentials
   ZOHO_CLIENT_ID=your_client_id_here
   ZOHO_CLIENT_SECRET=your_client_secret_here

   # Required - Generate these
   ENCRYPTION_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
   ADMIN_TOKEN=sync my expenses please

   # Auto-configured by Railway
   APP_BASE_URL=https://your-app-name.up.railway.app

   # Optional (defaults shown)
   SYNC_INTERVAL_MINUTES=15
   ENVIRONMENT=production
   ```

4. **Deploy**:
   - Railway will automatically build and deploy
   - Wait for deployment to complete (2-3 minutes)

### 4. Initial Setup

1. **Test Health**: Visit `https://your-app-name.up.railway.app/health`
2. **Authorize Zoho**: Visit `https://your-app-name.up.railway.app/oauth/zoho/login`
3. **Test Sync**:
   ```bash
   curl -X POST "https://your-app-name.up.railway.app/admin/sync?secret=sync my expenses please"
   ```
4. **View Reports**: Visit `https://your-app-name.up.railway.app/reports/summary`

### 5. API Documentation

Once deployed, visit `https://your-app-name.up.railway.app/docs` for interactive API documentation.

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