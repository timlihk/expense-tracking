'use client';
import React from 'react';

export function ExpensesTable({ rows }: { rows: any[] }) {
  return (
    <div className="card p-4 overflow-x-auto">
      <h2 className="text-lg font-semibold mb-2">Recent Expenses</h2>
      <table className="w-full text-sm">
        <thead>
          <tr>
            <th>Date</th><th>Merchant</th><th>Amount</th><th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td>{r.date}</td>
              <td>{r.merchant}</td>
              <td>{r.amount} {r.currency}</td>
              <td>{r.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}