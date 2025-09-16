'use client';
import React from 'react';

interface Expense {
  id: string;
  merchant: string;
  amount: number;
  currency: string;
  txn_date: string;
  reimbursement_status: string;
  category_name?: string;
  kirkland_te_report?: string;
}

export function ExpensesTable({ rows }: { rows: Expense[] }) {
  if (!rows || rows.length === 0) {
    return (
      <div className="card p-4">
        <h2 className="text-lg font-semibold mb-4">Recent Expenses</h2>
        <div className="text-center py-8 text-gray-400">
          <div className="text-6xl mb-4">📊</div>
          <div className="text-lg">No expenses found</div>
          <div className="text-sm">Try triggering a sync to load data from Zoho</div>
        </div>
      </div>
    );
  }

  return (
    <div className="card p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Recent Expenses</h2>
        <div className="text-sm text-gray-400">{rows.length} transactions</div>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-700 text-left">
              <th className="pb-3 pr-4 font-medium text-gray-300">Date</th>
              <th className="pb-3 pr-4 font-medium text-gray-300">Merchant</th>
              <th className="pb-3 pr-4 font-medium text-gray-300">Category</th>
              <th className="pb-3 pr-4 font-medium text-gray-300 text-right">Amount</th>
              <th className="pb-3 pr-4 font-medium text-gray-300">Status</th>
              <th className="pb-3 font-medium text-gray-300">T&E Report</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((expense, index) => (
              <tr
                key={expense.id}
                className={`border-b border-gray-800 hover:bg-gray-800/30 transition-colors ${
                  index % 2 === 0 ? 'bg-gray-900/20' : ''
                }`}
              >
                <td className="py-3 pr-4 text-gray-300">
                  {new Date(expense.txn_date).toLocaleDateString('en-US', {
                    month: 'short',
                    day: 'numeric'
                  })}
                </td>
                <td className="py-3 pr-4 text-white font-medium">
                  {expense.merchant || 'Unknown'}
                </td>
                <td className="py-3 pr-4 text-gray-400">
                  <span className="px-2 py-1 bg-gray-700 rounded text-xs">
                    {expense.category_name || 'Other'}
                  </span>
                </td>
                <td className="py-3 pr-4 text-right text-white font-medium">
                  ${expense.amount?.toFixed(2)} {expense.currency}
                </td>
                <td className="py-3 pr-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    expense.reimbursement_status === 'Reimbursed'
                      ? 'bg-green-900/30 text-green-400'
                      : expense.reimbursement_status === 'Submitted for Reimbursement'
                      ? 'bg-yellow-900/30 text-yellow-400'
                      : 'bg-red-900/30 text-red-400'
                  }`}>
                    {expense.reimbursement_status || 'Pending'}
                  </span>
                </td>
                <td className="py-3 text-gray-400 text-xs">
                  {expense.kirkland_te_report || '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {rows.length >= 20 && (
        <div className="mt-4 text-center">
          <div className="text-sm text-gray-400">
            Showing {rows.length} most recent expenses
          </div>
        </div>
      )}
    </div>
  );
}