import { NextRequest, NextResponse } from 'next/server';

const API_BASE = process.env.API_BASE || 'http://localhost:8000';
const ADMIN_TOKEN = process.env.ADMIN_TOKEN || '';

export async function POST(request: NextRequest) {
  if (!ADMIN_TOKEN) {
    return NextResponse.json(
      { error: 'Admin token not configured' },
      { status: 500 }
    );
  }

  try {
    const response = await fetch(`${API_BASE}/expenses/admin/sync`, {
      method: 'POST',
      headers: {
        'x-admin-token': ADMIN_TOKEN,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      return NextResponse.json(
        { error: `Sync failed: ${response.status} - ${errorText}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: `Network error: ${error.message}` },
      { status: 500 }
    );
  }
}