# World-Class T&E Dashboard

An enterprise-grade Next.js 14 dashboard for the Zoho Expense tracking system with advanced analytics, security hardening, and professional UI/UX.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Set up environment (SECURE)
cp .env.local.example .env.local
# Edit .env.local with your configuration (see below)

# Start development server
npm run dev
```

Visit http://localhost:3000

## 🔧 Configuration

Edit `.env.local`:

```bash
# PUBLIC: Exposed to browser for direct API calls
NEXT_PUBLIC_API_BASE=http://localhost:8000

# SERVER-SIDE ONLY: Used in Next.js API routes (NEVER exposed to browser)
API_BASE=http://localhost:8000
ADMIN_TOKEN=sync my expenses please
```

⚠️ **CRITICAL SECURITY**: The `ADMIN_TOKEN` is only used server-side in `/api/sync` and `/api/recon` routes. This prevents credential exposure to the browser, eliminating security vulnerabilities.

## 📊 Features

### 📈 **Analytics & Visualization**
- **KPI Dashboard**: Total expenses, outstanding amounts, transaction counts
- **Category Analysis**: Pie chart showing spend distribution by expense category
- **Merchant Analysis**: Bar chart highlighting top vendors and suppliers
- **Trend Analysis**: Line chart showing spending patterns over time
- **Mock Data**: Displays sample charts when no real data is available

### 🔄 **Sync & Reconciliation**
- **Secure Manual Sync**: Server-side proxy keeps admin tokens secure
- **CSV Upload**: Upload company T&E reports for reconciliation
- **Match Detection**: Automatic matching with confidence scoring
- **Visual Feedback**: Color-coded status indicators and progress displays

### 📋 **Data Management**
- **Enhanced Expense Table**: Categorized, color-coded with hover effects
- **Real-time Updates**: SWR for automatic data refreshing after sync
- **Responsive Design**: Optimized layouts for desktop, tablet, and mobile
- **Professional UI**: Dark theme with smooth transitions and hover effects

### 🔐 **Security**
- **Server-side API Proxy**: Admin tokens never exposed to browser
- **Environment Configuration**: Secure credential management
- **Error Handling**: Graceful degradation with user-friendly messages

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