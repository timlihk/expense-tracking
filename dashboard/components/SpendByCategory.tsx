'use client';
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#5cc8ff', '#00d4aa', '#ffb347', '#ff6b6b', '#c471ed', '#32d74b', '#007aff', '#ff9500'];

interface CategoryData {
  name: string;
  value: number;
  count: number;
}

export function SpendByCategory({ data }: { data: CategoryData[] }) {
  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-gray-800 border border-gray-600 rounded p-2 text-sm">
          <p className="text-white">{data.name}</p>
          <p className="text-blue-400">${data.value.toLocaleString()}</p>
          <p className="text-gray-300">{data.count} expenses</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="card p-4">
      <h2 className="text-lg font-semibold mb-4">Spend by Category</h2>
      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={100}
              paddingAngle={2}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
              formatter={(value: string, entry: any) =>
                `${value} ($${entry.payload?.value?.toLocaleString() || 0})`
              }
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}