// POST /api/approval — 승인 결정 저장 (STEP 24B)
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { saveApproval } from "@/lib/server/persist";

const Schema = z.object({
  inventionId: z.string().min(1),
  status: z.enum(["PENDING", "APPROVED", "REJECTED"]),
  reviewer: z.string(),
  comment: z.string(),
  decidedAt: z.string().nullable(),
});

export async function POST(req: NextRequest) {
  const parsed = Schema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json({ error: "입력 형식 오류" }, { status: 422 });
  }
  try {
    await saveApproval(parsed.data.inventionId, parsed.data);
    return NextResponse.json({ ok: true });
  } catch (err) {
    console.error("[api/approval]", err);
    return NextResponse.json({ error: "저장 실패" }, { status: 500 });
  }
}
