import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const formData = await req.formData();
  const token = process.env.ADMIN_TOKEN;

  if (!token) {
    return NextResponse.json({ ok: false, error: 'Admin token not set' }, { status: 500 });
  }

  try {
    const res = await fetch(`${process.env.API_BASE}/recon/upload?dry_run=true`, {
      method: 'POST',
      headers: { 'x-admin-token': token },
      body: formData
    });
    const data = await res.json();
    return NextResponse.json(data, { status: res.status });
  } catch (err: any) {
    return NextResponse.json({ ok: false, error: err.message }, { status: 500 });
  }
}