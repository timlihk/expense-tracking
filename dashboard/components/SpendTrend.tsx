'use client';
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface TrendData {
  period: string;
  amount: number;
  count: number;
}

export function SpendTrend({ data }: { data: TrendData[] }) {
  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 border border-gray-600 rounded p-2 text-sm">
          <p className="text-white">{label}</p>
          <p className="text-blue-400">${data.amount.toLocaleString()}</p>
          <p className="text-gray-300">{data.count} expenses</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-4">Spending Trend (Last 6 Months)</h2>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis
              dataKey="period"
              tick={{ fontSize: 12, fill: '#9CA3AF' }}
            />
            <YAxis tick={{ fontSize: 12, fill: '#9CA3AF' }} />
            <Tooltip content={<CustomTooltip />} />
            <Line
              type="monotone"
              dataKey="amount"
              stroke="#5cc8ff"
              strokeWidth={3}
              dot={{ fill: '#5cc8ff', strokeWidth: 2, r: 6 }}
              activeDot={{ r: 8, stroke: '#5cc8ff', strokeWidth: 2 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}