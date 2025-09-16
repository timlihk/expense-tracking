import './globals.css';
import React from 'react';

export const metadata = {
  title: 'T&E Dashboard',
  description: 'World-class dashboard for Expense Tracking',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="max-w-7xl mx-auto p-4 md:p-8">
          <header className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">Expense Dashboard</h1>
            <a href="https://github.com/timlihk/expense-tracking" target="_blank" className="underline">Repo</a>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}