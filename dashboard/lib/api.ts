export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";
export const ADMIN_TOKEN = process.env.NEXT_PUBLIC_ADMIN_TOKEN || "";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

export async function fetchSummary() {
  return get(`/reports/summary`);
}

export async function fetchExpenses() {
  return get(`/expenses?limit=20`);
}

export async function triggerSync() {
  const res = await fetch(`${API_BASE}/expenses/admin/sync`, {
    method: "POST",
    headers: { "x-admin-token": ADMIN_TOKEN }
  });
  if (!res.ok) throw new Error("Sync failed");
  return res.json();
}