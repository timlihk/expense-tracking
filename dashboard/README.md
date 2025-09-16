# T&E Dashboard

A modern Next.js dashboard for the Zoho Expense tracking system.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local
# Edit .env.local with your API configuration

# Start development server
npm run dev
```

Visit http://localhost:3000

## 🔧 Configuration

Edit `.env.local`:

```bash
# Point to your FastAPI backend
NEXT_PUBLIC_API_BASE=http://localhost:8080

# Your admin token for sync operations
NEXT_PUBLIC_ADMIN_TOKEN=sync my expenses please
```

## 📊 Features

- **KPI Dashboard**: Total expenses, recent activity, sync status
- **Expense Table**: Recent transactions with filtering
- **Manual Sync**: Trigger Zoho sync from the UI
- **Real-time Updates**: SWR for automatic data refreshing
- **Responsive Design**: Works on desktop and mobile
- **Dark Theme**: Professional dark UI

## 🛠️ Tech Stack

- **Next.js 14**: App router with TypeScript
- **Tailwind CSS**: Utility-first styling
- **SWR**: Data fetching and caching
- **Recharts**: Data visualization (ready for charts)

## 📈 Development

```bash
npm run dev     # Development server
npm run build   # Production build
npm run start   # Production server
npm run lint    # Code linting
```

## 🔗 API Integration

The dashboard connects to your FastAPI backend endpoints:

- `GET /reports/summary` - Financial summary data
- `GET /expenses?limit=20` - Recent expenses list
- `POST /expenses/admin/sync` - Manual sync trigger

Make sure your FastAPI backend is running on the configured `NEXT_PUBLIC_API_BASE` URL.