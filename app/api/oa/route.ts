// POST /api/oa — 청구항 + 선행기술로 가상 거절이유 생성 (STEP 21)
import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { simulateOA } from "@/lib/server/oa";

const Schema = z.object({
  claims: z.string().min(1, "청구항이 비어 있습니다"),
  evidence: z.array(
    z.object({
      id: z.string(),
      title: z.string(),
      source: z.string(),
      pubDate: z.string(),
      summary: z.string(),
    })
  ),
});

export async function POST(req: NextRequest) {
  const parsed = Schema.safeParse(await req.json().catch(() => null));
  if (!parsed.success) {
    return NextResponse.json(
      { error: parsed.error.issues.map((i) => i.message).join(", ") },
      { status: 422 }
    );
  }
  try {
    const result = await simulateOA(parsed.data);
    return NextResponse.json(result);
  } catch (err) {
    console.error("[api/oa]", err);
    return NextResponse.json({ error: "생성 실패" }, { status: 500 });
  }
}
