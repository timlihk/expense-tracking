import React from 'react';

export function KPI({ label, value }: { label:string; value:string|number }) {
  return (
    <div className="card p-4">
      <div className="text-sm text-gray-400">{label}</div>
      <div className="text-2xl font-semibold">{value}</div>
    </div>
  );
}