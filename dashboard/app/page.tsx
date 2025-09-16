'use client';
import React, { useState } from 'react';
import useSWR from 'swr';
import { KPI } from '../components/KPI';
import { ExpensesTable } from '../components/ExpensesTable';
import { SpendByCategory } from '../components/SpendByCategory';
import { TopMerchants } from '../components/TopMerchants';
import { SpendTrend } from '../components/SpendTrend';
import { ReconciliationUpload } from '../components/ReconciliationUpload';
import { fetchSummary, fetchExpenses, fetchOutstanding, fetchAgeing, triggerSync } from '../lib/api';
import {
  generateCategoryData,
  generateMerchantData,
  generateTrendData,
  generateMockCategoryData,
  generateMockMerchantData,
  generateMockTrendData
} from '../lib/chartData';

export default function Dashboard() {
  const { data: summary } = useSWR('summary', fetchSummary);
  const { data: expenses, mutate: mutateExpenses } = useSWR('expenses', fetchExpenses);
  const { data: outstanding } = useSWR('outstanding', fetchOutstanding);
  const { data: ageing } = useSWR('ageing', fetchAgeing);

  const [syncMsg, setSyncMsg] = useState<string | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);

  // Generate chart data
  const categoryData = expenses?.length ? generateCategoryData(expenses) : generateMockCategoryData();
  const merchantData = expenses?.length ? generateMerchantData(expenses) : generateMockMerchantData();
  const trendData = expenses?.length ? generateTrendData(expenses) : generateMockTrendData();

  async function onSync() {
    setIsSyncing(true);
    setSyncMsg(null);

    try {
      const res = await triggerSync();
      setSyncMsg(`✅ Sync completed: ${res.expenses_synced || 0} expenses processed`);
      // Refresh data after sync
      mutateExpenses();
    } catch (e: any) {
      setSyncMsg(`❌ Sync failed: ${e.message}`);
    } finally {
      setIsSyncing(false);
    }
  }

  // Calculate KPI values
  const totalAmount = summary?.total_amount || 0;
  const outstandingAmount = outstanding?.total_outstanding || 0;
  const recentCount = expenses?.length || 0;

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPI
          label="Total Expenses"
          value={`$${totalAmount.toLocaleString()}`}
        />
        <KPI
          label="Outstanding Amount"
          value={`$${outstandingAmount.toLocaleString()}`}
        />
        <KPI
          label="Recent Expenses"
          value={recentCount}
        />
      </div>

      {/* Sync Controls */}
      <div className="flex items-center space-x-4">
        <button
          onClick={onSync}
          disabled={isSyncing}
          className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-4 py-2 rounded-md transition-colors"
        >
          {isSyncing ? 'Syncing...' : 'Trigger Sync'}
        </button>
        {syncMsg && (
          <div className="text-sm text-gray-300 bg-gray-800 px-3 py-2 rounded">
            {syncMsg}
          </div>
        )}
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SpendByCategory data={categoryData} />
        <TopMerchants data={merchantData} />
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SpendTrend data={trendData} />
        <ReconciliationUpload />
      </div>

      {/* Expenses Table */}
      <ExpensesTable rows={expenses || []} />
    </div>
  );
}