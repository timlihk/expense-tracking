'use client';
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface MerchantData {
  merchant: string;
  amount: number;
  count: number;
}

export function TopMerchants({ data }: { data: MerchantData[] }) {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 border border-gray-600 rounded p-2 text-sm">
          <p className="text-white">{label}</p>
          <p className="text-blue-400">${data.amount.toLocaleString()}</p>
          <p className="text-gray-300">{data.count} transactions</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-4">Top Merchants</h2>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis
              dataKey="merchant"
              angle={-45}
              textAnchor="end"
              height={80}
              tick={{ fontSize: 12, fill: '#9CA3AF' }}
            />
            <YAxis tick={{ fontSize: 12, fill: '#9CA3AF' }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="amount" fill="#5cc8ff" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}