export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

async function post<T>(path: string, body?: any): Promise<T> {
  const res = await fetch(path, {
    method: "POST",
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.error || `POST ${path} failed: ${res.status}`);
  }
  return res.json();
}

// Public API endpoints (no auth required)
export async function fetchSummary() {
  return get(`/reports/summary`);
}

export async function fetchExpenses() {
  return get(`/expenses?limit=20`);
}

export async function fetchOutstanding() {
  return get(`/reports/outstanding`);
}

export async function fetchAgeing() {
  return get(`/reports/ageing`);
}

// Analytics endpoints for charts
export async function fetchByCategory() {
  return get<{category:string; total:number;}[]>(`/reports/by_category`);
}

export async function fetchByMerchant() {
  return get<{merchant:string; total:number;}[]>(`/reports/by_merchant`);
}

export async function fetchTrends() {
  return get<{date:string; total:number;}[]>(`/reports/trends`);
}

// Secure endpoints via Next.js API routes
export async function triggerSync() {
  return post(`/api/sync`);
}

export async function uploadReconCSV(file: File) {
  const form = new FormData();
  form.append('file', file);
  const res = await fetch('/api/recon', { method: 'POST', body: form });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}