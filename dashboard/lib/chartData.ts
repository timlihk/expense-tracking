// Transform expense data for chart components

interface Expense {
  id: string;
  merchant: string;
  amount: number;
  currency: string;
  category_id?: string;
  category_name?: string;
  txn_date: string;
  reimbursement_status: string;
}

export function generateCategoryData(expenses: Expense[]) {
  const categoryMap = new Map();

  expenses.forEach(expense => {
    const category = expense.category_name || expense.category_id || 'Other';
    const current = categoryMap.get(category) || { name: category, value: 0, count: 0 };
    current.value += expense.amount;
    current.count += 1;
    categoryMap.set(category, current);
  });

  return Array.from(categoryMap.values())
    .sort((a, b) => b.value - a.value)
    .slice(0, 8); // Top 8 categories
}

export function generateMerchantData(expenses: Expense[]) {
  const merchantMap = new Map();

  expenses.forEach(expense => {
    const merchant = expense.merchant || 'Unknown';
    const current = merchantMap.get(merchant) || { merchant, amount: 0, count: 0 };
    current.amount += expense.amount;
    current.count += 1;
    merchantMap.set(merchant, current);
  });

  return Array.from(merchantMap.values())
    .sort((a, b) => b.amount - a.amount)
    .slice(0, 10); // Top 10 merchants
}

export function generateTrendData(expenses: Expense[]) {
  const now = new Date();
  const months = [];

  // Generate last 6 months
  for (let i = 5; i >= 0; i--) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
    months.push({
      period: date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
      year: date.getFullYear(),
      month: date.getMonth(),
      amount: 0,
      count: 0
    });
  }

  expenses.forEach(expense => {
    const expenseDate = new Date(expense.txn_date);
    const monthData = months.find(m =>
      m.year === expenseDate.getFullYear() && m.month === expenseDate.getMonth()
    );

    if (monthData) {
      monthData.amount += expense.amount;
      monthData.count += 1;
    }
  });

  return months.map(({ period, amount, count }) => ({ period, amount, count }));
}

// Mock data generators for development/demo
export function generateMockCategoryData() {
  return [
    { name: 'Travel', value: 12450, count: 28 },
    { name: 'Meals', value: 8200, count: 45 },
    { name: 'Software', value: 5600, count: 12 },
    { name: 'Office Supplies', value: 3400, count: 18 },
    { name: 'Transportation', value: 2100, count: 22 },
    { name: 'Entertainment', value: 1800, count: 15 },
  ];
}

export function generateMockMerchantData() {
  return [
    { merchant: 'UBER', amount: 3200, count: 18 },
    { merchant: 'STARBUCKS', amount: 2800, count: 24 },
    { merchant: 'AMAZON', amount: 2400, count: 8 },
    { merchant: 'DELTA AIR LINES', amount: 2200, count: 4 },
    { merchant: 'MARRIOTT', amount: 1900, count: 6 },
    { merchant: 'ZOOM', amount: 1200, count: 3 },
    { merchant: 'LYFT', amount: 980, count: 12 },
    { merchant: 'SLACK', amount: 840, count: 2 },
  ];
}

export function generateMockTrendData() {
  return [
    { period: 'Aug 24', amount: 8200, count: 32 },
    { period: 'Sep 24', amount: 9800, count: 38 },
    { period: 'Oct 24', amount: 7600, count: 28 },
    { period: 'Nov 24', amount: 11200, count: 45 },
    { period: 'Dec 24', amount: 6800, count: 24 },
    { period: 'Jan 25', amount: 9400, count: 36 },
  ];
}