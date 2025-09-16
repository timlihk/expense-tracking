'use client';
import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend
} from 'recharts';

const COLORS = ['#5cc8ff', '#00d4aa', '#ffb347', '#ff6b6b', '#c471ed', '#32d74b', '#007aff', '#ff9500'];

// Pie Chart Component
export function PieCard({ title, data, nameKey, valueKey }: {
  title: string;
  data: any[];
  nameKey: string;
  valueKey: string;
}) {
  return (
    <div className="card p-4 w-full">
      <div className="text-lg font-semibold mb-3">{title}</div>
      <div style={{ width: '100%', height: 240 }}>
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              innerRadius={40}
              outerRadius={80}
              paddingAngle={2}
              dataKey={valueKey}
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: any) => [`$${value?.toLocaleString()}`, 'Amount']} />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
              formatter={(value: string, entry: any) => value}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// Bar Chart Component
export function BarCard({ title, data, xKey, yKey }: {
  title: string;
  data: any[];
  xKey: string;
  yKey: string;
}) {
  return (
    <div className="card p-4 w-full">
      <div className="text-lg font-semibold mb-3">{title}</div>
      <div style={{ width: '100%', height: 240 }}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{ bottom: 20 }}>
            <XAxis
              dataKey={xKey}
              stroke="#93a4b7"
              angle={-45}
              textAnchor="end"
              height={60}
              fontSize={11}
            />
            <YAxis stroke="#93a4b7" />
            <Tooltip formatter={(value: any) => [`$${value?.toLocaleString()}`, 'Total']} />
            <Bar dataKey={yKey} fill="#5cc8ff" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

// Line Chart Component
export function LineCard({ title, data, xKey, yKey }: {
  title: string;
  data: any[];
  xKey: string;
  yKey: string;
}) {
  return (
    <div className="card p-4 w-full">
      <div className="text-lg font-semibold mb-3">{title}</div>
      <div style={{ width: '100%', height: 240 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <XAxis dataKey={xKey} stroke="#93a4b7" />
            <YAxis stroke="#93a4b7" />
            <Tooltip formatter={(value: any) => [`$${value?.toLocaleString()}`, 'Total']} />
            <Line
              type="monotone"
              dataKey={yKey}
              stroke="#5cc8ff"
              strokeWidth={2}
              dot={{ fill: '#5cc8ff', strokeWidth: 2, r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}