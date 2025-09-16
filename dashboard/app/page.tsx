'use client';
import React, { useState } from 'react';
import useSWR from 'swr';
import { KPI } from '../components/KPI';
import { ExpensesTable } from '../components/ExpensesTable';
import { fetchSummary, fetchExpenses, triggerSync } from '../lib/api';

export default function Dashboard() {
  const { data: summary } = useSWR('summary', fetchSummary);
  const { data: expenses } = useSWR('expenses', fetchExpenses);
  const [msg, setMsg] = useState<string|null>(null);

  async function onSync() {
    try {
      const res = await triggerSync();
      setMsg(`Sync triggered: ${JSON.stringify(res)}`);
    } catch (e:any) {
      setMsg(`Sync failed: ${e.message}`);
    }
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-4">
        <KPI label="Total Expenses" value={summary?.by_currency?.length || 0} />
        <KPI label="Recent Expenses" value={expenses?.length || 0} />
        <KPI label="Last Sync" value={new Date().toLocaleDateString()} />
      </div>

      <button onClick={onSync} className="btn bg-blue-600 text-white px-3 py-2 rounded">Trigger Sync</button>
      {msg && <div className="text-sm text-gray-400">{msg}</div>}

      <ExpensesTable rows={expenses || []} />
    </div>
  );
}